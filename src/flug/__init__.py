import click
from flug.utils.db_actions import assert_db_initialized, nuke_db
from flug.commands import add, list, remove, start, stop, update
import time

@click.group()
def cli():
    # If this is the first run of ATC, we need to initialize the internal db
    assert_db_initialized()

@click.command()
def service():
    while True:
        print("tick")
        time.sleep(5)

@click.command()
def status():
    click.echo("Status2")

@click.command()
def nuke():
    nuke_db()



cli.add_command(status)
cli.add_command(nuke)
cli.add_command(add.add)
cli.add_command(list.list)
cli.add_command(start.start)
cli.add_command(remove.remove)
cli.add_command(stop.stop)
cli.add_command(update.update)
cli.add_command(service)
