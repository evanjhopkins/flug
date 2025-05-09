import click
from flug.utils.db_actions import Tasks
from pony.orm import db_session, select

# from tabulate import tabulate
from rich.console import Console
from rich.table import Table as RichTable
from rich.style import Style


@click.command()
@db_session
def list():
    tasks = select(t for t in Tasks)[:]

    if len(tasks) == 0:
        print("[FLUG] No tasks have been registered")
        return

    console = Console()
    table = RichTable(show_header=True, header_style="bold", box=None)
    table.add_column("ID")
    table.add_column("Namespace")
    table.add_column("Active")
    table.add_column("Dir")

    for t in tasks:
        style = Style(color="green") if t.active else Style(color="grey50")
        table.add_row(
            str(t.id), t.namespace, str(t.active), t.working_dir or "", style=style
        )

    console.print(table)
