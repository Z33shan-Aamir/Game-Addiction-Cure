PRODUCTIVE_APPS = ["Chrome.exe", "Code.exe"]
UNPRODUCTIVE_APPS = ["Control_DX12.exe"]
ALL_APPS = PRODUCTIVE_APPS + UNPRODUCTIVE_APPS

def lowercase_list(input_list):
    """Converts all string elements in a list to lowercase.

    Args:
        input_list: The list to be converted.

    Returns:
        A new list with all string elements converted to lowercase.
    """
    return [item.lower() if isinstance(item, str) else item for item in input_list]

