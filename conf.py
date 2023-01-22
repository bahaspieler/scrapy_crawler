import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
SCROLL_PAUSE_TIME = 4
LOGGING = {
    "version": 1,
    'disable_existing_loggers': False,
    "handlers": {
        "console": {
            "formatter": "std_out",
            "class": "logging.StreamHandler",
            "level": "DEBUG"
        },
        "main": {
            "formatter": "std_out",
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "filename": "news_crawler.log",
            "encoding": "utf-8"
        },
    },
    "formatters": {
        "std_out": {
            "format": "[%(asctime)s] : %(levelname)s : [%(module)s:%(lineno)s] : [%(funcName)s] : %(message)s"
        }
    },
    'loggers': {
        "main": {
            "handlers": ["console", "main"],
            "level": "DEBUG",
            "propagate": True,
        },

    }
}
