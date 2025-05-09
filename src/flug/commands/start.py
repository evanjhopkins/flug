import click
import yaml
import os
from pony.orm import db_session
from flug.utils.db_actions import Tasks


@click.command()
@click.argument("file_path", type=click.Path(exists=True, dir_okay=False))
@db_session
def start(file_path):
    abs_path = os.path.abspath(file_path)
    with open(abs_path, "r") as f:
        data = yaml.safe_load(f)

    namespace = data.get("namespace")
    if not namespace:
        print("[FLUG] No namespace found in the file.")
        return

    registered_task = Tasks.get(namespace=namespace)
    if registered_task is None:
        print(f"[FLUG] Task with namespace '{namespace}' is not registered.")
        return

    if registered_task.active:
        print(f"[FLUG] Task '{namespace}' is already up.")
        return

    registered_task.active = True
    print(f"[FLUG] Task '{namespace}' has been marked as up.")
