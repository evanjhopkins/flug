from pony.orm import Database, Required, db_session
import os
from datetime import datetime
from flug.utils.general import get_storage_dir

db = Database()


class Tasks(db.Entity):
    namespace = Required(str, unique=True)
    active = Required(bool)
    definition = Required(str)
    md5 = Required(str)
    working_dir = Required(str)


class HeartBeat(db.Entity):
    name = Required(str, unique=True)
    last = Required(datetime)


class Run(db.Entity):
    namespace = Required(str)
    execution_time = Required(datetime)
    status = Required(bool)

def get_db_path():
    storage_path = get_storage_dir()
    storage_path.mkdir(parents=True, exist_ok=True)
    db_dir = storage_path / "flug.db"
    return db_dir


def assert_db_initialized():
    DB_PATH = get_db_path()
    is_new = not os.path.exists(DB_PATH)
    db.bind(provider="sqlite", filename=str(DB_PATH), create_db=True)
    db.generate_mapping(create_tables=is_new)


@db_session
def does_namespace_exist(namespace: str):
    assert_db_initialized()
    return Tasks.get(namespace=namespace) is not None


def nuke_db():
    DB_PATH = get_db_path()
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"[ATC] Nuked DB")
    else:
        print(f"[ATC] No DB to Nuke")
