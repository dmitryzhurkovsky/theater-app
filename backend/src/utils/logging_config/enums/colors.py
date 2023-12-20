from enum import Enum


class ColorsEnum(Enum):
    GREY = "\x1b[39;1m"
    GREEN = "\x1b[32;1m"
    CYAN = "\x1b[36;1m"
    YELLOW = "\x1b[33;1m"
    RED = "\x1b[31;1m"
    BOLD_RED = "\x1b[41;1m"
    BLUE = "\x1b[1;34m"
    RESET = "\x1b[0m"
