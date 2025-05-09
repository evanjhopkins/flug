from flug.utils.general import get_storage_dir
from datetime import datetime


def get_log_file_path():
    storage_path = get_storage_dir()
    log_file = str(storage_path) + "/flug.log"
    return log_file


def log_internal(message: str, print_in_console=False):
    log_file = get_log_file_path()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{now} {message}\n")
        if print_in_console:
            print(message)


def print_internal_log(n=5, prefix=""):
    log_file = get_log_file_path()
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines[-n:]:
            print(prefix + line, end="")
    except FileNotFoundError:
        print("(none)")
