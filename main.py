import psutil
import datetime, time

# local imports
from write import write_session_data_to_file, session_end_stamp
# from time_allocation import ellapsed_time

PRODUCTIVE_APPS = ["Chrome.exe", "Code.exe"]
UNPRODUCTIVE_APPS = ["Control_DX12.exe"]

ALL_APPS = PRODUCTIVE_APPS + UNPRODUCTIVE_APPS


"""Testing is Done"""
active_tasks = {}
def track_session_data(process_name, pid):
    if pid not in active_tasks and check_if_process_is_active(process_name, pid):
        # Process started
        session_start = datetime.datetime.now()
        print(f"(++)Session started: {session_start} | Process: {process_name} | PID: {pid}")
        if process_name in PRODUCTIVE_APPS:
            write_session_data_to_file(process_name, session_start=session_start, is_productive=True)
            
        elif process_name in UNPRODUCTIVE_APPS:
            write_session_data_to_file(process_name, session_start=session_start, is_productive=False)
        else:
            write_session_data_to_file(process_name, is_productive=None, session_start=session_start)
        active_tasks[pid] = (process_name, session_start)
        session_start = active_tasks[pid][1]




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

def main(process_name):
    top_process = get_largest_memory_process(process_name)
    
    if top_process:
        track_session_data(top_process.info["name"], top_process.pid)
    
    current_pids = {proc.info["pid"] for proc in psutil.process_iter(attrs=["pid"])}
    
    for pid in list(active_tasks.keys()):
        if pid not in current_pids:
            session_end = datetime.datetime.now()
            pname, session_start = active_tasks.pop(pid)
            print(f" (--) Session ended: {session_end} | Process: {pname} | PID: {pid}")
            session_end_stamp(process_name=pname, session_end=session_end, session_start=session_start)


if __name__ == "__main__":
    while True:
        for apps in ALL_APPS:
            main(apps)
            time.sleep(1.5)
            
        
        
        
