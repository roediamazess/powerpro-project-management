import multiprocessing
import os

# Gunicorn configuration for high-performance FastAPI deployment
# -------------------------------------------------------------

# Use the environment variable PORT if set, otherwise default to 8000
port = os.getenv("PORT", "8000")
bind = f"0.0.0.0:{port}"

# Recommended workers: (2 x cores) + 1
workers_per_core = float(os.getenv("WORKERS_PER_CORE", "2"))
cores = multiprocessing.cpu_count()
workers = int(os.getenv("WEB_CONCURRENCY", cores * workers_per_core + 1))

# Process management
timeout = int(os.getenv("TIMEOUT", "120"))
keepalive = int(os.getenv("KEEP_ALIVE", "5"))

# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.getenv("LOG_LEVEL", "info")
