from config.settings.base import APP, BASE_DIR
import os


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s[%(asctime)s] [%(process)d] [%(module)s] [%(levelname)s] %(message)s %(reset)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
            "style": "%",
        },
    },
    "handlers": {
        f"{APP.name}": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, f"logs/{APP.name}.log"),
            "formatter": "colored",
        },
    },
    "loggers": {
        f"{APP.name}": {
            "handlers": [f"{APP.name}"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
