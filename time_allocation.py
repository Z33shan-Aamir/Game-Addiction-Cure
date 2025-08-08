#Library imports
from datetime import datetime
import sys
import threading
import time
import psutil
####   local import:   #####
#variavle import
from config import ALL_APPS
#local function import:
from utilities.process_utils import check_if_process_is_active
from write import session_end_stamp
# from write import serialize_datetime

lock = threading.Lock()
with lock:
    allocated_time_to_unproductive_apps = 20

def ellapsed_time_and_allocated_time(session_start : datetime,app_data,is_productive : bool, event : threading.Event | None = None, debug=True ):
    global allocated_time_to_unproductive_apps
    print(allocated_time_to_unproductive_apps)
    process = app_data.info["name"]
    if is_productive:
        print(f"thread is running for productive process: {process}")
    else:
        print(f"thread is running for unproductive process: {process}")
    time_threshold = 2
    while True:
        # time.sleep(1)
        if event and event.is_set() and is_productive:
            print("(??)Threading.Event was set to true meaning the unporductive thread is running and all productive threads will be down.")
            with lock:
                session_end = datetime.now().isoformat()
                session_end_stamp(process_name=process, session_end=session_end, session_start=session_start)
                print(f"(--) Session ended: {session_end} | Process: {process} | PID: {app_data.info["pid"]}")
            break
        if app_data:
            if check_if_process_is_active(process):
                time_elapsed = (datetime.now() - session_start).total_seconds()
                if is_productive and time_elapsed >= time_threshold:
                    time.sleep(2)
                    with lock:
                        allocated_time_to_unproductive_apps += 1
                        if debug:
                            print(f"(++)Time allocated to unporductive apps: {allocated_time_to_unproductive_apps} seconds")
                    time_threshold += 2
                    
                elif not is_productive:
                    with lock:
                        allocated_time_to_unproductive_apps = allocated_time_to_unproductive_apps - 2
                        time.sleep(2)
                        if debug:
                            print(f"(--)Time de-allocated to unporductive apps: {allocated_time_to_unproductive_apps} seconds")
                    if allocated_time_to_unproductive_apps <= 0 and time_elapsed >= 20:
                        allocated_time_to_unproductive_apps = 0
                        try:
                            if debug:
                                print("Killing process.....")
                            else:
                                print("Killing Process In 60 seconds")
                                time.sleep(60)
                            kill_process_by_name(process_name=process)
                            with lock:
                                session_end = datetime.now().isoformat()
                                session_end_stamp(process_name=process, session_end=session_end, session_start=session_start)
                                print(f"(--) Session ended: {session_end} | Process: {process} | PID: {app_data.info["pid"]}")
                            print(f"Killed unproductive process: {process}")
                        except Exception as e:
                            print(f"Error killing process: {e}")
                        if event and event.is_set():
                            event.clear()
                            
            elif not check_if_process_is_active(process):  
                print("Thread was stopped because process is no longer active")
                with lock:
                    session_end = datetime.now().isoformat()
                    session_end_stamp(process_name=process, session_end=session_end, session_start=session_start)
                    print(f"(--) Session ended: {session_end} | Process: {process} | PID: {app_data.info["pid"]}")
                if event:
                    event.clear()
                break                 
            
         

def kill_process_by_name(process_name):
    for proc in psutil.process_iter(attrs=["name", "pid"]):
        if proc.info["name"].lower() == process_name.lower():
            try:
                proc.kill()
                print(f"Killed {process_name} (PID {proc.info['pid']})")
            except Exception as e:
                print(f"Could not kill {process_name}: {e}")
                
def main():
    """
    Only for debug purposes pass an command line argument with the process name to kill it.
    """
    if len(sys.argv) >1:
        kill_process_by_name(sys.argv[1])
    else:
        print("Sorry you didn't provide an argument")
