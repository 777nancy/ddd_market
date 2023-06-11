import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "%(asctime)s : %(threadName)s : %(module)s : %(funcName)s : %(levelname)s : %(message)s"}
    },
    "handlers": {
        "StreamHandler": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        }
    },
    "loggers": {
        "__main__": {"level": "INFO", "handlers": ["StreamHandler"]},
        "marketanalysis": {"level": "INFO", "handlers": ["StreamHandler"]},
        "numpy": {"level": "NOTSET", "handlers": ["StreamHandler"]},
        "pandas": {"level": "NOTSET", "handlers": ["StreamHandler"]},
    },
}


def initialize_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
