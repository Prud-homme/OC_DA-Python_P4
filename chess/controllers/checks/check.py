import os
import sys
from datetime import datetime

checkdir = os.path.dirname(os.path.realpath(__file__))
controllersdir = os.path.dirname(checkdir)
chessdir = os.path.dirname(controllersdir)
sys.path.append(chessdir)
from utils import pause, clear_display
from logger import logger
from views import display_message, entry_request
from typing import Optional, Callable, Union


def choice_is_valid(choice: str, handler: dict) -> bool:
    """Check if the user's choice corresponds to one of the handler's choices"""
    for key, value in handler.items():
        if choice == key:
            return True
    return False


def entry_is_not_empty(entry: str, **kwargs) -> bool:
    """Check if the user has entered something"""
    if len(entry) > 0:
        return True
    else:
        logger.error("Entry is empty")
        return False


def entry_is_integer_under_max_value(entry: str, **kwargs) -> bool:
    """
    Check if the user has entered an positive integer.
    It is also possible to set a value not to be exceeded
    """
    max_value: int = kwargs.get("max_value", None)

    if max_value == None:
        if entry.isdecimal() and int(entry) >= 0:
            return True
        else:
            logger.error("Entry is not a positive integer")
            return False

    if entry.isdecimal() and int(entry) <= max_value and int(entry) >= 0:
        return True
    else:
        logger.error(f"Entry is not a positive interger under {max_value}")
        return False


def entry_belongs_list(entry: str, **kwargs) -> bool:
    """Check if the user has entered a value in the list provided"""
    allowed_list: list = kwargs.get("allowed_list", None)
    if allowed_list == None:
        return True
    if allowed_list == None or entry.lower() in allowed_list or entry.upper() in allowed_list:
        return True
    else:
        logger.error(f"""Entry is not in {' '.join(allowed_list)}""")
        return False


def entry_is_valid_datetime(entry: str, **kwargs) -> bool:
    """Check if the user has entered a datetime in the requested format"""
    min_date_str: str = kwargs.get("min_date_str", "1582-10-15 00:00")

    try:
        min_date = datetime.strptime(min_date_str, "%Y-%m-%d %H:%M")
        date = datetime.strptime(entry, "%Y-%m-%d %H:%M")

        if min_date <= date:
            return True
        else:
            logger.error(f"The date entered is less than {min_date_str}")
            return False

    except Exception as e:
        logger.error(e)
        return False


def entry_is_valid_date(entry: str, **kwargs) -> bool:
    """Check if the user has entered a date in the requested format"""
    min_date_str: str = kwargs.get("min_date_str", "1920-01-01")

    try:
        min_date = datetime.strptime(min_date_str, "%Y-%m-%d")
        date = datetime.strptime(entry, "%Y-%m-%d")
        if min_date <= date:
            return True
        else:
            logger.error(f"The date entered is less than {min_date_str}")
            return False

    except Exception as e:
        logger.error(e)
        return False


def entry_is_valid(entry: Optional[str], **kwargs) -> bool:
    """Check if the user has entered a value that meets each test criteria"""
    if entry == None:
        return False

    check_functions: Callable = kwargs.get("check_functions", [])
    title: str = kwargs.get("title", None)

    for function in check_functions:
        if not function(entry=entry, **kwargs):
            pause()
            clear_display()
            if title != None:
                display_message(title)
            return False
    return True


def get_valid_entry(input_function: Callable[[str], str], message: str, **kwargs) -> Union[str, int]:
    """Requests an entry as long as it does not pass all the requested tests"""
    default_value: Union[int, str] = kwargs.get("default_value", None)
    entry = None
    while not entry_is_valid(entry, **kwargs):
        entry = input_function(message)
        if entry == "" and default_value != None:
            return default_value
    return entry
