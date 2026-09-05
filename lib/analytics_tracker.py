"""
Visitor Analytics Tracker
Tracks device type, bot classification and coarse location — never an address.

This ledger is the raw material for two things:

1. the app's own record of who read the docs, and
2. the hourly rollup this app POSTs to 2plot.ai (``lib/satellite_reporter``),
   which is what the network ``/traffic`` dashboard charts.

Because the hub compares apps side by side, the fields written here match the
hub's own ledger exactly: ``{timestamp, path, device_type, user_agent,
visitor_key, bot_type?, location?}``. Crawler rows (``device_type == "bot"``)
additionally carry ``{vendor_key, vendor_class, verified, lane}`` since
1.6.34; human rows are unchanged.

Since 1.6.34 the same file holds a SECOND table, ``reads``: one row per
corpus document dash-improve-my-llms served, handed to :meth:`record_read`
through the package's ``on_document_read`` hook (2.8.0). ``visits`` is what
the request hook saw; ``reads`` is what the package says it served (tier,
verdict, bytes, verified vendor). They are joined by ``lib/traffic_rollup``
and never summed into each other.

THERE IS ONE CLASSIFIER — ``dash_improve_my_llms.classify()``. This module
carried its own User-Agent lists for a year; they filed ClaudeBot (Anthropic's
*training* crawler) under "search", still named the retired ``anthropic-ai`` /
``claude-web`` tokens, knew nothing of ``bytespider`` or ``Claude-User``, and
counted every UA-less or library client (``httpx``, ``Go-http-client``) as a
person. Every host in the fleet reported those numbers. The lists are gone:
``is_bot`` / ``detect_bot_type`` keep their names for callers and delegate. A
token the registry lacks is a pushback to the package, never a list here —
``tests/test_analytics_classifier.py`` greps this file for the old tokens.

Accuracy notes (these are the things that quietly wreck the numbers):

- **Network machinery is never a visitor.** Any request whose User-Agent
  carries ``lib.constants.INTERNAL_UA_TOKEN`` is dropped in ``track_visit``
  before device detection — the network's internal-traffic contract
  (https://2plot.ai/docs/satellite-analytics). ``/healthz`` is dropped there
  too. Both are write-time rules on purpose; see the comment in ``track_visit``.
- **The client address is never stored** (sync 1.6.44 item 16). It is read
  from the proxy headers — behind Cloudflare/Render ``remote_addr`` is the
  *proxy*, so every visitor would otherwise collapse into one — hashed with a
  per-deployment salt into ``visitor_key``, and discarded. Set
  ``ANALYTICS_KEEP_CLIENT_IP=1`` to keep the raw value; the default is off,
  and it is the same switch ``record_read`` already honoured.
- **Location comes only from the edge headers** the CDN attached
  (``CF-IPCountry``, ``CF-IPCity``). There is no outbound lookup: the
  ip-api.com call that used to POST every reader's address to a third party
  over plaintext HTTP is gone. A request with neither header carries no
  location, which is what this host actually knows.
- **Writes are buffered, locked and pruned.** Multiple gunicorn/uvicorn workers
  share this file; without an ``flock`` around the read-modify-write they
  silently overwrite each other's hits. The buffer keeps a docs site from
  rewriting the whole file on every request, and retention keeps it bounded.
"""
import atexit
import json
import os
import threading
import time
import hashlib
import secrets
from pathlib import Path
from datetime import datetime, timedelta

from dash_improve_my_llms import classify
from dash_improve_my_llms._ledger import EVENT_FIELDS

try:  # POSIX only — Windows dev boxes just run without the cross-process lock
    import fcntl
except ImportError:  # pragma: no cover
    fcntl = None


_REPO_ROOT = Path(__file__).resolve().parent.parent

# How many hits to hold in memory before touching disk, and the longest a hit
# may sit in the buffer. Both are tiny; the point is to turn "rewrite the file
# on every request" into "rewrite it a few times a minute".
FLUSH_EVERY = int(os.getenv("ANALYTICS_FLUSH_EVERY", "10"))
FLUSH_INTERVAL_S = float(os.getenv("ANALYTICS_FLUSH_INTERVAL_S", "30"))

# Retention. The hub keeps the durable history (every rollup we POST rides its
# heartbeat store), so this file only needs enough runway to build a rollup and
# show recent local history.
RETENTION_DAYS = int(os.getenv("ANALYTICS_RETENTION_DAYS", "45"))
MAX_VISITS = int(os.getenv("ANALYTICS_MAX_VISITS", "20000"))

# The read event carries the client address; it is dropped from the stored
# row unless the operator opts in. The row is shown to vendors later (the
# ledger plan's reconciliation) and the package's docstring leaves the
# decision to the app — this is the decision.
KEEP_CLIENT_IP = os.getenv("ANALYTICS_KEEP_CLIENT_IP", "0") == "1"

# The keys a crawler row gains from classify(); a human row never carries
# them, so the v3 rollup sees human rows byte-for-byte as before.
_VENDOR_KEYS = ("vendor_key", "vendor_class", "verified", "lane")

_IP_HEADERS = (
    "cf-connecting-ip",     # Cloudflare
    "true-client-ip",       # Cloudflare Enterprise / Akamai
    "x-real-ip",            # nginx
    "x-forwarded-for",      # everything else (first hop = the client)
)

_PRIVATE_PREFIXES = ('10.', '172.', '192.168.', 'fe80:', 'fc00:', 'fd00:')


def analytics_path() -> Path:
    """Resolve the ledger path (env override, else repo root).

    Absolute on purpose: the old relative default wrote a *different* file
    depending on the process working directory, which split the numbers.
    """
    return Path(os.getenv("TRAFFIC_ANALYTICS_FILE")
                or _REPO_ROOT / "visitor_analytics.json")


def _lower_headers(headers) -> dict:
    """Normalise any header mapping (Flask, Starlette, dict) to lowercase."""
    if not headers:
        return {}
    try:
        return {str(k).lower(): v for k, v in headers.items()}
    except Exception:
        return {}


def client_ip(headers=None, fallback=None):
    """The real client address, reading proxy headers before ``remote_addr``."""
    lc = _lower_headers(headers)
    for name in _IP_HEADERS:
        raw = lc.get(name)
        if not raw:
            continue
        # X-Forwarded-For is "client, proxy1, proxy2" — the client is first.
        ip = str(raw).split(",")[0].strip()
        if ip:
            return ip
    return fallback


def header_country(headers=None):
    """ISO country code from Cloudflare's ``CF-IPCountry``, if present.

    ``XX`` (unknown) and ``T1`` (Tor) are not countries — treated as absent.
    """
    cc = (_lower_headers(headers).get("cf-ipcountry") or "").strip().upper()
    return cc if cc and cc not in ("XX", "T1") else None


# ---------------------------------------------------------------------------
# THE VISITOR KEY (sync 1.6.44 item 16 — privacy by design)
# ---------------------------------------------------------------------------
# No raw client address is stored, and no address ever leaves this process.
#
# What was here until 2026-09-05, and why it is gone: `_geolocate` POSTed
# every non-bot visitor's IP address to `http://ip-api.com` — a third party,
# over PLAINTEXT HTTP — to turn it into a city, and `geo_for` /
# `_backfill_geo` ran that lookup on a background thread so the round trip
# did not block a page view. The visit row then stored the raw
# `ip_address` alongside it. Three separate problems in one path: a
# third-party disclosure of the reader's address that nothing on the site
# disclosed, in cleartext, plus an identifier in the ledger that makes every
# row personally identifying for as long as retention holds it.
#
# What replaces it: nothing outbound at all. Location comes only from the
# edge headers the CDN already attached to the request (`cf-ipcountry`, and
# `cf-ipcity` where present) — facts this host was told, not facts it went
# and looked up. Identity across requests comes from a SALTED HASH of the
# address, computed here and never stored in reverse.
#
# The salt lives in a file that is gitignored IN THE SAME COMMIT that
# introduced it. A committed salt would make every visitor_key in every fork
# recomputable by anyone holding the repo, which undoes the item entirely —
# the hash would be a slower way of storing the address.
VISITOR_SALT_FILE = Path(
    os.getenv("VISITOR_SALT_FILE")
    or (_REPO_ROOT / ".visitor_salt")
)

_salt_lock = threading.Lock()
_salt_cache: dict = {}


def _visitor_salt() -> bytes:
    """The per-deployment salt, created on first use.

    Regenerating it (a fresh container with no disk, say) rotates every
    visitor key — returning readers look new. That is the correct trade for a
    documentation site's ledger: the salt is not a secret that must survive,
    it is the thing that stops the hash being reversible by anyone who can
    guess an address, and rotation only costs continuity of a count.
    """
    with _salt_lock:
        cached = _salt_cache.get("salt")
        if cached:
            return cached
        salt = None
        try:
            salt = VISITOR_SALT_FILE.read_bytes().strip() or None
        except Exception:
            salt = None
        if not salt:
            salt = secrets.token_hex(32).encode()
            try:
                VISITOR_SALT_FILE.parent.mkdir(parents=True, exist_ok=True)
                VISITOR_SALT_FILE.write_bytes(salt)
                os.chmod(VISITOR_SALT_FILE, 0o600)
            except Exception:
                # A read-only filesystem is not a reason to start storing
                # addresses. An in-memory salt still hashes; it just rotates
                # on restart.
                pass
        _salt_cache["salt"] = salt
        return salt


def visitor_key_for(ip_address, user_agent) -> str:
    """A stable, non-reversible per-visitor identifier.

    Salted SHA-256 over address + User-Agent, truncated. The User-Agent is in
    the hash for the same reason the OLD composite key used it: two readers
    behind one NAT are not one reader.
    """
    material = b"|".join([
        _visitor_salt(),
        (ip_address or "?").encode("utf-8", "replace"),
        (user_agent or "?").encode("utf-8", "replace"),
    ])
    return hashlib.sha256(material).hexdigest()[:16]


def header_location(headers=None):
    """Location from the EDGE HEADERS only — never a lookup.

    Country where the CDN gave one, city too where it gave that. A request
    with neither header carries no location at all, which is the honest
    answer: this host does not know.
    """
    lower = _lower_headers(headers)
    cc = header_country(headers)
    city = (lower.get("cf-ipcity") or "").strip() or None
    if not cc and not city:
        return None
    out = {}
    if cc:
        out["country"] = cc
        out["country_code"] = cc
    if city:
        out["city"] = city
    return out


class AnalyticsTracker:
    """Track visitor analytics to JSON file."""

    def __init__(self, data_file=None):
        self._data_file = Path(data_file) if data_file else None
        self._buffer = []
        self._reads_buffer = []
        self._buffer_lock = threading.Lock()
        self._last_flush = time.time()
        atexit.register(self.flush)

    @property
    def data_file(self) -> Path:
        return self._data_file or analytics_path()

    def _ensure_file_exists(self):
        """Create analytics file if it doesn't exist."""
        if not self.data_file.exists():
            self.data_file.parent.mkdir(parents=True, exist_ok=True)
            self.data_file.write_text(json.dumps({
                "visits": [],
                "reads": [],
                "stats": {
                    "desktop": 0,
                    "mobile": 0,
                    "tablet": 0,
                    "bot": 0,
                    "total": 0
                }
            }, indent=2))

    def detect_device_type(self, user_agent, classification=None):
        """Detect device type from user agent string.

        ``classification`` is an already-computed ``classify()`` result so a
        caller that needs the vendor keys too classifies exactly once.
        """
        # Bots first — including the EMPTY User-Agent, which the package puts
        # on the crawler lane (no browser sends none) and this method used to
        # file as a desktop human.
        c = classification if classification is not None else _classify(user_agent)
        if c["lane"] == "crawler":
            return "bot"

        user_agent = (user_agent or "").lower()

        # Check for tablet before mobile — iPads and most Android tablets also
        # carry a mobile token, so the mobile test would swallow them.
        if any(tablet in user_agent for tablet in ['ipad', 'tablet', 'kindle', 'silk']):
            return "tablet"

        if any(mobile in user_agent for mobile in ['mobile', 'android', 'iphone', 'ipod', 'blackberry', 'windows phone']):
            return "mobile"

        return "desktop"

    def is_bot(self, user_agent, client_ip=None):
        """Is this request on the crawler lane? Delegates to the package.

        Kept by name for callers and forks' tests; the body is the one
        classifier. Note the contract change from the list this replaced:
        an absent UA is a bot now, not a desktop visitor.
        """
        return _classify(user_agent, client_ip)["lane"] == "crawler"

    def detect_bot_type(self, user_agent, client_ip=None):
        """``training`` / ``search`` / ``traditional`` / ``unknown``, per the
        package's vendor registry — the same buckets robots.txt is rendered
        from, so what the site SAYS about a vendor and what it COUNTS agree."""
        return _classify(user_agent, client_ip)["bot_type"] or "unknown"

    def track_visit(self, path, user_agent, ip_address=None, headers=None):
        """Track a visitor.

        ``headers`` is optional but strongly recommended — it's what makes the
        client IP and country correct behind a proxy. See ``client_ip``.
        """
        # --- The network's internal-traffic contract, applied at WRITE time --
        #
        # https://2plot.ai/docs/satellite-analytics, "Internal traffic": a
        # request carrying INTERNAL_UA_TOKEN is 2plot machinery talking to
        # itself and is counted nowhere. This has to happen HERE, before
        # `detect_device_type`, and not in lib/traffic_rollup's read-time
        # filter, for two reasons:
        #
        #   1. classification would run first, and the health sweep and smoke
        #      batteries look like bots — they would land in `bot_hits` and be
        #      reported to the hub as crawler interest in these docs;
        #   2. the ledger is what a person reads on a local analytics view. A
        #      row that exists but is filtered on the way out is still a row
        #      somebody has to know to discount.
        #
        # The token is matched case-insensitively so a caller may capitalise
        # its suffix however it likes.
        from lib.constants import INTERNAL_UA_TOKEN

        if INTERNAL_UA_TOKEN in (user_agent or "").lower():
            return

        # Skip internal Dash paths and static assets. `/healthz` and `/health`
        # are here too: the hub sweeps /healthz hourly and Render's own probe
        # hits it far more often than that, so storing it turns the ledger into
        # a record of monitoring. lib/traffic_rollup also drops it at read time
        # — that stays, for ledgers written before this rule existed.
        skip_paths = [
            '.css', '.js', '.png', '.jpg', '.ico', '.svg', '.woff', '.woff2', '.ttf', '.eot',
            '_dash', '_reload-hash', 'favicon', '/_dash-update-component',
            '/_dash-layout', '/_dash-dependencies', '/_dash-component-suites',
            '/assets/', '/healthz', '/health', '[]'  # Also skip malformed paths
        ]
        if any(skip in path for skip in skip_paths):
            return

        # Only track valid paths that start with /
        if not path or not path.startswith('/') or path.startswith('//'):
            return

        # Resolve the REAL address first: `verified` is computed against the
        # client, and behind Cloudflare/Render `ip_address` is the proxy.
        ip_address = client_ip(headers, ip_address)

        # Classify exactly once per request — lane, bucket and vendor come
        # from the same call, so a row can never disagree with itself.
        c = _classify(user_agent, ip_address)
        device_type = self.detect_device_type(user_agent, classification=c)

        visit_data = {
            "timestamp": datetime.now().isoformat(),
            "path": path,
            "device_type": device_type,
            "user_agent": user_agent or "Unknown",
        }

        # Crawler rows carry the vendor identity; human rows are unchanged
        # byte-for-byte (the v3 rollup's tests pin that shape).
        if device_type == "bot":
            visit_data["bot_type"] = c["bot_type"] or "unknown"
            for key in _VENDOR_KEYS:
                visit_data[key] = c.get(key)

        # THE ADDRESS IS HASHED, NEVER STORED (sync 1.6.44 item 16). The row
        # keeps a salted, non-reversible `visitor_key` so sessionisation and
        # visitor counts still work, and `ip_address` is written only when an
        # operator has explicitly opted in — the same switch record_read
        # already honours, so both tables obey one rule.
        visit_data["visitor_key"] = visitor_key_for(ip_address, user_agent)
        if ip_address and KEEP_CLIENT_IP:
            visit_data["ip_address"] = ip_address

        # Location from the EDGE HEADERS ONLY — no outbound lookup exists any
        # more. A request the CDN told us nothing about carries no location,
        # which is the honest answer rather than a guess.
        location = header_location(headers)
        if location:
            visit_data["location"] = location

        self._enqueue(self._buffer, visit_data)

    def record_read(self, event):
        """Keep one read event from dash-improve-my-llms' ``on_document_read``.

        Registered once in ``run.py``. The package hands over every key in
        ``_ledger.EVENT_FIELDS`` for each corpus document it served — tier,
        lane, vendor, verified, policy, verdict, status, bytes — and does no
        I/O of its own. This is where the row is kept: the ``reads`` table of
        the same ledger, same buffer discipline, same lock, same retention.

        Called synchronously on the request path by the package, which also
        catches anything raised here (fail-open, warned once). Keep it cheap:
        it appends; the flush does the disk work.

        ``client_ip`` is dropped unless ``ANALYTICS_KEEP_CLIENT_IP=1``.

        THE INTERNAL-TRAFFIC DROP APPLIES HERE TOO (1.6.43 item 1, found by
        pipdocs). "Counted nowhere" includes the READ TABLE: a host whose
        contract says token-carrying traffic is counted nowhere, and whose
        ``reads`` table counts it, holds half the contract. The network's own
        machinery — the hub's hourly health sweep, every satellite's link
        audit, every post-deploy battery — fetches corpus documents, so
        without this it is the busiest "vendor" on the board.

        Keyed on ``ua``, which is what ``EVENT_FIELDS`` calls it. There is no
        ``user_agent`` key on a read event, and a drop keyed on the wrong
        name is silently a no-op — this item's own failure mode. Verified
        against the resolved wheel, not inferred:
        ``tests/test_internal_traffic.py`` asserts ``ua`` is in
        ``EVENT_FIELDS`` so a rename between package versions fails loudly
        here rather than quietly restoring the leak in production.

        BEFORE the row is built, mirroring ``track_visit``, so the ordering
        cannot drift apart from the rule it implements.
        """
        if not isinstance(event, dict):
            return
        from lib.constants import INTERNAL_UA_TOKEN

        if INTERNAL_UA_TOKEN in (event.get("ua") or "").lower():
            return
        row = {k: event.get(k) for k in EVENT_FIELDS}
        if not KEEP_CLIENT_IP:
            row.pop("client_ip", None)
        row["kind"] = "read"
        self._enqueue(self._reads_buffer, row)

    def _enqueue(self, buffer, row):
        with self._buffer_lock:
            buffer.append(row)
            pending = len(self._buffer) + len(self._reads_buffer)
            due = (pending >= FLUSH_EVERY
                   or (time.time() - self._last_flush) >= FLUSH_INTERVAL_S)
        if due:
            self.flush()

    # ------------------------------------------------------------------ disk --

    def flush(self):
        """Write buffered hits to disk under a cross-process lock.

        Safe to call at any time (the satellite reporter calls it before
        building a rollup so the numbers include the current minute).
        """
        with self._buffer_lock:
            pending, self._buffer = self._buffer, []
            reads, self._reads_buffer = self._reads_buffer, []
            self._last_flush = time.time()
        if not pending and not reads:
            return
        try:
            self._write(pending, reads)
        except Exception:
            # Never lose the app over analytics; put the hits back so the next
            # flush can retry them.
            with self._buffer_lock:
                self._buffer = pending + self._buffer
                self._reads_buffer = reads + self._reads_buffer

    def _write(self, pending, reads=()):
        self._ensure_file_exists()
        path = self.data_file
        lock_path = path.with_suffix(path.suffix + ".lock")
        lock_fh = open(lock_path, "a+") if fcntl else None
        try:
            if lock_fh:
                fcntl.flock(lock_fh, fcntl.LOCK_EX)
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                if not isinstance(data, dict):
                    raise ValueError("ledger is not an object")
            except Exception:
                data = {"visits": [], "reads": [],
                        "stats": {"desktop": 0, "mobile": 0,
                                  "tablet": 0, "bot": 0, "total": 0}}

            visits = data.setdefault("visits", [])
            # A ledger written before 1.6.34 has no `reads`; absence is empty.
            read_rows = data.setdefault("reads", [])
            stats = data.setdefault("stats", {})
            visits.extend(pending)
            for v in pending:
                dt = v["device_type"]
                stats[dt] = stats.get(dt, 0) + 1
                stats["total"] = stats.get("total", 0) + 1

            data["visits"] = _prune(visits)
            read_rows.extend(reads)
            data["reads"] = _prune(read_rows, stamp=_read_stamp)

            # Atomic replace: a crash mid-write can't leave a truncated ledger.
            tmp = path.with_suffix(path.suffix + ".tmp")
            with open(tmp, 'w') as f:
                json.dump(data, f, indent=2)
            os.replace(tmp, path)
        finally:
            if lock_fh:
                try:
                    fcntl.flock(lock_fh, fcntl.LOCK_UN)
                finally:
                    lock_fh.close()


def _visit_stamp(v):
    return v.get("timestamp") or ""


def _read_stamp(r):
    """Read rows carry the package's epoch ``ts``; compare on the same ISO
    axis the visit rows use so one retention rule covers both tables."""
    ts = r.get("ts")
    try:
        return datetime.fromtimestamp(float(ts)).isoformat()
    except (TypeError, ValueError, OverflowError, OSError):
        return ""


def _prune(rows, stamp=_visit_stamp):
    """Drop rows older than the retention window, then cap the total."""
    if RETENTION_DAYS > 0:
        cutoff = (datetime.now() - timedelta(days=RETENTION_DAYS)).isoformat()
        rows = [v for v in rows if stamp(v) >= cutoff]
    if MAX_VISITS > 0 and len(rows) > MAX_VISITS:
        rows = rows[-MAX_VISITS:]
    return rows


def _vendor_class_from_registry(vendor_key):
    """``vendors.get_vendor(key).cls``, or None.

    THE PACKAGE'S OWN REGISTRY, never a local map (sync 1.6.44 item 8). A
    second copy of this mapping in this repo is the same defect as the UA
    list the tracker used to carry: it goes stale silently, and the value it
    reports is then this app's opinion rather than the classification the
    rest of the network is grouping by.
    """
    if not vendor_key:
        return None
    try:
        from dash_improve_my_llms import vendors

        vendor = vendors.get_vendor(vendor_key)
    except Exception:
        return None
    return getattr(vendor, "cls", None) or None


def _classify(user_agent, client_ip=None):
    """The one classifier, made total: never raises, always has ``lane``.

    ``vendor_class`` PREFERS what the package emitted and derives only where
    it is absent (sync 1.6.44 item 8). Both halves are load-bearing, and the
    reason is this fork's `>=2.8.0` floor: `vendor_class` joined
    ``EVENT_FIELDS`` between dimll 2.9.0 and 2.9.4, so a resolved wheel below
    that emits a `vendor_key` with NO class, and a pure pass-through wrote
    nulls into every crawler row while the registry knew the answer all
    along. Preferring the event keeps the package authoritative when it does
    speak; deriving fills the gap when it does not.
    """
    try:
        c = classify(user_agent or "", client_ip)
    except Exception:
        c = {}
    vendor_key = c.get("vendor_key")
    return {
        "lane": c.get("lane") or "browser",
        "bot_type": c.get("bot_type"),
        "vendor_key": vendor_key,
        "vendor_class": (c.get("vendor_class")
                         or _vendor_class_from_registry(vendor_key)),
        "verified": c.get("verified") or "n/a",
    }


# Global tracker instance
tracker = AnalyticsTracker()
