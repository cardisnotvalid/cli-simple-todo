class Color:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    CYAN = "\033[0;36m"
    YELLOW = "\033[1;33m"
    END = "\033[0m"


def log(level, msg):
    match level:
        case "INFO":
            print(f"{level:<8} | {msg}")
        case "SUCCESS":
            print(f"{Color.GREEN}{level:<8}{Color.END} | {msg}")
        case "DEBUG":
            print(f"{Color.CYAN}{level:<8}{Color.END} | {msg}")
        case "WARNING":
            print(f"{Color.YELLOW}{level:<8}{Color.END} | {msg}")
        case "ERROR":
            print(f"{Color.RED}{level:<8}{Color.END} | {msg}")

