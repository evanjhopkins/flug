from pony.orm import Database, Required, db_session
import os

DB_PATH="C:/Users/evanj/code/atc/atc.db"
db = Database()

class Tasks(db.Entity):
    namespace = Required(str, unique=True)
    is_up = Required(bool)
    definition = Required(str)
    md5 = Required(str)


def assert_db_initialized():
	is_new = not os.path.exists(DB_PATH)

	db.bind(provider='sqlite', filename=DB_PATH, create_db=True)
	db.generate_mapping(create_tables=is_new)

	if is_new:
		print("[ATC] Initialized db")
	else:
		print("[ATC] db already exists")

	print("[ATC] Ready!")


def nuke_db():
	if os.path.exists(DB_PATH):
		os.remove(DB_PATH)
		print(f"[ATC] Nuked DB")
	else:
		print(f"[ATC] No DB to Nuke")