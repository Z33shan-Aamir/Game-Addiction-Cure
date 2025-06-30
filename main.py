import psutil
import datetime,time
import win32gui
import threading

import json

PRODUCTIVE_APPS = ["Code.exe", "notepad.exe"]
UNPRODUCTIVE_APPS = ["tiktok.exe", "discord.exe"]

ALL_APPS = PRODUCTIVE_APPS + UNPRODUCTIVE_APPS


"""Testing is Done"""
def track_session_data(process_name, pid):
    active_tasks = []
    if process_name not in active_tasks and check_if_process_is_active(process_name, pid): # if process is active and is in the above list then will mark the start time
        session_start = datetime.datetime.now()
        print(session_start)
        
        active_tasks.append(process_name)
    elif process_name in active_tasks and check_if_process_is_active(process_name, pid): # if process is no longer active, remove it from active tasks and mark the session end time 
        session_end = datetime.datetime.now()
        print(session_end)
        
    pass

"""Testing is done!!"""

def get_largest_memory_process(process_name) -> psutil.Process: # get the pid based on memory allocation  
    best_proc : psutil.Process | None = None
    max_mem = 0

    for proc in psutil.process_iter(attrs=["name", "pid", "memory_info"]):
        try:
            if proc.info["name"].lower() == process_name.lower():
                mem_usage = proc.info["memory_info"].rss  # Resident Set Size in bytes
                if mem_usage > max_mem:
                    max_mem = mem_usage
                    best_proc = proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return (best_proc : psutil.Process | none)

def check_if_process_is_active(process_name, pid : int):
    for proc in psutil.process_iter(attrs=["name", "pid"]):
        if proc.info["name"].lower() == process_name.lower() and proc.info["pid"] == pid:
            return True  # returns true if the process is running 
    # returns False if the process is not running

"""May not need this function any more"""
def get_pid(processes):
    for proc in psutil.process_iter(attrs=["name", "pid"]):
        for process in processes:
            if process.lower() == proc.info["name"].lower():
                data = {
                    proc.info["name"]:
                        {
                            "sessions":
                                [
                                    {
                                        "pid" : proc.info["pid"],
                                        "session_start" : datetime.datetime.now(),
                                        # "session_end" : da
                                    }
                                ]
                        }
                }
                print(json.dumps(data, indent=4))
                with open("./app_usage.json", "w") as f:
                    json.dump(data,f, indent=4)
def main():
    # get_pid(ALL_APPS)
    proc: psutil.Process | None = get_largest_memory_process("Code.exe")
    print(type(proc))
    print(proc)
    track_session_data("Code.exe", proc.info["pid"])
    print(check_if_process_is_active("Code.exe", proc.info["pid"]))
            


main()
