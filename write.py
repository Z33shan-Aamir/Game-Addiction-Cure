import json
import datetime
from typing import Dict, List, Optional,Any
# def wirte_session_data_to_file (process_name, session_start ,session_end = None):
#     data = {
#         process_name: {
#             "sessions" : [
#                 {
#                     "session_start": session_start,
#                     "session_end": session_end,
#                 }
#             ]
#         }
#     }
#     try:
#         with open("./app_usage.json", "a") as f:
#             json.dump(data, f, indent=4)
#     except:
#         print("Exeption Occoured on line 18 in write.py")

def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

class AppUsageData:
    def __init__(self, file: str = "./app_usage.json") -> None:
        """
        Initialize the AppUsageData instance.

        Args:
            file (str): Path to the JSON file storing app usage data.
        """
        self.file: str = file
        self.data: Dict[str, Any] = self._load_data()  # Loaded JSON data as a dictionary

    def _load_data(self) -> Dict[str, Any]:
        """
        Private method to load JSON data from the file.

        Returns:
            dict: Parsed JSON data as a dictionary. Returns empty dict if file not found or invalid.
        """
        try:
            with open(self.file, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return empty dict if file does not exist or contains invalid JSON
            return {}

    def get_process_data(self, process_name: str) -> Dict[str, Any]:
        """
        Return all data for a specific process.

        Args:
            process_name (str): The name of the process to retrieve data for.

        Returns:
            dict: Data dictionary for the given process. Empty dict if process not found.
        """
        return self.data.get(process_name, {})

    def get_session_starts(self, process_name: str) -> List[Optional[str]]:
        """
        Return a list of session start times for a given process.

        Args:
            process_name (str): The name of the process.

        Returns:
            list: List of session start timestamps (as strings or None if missing).
        """
        sessions = self.data.get(process_name, {}).get("sessions", [])
        return [session.get("session_start") for session in sessions]

    def get_session_ends(self, process_name: str) -> List[Optional[str]]:
        """
        Return a list of session end times for a given process.

        Args:
            process_name (str): The name of the process.

        Returns:
            list: List of session end timestamps (as strings or None if missing).
        """
        sessions = self.data.get(process_name, {}).get("sessions", [])
        return [session.get("session_end") for session in sessions]


app_usage = AppUsageData()

def write_session_data_to_file(process_name, is_productive, session_start, session_end=None, was_marked=False):
    try:
        # Create an instance to call the method properly
        data = app_usage._load_data()  # Call the method to get the data dictionary
        
    except Exception as e:
        print(f"Error loading data: {e}")
        data = {}
    session_start = session_start
    new_session_data = {
        "session_start": session_start,
        "session_end": session_end,  # Use the passed session_end, not always None
        "was_marked": False,
        "mark_day": str(datetime.date.today()),  # Convert date to string for JSON
        "is_productive": bool(is_productive)
    }
    if process_name not in data:
        data[process_name] = {"sessions": []}

    # Append the new session data to the sessions list
    data[process_name]["sessions"].append(new_session_data)
    # Write updated data back to the file
    with open("./app_usage.json", "w") as f:
        json.dump(data, f, indent=4,default=serialize_datetime)

           
def session_end_stamp(process_name: str, session_end, session_start):
    data = app_usage._load_data()
    session_data = data[process_name]["sessions"]
    # Convert session_start to ISO string if it's a datetime object
    if isinstance(session_start, datetime.datetime):
        session_start_str = session_start.isoformat()
    else:
        session_start_str = session_start  # assume already string
    
    for session in session_data:
        if session["session_end"] is None and session_start_str == session["session_start"]:
            session["session_end"] = session_end
            session["was_marked"] = True
            break
    
    with open("./app_usage.json", "w") as f:
        json.dump(data, f, indent=4, default=serialize_datetime)
    print("session end data has been written")

