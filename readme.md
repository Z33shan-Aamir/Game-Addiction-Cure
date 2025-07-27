# Game Addiction Cure

## Overview
The **Game Addiction Cure** project is designed to monitor and manage application usage on a system. It tracks productive and unproductive applications, logs session data, and can terminate unproductive applications if certain thresholds are exceeded.

---

## Features
- **Track Application Usage**:
  - Logs session start and end times for applications.
  - Differentiates between productive and unproductive applications.
- **Kill Unproductive Applications**:
  - Automatically terminates unproductive applications if usage exceeds allocated time.
- **Session Data Management**:
  - Stores session data in a JSON file for persistent tracking.
- **Foreground and Background Process Detection**:
  - Identifies whether an application is running in the foreground or background.

---

## File Structure
### **Main Files**
- `main.py`: Entry point for tracking application usage and managing sessions.
- `time_allocation.py`: Handles time allocation for applications and terminates unproductive apps.
- `write.py`: Manages session data storage and retrieval in JSON format.
- `utilities/config.py`: Contains configuration for productive and unproductive applications.
- `utilities/process_utils.py`: Provides utility functions for process management.

---

## Installation
1. Clone the repository:
```bash
   git clone https://github.com/your-repo/GameAddictionCure.git
```
2. Install dependencies:
```bash
pip install psutil pywin32
```
# Usage
### Run the Application
To start tracking application usage:
```bash
python main.py
```
Kill a Process
To manually kill a process by name:
```bash
python time_allocation.py <name-of-process>
```
Replace `<name-of-process>` with the name of process which will be like `notepad.exe` on windows and `steam` on linux
# Configuration
Productive and Unproductive Applications
Edit the utilities/config.py file to define productive and unproductive applications:

# Functions
Main Functions
### `main.py`

#### `track_session_data(process_name, pid)`
Tracks the start of a session for a given process and logs relevant data, distinguishing between productive and unproductive applications.

#### `main(process_name)`
Monitors active processes, manages session data, and coordinates tracking of productive/unproductive application usage.

---

### `time_allocation.py`

#### `ellapsed_time_and_allocated_time(session_start, is_productive)`
Calculates elapsed and allocated time for application sessions. Terminates unproductive applications if their usage exceeds predefined thresholds.

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
# Future Improvements
- Implement OS-level graceful shutdowns.
- Add support for real-time notifications or pop-ups.
- Enhance session data visualization.
- Create a GUI for the app and make it run as a daemon


