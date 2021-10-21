import os
import sys
from datetime import datetime
cls = lambda: os.system("cls")
currentdir = os.path.dirname(os.path.realpath(__file__))
chessdir = os.path.dirname(currentdir)
sys.path.append(chessdir)


def pause():
    programPause = input("\x1b[35mPress the <ENTER> key to continue...\x1b[0m")


from logger import logger
from views.view_master import display_message, entry_request


def choice_is_valid(choice, handler):
    """verifier si saisie existe"""
    for key, value in handler.items():
        if choice == key:
            return True
    return False


def entry_is_not_empty(entry, **kwargs):
    """verifier saisie soit non vide"""
    if len(entry) > 0:
        return True
    else:
        logger.error("Entry is empty")
        return False


def entry_is_positive_integer(entry, **kwargs):
    """verifier saisie est un entier strictement plus grand que 0"""
    if entry.isdecimal() and int(entry) >= 0:
        return True
    else:
        logger.error("Entry is not a positive integer")
        return False


def entry_is_integer_under_max_value(entry, **kwargs):
    """verifier saisie est un entier strictement positif inferieur a une valeur"""
    max_value = kwargs.get("max_value", None)
    if max_value == None:
        if entry.isdecimal() and int(entry) >= 0:
            return True
        else:
            logger.error("Entry is not a positive integer")

    if entry.isdecimal() and int(entry) <= max_value and int(entry) >= 0:
        return True
    else:
        logger.error(f"Entry is not a positive interger under {max_value}")
        return False


def entry_belongs_list(entry, **kwargs):
    """verifier saisie est parmis une liste donnée"""
    allowed_list = kwargs.get("allowed_list", None)
    # if allowed_list == None:
    #    return True
    if (
        allowed_list == None
        or entry.lower() in allowed_list
        or entry.upper() in allowed_list
    ):
        return True
    else:
        logger.error(f"""Entry is not in {' '.join(allowed_list)}""")
        return False


def entry_is_valid_datetime(entry, **kwargs):
    """saisie est une datetime"""
    min_date_str = kwargs.get("min_date_str", "1582-10-15 00:00")
    # if entry == None:
    #    return False
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


def entry_is_valid_date(entry, **kwargs):
    """saisie est une date"""
    min_date_str = kwargs.get("min_date_str", "1950-01-01")
    # if entry == None:
    #    return False
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


def entry_is_valid(entry, **kwargs):
    """verifier la saisie sur l'ensemble des criteres"""
    check_functions = kwargs.get("check_functions", [])
    title = kwargs.get("title", None)
    for function in check_functions:
        if not function(entry=entry, **kwargs):
            pause()
            cls()
            if title != None:
                print(title)
            return False
    return True


def get_valid_entry(input_fonction, message, **kwargs):
    """redemander une saisie tant qu'elle ne correspond pas a certain critere"""
    default_value = kwargs.get("default_value", None)
    # clear_display = kwargs.get("clear_display", None)
    entry = input_fonction(message)
    if entry == "" and default_value != None:
        return default_value
    while not entry_is_valid(entry, **kwargs):
        # if clear_display != None:
        #    clear_display()
        entry = input_fonction(message)
        if entry == "" and default_value != None:
            return default_value
    return entry
