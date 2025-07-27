#Library imports

from datetime import datetime
import sys
import psutil
####   local import:   #####
#variavle import
# from main import PRODUCTIVE_APPS, UNPRODUCTIVE_APPS, ALL_APPS, active_tasks
from config import ALL_APPS
#functions:
from process_utils import check_if_process_is_active, get_largest_memory_process
# from write import serialize_datetime


allocated_time_to_unproductive_apps = 0

def ellapsed_time_and_allocated_time(session_start, is_productive):
    global allocated_time_to_unproductive_apps
    time_threshold = 300
    while True:
        for process in ALL_APPS:
            app_data = get_largest_memory_process(process)
            if app_data:
                if check_if_process_is_active(process):
                    time_elapsed = (datetime.now() - session_start).total_seconds()
                    if is_productive and time_elapsed >= time_threshold:
                        allocated_time_to_unproductive_apps += 300
                        time_threshold += 300
                    elif not is_productive:
                        allocated_time_to_unproductive_apps = allocated_time_to_unproductive_apps - time_elapsed
                        if allocated_time_to_unproductive_apps <= 0 and time_elapsed >= 300:
                            try:
                                app_data.kill()
                            except Exception as e:
                                print(f"Error killing process: {e}")
                            
                            
                if not check_if_process_is_active(process):
                    break
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
if __name__ == "__main__":
    main()