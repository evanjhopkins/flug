import click
from pony.orm import db_session
from flug.utils.db_actions import assert_db_initialized
from flug.utils.messaging import FAILED_TO_RESOLVE_TASK
from flug.utils.resolve_task import resolve_task


@click.command()
@click.argument("target", type=str)
def enable(target):
    assert_db_initialized()
    _internal(target)

@db_session
def _internal(target):
    task = resolve_task(target)
    if task is None:
        print(FAILED_TO_RESOLVE_TASK)
        return

    if task.active:
        print(f"[FLUG] Task '{task.namespace}' is already up.")
        return

    task.active = True
    print(f"[FLUG] Task '{task.namespace}' has been marked as up.")