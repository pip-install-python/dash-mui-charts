"""Local traffic recorder — the data source for the satellite rollup.

Every hit lands as one JSON line in a per-day file; ``lib/traffic_report``
folds those files into the hourly rollup this app POSTs to the 2plot.ai
hub (contract: 2plotai/docs/network/satellite-analytics.md).

Two kinds of row, and the distinction is the whole point:

- ``source="doc"`` — an HTTP document request, written by the
  ``before_request`` hook in app.py. Crawlers only ever appear here: they
  do not run JavaScript, so they never reach a Dash callback.
- ``source="spa"`` — a RENDERED PAGE VIEW, written by the ``url.pathname``
  callback in app.py. This app is a single-page app (every doc page is a
  ``dcc.Location`` navigation), so document requests alone would report
  one hit per visitor with ``/`` as the only page and no measurable
  session. The spa rows are the real page-view stream.

Definitions are kept identical to the hub's (2plotai/lib/traffic_insights)
so the numbers compare across the network: a visitor is an (IP, user-agent)
pair, and the bot pattern list below is copied verbatim.

Storage is append-only on purpose: render.yaml runs gunicorn with two
workers, and a single ``O_APPEND`` line write under the pipe-buffer size is
atomic, whereas a read-modify-write of one JSON blob would lose hits
between processes. Both workers write the same day file and read all of it.

Env:
    ANALYTICS_DIR — where day files live (default ``<repo>/analytics``).
                    Point it at a mounted disk to survive deploys.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import threading
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

RETENTION_DAYS = 3        # the rollup only ever reads today + yesterday

# Copied verbatim from 2plotai/lib/traffic_insights._BOT_NAMES so this app's
# human/bot split matches the hub's. First match wins — specific → generic.
_BOT_NAMES = [
    ('gptbot', 'GPTBot'), ('chatgpt-user', 'ChatGPT-User'), ('oai-searchbot', 'OAI-SearchBot'),
    ('claudebot', 'ClaudeBot'), ('claude-web', 'Claude-Web'), ('anthropic', 'Anthropic'),
    ('perplexitybot', 'PerplexityBot'), ('youbot', 'YouBot'),
    ('google-extended', 'Google-Extended'), ('googlebot', 'Googlebot'),
    ('bingbot', 'Bingbot'), ('duckduckbot', 'DuckDuckBot'), ('slurp', 'Yahoo Slurp'),
    ('yandex', 'Yandex'), ('baidu', 'Baidu'), ('ccbot', 'CCBot'), ('facebookbot', 'FacebookBot'),
    ('python-requests', 'python-requests'), ('curl', 'curl'), ('wget', 'wget'),
    ('scraper', 'Scraper'), ('spider', 'Spider'), ('crawler', 'Crawler'), ('bot', 'Other bot'),
]

# Paths that are never a page view: Dash plumbing, static assets, probes.
_SKIP_FRAGMENTS = (
    '/assets/', '/_dash', '/_reload-hash', '/_favicon', 'favicon',
    '/healthz', '/robots.txt', '/sitemap', '/llms.txt', '[]',
)
_SKIP_SUFFIXES = ('.css', '.js', '.map', '.png', '.jpg', '.jpeg', '.gif', '.ico',
                  '.svg', '.webp', '.woff', '.woff2', '.ttf', '.eot', '.txt', '.xml')

_write_lock = threading.Lock()   # orders writes within a process; across
                                 # processes O_APPEND does the ordering


def analytics_dir() -> Path:
    return Path(os.environ.get("ANALYTICS_DIR")
                or Path(__file__).resolve().parent.parent / "analytics")


def day_file(date: str | None = None) -> Path:
    """Path of one day's hit log (the app's own local day — consistent is
    all the contract asks)."""
    date = date or datetime.now().strftime("%Y-%m-%d")
    return analytics_dir() / f"hits-{date}.jsonl"


def is_bot(user_agent: str | None) -> bool:
    ua = (user_agent or "").lower()
    return any(pat in ua for pat, _ in _BOT_NAMES)


def bot_name(user_agent: str | None) -> str:
    ua = (user_agent or "").lower()
    for pat, name in _BOT_NAMES:
        if pat in ua:
            return name
    return "Unknown bot"


def visitor_key(ip: str | None, user_agent: str | None) -> str:
    """The hub's visitor identity: an (IP, browser) pair. Shared IPs can
    merge people and private windows can split them — stated, not hidden."""
    ua = hashlib.md5((user_agent or "?").encode()).hexdigest()[:8]
    return f"{ip or '?'}|{ua}"


def client_ip(headers=None, remote_addr: str | None = None) -> str | None:
    """The real client address behind Render's proxy (and Cloudflare, if a
    CF-fronted domain is ever put in front)."""
    try:
        get = headers.get if headers is not None else (lambda _k, _d=None: None)
        cf = (get("CF-Connecting-IP") or "").strip()
        if cf:
            return cf
        fwd = (get("X-Forwarded-For") or "").strip()
        if fwd:
            return fwd.split(",")[0].strip()
    except Exception:
        pass
    return remote_addr


def cf_country(headers=None) -> str | None:
    """ISO country from Cloudflare's free header when present. This app is
    on onrender.com today (no CF), so lib/traffic_report falls back to an
    IP lookup — but the day a CF-fronted domain fronts it, geo gets free
    and accurate with no code change."""
    try:
        cc = (headers.get("CF-IPCountry") or "").strip().upper() if headers else ""
    except Exception:
        return None
    return cc if len(cc) == 2 and cc != "XX" else None


def trackable_path(path: str | None) -> bool:
    """True for paths that represent a page a person could read."""
    if not path or not path.startswith("/") or path.startswith("//"):
        return False
    low = path.lower()
    return not (any(f in low for f in _SKIP_FRAGMENTS)
                or low.endswith(_SKIP_SUFFIXES))


def record(path: str | None, user_agent: str | None, ip: str | None,
           source: str = "doc", country: str | None = None) -> None:
    """Append one hit. Never raises — analytics must not break a page view."""
    try:
        # The network's internal-traffic contract, applied at WRITE time,
        # before bot classification: a UA carrying the token is 2plot
        # machinery talking to itself (hub health sweeps, CI batteries,
        # smoke probes) and is counted NOWHERE — not as a bot, not ever.
        from lib.constants import INTERNAL_UA_TOKEN

        if INTERNAL_UA_TOKEN in (user_agent or "").lower():
            return
        if not trackable_path(path):
            return
        row = {
            "ts": datetime.now().isoformat(timespec="seconds"),
            "path": path[:160],
            "ua": (user_agent or "")[:300],
            "ip": ip or "",
            "bot": is_bot(user_agent),
            "source": source,
        }
        if country:
            row["country"] = country
        line = json.dumps(row, separators=(",", ":")) + "\n"
        target = day_file()
        with _write_lock:
            target.parent.mkdir(parents=True, exist_ok=True)
            # O_APPEND: two gunicorn workers can share this file safely.
            with open(target, "a", encoding="utf-8") as fh:
                fh.write(line)
    except Exception:  # noqa: BLE001 — recording is best-effort, always
        logger.debug("analytics record failed", exc_info=True)


def load_day(date: str | None = None) -> list[dict]:
    """Every row of one day, oldest first. Corrupt lines are skipped."""
    out: list[dict] = []
    try:
        with open(day_file(date), encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except ValueError:
                    continue
    except FileNotFoundError:
        return []
    except Exception:  # noqa: BLE001
        logger.debug("analytics read failed", exc_info=True)
        return out
    return out


def prune(keep_days: int = RETENTION_DAYS) -> None:
    """Drop day files older than the retention window (called from the
    reporter thread, never from a request)."""
    try:
        keep = {(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
                for i in range(keep_days + 1)}
        for f in analytics_dir().glob("hits-*.jsonl"):
            if f.stem.replace("hits-", "") not in keep:
                f.unlink(missing_ok=True)
    except Exception:  # noqa: BLE001
        logger.debug("analytics prune failed", exc_info=True)
