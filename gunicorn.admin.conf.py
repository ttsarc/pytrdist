"""gunicorn WSGI server configuration."""
#from multiprocessing import cpu_count
from os import environ

#def max_workers():
#    return cpu_count()

bind = 'localhost:' + environ.get('PORT', '8001')
max_requests = 1000
worker_class = 'gevent'
workers = 2
