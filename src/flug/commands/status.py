import click
from flug.utils.db_actions import HeartBeat
from pony.orm import db_session
from datetime import datetime
from flug.utils.general import get_storage_dir
from flug.utils.logging import print_internal_log
from rich import print


@click.command()
@db_session
def status():
    is_running = "NO"
    last_hb = "(none)"
    storage_dir = get_storage_dir()

    hb = HeartBeat.get(name="service")
    if hb is not None:
        elapsed_sec = (datetime.now() - hb.last).total_seconds()
        color = "green" if elapsed_sec < 5 else "red"
        is_running = "YES" if elapsed_sec < 5 else "NO"
        colored_is_running = f"[{color}]{is_running}[/{color}]"
        last_hb = hb.last.strftime("%Y-%m-%d %H:%M:%S")
    print("Is Service Running:", colored_is_running)
    print("Last Heartbeat:", last_hb)
    print("Internal Storage:", storage_dir)
    print("Recent Logs:")
    print_internal_log(n=5, prefix="-> ")
