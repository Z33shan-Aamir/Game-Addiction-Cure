import psutil
import datetime,time
import win32gui

import json

PRODUCTIVE_APPS = ["Code.exe", "excel.exe"]
UNPRODUCTIVE_APPS = ["tiktok.exe", "discord.exe"]

ALL_APPS = PRODUCTIVE_APPS + UNPRODUCTIVE_APPS

def get_pid(processes):
    for proc in psutil.process_iter(attrs=["name", "pid"]):
        for process in processes:
            if process.lower() == proc.info["name"].lower:
                data = {
                    proc.info["name"]:
                        {
                            "sessions":
                                [
                                    {
                                        "pid" : proc.info["pid"],
                                        "start_time" : datetime.datetime.now()
                                    }
                                ]
                        }
                }
                print(json.dumps(data, indent=4))
                with open("./app_usage.json", "w") as f:
                    json.dump(data,f, indent=4)
def main():
    get_pid(ALL_APPS)        

main()


# while True:
#     # active_window = get_active_window().lower()
#     for proc in psutil.process_iter(attrs=["name","pid"]):
#         if proc.info["name"].lower() in PRODUCTIVE_APPS:
#             print(f"Working on: {proc.info['name']}")
#         if proc.info["name"].lower() in UNPRODUCTIVE_APPS:
#             print(f"Slacking off on: {proc.info['name']}")
#     time.sleep(5)