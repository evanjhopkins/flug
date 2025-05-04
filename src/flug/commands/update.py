import click
import yaml
import os
from pony.orm import db_session
from flug.utils.db_actions import Tasks
import hashlib

@click.command()
@click.argument('file_path', type=click.Path(exists=True, dir_okay=False))
@db_session
def update(file_path):
    abs_path = os.path.abspath(file_path)
    with open(abs_path, 'r') as f:
        data = yaml.safe_load(f)

    namespace = data.get('namespace')
    
    registered_task = Tasks.get(namespace=namespace)

    if registered_task is None:
        print("[ATC] Cannot update a task that has not yet been registered")
        return

    yaml_string = yaml.dump(data)
    yaml_hash = hashlib.md5(yaml_string.encode('utf-8')).hexdigest()
    has_changes = yaml_hash != registered_task.md5

    if not has_changes:
        print(f"[ATC] Cannot update because there are no changes")
        return

    registered_task.definition = yaml_string
    registered_task.md5 = yaml_hash
    print(f"[ATC] Task has been updated!")
