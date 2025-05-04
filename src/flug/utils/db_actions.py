from pony.orm import Database, Required, db_session
import os
from pathlib import Path

db = Database()

class Tasks(db.Entity):
    namespace = Required(str, unique=True)
    active = Required(bool)
    definition = Required(str)
    md5 = Required(str)


def get_storage_dir():
	return Path(Path.home() / ".local/share" / "atc")

def get_db_path():
	storage_path = get_storage_dir()
	storage_path.mkdir(parents=True, exist_ok=True)
	return storage_path / "atc.db"

def assert_db_initialized():
	DB_PATH = get_db_path()

	# print(f"[ATC] Persist path {DB_PATH}")
	is_new = not os.path.exists(DB_PATH)
	# print("is new?", is_new)

	db.bind(provider='sqlite', filename=str(DB_PATH), create_db=True)
	db.generate_mapping(create_tables=is_new)

	# if is_new:
	# 	print("[ATC] Initialization comlete")
	# else:
	# 	print("[ATC] db already exists")

	# print("[ATC✈️] Ready!")


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
