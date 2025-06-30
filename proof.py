import psutil
import time
import json

def main():
    # List of target apps (e.g., "notepad.exe", "msedge.exe")
    target_apps = ["notepad.exe", "msedge.exe"]  # Add more apps as needed
    
    # Dictionary to store start times for each app
    app_start_times = {}
    
    try:
        while True:
            # Check if any app is running
            current_processes = [proc.info for proc in psutil.process_iter(attrs=["name"])]
            
            # For each target app, check if it's running and record its start time
            for app in target_apps:
                if app.lower() in [p["name"].lower() for p in current_processes]:
                    # If the app started since last check, record start time
                    if app not in app_start_times:
                        app_start_times[app] = time.time()
                else:
                    # If the app stopped, calculate duration and reset
                    if app in app_start_times:
                        duration = time.time() - app_start_times[app]
                        print(f"{app} was used for {duration:.2f} seconds.")
                        del app_start_times[app]
            
            # Check every second
            time.sleep(1)
    
    except KeyboardInterrupt:
        # Finalize and save results to JSON on exit
        if app_start_times:
            for app in app_start_times:
                duration = time.time() - app_start_times[app]
                print(f"{app} was used for {duration:.2f} seconds.")
        
        # Save data to a JSON file
        usage_data = {
            "app_usage": [
                {"app_name": app, "total_time_seconds": duration}
                for app, duration in app_start_times.items()
            ]
        }
        
        with open("app_usage.json", "w") as f:
            json.dump(usage_data, f, indent=4)
        print("Usage data saved to app_usage.json.")

if __name__ == "__main__":
    main()
