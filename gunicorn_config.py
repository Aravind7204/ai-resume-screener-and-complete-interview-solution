"""
Gunicorn configuration for AI Resume Screener
Optimized for AWS EC2 t2.micro instance
"""

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = 1  # Conservative for t2.micro (1 CPU core)
worker_class = "sync"
worker_connections = 1000
timeout = 300  # 5 minutes for ML model processing
keepalive = 2

# Restart workers after this many requests, to help control memory leaks
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/opt/ai-resume-screener/logs/access.log"
errorlog = "/opt/ai-resume-screener/logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'ai-resume-screener'

# Server mechanics
daemon = False
pidfile = '/tmp/ai-resume-screener.pid'
user = None
group = None
tmp_upload_dir = None

# SSL (if needed in future)
keyfile = None
certfile = None

# Application preloading
preload_app = True  # Load application before forking workers

# Worker timeout
graceful_timeout = 30
worker_tmp_dir = "/dev/shm"  # Use RAM for temporary files

# Memory management
memory_limit = 512 * 1024 * 1024  # 512MB limit per worker
