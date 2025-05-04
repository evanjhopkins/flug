import click
import yaml
from flug.utils.db_actions import assert_db_initialized, Tasks
import os
import hashlib
from pony.orm import db_session

@click.command()
@click.argument('file_path', type=click.Path(exists=True, dir_okay=False))
@db_session
def add(file_path):
    print(os.getcwd())
    abs_path = os.path.abspath(file_path)
    print(abs_path)
    with open(abs_path, 'r') as f:
        data = yaml.safe_load(f)

    namespace = data.get('namespace')
    # print(namespace, does_namespace_exist(namespace))

    does_namespace_exist = Tasks.get(namespace=namespace) is not None
    if does_namespace_exist:
        print("[ATC] Cannot register a namespace that already exists")
        return

    yaml_string = yaml.dump(data)
    yaml_hash = hashlib.md5(yaml_string.encode('utf-8')).hexdigest()

    Tasks(namespace=namespace, active=0, definition=yaml_string, md5=yaml_hash)