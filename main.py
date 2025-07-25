import psutil
import datetime, time

# local imports
from write import write_session_data_to_file, session_end_stamp
from time_allocation import ellapsed_time_and_allocated_time
from process_utils import check_if_process_is_active, get_largest_memory_process
from config import lowercase_list
# variable imports
from config import ALL_APPS, PRODUCTIVE_APPS, UNPRODUCTIVE_APPS


"""Testing is Done"""
active_tasks = {}
def track_session_data(process_name, pid):
    process_name = process_name.lower()
    if pid not in active_tasks and check_if_process_is_active(process_name, pid):
        # Process started
        session_start = datetime.datetime.now()
        print(f"(++)Session started: {session_start} | Process: {process_name} | PID: {pid}")
        if process_name in lowercase_list(PRODUCTIVE_APPS):
            # ellapsed_time_and_allocated_time(session_start=session_start, process_name=process_name, is_productive=True)
            write_session_data_to_file(process_name, session_start=session_start, is_productive=True)
            
            
        elif process_name in lowercase_list(UNPRODUCTIVE_APPS):
            # ellapsed_time_and_allocated_time(session_start=session_start, process_name=process_name, is_productive=True)
            write_session_data_to_file(process_name, session_start=session_start, is_productive=False)
        else:
            write_session_data_to_file(process_name, is_productive=None, session_start=session_start)
        active_tasks[pid] = (process_name, session_start)
        session_start = active_tasks[pid][1]

def main(process_name):
    process_name = process_name.lower()
    top_process = get_largest_memory_process(process_name)
    
    if top_process:
        track_session_data(top_process.info["name"], top_process.pid)

    current_pids = {proc.info["pid"] for proc in psutil.process_iter(attrs=["pid"])}
    
    for pid in list(active_tasks.keys()):
        if pid not in current_pids:
            session_end = datetime.datetime.now()
            pname, session_start = active_tasks.pop(pid)
            print(f"(--) Session ended: {session_end} | Process: {pname} | PID: {pid}")
            session_end_stamp(process_name=pname, session_end=session_end, session_start=session_start)


if __name__ == "__main__":
    while True:
        for apps in ALL_APPS:
            main(apps)
            time.sleep(1.5)
            
        
        
        
