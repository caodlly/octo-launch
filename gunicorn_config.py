# WSGI application entry point
wsgi_app = "config.wsgi:application"

# Address and port to bind
bind = "0.0.0.0:8080"

# Worker class to use
worker_class = "gevent"

# Timeout for each worker (seconds)
timeout = 120

# Reload the application automatically on code changes
reload = True

# Restart workers after this many requests
max_requests = 1000

# Add random jitter to max_requests to avoid all workers restarting at the same time
max_requests_jitter = 200

# Number of worker processes
workers = 4

# Graceful timeout for worker shutdown (seconds)
graceful_timeout = 30

# Access log file
# accesslog = "./logs/access.log"

# Error log file
# errorlog = "./logs/error.log"

# Logging level
loglevel = "info"

# File to store the process ID
pidfile = "./server-gunicorn.pid"

# Capture stdout and stderr output to the error log
# capture_output = True

# Run Gunicorn as a background daemon
# daemon = True
