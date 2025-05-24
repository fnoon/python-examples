#!/usr/bin/env python3

from pathlib import Path
import datetime
import psutil
from subprocess import check_call, CalledProcessError
import shutil

# Kill a process whose PID is contained in a file.
def kill_process(pidfile_path=Path("example.pid")):
    try:
        pid = int(pidfile_path.read_text())
    except FileNotFoundError:
        print(f"No {pidfile_path}")
        return
    except ValueError:
        print(f"Invalid {pidfile_path}")
        return

    try:
        proc = psutil.Process(pid)
        print("Killing", proc.name())
        proc.kill()
    except psutil.NoSuchProcess as ex:
        print(f"{pid} - no such process")


def date(format="%Y%m%d"):
    return datetime.datetime.utcnow().strftime(format)

def make_output_dir() -> Path:
    today = date()
    output_dir = Path(".") / f"results_{today}"
    output_dir.mkdir(exist_ok=True)
    return output_dir

APP_NAME = ["python3", "module_design_analytics.py"]

def run_analytics(
    output_dir: Path,
    root_path: Path=Path('/path/to/data')) -> Path:
    path = next(iter(sorted(root_path.glob("*.yaml"), reverse=True)))
    print(path.name)
    output_path = output_dir / f"summary_{path.name}.txt"

    try:
        with output_path.open('w') as output_file:
            check_call(APP_NAME+[str(path)], stdout=output_file)
    except CalledProcessError as ex:
        print(f"Error {ex.returncode} in app")

    return output_path

def copy_to_current(result_path: Path):
    target = Path("current.txt")
    if result_path.stat().st_mtime > target.stat().st_mtime:
        shutil.copy2(str(result_path), str(target))
    else:
        print(f"{result_path} not newer")

if __name__ == "__main__":
    kill_process()
    output_dir = make_output_dir()
    result_path = run_analytics(output_dir)
    copy_to_current(result_path)
