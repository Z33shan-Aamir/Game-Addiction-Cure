import psutil
import datetime, time

# local imports
from write import wirte_session_data_to_file


PRODUCTIVE_APPS = ["code"]
UNPRODUCTIVE_APPS = ["heroic"]

ALL_APPS = PRODUCTIVE_APPS + UNPRODUCTIVE_APPS


"""Testing is Done"""
active_tasks = {}
def track_session_data(process_name, pid):
    if pid not in active_tasks and check_if_process_is_active(process_name, pid):
        # Process started
        session_start = datetime.datetime.now()
        print(f"Session started: {session_start} | Process: {process_name} | PID: {pid}")
        # wirte_session_data_to_file(process_name, session_start)
        active_tasks[pid] = (process_name, session_start)
        print(active_tasks)

    elif pid in active_tasks and not check_if_process_is_active(process_name, pid):
        # Process ended
        process_name, session_start = active_tasks.pop(pid)
        session_end = datetime.datetime.now()
        print(f"Session ended: {session_end} | Process: {process_name} | PID: {pid}")
        # You can call a function here to write session data with start and end


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
# def main():
#     pid = get_largest_memory_process("firefox")
#     if pid is not None:
#             # print(f"pid: {pid}")
#         track_session_data("firefox", pid.info["pid"])



def main():
    # Check all running instances of the tracked app
    for proc in psutil.process_iter(attrs=["name", "pid"]):
        if proc.info["name"] and proc.info["name"].lower() == "firefox":
            track_session_data(proc.info["name"], proc.info["pid"])

    # Detect if any tracked PIDs have disappeared (process ended)
    current_pids = {proc.info["pid"] for proc in psutil.process_iter(attrs=["pid"])} # stores all the pids for workin processes
    for pid in list(active_tasks.keys()):
        if pid not in current_pids: #if the process pid is not in all process pids then it will run the code
            process_name, session_start = active_tasks.pop(pid)
            session_end = datetime.datetime.now()
            print(f"Session ended: {session_end} | Process: {process_name} | PID: {pid}")  # marks the session end

if __name__ == "__main__":
    while True:
        main()
        time.sleep(1)