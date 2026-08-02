FROM python:3.11-slim

# Block-buffered stdout never reaches platform logs through gunicorn —
# boot diagnostics (traffic reporter state, license warnings) must flush.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# ONE requirements file, shared with Render (render.yaml buildCommand).
# A separate deploy file drifted once — it lost `requests` and the image
# could not import app.py while Render, reading requirements.txt, masked it.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project and install dash-mui-charts from local source
COPY . .
RUN pip install --no-cache-dir .

EXPOSE 8550

CMD ["gunicorn", "app:server", "-b", "0.0.0.0:8550", "--workers", "2", "--timeout", "120"]
