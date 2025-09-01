#The suggested maximum concurrent requests when using workers and threads is (2*CPU)+1.

# gunicorn config file
bind = "0.0.0.0:5000"
workers = 4
threads = 1
timeout = 120

worker_class = 'sync'

daemon = False
pidfile = None
umask = 0

loglevel = 'ERROR'
error_log = '-'     # means stdout
access_log = '-'    # means stdout
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'