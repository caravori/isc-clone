# Gunicorn configuration file

import multiprocessing
import sys

# Server socket
bind = '0.0.0.0:8000'
backlog = 2048

# Worker processes - reduced for initial stability
workers = 2
worker_class = 'sync'
worker_connections = 1000
timeout = 300  # 5 minutes - very generous for debugging
graceful_timeout = 60
keepalive = 5
max_requests = 1000  # Restart workers after 1000 requests
max_requests_jitter = 50

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Capture output
capture_output = True
enable_stdio_inheritance = True

# Process naming
proc_name = 'isc-clone'

# Server mechanics
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# Preload app for faster worker startup
preload_app = True

# SSL
keyfile = None
certfile = None

# Hooks for debugging
def on_starting(server):
    print("[GUNICORN] Starting server...", file=sys.stderr, flush=True)

def when_ready(server):
    print("[GUNICORN] Server is ready!", file=sys.stderr, flush=True)

def worker_int(worker):
    print(f"[GUNICORN] Worker {worker.pid} interrupted", file=sys.stderr, flush=True)

def worker_abort(worker):
    print(f"[GUNICORN] Worker {worker.pid} ABORTED (timeout)!", file=sys.stderr, flush=True)
