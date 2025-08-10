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
active_unproductive = []
executor = ThreadPoolExecutor(max_workers=3)
def check_and_remove_unproductive_tasks(debug=True):
    time.sleep(2)
    for app in UNPRODUCTIVE_APPS:
        if check_if_process_is_active(app):
            if app not in active_unproductive:
                active_unproductive.append(app)
                if debug:
                    print(app, "was added to active_unproductive")

        elif not check_if_process_is_active(app) and app in active_unproductive:
            if debug:
                print(app, "was removed from active_unproductive")
            active_unproductive.remove(app)
    if not(active_unproductive):
        event.clear()
    if active_unproductive:
        event.set()
def remove_unactive_tasks():
    time.sleep(2)
    for app in list(active_tasks.keys()):
        if app is not(check_if_process_is_active(app)) and app in active_tasks: 
            active_tasks.pop(app)
            
def track_session_data(process_name, pid):
    process_name = process_name.lower()
    if process_name not in active_tasks.keys() and check_if_process_is_active(process_name): #and check_if_process_is_running_in_background(process_name):
        # Process started
        session_start = datetime.datetime.now()
        print(f"(++)Session started: {session_start} | Process: {process_name} | PID: {pid}")
        
        active_tasks[process_name] = (pid, session_start)
        if process_name in lowercase_list(PRODUCTIVE_APPS) and not(event.is_set()):
            # Run ellapsed_time_and_allocated_time concurrently using threading
            executor.submit(ellapsed_time_and_allocated_time, session_start, app_data=get_largest_memory_process(process_name),event=event, is_productive=True)
            write_session_data_to_file(process_name, session_start=session_start, is_productive=True)
        
            
        elif process_name in lowercase_list(UNPRODUCTIVE_APPS):
            active_tasks[process_name] = (pid, session_start)
            for app in PRODUCTIVE_APPS:
                 if app in active_tasks:
                    session_start = active_tasks[app][1]
                    active_tasks.pop(app)
                    session_end_stamp(app, session_end=datetime.datetime.now().isoformat(), session_start=session_start)
            # sets the internal flag to true
            # And this true is used to kill the thread (for productive apps)
            event.set()
            #ellapsed_time_and_allocated_time(session_start=session_start, process_name=process_name, is_productive=True)
            executor.submit(ellapsed_time_and_allocated_time, session_start, app_data=get_largest_memory_process(process_name), is_productive=False, event=event)
            write_session_data_to_file(process_name, session_start=session_start, is_productive=False)
        else:
            write_session_data_to_file(process_name, is_productive=None, session_start=session_start)


def main(process_name):
        process_name = process_name.lower()

        current_processes = {proc.info["name"] for proc in psutil.process_iter(attrs=["name"])}
        
        top_process = get_largest_memory_process(process_name)
        
        if top_process:
            track_session_data(top_process.info["name"], top_process.info["pid"])

        # I may remove this        
        for process in  list(active_tasks.keys()):
            
            if process not in current_processes and not(check_if_process_is_active(process)):
                active_tasks.pop(process)
                # print(f"(--) Session ended: {session_end} | Process: {process} | PID: {pid}")
                
                # session_end_stamp(process_name=process, session_end=session_end, session_start=session_start)


if __name__ == "__main__":
    try:
        
        print("App is now running")
        event = Event()  
        while True:
            check_and_remove_unproductive_tasks()

            # if event.is_set():
            #     print("Waiting for unproductive app thread to finish...")
            #     time.sleep(3)  # Wait for the event to be cleared
            #     continue
            if not(event.is_set()):
                for app in PRODUCTIVE_APPS:
                    time.sleep(1.5)
                    main(app)
            for app in UNPRODUCTIVE_APPS:
                time.sleep(2)
                main(app)
            
                
            
                
    except KeyboardInterrupt:
        executor.shutdown(wait=False)
# import cProfile
# import pstats
# with cProfile.Profile() as profile:
#     # for i in range(10):
#     #     for app in ALL_APPS:       
#     main("code.exe")
    
#     stats = pstats.Stats(profile)
#     stats.sort_stats(pstats.SortKey.TIME)
#     stats.print_stats()