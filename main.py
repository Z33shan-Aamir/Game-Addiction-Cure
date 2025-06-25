import psutil
from typing import List
process_name = "Discovery.exe"

def get_pid(process_name):
   for proc in psutil.process_iter():
       if proc.name() == process_name:
          return proc.pid

print(get_pid(process_name))