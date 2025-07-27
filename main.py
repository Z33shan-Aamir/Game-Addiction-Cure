import psutil
import datetime, time
import _asyncio
# local imports
from write import write_session_data_to_file, session_end_stamp
from time_allocation import ellapsed_time_and_allocated_time
from process_utils import check_if_process_is_active, get_largest_memory_process, check_if_process_is_running_in_background
from config import lowercase_list
# variable imports
from config import ALL_APPS, PRODUCTIVE_APPS, UNPRODUCTIVE_APPS


"""Testing is Done"""
active_tasks = {}

def track_session_data(process_name, pid):
    process_name = process_name.lower()
    if process_name not in active_tasks.keys() and check_if_process_is_active(process_name): #and check_if_process_is_running_in_background(process_name):
        # Process started
        session_start = datetime.datetime.now()
        print(f"(++)Session started: {session_start} | Process: {process_name} | PID: {pid}")
        if process_name in lowercase_list(PRODUCTIVE_APPS):
            #ellapsed_time_and_allocated_time(session_start=session_start, process_name=process_name, is_productive=True)
            write_session_data_to_file(process_name, session_start=session_start, is_productive=True)
            
            
        elif process_name in lowercase_list(UNPRODUCTIVE_APPS):
            # ellapsed_time_and_allocated_time(session_start=session_start, process_name=process_name, is_productive=True)
            write_session_data_to_file(process_name, session_start=session_start, is_productive=False)
        else:
            write_session_data_to_file(process_name, is_productive=None, session_start=session_start)
        active_tasks[process_name] = (pid, session_start)
        session_start = active_tasks[process_name][1]

def main(process_name):
    process_name = process_name.lower()
    top_process = get_largest_memory_process(process_name)
    
    if top_process:
        track_session_data(top_process.info["name"], top_process.pid)

    current_processes = {proc.info["name"] for proc in psutil.process_iter(attrs=["name"])}
    
    for process in list(active_tasks.keys()):
        if process not in current_processes:
            session_end = datetime.datetime.now()
            pid, session_start = active_tasks.pop(process)
            print(f"(--) Session ended: {session_end} | Process: {process} | PID: {pid}")
            session_end_stamp(process_name=process, session_end=session_end, session_start=session_start)


if __name__ == "__main__":
    while True:
        for apps in ALL_APPS:
            main(apps)
            time.sleep(1.5)
            
        
        
        
