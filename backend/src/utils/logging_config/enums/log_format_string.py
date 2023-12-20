from backend.src.utils.logging_config.enums.colors import ColorsEnum

grey = ColorsEnum.GREY.value
green = ColorsEnum.GREEN.value
cyan = ColorsEnum.CYAN.value
yellow = ColorsEnum.YELLOW.value
red = ColorsEnum.RED.value
bold_red = ColorsEnum.BOLD_RED.value
blue = ColorsEnum.BLUE.value
reset = ColorsEnum.RESET.value

start_log_line = f"{green}%(asctime)s{reset} {red}| {reset}"
end_log_line = (
    f" {red}| {reset}{cyan}%(pathname)s{reset}{red}:{reset}{cyan}%(funcName)s{reset}"
    f"{red}:{reset}{cyan}%(lineno)d {reset}{red}- {reset}"
)
log_string = (
    start_log_line + "{}%(levelname)s" + reset + end_log_line + "{}%(message)s" + reset
)
