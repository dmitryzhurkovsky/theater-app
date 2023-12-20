LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {"()": "src.utils.logging_config.formatter.CustomFormatter"},
    },
    "handlers": {
        "default": {
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": False,
        },  # root logger
        "__main__": {
            "handlers": ["default"],
            "level": "DEBUG",
            "propagate": False,
        },  # if __name__ == '__main__'
    },
}
