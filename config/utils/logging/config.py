from config.settings.base import app, BASE_DIR
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
        f"{app.name}": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, f"logs/{app.name}.log"),
            "formatter": "colored",
        },
        # "console": {
        #     'class': 'logging.StreamHandler',
        #     'formatter': 'colored',
        # },
    },
    "loggers": {
        f"{app.name}": {
            "handlers": [
                f"{app.name}",
                # "console"
            ],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
