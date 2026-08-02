# dash-mui-charts docs — production image (Render docker runtime).
#
# NO node toolchain: the dash_mui_charts component bundle + generated Python
# wrappers are COMMITTED to git (dash_mui_charts/*.min.js + *.py), so
# `pip install .` works without npm. TRADE-OFF: changes under src/lib require
# a local `npm run build` and committing the regenerated artifacts.
FROM python:3.11-slim

# Block-buffered stdout never reaches platform logs through gunicorn —
# boot diagnostics (traffic reporter state, bulletin state, dependency
# floors) must flush.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# dash-clerk-auth is not on PyPI; requirements.txt installs it from ./vendor.
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
