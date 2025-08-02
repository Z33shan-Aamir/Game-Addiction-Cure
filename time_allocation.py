#Library imports
from datetime import datetime
import sys
import threading
import time
import psutil
####   local import:   #####
#variavle import
from config import ALL_APPS
#functions:
from utilities.process_utils import check_if_process_is_active, get_largest_memory_process
# from write import serialize_datetime

lock = threading.Lock()
allocated_time_to_unproductive_apps = 0

def ellapsed_time_and_allocated_time(session_start, app_data, is_productive):
    global allocated_time_to_unproductive_apps
    print(allocated_time_to_unproductive_apps)
    with lock:
        print("thread is running")
    process = app_data.info["name"]
    time_threshold = 1
    while True:
        time.sleep(1.5)
        app_data = get_largest_memory_process(process)
        if app_data:
            if check_if_process_is_active(process):
                time_elapsed = (datetime.now() - session_start).total_seconds()
                if is_productive and time_elapsed >= time_threshold:
                    with lock:
                        allocated_time_to_unproductive_apps += 0.5
                        print(f"(++)Time allocated to unporductive apps: {allocated_time_to_unproductive_apps} seconds")
                    time_threshold += 1
                elif not is_productive:
                    with lock:
                        allocated_time_to_unproductive_apps = allocated_time_to_unproductive_apps - time_elapsed
                        print(f"(--)Time de-allocated to unporductive apps: {allocated_time_to_unproductive_apps} seconds")
                    if allocated_time_to_unproductive_apps <= 0 and time_elapsed >= 20:
                        try:
                            print("Killing process in 60 seconds.....")
                            time.sleep(60)
                            app_data.kill()
                        except Exception as e:
                            print(f"Error killing process: {e}")
                            
                            
            if not check_if_process_is_active(process):
                print("thread was killed because process has ended")
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
