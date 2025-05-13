import click
from pony.orm import db_session
from flug.utils.constants import LOG_FILE_POSTFIX
from flug.utils.resolve_task import resolve_task

TAIL = 20

@click.command()
@click.argument("target", type=str)
@db_session
def log(target):
    task = resolve_task(target)
    if task is None:
        return

    log_file_path = task.working_dir + "/" + LOG_FILE_POSTFIX
    try:
        with open(log_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines[-TAIL:]:
            print(line, end="")
    except FileNotFoundError:
        print("(none)")
