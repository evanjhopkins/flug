import click
from flug.utils.db_actions import assert_db_initialized
from pony.orm import db_session
from flug.utils.messaging import FAILED_TO_RESOLVE_TASK
from flug.utils.resolve_task import resolve_task


@click.command()
@click.argument("target", type=str)
def remove(target):
    assert_db_initialized()
    _internal(target)

@db_session
def _internal(target):
    assert_db_initialized()
    task = resolve_task(target)
    if task is None:
        print(FAILED_TO_RESOLVE_TASK)
        return

    target.delete()
    print("[FLUG] removed task:", target.namespace)
