from typing import Optional
import yaml
import os
from pony.orm import db_session
from flug.utils.db_actions import Tasks, assert_db_initialized
from pathlib import Path
from flug.utils.messaging import FAILED_TO_RESOLVE_TASK

@db_session
def resolve_task(target: str) -> Optional[Tasks]:
    assert_db_initialized()
    file_path = Path(target)
    abs_path = Path(os.path.abspath(file_path))
    namespace=target
    if abs_path.is_file():
        with open(abs_path, "r") as f:
            data = yaml.safe_load(f)
            namespace = data.get("namespace")
    
    task = Tasks.get(namespace=namespace)

    if task is None:
        print(FAILED_TO_RESOLVE_TASK)
        return None

    return task