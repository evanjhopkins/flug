import click
from flug.commands import add, disable, enable, list, remove, update, service, status, nuke, log


@click.group()
def cli():
    pass


cli.add_command(status.status)
cli.add_command(nuke.nuke)
cli.add_command(add.add)
cli.add_command(list.list)
cli.add_command(enable.enable)
cli.add_command(remove.remove)
cli.add_command(disable.disable)
cli.add_command(update.update)
cli.add_command(service.service)
cli.add_command(log.log)
