"""Headless verification for the satellite-analytics pipeline
(lib/analytics + lib/traffic_report + the app.py wiring). No server boot,
no outbound network.

Three things are checked, in order of how badly they'd bite:

1. THE COUNTING RULE — this app is a single-page app, so page views come
   from the url.pathname callback and document requests only supply the
   crawlers. The rollup must not double-count a human's first load.
2. THE APP WIRING — the Flask test client proves /healthz answers, that a
   document GET is recorded, and that the real Dash callback round-trip
   (POST /_dash-update-component) writes a page view.
3. THE SIGNATURE — the signed request our sender emits is fed through the
   HUB's own verifier (2plotai/lib/satellite_ingest.verify_and_record,
   loaded by file path). A pass there means 2plot.ai accepts our rollups
   verbatim. Without the sibling repo it degrades to a local recompute.

Run: python verify_traffic.py
"""
import importlib.util
import json
import os
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# Isolate every write from the real hit log, and keep the reporter asleep.
os.environ["ANALYTICS_DIR"] = tempfile.mkdtemp(prefix="charts-analytics-")
os.environ.pop("CROSS_APP_WEBHOOK_SECRET", None)

PASS, FAIL = "\033[32m✓\033[0m", "\033[31m✗\033[0m"
failures = []


def check(name, cond, detail=""):
    print(f"{PASS if cond else FAIL} {name}"
          + (f" — {detail}" if detail and not cond else ""))
    if not cond:
        failures.append(name)


# --------------------------------------------------------------------------- #
# 1. Recorder: skip rules, bot detection, proxied client IP                    #
# --------------------------------------------------------------------------- #
from lib import analytics  # noqa: E402

for noisy in ("/healthz", "/assets/app.css", "/_dash-update-component",
              "/_reload-hash", "/favicon.ico", "/robots.txt"):
    analytics.record(noisy, "Mozilla/5.0", "1.2.3.4", source="doc")
check("recorder skips probes, assets and Dash plumbing",
      analytics.load_day() == [], analytics.load_day())

check("bot UAs classified like the hub",
      all(analytics.is_bot(ua) for ua in
          ("Googlebot/2.1", "ClaudeBot/1.0", "python-requests/2.31", "curl/8"))
      and not analytics.is_bot("Mozilla/5.0 (Macintosh) Safari/605"))

check("client_ip prefers CF-Connecting-IP, then X-Forwarded-For",
      analytics.client_ip({"CF-Connecting-IP": "203.0.113.9"}, "10.0.0.1")
      == "203.0.113.9"
      and analytics.client_ip({"X-Forwarded-For": "198.51.100.7, 10.0.0.2"},
                              "10.0.0.1") == "198.51.100.7")

check("visitor identity is the hub's (ip, browser) pair",
      analytics.visitor_key("1.2.3.4", "UA-a")
      == analytics.visitor_key("1.2.3.4", "UA-a")
      != analytics.visitor_key("1.2.3.4", "UA-b"))


# --------------------------------------------------------------------------- #
# 2. Rollup: the counting rule, sessions, median, pages                        #
# --------------------------------------------------------------------------- #
from lib import traffic_report as tr  # noqa: E402

TODAY = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)


def row(minutes, path, source="spa", ua="Mozilla/5.0 (Macintosh)",
        ip="203.0.113.9"):
    return {"ts": (TODAY + timedelta(minutes=minutes)).isoformat(
                timespec="seconds"),
            "path": path, "ua": ua, "ip": ip,
            "bot": analytics.is_bot(ua), "source": source}


rows = [
    # one human: a hard load on / (doc + spa), then three SPA navigations
    row(0, "/", source="doc"),
    row(0, "/"),
    row(2, "/scatter"),
    row(5, "/heatmap"),
    row(9, "/tree-pro"),
    # …returns after a 45-minute gap: a second session, single hit
    row(54, "/candlestick"),
    # a second human, one page
    row(20, "/pie", ip="198.51.100.7", ua="Mozilla/5.0 (Windows)"),
    # a crawler: document requests only, never a page view
    row(30, "/", source="doc", ua="Googlebot/2.1", ip="66.249.66.1"),
    row(31, "/linechart-basic", source="doc", ua="Googlebot/2.1",
        ip="66.249.66.1"),
    # a JS-executing crawler: recorded, but kept out of the human numbers
    row(40, "/scatter", ua="ClaudeBot/1.0", ip="160.79.104.10"),
]
r = tr.build_rollup(TODAY.strftime("%Y-%m-%d"), rows=rows, geo=False)

check("human_hits counts page views, not the duplicate document request",
      r["human_hits"] == 6, r["human_hits"])
check("bot_hits counts crawler document requests only",
      r["bot_hits"] == 2, r["bot_hits"])
check("visitors = unique human (ip, browser) pairs",
      r["visitors"] == 2, r["visitors"])
check("sessions split on the hub's 30-minute gap",
      r["sessions"] == 3, r["sessions"])
check("median_session_s from multi-hit sessions only "
      "(single-hit visits never padded in)",
      r["median_session_s"] == 9 * 60, r.get("median_session_s"))
check("pages lists the real doc pages, not just /",
      [p["path"] for p in r["pages"]][:1] == ["/"]
      and {"/scatter", "/heatmap", "/tree-pro", "/pie"}
      <= {p["path"] for p in r["pages"]},
      r["pages"])
check("bot page views stay out of pages",
      all(p["path"] != "/scatter" or p["hits"] == 1 for p in r["pages"]),
      r["pages"])
check("payload carries app=charts and a YYYY-MM-DD date",
      r["app"] == "charts" and len(r["date"]) == 10, r)

empty = tr.build_rollup("1999-01-01", geo=False)
check("a day with no traffic is a valid zero rollup",
      empty["human_hits"] == 0 and empty["bot_hits"] == 0
      and "median_session_s" not in empty and "countries" not in empty)

check("reporting is OFF without the shared secret (dev can't clobber prod)",
      tr.reporting_enabled() is False)


# --------------------------------------------------------------------------- #
# 3. App wiring: healthz, document hit, and the real callback round-trip       #
# --------------------------------------------------------------------------- #
import app as demo_app  # noqa: E402  (boots the Dash app; reporter stays off)

client = demo_app.server.test_client()

hz = client.get("/healthz")
check("GET /healthz answers the hub's sweep without a Dash render",
      hz.status_code == 200 and hz.get_json() == {"ok": True, "app": "charts"},
      hz.data[:80])

before = len(analytics.load_day())
client.get("/", headers={"User-Agent": "Googlebot/2.1",
                         "X-Forwarded-For": "66.249.66.1"})
docs = [h for h in analytics.load_day()[before:] if h["source"] == "doc"]
check("a crawler's document GET is recorded as a bot doc hit",
      len(docs) == 1 and docs[0]["bot"] and docs[0]["ip"] == "66.249.66.1",
      docs)

before = len(analytics.load_day())
resp = client.post(
    "/_dash-update-component",
    json={"output": "analytics-sink.data",
          "outputs": {"id": "analytics-sink", "property": "data"},
          "inputs": [{"id": "url", "property": "pathname",
                      "value": "/tree-pro"}],
          "changedPropIds": ["url.pathname"]},
    headers={"User-Agent": "Mozilla/5.0 (Macintosh)",
             "X-Forwarded-For": "198.51.100.7"})
spa = [h for h in analytics.load_day()[before:] if h["source"] == "spa"]
check("the url.pathname callback records a real SPA page view",
      resp.status_code == 200 and len(spa) == 1
      and spa[0]["path"] == "/tree-pro" and spa[0]["ip"] == "198.51.100.7",
      (resp.status_code, spa))

check("the /healthz probe itself never lands in the traffic numbers",
      all(h["path"] != "/healthz" for h in analytics.load_day()))


# --------------------------------------------------------------------------- #
# 4. Signature: fed through the hub's own verifier                             #
# --------------------------------------------------------------------------- #
SECRET = "verify-only-secret"
body = json.dumps(r).encode()
ts = str(int(datetime.now().timestamp()))
sig = tr.sign(body, ts, SECRET)

hub_ingest = Path("/Users/pip/PycharmProjects/2plotai/lib/satellite_ingest.py")
if hub_ingest.exists():
    import types

    os.environ["CROSS_APP_WEBHOOK_SECRET"] = SECRET
    # Stand in for the hub's heartbeat store (its real one needs Postgres /
    # the JSONL event dir) and capture what it would persist.
    stored = {}
    pulse = types.ModuleType("lib.pulse")
    hb_stub = types.ModuleType("lib.pulse.heartbeat")
    hb_stub.record_note = lambda *a, **k: None
    hb_stub.record_api_call = lambda **kw: stored.update(kw.get("extras") or {})
    pulse.heartbeat = hb_stub
    sys.modules.setdefault("lib.pulse", pulse)
    sys.modules.setdefault("lib.pulse.heartbeat", hb_stub)

    # The ingest folds app ids through the hub's OWN lib.network_directory —
    # an absolute import that would otherwise resolve to THIS repo's lib
    # package and turn every payload into "bad payload". Load the real one
    # (pure data, no further imports) under the name the hub expects.
    nd_spec = importlib.util.spec_from_file_location(
        "lib.network_directory", hub_ingest.parent / "network_directory.py")
    nd_mod = importlib.util.module_from_spec(nd_spec)
    nd_spec.loader.exec_module(nd_mod)
    sys.modules["lib.network_directory"] = nd_mod

    spec = importlib.util.spec_from_file_location("hub_ingest", hub_ingest)
    hub = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hub)

    reply, status = hub.verify_and_record(
        body, {"X-AI-Canvas-Timestamp": ts, "X-AI-Canvas-Signature": sig})
    check("the hub's verifier accepts our signed rollup",
          status == 200 and reply.get("ok"), (status, reply))
    check("every v2 field survives the hub's validation and caps",
          stored.get("app") == "charts"
          and stored.get("human_hits") == r["human_hits"]
          and stored.get("visitors") == r["visitors"]
          and stored.get("sessions") == r["sessions"]
          and stored.get("median_session_s") == r["median_session_s"]
          and len(stored.get("pages") or []) == len(r["pages"]),
          stored)

    bad_reply, bad_status = hub.verify_and_record(
        body, {"X-AI-Canvas-Timestamp": ts, "X-AI-Canvas-Signature": "deadbeef"})
    check("the hub rejects a bad signature (the check is real)",
          bad_status == 400, (bad_status, bad_reply))
    del os.environ["CROSS_APP_WEBHOOK_SECRET"]
else:
    import hashlib
    import hmac
    check("signature matches the documented scheme (hub repo absent)",
          hmac.new(SECRET.encode(), f"{ts}.".encode() + body,
                   hashlib.sha256).hexdigest() == sig)


print()
if failures:
    print(f"\033[31m{len(failures)} check(s) failed:\033[0m "
          + ", ".join(failures))
    sys.exit(1)
print("\033[32mAll satellite-analytics checks passed.\033[0m")
