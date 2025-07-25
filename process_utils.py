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

def check_if_process_is_active(process_name, pid):
    process_name = process_name.lower()
    for proc in psutil.process_iter(attrs=["name", "pid"]):
        if proc.info["name"].lower() == process_name and proc.info["pid"] == pid:
            return True
    return False