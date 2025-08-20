# Game Addiction Cure

## Overview
The **Game Addiction Cure** project is designed to monitor and manage application usage on a system. It tracks productive and unproductive applications, logs session data, and can terminate unproductive applications if certain thresholds are exceeded.

---

## Features
- Tracks productive and unproductive applications.
- Logs session start and end times for each application.
- Allocates time dynamically to unproductive apps.
- Terminates unproductive apps when their allocated time is exceeded.
- Uses threading for concurrent monitoring of multiple applications.
---

## Project Structure

```
GameAddictionCure/
│
├── main.py                  # Entry point of the application
├── time_allocation.py       # Handles time allocation and session management
├── write.py                 # Handles session data logging
├── config.py                # Loads app configuration
├── utilities/
│   └── process_utils.py     # Utility functions for process management
├── data/
│   ├── config.json          # Configuration file for app tracking
│   └── app_usage.json       # Logs app usage data
└── dist/
    └── data/
        └── config.json      # Backup configuration file
```
---

## Installation
1. Clone the repository:
```bash
   git clone https://github.com/your-repo/GameAddictionCure.git
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```

# Usage
### Run the Application
To start tracking application usage:

```bash
python main.py
```

### Kill a Process
To manually kill a process by name:
```bash
python time_allocation.py <name-of-process>
```
Replace `<name-of-process>` with the name of process which will be like `notepad.exe` on windows and `steam` on linux
> [!warning]
> In case of linux using the name of the process may not work.
> Instead use the name for the app used in `htop` or `btop` or any other resource monitor
> for example command to launch chrome is `google-chrome-stable` but in the resource monitor it's `chrome`

### Degugging:
  - Enable debug mode in `check_and_remove_unproductive_tasks(debug=True)` to see detailed logs.

### Add/Remove Apps
  - Update `data/config.json` to modify the list of productive and unproductive apps.
# Configuration


```JSON
{
    "productive_apps": ["code.exe"],
    "unproductive_apps": ["chrome.exe"]
}
```
- `productive_apps`: List of apps considered productive.
- `unproductive_apps`: List of apps considered unproductive.
---

# Functions
Main Functions
### `main.py`

#### `track_session_data(process_name, pid)`
Tracks the start of a session for a given process and logs relevant data, distinguishing between productive and unproductive applications.

#### `main(process_name)`
Monitors active processes, manages session data, and coordinates tracking of productive/unproductive application usage.

---

### `time_allocation.py`

#### `ellapsed_time_and_allocated_time(session_start, app_data, is_productive, event)`
- Tracks elapsed time for productive and unproductive apps.
- Dynamically adjusts allocated time for unproductive apps.
- Terminates unproductive apps when their time is exceeded.

#### `kill_process_by_name(process_name)`
Terminates all processes matching the specified name.

---

### `write.py`

#### `write_session_data_to_file(process_name, is_productive, session_start, session_end=None, was_marked=False)`
Writes session data for a process to a JSON file, including session start/end times, productivity status, and marking information.

#### `session_end_stamp(process_name, session_end, session_start)`
Updates the session end time for a process in the JSON file.

---

### `process_utils.py`

#### `get_largest_memory_process(process_name)`
Identifies and returns the process with the highest memory usage for the specified process name.

#### `check_if_process_is_active(process_name)`
Checks if a process with the given name is currently active.

#### `check_if_process_is_running_in_background(process_name)`
Determines whether a process is running in the background.

---

### JSON Data Format

Session data is stored in `app_usage.json` with the following structure:
```json
{
    "chrome.exe": {
        "sessions": [
            {
                "session_start": "2025-07-27T10:00:00",
                "session_end": "2025-07-27T11:00:00",
                "was_marked": true,
                "mark_day": "2025-07-27",
                "is_productive": true
            }
        ]
    }
}
```
---
# How It Works
1. Initialization:

  - The app reads the configuration file to load productive and unproductive apps.
  - Threads are initialized for concurrent monitoring.
2. Monitoring:

  - Active processes are checked periodically.
  - Productive and unproductive apps are tracked separately.

3. Time Management:

  - Productive apps increase the allocated time for unproductive apps.
  - Unproductive apps decrease their allocated time.
4. Termination:

  -If an unproductive app exceeds its allocated time, it is terminated.

---

# Future Improvements
- Implement OS-level graceful shutdowns.
- Add support for real-time notifications or pop-ups.
- Enhance session data visualization.
- Create a GUI for the app and make it run as a daemon
- Add Passive Aggressive Quote/Sentences To make you not spend time on Useless stuff

