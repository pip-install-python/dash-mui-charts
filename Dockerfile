# dash-mui-charts docs — the CI image. NOT what serves production.
#
# `render.yaml` line 4 declares `runtime: python`: Render's NATIVE runtime
# builds this service from requirements.txt and never reads this file. The
# only consumer is ci.yml's `docker image · boot · battery` job. The header
# here said "Render docker runtime" until 2026-08-26, which is how a
# 3.14 image and a 3.11.12 platform coexisted for two days without anyone
# reading the two lines as contradictory (SYNC-1.6.22-1.6.29 item 5).
#
# The FROM tag is still the fleet Python's single source — tests/
# test_python_version.py reads it and holds render.yaml, ci.yml and cd.yml
# to its minor, and scripts/network_smoke.py holds the live host to it.
#
# NO node toolchain: the dash_mui_charts component bundle + generated Python
# wrappers are COMMITTED to git (dash_mui_charts/*.min.js + *.py), so
# `pip install .` works without npm. TRADE-OFF: changes under src/lib require
# a local `npm run build` and committing the regenerated artifacts.
FROM python:3.14-slim

# Block-buffered stdout never reaches platform logs through gunicorn —
# boot diagnostics (traffic reporter state, bulletin state, dependency
# floors) must flush.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# dash-clerk-auth is not on PyPI; requirements.txt installs it from ./vendor.
#
# CACHE SEMANTICS (the round-2 fleet lesson, found by pannellum
# 2026-08-22): this layer re-runs ONLY when vendor/ or requirements.txt
# bytes change. A `>=` floor can NEVER pull a newer release through a
# cache hit — a code-only commit rebuilds the app layers below while pip
# silently keeps whatever version the image was first built with. Ship
# every dependency upgrade as a floor bump in requirements.txt (grep the
# number — it also lives in run.py's boot floor and the tests): the bump
# IS the cache bust, and the boot floor turns a stale image from a
# silent downgrade into a loud refusal to start.
#
# The fleet's outside check for this is /healthz: no `geo` block means a
# pre-2.7 package is serving, which means the floor bump never reached
# the image no matter what the commit says.
COPY vendor ./vendor
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# markdown2dash pins gunicorn<22, conflicting with the CVE-driven gunicorn>=23
# in requirements.txt (CVE-2024-6827, CVE-2024-1135 — request smuggling). Its
# real dependencies are all in requirements.txt already, so it is installed
# alone, without letting pip see the spurious pin. CI asserts the resulting
# gunicorn version INSIDE this image (LESSONS §8).
RUN pip install --no-cache-dir --no-deps markdown2dash==0.1.2

# Copy project and install dash-mui-charts from local source
COPY . .
RUN pip install --no-cache-dir .

EXPOSE 8550

CMD ["gunicorn", "run:server", "-b", "0.0.0.0:8550", "--workers", "2", "--timeout", "120"]
