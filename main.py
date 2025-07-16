import psutil
import datetime, time

# local imports
from write import write_session_data_to_file, session_end_stamp


PRODUCTIVE_APPS = ["firefox"]
UNPRODUCTIVE_APPS = ["heroic"]

ALL_APPS = PRODUCTIVE_APPS + UNPRODUCTIVE_APPS


"""Testing is Done"""
active_tasks = {}
def track_session_data(process_name, pid):
    if pid not in active_tasks and check_if_process_is_active(process_name, pid):
        # Process started
        session_start = datetime.datetime.now()
        print(f"Session started: {session_start} | Process: {process_name} | PID: {pid}")
        if process_name in PRODUCTIVE_APPS:
            write_session_data_to_file(process_name, session_start=session_start, is_productive=True)
        elif process_name in UNPRODUCTIVE_APPS:
            write_session_data_to_file(process_name, session_start=session_start, is_productive=False)
        else:
            write_session_data_to_file(process_name, is_productive=None, session_start=session_start)
        active_tasks[pid] = (process_name, session_start)
        session_start = active_tasks[pid][1]


def check_if_process_is_active(process_name, pid : int) -> bool:
    for proc in psutil.process_iter(attrs=["name", "pid"]):
        if proc.info["name"].lower() == process_name.lower() and proc.info["pid"] == pid:
            return True  # returns true if the process is running 
    return False# returns False if the process is not running

def main(process_name):
    # Check all running instances of the tracked app
    for proc in psutil.process_iter(attrs=["name", "pid"]):
        if proc.info["name"] and proc.info["name"].lower() == "firefox":
            track_session_data(proc.info["name"], proc.info["pid"])

