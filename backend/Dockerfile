# Stage 1: Build & Operational Environment
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /app
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Production execution using Gunicorn + Uvicorn workers
# Binding to 0.0.0.0 is essential for Docker networking
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "app/core/gunicorn_conf.py", "app.main:app"]
