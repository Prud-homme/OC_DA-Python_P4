from __future__ import annotations

from typing import Optional

from ..logger import logger
from ..models import Player
from ..settings import PLAYERS_TABLE
from ..utils import autopause, clear_display
from ..views import display_menu_add_player, display_message, entry_request
from .checks import (
    choice_is_valid,
    entry_belongs_list,
    entry_is_integer_under_max_value,
    entry_is_not_empty,
    entry_is_valid_date,
    get_valid_entry,
)


def search_player() -> Optional[Player]:
    """
    The function searches the player database for players matching the entered data
    (firstname and lastname).
    If there are results, the user can select a player from the list and
    the function will return the player instance of this player.
    Returns None if no player is found in the database.
    """
    clear_display()
    title = "\x1b[32m♟️ Search a player ♟️\x1b[0m"
    display_message(title)

    firstname = get_valid_entry(
        input_function=entry_request,
        message="\x1b[35mPress Enter to not filter by first name.\x1b[0m\n> Enter a first name: ",
    )
    lastname = get_valid_entry(
        input_function=entry_request,
        message="\x1b[35mPress Enter to not filter by last name.\x1b[0m\n> Enter a last name: ",
    )
    results = PLAYERS_TABLE.search_by_first_and_last_name(firstname, lastname)

    message = Player().display_players_choice(results)
    if message is not None:
        player_selected = get_valid_entry(
            input_function=entry_request,
            message=message,
            check_functions=[entry_is_integer_under_max_value],
            max_value=len(results),
            title=title,
        )
        if player_selected == "0":
            logger.info("Research cancelled with success.")
            autopause()
            return None
        player_serial_data = results[int(player_selected) - 1]
        player = Player(**player_serial_data)

        return player

    else:
        logger.info("No players were found.")
        autopause()
        return None


def create_player_firstname(title: str) -> str:
    """Requests the entry of the player's firstname for the creation of a player"""
    firstname = get_valid_entry(
        input_function=entry_request,
        message="> Enter a first name: ",
        check_functions=[entry_is_not_empty],
        title=title,
    )
    return firstname


def create_player_lastname(title: str) -> str:
    """Requests the entry of the player's lastname for the creation of a player"""
    lastname = get_valid_entry(
        input_function=entry_request,
        message="> Enter a last name: ",
        check_functions=[entry_is_not_empty],
        title=title,
    )
    return lastname


def create_player_birthdate(title: str) -> str:
    """Requests the entry of the player's birthdate for the creation of a player"""
    birthdate = get_valid_entry(
        input_function=entry_request,
        message="> Enter a birth date (yyyy-mm-dd): ",
        check_functions=[entry_is_valid_date],
        title=title,
    )
    return birthdate


def create_player_gender(title: str) -> str:
    """Requests the entry of the player's gender for the creation of a player"""
    gender = get_valid_entry(
        input_function=entry_request,
        message="> Enter a gender (M/F): ",
        check_functions=[entry_belongs_list],
        allowed_list=["M", "F"],
        title=title,
    )
    return gender


def create_player_ranking(title: str) -> str:
    """Requests the entry of the player's ranking for the creation of a player"""
    ranking = get_valid_entry(
        input_function=entry_request,
        message="> Enter a ranking: ",
        check_functions=[entry_is_integer_under_max_value],
        title=title,
    )
    return int(ranking)


def create_player() -> Optional[Player]:
    """
    Retrieve the information entered to create the player instance
    and insert it into the player database.
    Return the player instance.
    """
    clear_display()
    title = "\x1b[32m♟️ Create a player ♟️\x1b[0m"
    display_message(title)
    firstname = create_player_firstname(title)
    lastname = create_player_lastname(title)
    birthdate = create_player_birthdate(title)
    gender = create_player_gender(title)
    ranking = create_player_ranking(title)

    player = Player(
        firstname=firstname,
        lastname=lastname,
        birthdate=birthdate,
        gender=gender,
        ranking=ranking,
    )

    player.insert_in_database()
    return player


def get_player() -> Optional[Player]:
    """
    Retrieve a player's instance from a search in the player database
    or after creating a new player.
    Return the player instance or None if the user chooses not to add a player.
    """
    clear_display()
    choice = None
    handler = {
        "1": search_player,
        "2": create_player,
    }
    while choice != "0":
        clear_display()
        choice = display_menu_add_player()
        if choice_is_valid(choice, handler):
            player = handler[choice]()
            return player
    return None


def edit_player_ranking() -> None:
    """
    Retrieves the player selected via the function search_player()
    The user enters the new ranking and the user is updated in the database
    """
    player = search_player()
    if player is None:
        logger.info("No player selected")
        autopause()
        return None

    ranking = create_player_ranking(title="\x1b[32m♟️ Edit a player rank ♟️\x1b[0m")
    player.ranking = ranking
    player.update_in_database()
