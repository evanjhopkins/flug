import click
import yaml
from flug.utils.db_actions import Tasks, assert_db_initialized
import os
from pony.orm import db_session


@click.command()
@click.argument("file_path", type=click.Path(exists=True, dir_okay=False))
@db_session
def remove(file_path):
    assert_db_initialized()
    abs_path = os.path.abspath(file_path)
    with open(abs_path, "r") as f:
        data = yaml.safe_load(f)

    namespace = data.get("namespace")
    registered_task = Tasks.get(namespace=namespace)
    if registered_task is None:
        print("[FLUG] Cannot remove a task that has not been registered.")
        return

    registered_task.delete()
    print("[FLUG] removed task:", namespace)
