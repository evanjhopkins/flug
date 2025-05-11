import click
from flug.utils.db_actions import nuke_db

@click.command()
def nuke():
    nuke_db()