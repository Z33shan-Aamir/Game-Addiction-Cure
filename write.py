import json
import datetime

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


def write_sessison_data_to_file(process_name, session_start, session_end = None):
    try:
        data = get_data_from_json_file()
    except:
        data = {}
    else:
        new_session_data = {
            "session_start": session_start,
            "session_end" : None,
            "was_marked" : False,
            "mark_day" : datetime.date.today()
        }
        data[process_name]["sessions"]
def session_end_stamp(process_name, session_end):
    with open("./app_usage.json", "r") as f:
        data = json.load(f)
    for i, session_data in enumerate(data["process_name"]["sessions"]):
        if session_data["session_end"] == None:
            session_data["session_end"] = session_end 
            write_sessison_data_to_file(process_name, data["process_name"]["sessions"][i]["session_start"], session_end )
            print("session end data has been written")

def random_exit(process_name):
    pass

def get_data_from_json_file(
    file="./app_usage.json",
    process_name=None,
    need_session_start_data=None,
    need_session_end_data=None
):
    with open(file, "r") as f:
        data = json.load(f)

    # If no process_name given, return full data
    if not process_name:
        return data

    # If process_name not in data, return empty
    if process_name not in data:
        return {}

    sessions = data[process_name].get("sessions", [])

    # If need_session_start_data is True, return all start times
    if need_session_start_data:
        return [session.get("session_start") for session in sessions]

    # If need_session_end_data is True, return all end times
    if need_session_end_data:
        return [session.get("session_end") for session in sessions]

    # If none of the above, return full data for that process
    return data[process_name]
