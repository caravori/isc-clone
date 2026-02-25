# Gunicorn configuration file

import multiprocessing
import sys

# Server socket
bind = '0.0.0.0:8000'
backlog = 2048

# Worker processes
workers = 3
worker_class = 'sync'
worker_connections = 1000
timeout = 120  # Increased timeout for initial startup
graceful_timeout = 30
keepalive = 2

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'debug'  # Changed to debug
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

# SSL
keyfile = None
certfile = None

# Hooks for debugging
def on_starting(server):
    print(f"[GUNICORN] Starting server on {bind}", file=sys.stderr)

def on_reload(server):
    print("[GUNICORN] Reloading...", file=sys.stderr)

def when_ready(server):
    print("[GUNICORN] Server is ready. Spawning workers", file=sys.stderr)

def pre_fork(server, worker):
    print(f"[GUNICORN] Worker {worker.pid} is being forked", file=sys.stderr)

def post_fork(server, worker):
    print(f"[GUNICORN] Worker {worker.pid} has been forked", file=sys.stderr)

def pre_request(worker, req):
    print(f"[GUNICORN] Worker {worker.pid} handling: {req.method} {req.path}", file=sys.stderr)

def post_request(worker, req, environ, resp):
    print(f"[GUNICORN] Worker {worker.pid} responded: {resp.status}", file=sys.stderr)

def worker_abort(worker):
    print(f"[GUNICORN] Worker {worker.pid} ABORTED!", file=sys.stderr)
