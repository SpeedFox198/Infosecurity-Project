from hypercorn.config import Config


HOST = "127.0.0.1"
PORT = 5000
ASYNC_MODE = "asgi"
CORS_ALLOWED_ORIGINS = "http://localhost"


config = Config()
config.access_log_format = "%(h)s %(r)s %(s)s %(b)s %(D)s"
config.accesslog = "-"
config.bind = [f"{HOST}:{PORT}"]
config.errorlog = config.accesslog
