import psutil
import datetime,time
import win32gui
import threading

import json

PRODUCTIVE_APPS = ["Code.exe", "notepad.exe"]
UNPRODUCTIVE_APPS = ["tiktok.exe", "discord.exe"]

ALL_APPS = PRODUCTIVE_APPS + UNPRODUCTIVE_APPS


"""Testing is Done"""
active_tasks = []
def track_session_data(process_name, pid):
    if process_name not in active_tasks and check_if_process_is_active(process_name, pid): # if process is active and is in the above list then will mark the start time
        session_start = datetime.datetime.now()
        print(f"session_start: {session_start}\nProcess name: {process_name}")
        
        active_tasks.append(process_name)
    elif process_name in active_tasks and check_if_process_is_active(process_name, pid) == False: # if process is no longer active, remove it from active tasks and mark the session end time 
        active_tasks.remove(process_name)
        session_end = datetime.datetime.now()
        print(f"session_end: {session_end}\nProcess name: {process_name}")
        
    pass

"""Testing is done!!"""

def get_largest_memory_process(process_name) -> psutil.Process | None: # get the pid based on memory allocation  
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

    return best_proc

def check_if_process_is_active(process_name, pid : int) -> bool:
    for proc in psutil.process_iter(attrs=["name", "pid"]):
        if proc.info["name"].lower() == process_name.lower() and proc.info["pid"] == pid:
            return True  # returns true if the process is running 
    return False# returns False if the process is not running

"""May not need this function any more"""
# def get_pid(processes):
#     for proc in psutil.process_iter(attrs=["name", "pid"]):
#         for process in processes:
#             if process.lower() == proc.info["name"].lower():
#                 data = {
#                     proc.info["name"]:
#                         {
#                             "sessions":
#                                 [
#                                     {
#                                         "pid" : proc.info["pid"],
#                                         "session_start" : datetime.datetime.now(),
#                                         # "session_end" : da
#                                     }
#                                 ]
#                         }
#                 }
#                 print(json.dumps(data, indent=4))
#                 with open("./app_usage.json", "w") as f:
#                     json.dump(data,f, indent=4)
def main():
    pid = get_largest_memory_process("Notepad.exe")
    while True:
        if pid is not None:
            track_session_data("Notepad.exe", pid.info["pid"])

if __name__ == "__main__":
    main()