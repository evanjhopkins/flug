import click
from flug.commands import add, list, remove, start, stop, update, service, status, nuke


@click.group()
def cli():
    pass


cli.add_command(status.status)
cli.add_command(nuke.nuke)
cli.add_command(add.add)
cli.add_command(list.list)
cli.add_command(start.start)
cli.add_command(remove.remove)
cli.add_command(stop.stop)
cli.add_command(update.update)
cli.add_command(service.service)
