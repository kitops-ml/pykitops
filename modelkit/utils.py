from .errors import NullOrEmptyStringError, NullOrEmptyListError

def is_empty_string(value: str) -> bool:
    return (value == None or value.strip() == "")

def is_valid_string(obj: object) -> bool:
    return isinstance(obj, str) and not is_empty_string(obj)

def is_empty_list(list: list) -> bool:
    return (list == None or len(list) == 0)

def is_valid_list(obj: object) -> bool:
    return isinstance(obj, list) and len(obj) > 0

def check_string_validity(value: str) -> str:
    if is_empty_string(value):
        raise NullOrEmptyStringError(
                "String must not be None nor the empty string.")
    return value
    
def check_list_validity(list: list) -> list:
    if is_empty_list(list):
        raise NullOrEmptyListError(
                "List must not be None nor empty" )
    return list

# Custom representer function
def custom_dict_representer(dumper, data):
    return dumper.represent_dict(data.items())