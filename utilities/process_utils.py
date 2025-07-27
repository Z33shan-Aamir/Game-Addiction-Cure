import win32gui, win32process
import time
import psutil

def get_largest_memory_process(process_name):
    best_proc = None
    max_mem = 0
    process_name = process_name.lower()
    for proc in psutil.process_iter(attrs=["name", "pid", "memory_info"]):
        try:
            if proc.info["name"].lower() == process_name:
                mem_usage = proc.info["memory_info"].rss
                if mem_usage > max_mem:
                    max_mem = mem_usage
                    best_proc = proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return best_proc

def check_if_process_is_active(process_name):
    """_summary_
    Check if a process is running
    Args:
        process_name (str): Name of the process that is to be checked

    Returns:
        boolean: Returns true if process is active and false if not
    """
    process_name = process_name.lower()
    for proc in psutil.process_iter(attrs=["name", "pid"]):
        if proc.info["name"].lower() == process_name:
            return True
    return False


def check_if_process_is_running_in_background(process_name):
    """_summary_
    The name explains it all and only returns true if the user is interacting with it
    Args:
        process_name (str): name of the porcess

    Returns:
        bool: returns true if app is not being interacted with
    """
    # Get the foreground window's HWND
    hwnd = win32gui.GetForegroundWindow()
    if hwnd == 0:
        # No foreground window found
        return None

    # Get PID of foreground window's process
    _, foreground_pid = win32process.GetWindowThreadProcessId(hwnd)

    # Track if process is running at all
    process_running = False

    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            process_running = True
            # Check if this process's PID matches foreground window PID
            if proc.info['pid'] == foreground_pid:
                print(f"{process_name} is running in the foreground.")
                return False  # Process is in foreground
            else:
                # Found process but not foreground window PID
                # Keep checking all processes
                continue

    if process_running:
        # Process found but not foreground
        print(f"{process_name} is running but not in the foreground.")
        return True
    else:
        # Process not found at all
        print(f"{process_name} is not running.")
        return None



def main():
    time.sleep(5)
    status = check_if_process_is_running_in_background("chrome.exe")
    if status is True:
        print("chrome.exe is running in the background.")
    elif status is False:
        print("chrome.exe is running in the foreground.")
    else:
        print("chrome.exe is not running.")

main()
