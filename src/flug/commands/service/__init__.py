import click
from flug.utils.db_actions import Tasks, HeartBeat
from pony.orm import db_session, select, commit
import yaml
from datetime import datetime, timedelta
from dataclasses import dataclass
import subprocess
import time

from flug.utils.logging import log_internal


@dataclass
class ScheduledExecution:
    namespace: str
    execute_at: datetime
    cmd: str
    working_dir: str


def time_str_to_dt(time_str: str, date_o):
    time_o = datetime.strptime(time_str, "%H:%M:%S").time()
    return datetime.combine(date_o, time_o)


# @db_session
def update_heartbeat(name: str):
    now = datetime.now()
    hb = HeartBeat.get(name=name)
    if hb:
        hb.last = now
    else:
        HeartBeat(name=name, last=now)
    commit()

def build_ex_command(raw_cmd: list[str]):
    cmd = (
        " && ".join(raw_cmd) if isinstance(raw_cmd, tuple) else raw_cmd
    )
    return cmd


@db_session
def get_scheduled_executions(now=datetime.now()):
    run_date = now.date()
    tasks = select(t for t in Tasks)[:]
    executions = []

    for task in tasks:
        config = yaml.safe_load(task.definition)
        schedule = config["schedule"]

        time_of_day = schedule.get("time_of_day", None)
        if time_of_day is not None:
            for time_str in time_of_day:
                execute_at = time_str_to_dt(time_str, run_date)
                if execute_at > now:
                    raw_cmd = config.get("command", None)
                    cmd = build_ex_command(raw_cmd)                    
                    ex = ScheduledExecution(
                        namespace=task.namespace,
                        execute_at=execute_at,
                        cmd=cmd,
                        working_dir=task.working_dir,
                    )
                    executions.append(ex)

        window_interval = schedule.get("window_interval", None)
        if window_interval is not None:
            first_str = window_interval.get("start", None)
            last_str = window_interval.get("stop", None)
            interval_sec = window_interval.get("interval_sec", None)
            if any(x is None for x in (first_str, last_str, interval_sec)):
                print(
                    f"[FLUG] Unable to use window_interval schedule for {task.namespace}, skipping."
                )
                continue

            first_dt = time_str_to_dt(first_str, run_date)
            last_dt = time_str_to_dt(last_str, run_date)
            step = timedelta(seconds=interval_sec)
            curr = first_dt
            while curr <= last_dt:
                ex_dt = curr
                if ex_dt > now:
                    raw_cmd = config.get("command", None)
                    cmd = build_ex_command(raw_cmd)
                    ex = ScheduledExecution(
                        namespace=task.namespace,
                        execute_at=ex_dt,
                        cmd=cmd,
                        working_dir=task.working_dir,
                    )
                    executions.append(ex)
                curr += step

    # sort to be in time order
    sorted_executions = sorted(executions, key=lambda x: x.execute_at)

    return sorted_executions


@click.command()
@db_session
def service():
    log_internal("Service started", print_in_console=True)
    scheduled_executions = get_scheduled_executions()

    curr_date = datetime.now().date()
    while True:
        update_heartbeat("service")
        tick_start_time = datetime.now()
        to_execute = [
            e for e in scheduled_executions if e.execute_at <= tick_start_time
        ]
        scheduled_executions = [
            e for e in scheduled_executions if e.execute_at > tick_start_time
        ]
        if len(to_execute) > 0:
            for ex in to_execute:
                try:
                    log_file = ex.working_dir + "/.flug.log"
                    with open(log_file, "a", encoding="utf-8") as log:
                        subprocess.run(
                            ex.cmd,
                            cwd=ex.working_dir,
                            shell=True,
                            stdout=log,
                            stderr=log,
                            text=True,
                            check=True,
                        )
                except:
                    log_internal(f"{ex.namespace} FAILED")

        # after all executions for this tick, check if we have moved into the next day
        # if yes, we must rebuild the schedules
        if tick_start_time.date() > curr_date:
            scheduled_executions = get_scheduled_executions(tick_start_time)
            curr_date = tick_start_time.date()
            print(
                f"Updating for next day, rebuilding schedules {tick_start_time.date()}"
            )
        time.sleep(5)
