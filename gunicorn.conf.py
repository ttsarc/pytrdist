"""gunicorn WSGI server configuration."""
from multiprocessing import cpu_count
from os import environ

def max_workers():
    return cpu_count()
daemon=True
bind = 'localhost:' + environ.get('PORT', '8000')
max_requests = 1000
worker_class = 'gevent'
workers = max_workers()
pidfile='/var/run/gunicorn/trwk.pid'
