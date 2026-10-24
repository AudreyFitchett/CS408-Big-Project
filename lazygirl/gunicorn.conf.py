# Gunicorn configuration file

# Bind to a local TCP port (or use a Unix socket like 'unix:/opt/todo-app/todo.sock')
bind = "127.0.0.1:8000"

# Number of worker processes (usually 2-4 x number of CPU cores)
workers = 2

# Worker class (sync is default, gevent/uvicorn can be used for async)
worker_class = "sync"

# Maximum number of simultaneous clients per worker
worker_connections = 1000

# Timeout in seconds; requests taking longer than this are killed and restarted
timeout = 30

# Keep-alive connections
keepalive = 2

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = "info"

# Process naming
proc_name = "lazygirl"