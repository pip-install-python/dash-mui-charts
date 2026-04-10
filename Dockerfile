FROM python:3.11-slim

WORKDIR /app

# Install deploy dependencies first (cached layer)
COPY requirements-deploy.txt .
RUN pip install --no-cache-dir -r requirements-deploy.txt

# Copy project and install dash-mui-charts from local source
COPY . .
RUN pip install --no-cache-dir .

EXPOSE 8550

CMD ["gunicorn", "app:server", "-b", "0.0.0.0:8550", "--workers", "2", "--timeout", "120"]
