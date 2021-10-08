import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
chessdir = os.path.dirname(currentdir)
sys.path.append(chessdir)

from settings import PLAYERS_TABLE, TOURNAMENTS_TABLE

cls = lambda: os.system("cls")


def pause():
    programPause = input("\x1b[35mPress the <ENTER> key to continue...\x1b[0m")


from controllers.checks import check
#     unsorted_list = [(dictionary[field], dictionary) for dictionary in list_of_dict]
#     unsorted_list.sort()
#     sorted_list = [dictionary for (field_value, dictionary) in unsorted_list]
#     return sorted_list
from controllers.checks.check import (choice_is_valid, entry_belongs_list,
                                      entry_is_integer_under_max_value,
                                      entry_is_not_empty,
                                      entry_is_positive_integer,
                                      entry_is_valid, entry_is_valid_datetime,
                                      get_valid_entry)
from controllers.controller_tournament import TournamentController
from models import Match, Player, Tournament, Turn
from views.view_master import display_message, entry_request
from views.view_report import (display_menu_report,
                               display_menu_report_player_filter,
                               display_menu_report_tournament)

# def sort_by_field(list_of_dict, field):
#     """"""


def launch_report():
    choice = None
    handler = {
        "1": {
            "function": set_players_filter,
            "parameters": [
                Player().unserializing_players_list(PLAYERS_TABLE.table.all())
            ],
        },
        "2": {"function": Tournament().display_all_tournaments, "parameters": []},
        "3": {"function": report_tournament, "parameters": []},
    }
    while choice != "0":
        cls()
        choice = display_menu_report()
        if choice_is_valid(choice, handler):
            handler[choice]["function"](*handler[choice]["parameters"])


# players_list = Player().unserializing_players_list(PLAYERS_TABLE.table.all())


def set_players_filter(players_list):
    choice = None
    handler = {
        "1": "ranking",
        "2": "lastname",
    }
    while choice != "0":
        cls()
        choice = display_menu_report_player_filter()
        if choice_is_valid(choice, handler):
            Player().display_players(players_list, sort_field=handler[choice])
            pause()


def select_tournament():
    cls()
    display_message("\x1b[32m>>> Select a Tournament <<<\x1b[0m")
    name = get_valid_entry(
        input_fonction=entry_request,
        message="\x1b[35mPress Enter to not filter by name.\x1b[0m\n> Enter a tournament name: ",
        title="\x1b[32m>>> Load a Tournament <<<\x1b[0m",
    )
    location = get_valid_entry(
        input_fonction=entry_request,
        message="\x1b[35mPress Enter to not filter by location.\x1b[0m\n> Enter a tournament location: ",
        title="\x1b[32m>>> Load a Tournament <<<\x1b[0m",
    )
    results = TOURNAMENTS_TABLE.search_by_name_and_location(name, location)
    cls()
    display_message("\x1b[32m>>> Select a Tournament <<<\x1b[0m")
    if results != None and len(results) != 0:

        message = (
            f"\x1b[35mNumber of tournament found: {len(results)}\x1b[0m\n0: Cancel load"
        )
        i = 1
        for result in results:
            message += (
                f'\n{i}: {result["name"]}, {result["location"]}, {result["date"]}'
            )
            i += 1
        message += "\n\x1b[32m> Select a tournament: \x1b[0m"
        # print(len(results))
        tournament_selected = get_valid_entry(
            input_fonction=entry_request,
            message=message,
            check_functions=[entry_is_integer_under_max_value],
            max_value=len(results),
            title="\x1b[32m>>> Load a Tournament <<<\x1b[0m",
        )

        if tournament_selected == "0":
            print("cancel ok")  # temporaire
            pause()
            return None

        tournament = Tournament()
        tournament.unserializing(
            Match(),
            Turn(),
            Player(),
            results[int(tournament_selected) - 1],
        )
        return tournament

    return None


def report_tournament():
    tournament = select_tournament()

    if tournament == None:
        print("no tournament")
        pause()
        return None

    choice = None
    handler = {
        "1": {"function": set_players_filter, "parameters": [tournament.players]},
        "2": {
            "function": Turn().display_turns_without_match,
            "parameters": [tournament.turns],
        },
        "3": {
            "function": Match().display_only_matchs,
            "parameters": [tournament.turns],
        },
    }
    while choice != "0":
        cls()
        choice = display_menu_report_tournament()
        if choice_is_valid(choice, handler):
            handler[choice]["function"](*handler[choice]["parameters"])


if __name__ == "__main__":
    launch_report()

"""
    handler = {
            "1": {'function': display_menu_report_filter, 'parameters': [Player().unserializing_players_list(PLAYERS_TABLE.table.all())]},
            "2": {'function': launch_report, 'parameters': []},
        }
    return_value = handler[choice]['function'](*handler[choice]['parameters'])

    while choice != "0":
        cls()
        choice = display_menu_report()
        if choice_is_valid(choice, handler):
            handler[choice]['function'](*handler[choice]['parameters'])
"""
