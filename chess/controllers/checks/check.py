from datetime import datetime


def choice_is_valid(choice, handler):
    """verifier si saisie existe"""
    for key, value in handler.items():
        if choice == key:
            return True
    return False


def entry_is_not_empty(entry, **kwargs):
    """verifier saisie soit non vide"""
    try:
        return len(entry) > 0
    except:
        return False


def entry_is_positive_integer(entry, **kwargs):
    """verifier saisie est un entier strictement plus grand que 0"""
    try:
        return entry.isdecimal() and int(entry) > 0
    except:
        return False


def entry_is_integer_under_max_value(entry, **kwargs):
    """verifier saisie est un entier strictement positif inferieur a une valeur"""
    max_value = kwargs.get("max_value", None)
    if max_value == None:
        return entry.isdecimal() and int(entry) > 0
    try:
        return entry.isdecimal() and int(entry) <= max_value and int(entry) > 0
    except:
        return False


def entry_belongs_list(entry, **kwargs):
    """verifier saisie est parmis une liste donnée"""
    allowed_list = kwargs.get("allowed_list", None)
    if allowed_list == None:
        return True
    try:
        return entry.lower() in allowed_list or entry.upper() in allowed_list
    except:
        return False


def entry_is_valid_datetime(entry, **kwargs):
    """saisie est une datetime"""
    if entry == None:
        return False
    try:
        date = datetime.strptime(entry, "%Y-%m-%d %H:%M")
        return True
    except Exception as e:
        print(e)  # temporaire
        return False


def entry_is_valid_date(entry, **kwargs):
    """saisie est une date"""
    if entry == None:
        return False
    try:
        date = datetime.strptime(entry, "%Y-%m-%d")
        return True
    except Exception as e:
        print(e)  # temporaire
        return False


def entry_is_valid(entry, **kwargs):
    """verifier la saisie sur l'ensemble des criteres"""
    check_functions = kwargs.get("check_functions", [])
    for function in check_functions:
        if not function(entry=entry, **kwargs):
            return False
    return True
