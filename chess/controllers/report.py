from __future__ import annotations

from typing import Optional

from ..logger import logger
from ..models import Player, Tournament
from ..settings import PLAYERS_TABLE, TOURNAMENTS_TABLE
from ..utils import autopause, clear_display, pause
from ..views import (
    display_menu_report,
    display_menu_report_player_filter,
    display_menu_report_tournament,
    display_message,
    entry_request,
)
from .checks import choice_is_valid, entry_is_integer_under_max_value, get_valid_entry


def launch_report() -> None:
    """
    Selection of a choice from the report menu.
    After a choice among the selection, it launches the function associated
    with this choice
    """
    choice = None
    handler = {
        "1": set_players_filter,
        "2": Tournament().display_all_tournaments,
        "3": report_tournament,
    }
    sort_field = None
    while choice != "0":
        clear_display()
        choice = display_menu_report()
        if choice == "1":
            sort_field = handler[choice]()
            if sort_field is not None:
                clear_display()
                message = Player().display_players(
                    Player().unserializing_players_list(PLAYERS_TABLE.table.all()),
                    sort_field=sort_field,
                )
                display_message(message)
                pause()
        elif choice == "2":
            clear_display()
            display_message(handler[choice]())
            pause()
        elif choice == "3":
            handler[choice]()


def set_players_filter() -> str:
    """Selection of the sorting order by the user"""
    choice = None
    handler = {
        "1": "ranking",
        "2": "lastname",
    }
    while choice != "0":
        clear_display()
        choice = display_menu_report_player_filter()
        if choice_is_valid(choice, handler):
            return handler[choice]


def select_tournament() -> Optional[Tournament]:
    """
    Search for a tournament in the database
    The user can choose a tournament from the list found if it is not empty
    """
    clear_display()
    display_message("\x1b[32m♟️ Select a Tournament ♟️\x1b[0m")
    name = get_valid_entry(
        input_function=entry_request,
        message="\x1b[35mPress Enter to not filter by name.\x1b[0m\n> Enter a tournament name: ",
        title="\x1b[32m♟️ Load a Tournament ♟️\x1b[0m",
    )
    location = get_valid_entry(
        input_function=entry_request,
        message="\x1b[35mPress Enter to not filter by location.\x1b[0m\n> Enter a tournament location: ",
        title="\x1b[32m♟️ Load a Tournament ♟️\x1b[0m",
    )
    results = TOURNAMENTS_TABLE.search_by_name_and_location(name, location)

    if results is not None and len(results) != 0:

        message = (
            f"\x1b[35mNumber of tournament found: {len(results)}\x1b[0m\n0: Cancel load"
        )
        i = 1
        tournament = Tournament()
        for result in results:
            tournament.unserializing(result)
            message += f"""\n{i}: {tournament.name}, {tournament.location},
    {" and ".join([f"{key} on {value}" for key, value in tournament.date.items()])}"""
            i += 1
        message += "\n\x1b[32m> Select a tournament: \x1b[0m"
        tournament_selected = get_valid_entry(
            input_function=entry_request,
            message=message,
            check_functions=[entry_is_integer_under_max_value],
            max_value=len(results),
            title="\x1b[32m♟️ Load a Tournament ♟️\x1b[0m",
        )
        if tournament_selected == "0":
            logger.info("Canceled load.")
            autopause()
            return None
        tournament = Tournament()
        tournament.unserializing(results[int(tournament_selected) - 1])
        return tournament
    return None


def report_tournament() -> None:
    """
    Retrieves the tournament selected via the function select_tournament()
    Selection of a choice from the report menu for the tournament.
    After a choice among the selection, it launches the function associated
    with this choice
    """
    tournament = select_tournament()

    if tournament is None:
        logger.info("No tournament selected")
        autopause()
        return None

    choice = None
    handler = {
        "1": set_players_filter,
        "2": tournament.display_turns_without_match,
        "3": tournament.display_only_matches,
        "4": tournament.display_final_ranking,
    }

    while choice != "0":
        sort_field = None
        message = None
        clear_display()
        choice = display_menu_report_tournament()

        if choice == "1":
            sort_field = handler[choice]()
            if sort_field is not None:
                message = Player().display_players(
                    tournament.players, sort_field=sort_field
                )
        elif choice in ["2", "3", "4"]:
            message = handler[choice]()

        if message is not None:
            clear_display()
            display_message(message)
            pause()
