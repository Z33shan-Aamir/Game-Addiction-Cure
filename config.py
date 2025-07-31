# library imports
import json
# local imports 


def get_app_names_for_tracking():
    """_summary_
    returns a dictionary of apps that are to be tracked
    Returns:
        dict: A dictionary of format app_type: [app_names]
    """
    try:
        with open("./data/config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        with open("../data/config.json", "w") as f:
            default_format = {
                "unproductive_apps": [],
                "productive_apps": []
            }
            json.dump(default_format, f, indent=4)


app_name_data = get_app_names_for_tracking()

if app_name_data:
    PRODUCTIVE_APPS = app_name_data["productive_apps"]
    UNPRODUCTIVE_APPS = app_name_data["unproductive_apps"]
    ALL_APPS = PRODUCTIVE_APPS + UNPRODUCTIVE_APPS
else:
    pass 
    """Todo:
    Call a fucntion to add these
    """
def lowercase_list(input_list):
    """Converts all string elements in a list to lowercase.

    Args:
        input_list: The list to be converted.

    Returns:
        A new list with all string elements converted to lowercase.
    """
    return [item.lower() if isinstance(item, str) else item for item in input_list]

