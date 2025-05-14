import click
import yaml
from flug.utils.db_actions import Tasks, assert_db_initialized
import os
import hashlib
from pony.orm import db_session
from pathlib import Path


@click.command()
@click.argument("file_path", type=click.Path(exists=True, dir_okay=False))
@click.option("-e", "--enable", is_flag=True, help="Optional flag for enabling while adding a new task.")
def add(file_path, enable):
    assert_db_initialized()
    _internal(file_path, enable)

@db_session
def _internal(file_path, enable):
    abs_path = Path(os.path.abspath(file_path))
    working_dir = str(abs_path.parent)
    with open(abs_path, "r") as f:
        data = yaml.safe_load(f)

    namespace = data.get("namespace")

    does_namespace_exist = Tasks.get(namespace=namespace) is not None
    if does_namespace_exist:
        print("[FLUG] Cannot register a namespace that already exists")
        return

    yaml_string = yaml.dump(data)
    yaml_hash = hashlib.md5(yaml_string.encode("utf-8")).hexdigest()

    Tasks(
        namespace=namespace,
        active=enable,
        definition=yaml_string,
        md5=yaml_hash,
        working_dir=working_dir,
    )
