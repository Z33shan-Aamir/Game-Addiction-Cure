import psutil
import datetime, time
# import threading
from concurrent.futures import ThreadPoolExecutor
from threading import Event
# local imports

from write import write_session_data_to_file, session_end_stamp
from time_allocation import ellapsed_time_and_allocated_time
from utilities.process_utils import check_if_process_is_active, get_largest_memory_process, check_if_process_is_running_in_background
from config import lowercase_list
# variable imports
from config import ALL_APPS, PRODUCTIVE_APPS, UNPRODUCTIVE_APPS

# Used to communicate with the thread. In this app, used to kill the threads
event = Event()  

active_tasks = {}

executor = ThreadPoolExecutor(max_workers=3)
def track_session_data(process_name, pid):
    process_name = process_name.lower()
    if process_name not in active_tasks.keys() and check_if_process_is_active(process_name): #and check_if_process_is_running_in_background(process_name):
        # Process started
        session_start = datetime.datetime.now()
        print(f"(++)Session started: {session_start} | Process: {process_name} | PID: {pid}")
        active_tasks[process_name] = (pid, session_start)
        if process_name in lowercase_list(PRODUCTIVE_APPS):
            
            # Run ellapsed_time_and_allocated_time concurrently using threading
            executor.submit(ellapsed_time_and_allocated_time, session_start, app_data=get_largest_memory_process(process_name),event=event, is_productive=True)
            write_session_data_to_file(process_name, session_start=session_start, is_productive=True)
            
            
        elif process_name in lowercase_list(UNPRODUCTIVE_APPS):
            # sets the internal flag to true
            # And this true is used to kill the thread (for productive apps)
            event.set()
            #ellapsed_time_and_allocated_time(session_start=session_start, process_name=process_name, is_productive=True)
            executor.submit(ellapsed_time_and_allocated_time, session_start, app_data=get_largest_memory_process(process_name), is_productive=False)
            write_session_data_to_file(process_name, session_start=session_start, is_productive=False)
        else:
            write_session_data_to_file(process_name, is_productive=None, session_start=session_start)

def main(process_name):
        process_name = process_name.lower()
    
        current_processes = {proc.info["name"] for proc in psutil.process_iter(attrs=["name"])}
        
        top_process = get_largest_memory_process(process_name)
        
        if top_process:
            track_session_data(top_process.info["name"], top_process.info["pid"])

        
        for process in  list(active_tasks.keys()):
            if process not in current_processes and not(check_if_process_is_active(process)):
                session_end = datetime.datetime.now()
                pid, session_start = active_tasks.pop(process)
                print(f"(--) Session ended: {session_end} | Process: {process} | PID: {pid}")
                session_end_stamp(process_name=process, session_end=session_end, session_start=session_start)


if __name__ == "__main__":
        while True:
            for apps in ALL_APPS:
                time.sleep(1.5)
                main(apps)
# import cProfile
# import pstats
# with cProfile.Profile() as profile:
#     # for i in range(10):
#     #     for app in ALL_APPS:       
#     main("code.exe")
    
#     stats = pstats.Stats(profile)
#     stats.sort_stats(pstats.SortKey.TIME)
#     stats.print_stats()