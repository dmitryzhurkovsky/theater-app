import logging

from backend.src.utils.logging_config.enums.colors import ColorsEnum
from backend.src.utils.logging_config.enums.log_format_string import log_string


class CustomFormatter(logging.Formatter):
    grey = ColorsEnum.GREY.value
    green = ColorsEnum.GREEN.value
    cyan = ColorsEnum.CYAN.value
    yellow = ColorsEnum.YELLOW.value
    red = ColorsEnum.RED.value
    bold_red = ColorsEnum.BOLD_RED.value
    blue = ColorsEnum.BLUE.value
    reset = ColorsEnum.RESET.value

    format = log_string

    FORMATS = {
        logging.DEBUG: format.format(blue, blue),
        logging.INFO: format.format(grey, grey),
        logging.WARNING: format.format(yellow, yellow),
        logging.ERROR: format.format(red, red),
        logging.CRITICAL: format.format(bold_red, bold_red),
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
