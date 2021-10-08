import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(currentdir)
# chessdir = os.path.dirname(currentdir)
# sys.path.append(chessdir)

# from logger import logger

from checks import check


def get_valid_entry(input_fonction, message, **kwargs):
    """redemander une saisie tant qu'elle ne correspond pas a certain critere"""
    default_value = kwargs.get("default_value", None)
    entry = None
    while entry == None or not check.entry_is_valid(entry, **kwargs):
        entry = input_fonction(message)
        if entry == "" and default_value != None:
            return default_value
    return entry


if __name__ == "__main__":
    get_valid_entry(
        input_fonction=input,
        message="Enter a integer value: ",
        check_functions=[check.entry_is_positive_integer],
    )

    get_valid_entry(
        input_fonction=input,
        message="Enter something: ",
        check_functions=[check.entry_is_not_empty],
    )

    get_valid_entry(
        input_fonction=input,
        message="Enter a positive integer under 100: ",
        check_functions=[
            check.entry_is_positive_integer,
            check.entry_is_integer_under_max_value,
        ],
        max_value=100,
    )

    get_valid_entry(
        input_fonction=input,
        message="Enter a value (azerty or qwerty): ",
        check_functions=[check.entry_belongs_list],
        allowed_list=["azerty", "qwerty"],
    )

    get_valid_entry(
        input_fonction=input,
        message="Enter a date (yyyy-mm-dd hh:mm): ",
        check_functions=[check.entry_is_valid_date],
    )
