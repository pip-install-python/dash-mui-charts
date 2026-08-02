"""Satellite traffic reporting — dash-mui-charts → the 2plot.ai hub.

2plot.ai is the analytics home for the whole network: its owner-only
/traffic dashboard charts every app's daily humans/bots, visitors,
sessions, top pages and countries. Each satellite POSTs a signed rollup to
``POST {hub}/api/satellite/traffic`` hourly; re-POSTing the same
(app, date) overwrites, so today's numbers just firm up through the day.
Contract: 2plotai/docs/network/satellite-analytics.md (v1 required fields
plus every v2 optional field are sent).

Pieces here:
- ``build_rollup(date)`` — fold lib/analytics' per-day hit log into the
  payload. Session rule matches the hub's: hits grouped per unique
  (ip, user-agent) human visitor, split on 30-minute gaps;
  median_session_s covers MULTI-HIT sessions only (never padded).
- ``report_traffic(rollup)`` — HMAC-SHA256 sender (the wallet-provision
  scheme: ``X-AI-Canvas-Timestamp`` + ``X-AI-Canvas-Signature`` over
  ``f"{ts}." + raw_body`` keyed by CROSS_APP_WEBHOOK_SECRET). The secret is
  never logged.
- ``start_traffic_reporter()`` — hourly daemon thread. Reports today AND
  yesterday each cycle so a deploy near midnight can't strand yesterday's
  tail. GATED to prod (``RENDER`` env) unless ``TRAFFIC_REPORT=1`` — local
  dev holds the same shared secret, and a dev POST would OVERWRITE the
  hub's real (charts, date) row with dev counts.
- ``register_healthz(server)`` — the tiny Flask liveness probe the hub's
  hourly satellite sweep GETs (it must not render the whole Dash index).

THE COUNTING RULE (this app is a single-page app — see lib/analytics):

    human_hits  = "spa" rows with a human UA   (one per rendered page,
                  initial load included)
    bot_hits    = "doc" rows with a bot UA     (crawlers run no JS, so
                  they never produce a spa row)

Human "doc" rows and bot "spa" rows are recorded but deliberately left out
of the sums. That is what stops a human's first page load being counted
twice — once as the document request, once as the page view — and it is
also what keeps a JS-executing crawler out of the human sessions. Every
other field (visitors, sessions, median, pages, countries) derives from the
human spa rows, which is why `pages` shows the real doc pages people read
instead of a single `/`.

Known limitation: Render gives this service no persistent disk, so a deploy
or restart wipes the day's hit log and the next hourly POST overwrites the
hub row with a smaller number for that day (the hub is last-report-wins and
offers no read-back). Point ``ANALYTICS_DIR`` at a mounted disk to fix it.
"""
from __future__ import annotations

import hashlib
import hmac
import ipaddress
import json
import logging
import os
import random
import threading
import time
import urllib.request
from datetime import datetime, timedelta
from statistics import median

from lib import analytics

logger = logging.getLogger(__name__)

APP_KEY = "charts"                # our key in the hub's network directory
SESSION_GAP_S = 30 * 60           # the hub's session-split rule — keep in sync
REPORT_INTERVAL_S = 60 * 60
_STARTUP_DELAY_S = 90             # let the app settle before the first POST
_GEO_LOOKUPS_PER_PASS = 60        # ip-api.com is free at ~45 req/min

_started = False


def _secret() -> str:
    return (os.environ.get("CROSS_APP_WEBHOOK_SECRET") or "").strip()


def hub_url() -> str:
    """TRAFFIC_HUB_URL → PRIMARY_HOST → the hub's canonical domain."""
    base = (os.environ.get("TRAFFIC_HUB_URL")
            or os.environ.get("PRIMARY_HOST")
            or "https://2plot.ai")
    return base.rstrip("/")


def reporting_enabled() -> bool:
    """Prod-only unless forced: dev machines hold the same shared secret, and
    the hub OVERWRITES per (app, date) — a local run must never clobber the
    real numbers. TRAFFIC_REPORT=0 is the prod kill switch."""
    if not _secret():
        return False
    forced = os.environ.get("TRAFFIC_REPORT")
    if forced is not None:
        return forced == "1"
    return bool(os.environ.get("RENDER"))


# --------------------------------------------------------------------------- #
# Geo — resolved off the request path, in the reporter thread                   #
# --------------------------------------------------------------------------- #

def _geo_cache_path():
    return analytics.analytics_dir() / "geo_cache.json"


def _load_geo_cache() -> dict:
    try:
        with open(_geo_cache_path(), encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, dict) else {}
    except Exception:  # noqa: BLE001 — missing/corrupt cache → start empty
        return {}


def _save_geo_cache(cache: dict) -> None:
    try:
        path = _geo_cache_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps(cache), encoding="utf-8")
        tmp.replace(path)
    except Exception:  # noqa: BLE001
        logger.debug("geo cache write failed", exc_info=True)


def _is_public_ip(ip: str) -> bool:
    try:
        addr = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return not (addr.is_private or addr.is_loopback or addr.is_link_local
                or addr.is_reserved or addr.is_multicast)


def _lookup_country(ip: str) -> str | None:
    """One ip-api.com lookup (free, no key). Failures cache as unknown so a
    dead lookup isn't retried every hour."""
    try:
        import requests

        r = requests.get(f"http://ip-api.com/json/{ip}",
                         params={"fields": "status,countryCode"}, timeout=2)
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "success":
                cc = (data.get("countryCode") or "").strip().upper()
                return cc if len(cc) == 2 else None
    except Exception:  # noqa: BLE001 — geo is optional, never fatal
        logger.debug("geo lookup failed for %s", ip, exc_info=True)
    return None


def resolve_countries(ips, budget: int = _GEO_LOOKUPS_PER_PASS) -> dict:
    """ip → ISO country for the given addresses, cached on disk. Only public
    IPs are looked up, and at most ``budget`` new ones per call."""
    cache = _load_geo_cache()
    dirty = False
    for ip in ips:
        if not ip or ip in cache or not _is_public_ip(ip):
            continue
        if budget <= 0:
            break
        budget -= 1
        cache[ip] = _lookup_country(ip) or ""   # "" = looked up, unknown
        dirty = True
    if dirty:
        _save_geo_cache(cache)
    return cache


# --------------------------------------------------------------------------- #
# Rollup                                                                       #
# --------------------------------------------------------------------------- #

def build_rollup(date: str | None = None, rows: list[dict] | None = None,
                 geo: bool = True) -> dict:
    """The full v1+v2 payload for one local day (default: today).

    ``rows`` (test seam) defaults to that day's hit log; ``geo=False`` skips
    the ip-api enrichment so unit checks stay offline.
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    if rows is None:
        rows = analytics.load_day(date)

    # See THE COUNTING RULE in the module docstring.
    humans = [r for r in rows if r.get("source") == "spa" and not r.get("bot")]
    bot_hits = sum(1 for r in rows if r.get("source") == "doc" and r.get("bot"))

    rollup: dict = {
        "app": APP_KEY,
        "date": date,
        "human_hits": len(humans),
        "bot_hits": bot_hits,
    }

    # visitors — unique (ip, browser) pairs, humans only
    by_visitor: dict[str, list[float]] = {}
    for r in humans:
        try:
            ts = datetime.fromisoformat(r["ts"]).timestamp()
        except (KeyError, ValueError):
            continue
        by_visitor.setdefault(
            analytics.visitor_key(r.get("ip"), r.get("ua")), []).append(ts)
    rollup["visitors"] = len(by_visitor)

    # sessions — per-visitor hit groups split on 30-minute gaps (hub rule);
    # median_session_s from multi-hit sessions ONLY.
    session_count = 0
    spans: list[float] = []
    for stamps in by_visitor.values():
        stamps.sort()
        start = prev = stamps[0]
        hits = 1
        for ts in stamps[1:]:
            if ts - prev > SESSION_GAP_S:
                session_count += 1
                if hits > 1:
                    spans.append(prev - start)
                start, hits = ts, 1
            else:
                hits += 1
            prev = ts
        session_count += 1
        if hits > 1:
            spans.append(prev - start)
    rollup["sessions"] = session_count
    if spans:
        rollup["median_session_s"] = round(median(spans), 1)

    # pages — human page views per path, top 20
    page_hits: dict[str, int] = {}
    for r in humans:
        p = r.get("path") or "/"
        page_hits[p] = page_hits.get(p, 0) + 1
    rollup["pages"] = [{"path": p, "hits": n} for p, n in
                       sorted(page_hits.items(), key=lambda kv: -kv[1])[:20]]

    # countries — humans only, top 20. CF-IPCountry when a Cloudflare-fronted
    # domain ever supplies it; otherwise the cached ip-api lookup.
    cache = resolve_countries({r.get("ip") for r in humans}) if geo else {}
    country_hits: dict[str, int] = {}
    for r in humans:
        cc = (r.get("country") or cache.get(r.get("ip") or "") or "").upper()
        if len(cc) == 2:
            country_hits[cc] = country_hits.get(cc, 0) + 1
    if country_hits:
        rollup["countries"] = dict(
            sorted(country_hits.items(), key=lambda kv: -kv[1])[:20])

    return rollup


# --------------------------------------------------------------------------- #
# Sender                                                                       #
# --------------------------------------------------------------------------- #

def sign(body: bytes, ts: str, secret: str) -> str:
    """HMAC_SHA256(secret, f"{ts}." + raw_body) — the network's shared scheme."""
    return hmac.new(secret.encode(), f"{ts}.".encode() + body,
                    hashlib.sha256).hexdigest()


def report_traffic(rollup: dict, *, secret: str | None = None,
                   hub: str | None = None, timeout: float = 10.0) -> dict:
    """POST one rollup to the hub. Returns the hub's JSON reply; raises on
    network/HTTP errors (the daemon catches — a down hub must never hurt us)."""
    secret = secret or _secret()
    if not secret:
        raise RuntimeError("CROSS_APP_WEBHOOK_SECRET unset")
    body = json.dumps(rollup).encode()
    ts = str(int(time.time()))
    req = urllib.request.Request(
        f"{hub or hub_url()}/api/satellite/traffic", data=body,
        headers={"Content-Type": "application/json",
                 "X-AI-Canvas-Timestamp": ts,
                 "X-AI-Canvas-Signature": sign(body, ts, secret)})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def report_pass() -> None:
    """One reporting cycle: today + yesterday (self-heals deploy gaps and the
    midnight rollover — re-POSTs overwrite on the hub)."""
    today = datetime.now()
    for day in (today, today - timedelta(days=1)):
        date = day.strftime("%Y-%m-%d")
        try:
            rollup = build_rollup(date)
            res = report_traffic(rollup)
            logger.info("traffic report %s: %s human / %s bot → %s",
                        date, rollup["human_hits"], rollup["bot_hits"],
                        res.get("ok"))
        except Exception as e:  # noqa: BLE001 — reporting must never crash us
            logger.warning("traffic report %s failed: %r", date, e)
    analytics.prune()


def start_traffic_reporter() -> None:
    """Hourly reporter daemon. No-op when gated off.

    Both gunicorn workers run one: they read the same shared hit log, so the
    rollups are identical and last-write-wins makes the duplicate harmless.
    The jitter just keeps the two POSTs from landing at the same instant.
    """
    global _started
    if _started:
        return
    if not reporting_enabled():
        print("[traffic] satellite reporting OFF "
              "(needs CROSS_APP_WEBHOOK_SECRET + RENDER, or TRAFFIC_REPORT=1)")
        return
    _started = True

    def _loop():
        time.sleep(_STARTUP_DELAY_S + random.uniform(0, 60))
        while True:
            report_pass()
            time.sleep(REPORT_INTERVAL_S)

    threading.Thread(target=_loop, daemon=True, name="traffic-report").start()
    print(f"[traffic] satellite reporter ON → {hub_url()}/api/satellite/traffic "
          f"(hourly, app={APP_KEY!r})")


# --------------------------------------------------------------------------- #
# Health probe                                                                 #
# --------------------------------------------------------------------------- #

def register_healthz(server) -> None:
    """GET /healthz — the network liveness convention the hub's hourly
    satellite sweep polls. Tiny JSON, no Dash render, untracked by analytics."""
    from flask import jsonify

    @server.get("/healthz")
    def healthz():
        return jsonify({"ok": True, "app": APP_KEY})
