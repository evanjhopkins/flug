import click
from flug.utils.db_actions import Tasks
import time
from pony.orm import db_session, select
import yaml
from datetime import datetime, timedelta
from dataclasses import dataclass
import subprocess


@dataclass
class ScheduledExecution:
    namespace: str
    execute_at: datetime
    cmd: str
    working_dir: str


def time_str_to_dt(time_str: str, date_o):
    time_o = datetime.strptime(time_str, "%H:%M:%S").time()
    return datetime.combine(date_o, time_o)


@db_session
def get_scheduled_executions(now=datetime.now()):
    run_date = now.date()
    tasks = select(t for t in Tasks)[:]
    executions = []

    for task in tasks:
        config = yaml.safe_load(task.definition)
        schedule = config["schedule"]
        print(task.namespace)
        print(schedule)

        time_of_day = schedule.get("time_of_day", None)
        if time_of_day is not None:
            for time_str in time_of_day:
                execute_at = time_str_to_dt(time_str, run_date)
                if execute_at > now:
                    ex = ScheduledExecution(
                        namespace=task.namespace,
                        execute_at=execute_at,
                        cmd="",
                        working_dir="",
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
                    cmd = (
                        " && ".join(raw_cmd) if isinstance(raw_cmd, tuple) else raw_cmd
                    )
                    ex = ScheduledExecution(
                        namespace=task.namespace,
                        execute_at=ex_dt,
                        cmd=cmd,
                        working_dir=task.working_dir,
                    )
                    executions.append(ex)
                curr += step

            # print(first_dt, last_dt)

    # sort to be in time order
    sorted_executions = sorted(executions, key=lambda x: x.execute_at)

    return sorted_executions


@click.command()
@db_session
def service():
    print("[FLUG] Service started")
    scheduled_executions = get_scheduled_executions()
    # print(scheduled_executions)

    while True:
        now = datetime.now()

        # print("tick:", now)
        to_execute = [e for e in scheduled_executions if e.execute_at <= now]
        scheduled_executions = [e for e in scheduled_executions if e.execute_at > now]
        if len(to_execute) > 0:
            for ex in to_execute:
                print("TO EXECUTE", ex.namespace)
                print("CMD:", ex.cmd)
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

        # print(to_execute)
        # print("REMAINING")
        # print(scheduled_executions)

        time.sleep(5)
