import click
import yaml
from lib.db_actions import assert_db_initialized, nuke_db
import os

@click.group()
def cli():
    pass

@click.command()
def status():
    assert_db_initialized()
    click.echo("Status")

@click.command()
def nuke():
    nuke_db()

@click.command()
@click.argument('file_path', type=click.Path(exists=True, dir_okay=False))
def register(file_path):
    print(os.getcwd())
    abs_path = os.path.abspath(file_path)
    print(abs_path)

cli.add_command(status)
cli.add_command(nuke)
cli.add_command(register)

if __name__ == "__main__":
    cli()
