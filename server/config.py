from hypercorn.config import Config
from constants import HOST, PORT

config = Config()
config.access_log_format = "%(h)s %(r)s %(s)s %(b)s %(D)s"
config.accesslog = "-"
config.bind = [f"{HOST}:{PORT}"]
config.errorlog = config.accesslog
