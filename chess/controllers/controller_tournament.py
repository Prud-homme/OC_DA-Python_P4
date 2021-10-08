import os
import sys
from datetime import datetime

currentdir = os.path.dirname(os.path.realpath(__file__))
chessdir = os.path.dirname(currentdir)
sys.path.append(chessdir)

from logger import logger

cls = lambda: os.system("cls")


def pause():
    programPause = input("\x1b[35mPress the <ENTER> key to continue...\x1b[0m")


import views
from controllers.checks import check
from controllers.checks.check import (choice_is_valid, entry_belongs_list,
                                      entry_is_integer_under_max_value,
                                      entry_is_not_empty,
                                      entry_is_positive_integer,
                                      entry_is_valid, entry_is_valid_datetime,
                                      get_valid_entry)
from controllers.controller_player import get_player
# from controllers.controller_master import get_valid_entry
from controllers.pair_generation import generate_pairs_swiss_system
from database import Table
from models import Match, Player, Tournament, Turn
from settings import (PLAYERS_TABLE, SCORE_VALUES, TIME_CONTROL,
                      TOURNAMENTS_TABLE)
from views.view_master import display_message, entry_request
from views.view_tournament import (display_menu_tournament_complete,
                                   display_menu_tournament_lack_players,
                                   display_menu_tournament_main,
                                   display_menu_tournament_resume)


class TournamentController:
    def __init__(self, **kwargs):
        # models
        self.model_tournament = kwargs.get("model_tournament", Tournament)
        self.model_turn = kwargs.get("model_turn", Turn)
        self.model_match = kwargs.get("model_match", Match)
        self.model_player = kwargs.get("model_player", Player)

        self.database_table = kwargs.get("database_table", Table)

        # views
        # self.views = kwargs.get("views", views)
        self.views_menu = kwargs.get("views_menu", views.view_menu)
        self.views_tournament = kwargs.get("views_tournament", views.view_tournament)
        self.views_turn = kwargs.get("views_turn", views.view_turn)
        self.views_match = kwargs.get("views_match", views.view_match)
        self.views_player = kwargs.get("views_player", views.view_player)

        self.table_players = kwargs.get("table_players", PLAYERS_TABLE)
        # self.table_tournaments = kwargs.get("table_tournaments", TOURNAMENTS_TABLE)

        self.time_controls = kwargs.get("time_controls", TIME_CONTROL)
        self.score_values = kwargs.get("score_values", SCORE_VALUES)

        self.tournament = self.model_tournament()
        self.turn = None
        self.match = self.model_match()
        self.player = self.model_player()
        self.generated_matchs = None
        self.previous_matchs = None

    def run(self):
        """menu principal des tournoi"""

        choice = None
        handler = {
            "1": self.new_tournament,
            "2": self.load_tournament,
            "3": self.resume_tournament,
        }
        while choice != "0":
            cls()
            choice = display_menu_tournament_main()
            if choice_is_valid(choice, handler):
                handler[choice]()

    def new_tournament(self):
        """creation d'un tournoi et ajout a la bdd"""
        cls()
        display_message("\x1b[32m>>> Create a Tournament <<<\x1b[0m")
        name = get_valid_entry(
            input_fonction=entry_request,
            message="> Enter a tournament name: ",
            check_functions=[check.entry_is_not_empty],
            title="\x1b[32m>>> Create a Tournament <<<\x1b[0m",
        )
        location = get_valid_entry(
            input_fonction=entry_request,
            message="> Enter a tournament location: ",
            check_functions=[entry_is_not_empty],
            title="\x1b[32m>>> Create a Tournament <<<\x1b[0m",
        )

        date_list = []
        choice = None
        while choice != "n":
            date = get_valid_entry(
                input_fonction=entry_request,
                message="> Enter a tournament date (yyyy-mm-dd hh:mm): ",
                check_functions=[entry_is_valid_datetime],
                min_date_str="2000-01-01 00:00",
                title="\x1b[32m>>> Create a Tournament <<<\x1b[0m",
            )
            date_list.append(date)

            choice = get_valid_entry(
                input_fonction=entry_request,
                message=f"> Enter a new date (y, n): ",
                check_functions=[entry_belongs_list],
                allowed_list=["y", "n"],
                title="\x1b[32m>>> Create a Tournament <<<\x1b[0m",
            )

        description = get_valid_entry(
            input_fonction=entry_request,
            message="> Enter a tournament description: ",
            title="\x1b[32m>>> Create a Tournament <<<\x1b[0m",
        )

        time_control = get_valid_entry(
            input_fonction=entry_request,
            message=f'> Enter a time control ({", ".join(self.time_controls)}): ',
            check_functions=[entry_belongs_list],
            allowed_list=self.time_controls,
            title="\x1b[32m>>> Create a Tournament <<<\x1b[0m",
        )

        turns_number = get_valid_entry(
            input_fonction=entry_request,
            message="> Enter a number of turns (press Enter for 4 turns): ",
            check_functions=[entry_is_positive_integer],
            default_value=4,
            title="\x1b[32m>>> Create a Tournament <<<\x1b[0m",
        )
        players_number = get_valid_entry(
            input_fonction=entry_request,
            message="> Enter a number of players (press Enter for 8 players): ",
            check_functions=[entry_is_positive_integer],
            default_value=8,
            title="\x1b[32m>>> Create a Tournament <<<\x1b[0m",
        )
        self.tournament = self.model_tournament(
            name=name,
            location=location,
            date=date_list,
            description=description,
            time_control=time_control,
            turns_number=int(turns_number),
            players_number=int(players_number),
        )
        continue_add = None
        while continue_add == "y":
            player = get_player()
            if player != None:
                self.tournament.add_player(player)
                continue_add = get_valid_entry(
                    input_fonction=entry_request,
                    message=f"> Want to add another player ? (y, n): ",
                    check_functions=[entry_belongs_list],
                    allowed_list=["y", "n"],
                )
            else:
                continue_add = "n"

        # self.tournament.add_player(get_player())#self.tournament, self.model_player, self.table_players)
        self.tournament.insert_in_database(
            self.model_match(),
            self.model_turn(),
            self.model_player(),
        )
        self.previous_matchs = []
        self.resume_tournament()

    def load_tournament(self):
        """chargement d'un tournoi depuis bdd"""
        # if self.table_tournaments == None:
        #    return None
        cls()
        display_message("\x1b[32m>>> Load a Tournament <<<\x1b[0m")
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
        display_message("\x1b[32m>>> Load a Tournament <<<\x1b[0m")
        if results != None and len(results) != 0:

            message = f"\x1b[35mNumber of tournament found: {len(results)}\x1b[0m\n0: Cancel load"
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

            self.tournament.unserializing(
                self.model_match(),
                self.model_turn(),
                self.model_player(),
                results[int(tournament_selected) - 1],
            )
            self.previous_matchs = self.tournament.list_previous_matchs()
            pause()
            self.resume_tournament()

        else:
            print("No tournament")  # temporaire
            pause()
            return None

    # def request_display_info(self, **kwargs):
    #     """afficher info d'un tournoi"""
    #     cls()
    #     self.tournament.display()
    #     self.tournament.display_turns()
    #     self.tournament.display_players()
    #     pause()
    #     return None

    def display_current_match(self, no_number=True):
        """affiche les matchs généré"""
        cls()
        if self.turn == None:
            print("No turn in memory")
            return None
        display_message(
            "\x1b[32m>>> Generated matchs <<<\x1b[0m\n"
            + self.match.display_matchs(self.generated_matchs, no_number=no_number)
        )
        if no_number:
            pause()

    def start_a_turn(self):
        """demarer un nouveau tour"""
        cls()
        display_message("\x1b[32m>>> New turn <<<\x1b[0m")
        if self.turn != None:
            print("Turn in memory")
            return None
        if len(self.tournament.turns) == self.tournament.turns_number:
            print("all turns defined")
            return None
        # name = get_valid_entry(
        #    input_fonction=entry_request,
        #    message="> Enter a turn name: ",
        #    check_functions=[check.entry_is_not_empty],
        # )
        name = f"Round {len(self.tournament.turns)+1}"
        self.turn = self.model_turn(name=name)

        if len(self.tournament.turns) == 0:
            self.generated_matchs = self.turn.generate_pairs_swiss_system(
                self.tournament.players,
                rankings=self.tournament.load_rankings(),
            )
        else:
            self.generated_matchs = self.turn.generate_pairs_swiss_system(
                self.tournament.players,
                scores=self.tournament.load_scores(),
                previous_matchs=self.previous_matchs,
            )
        self.previous_matchs.extend(self.generated_matchs)
        self.display_current_match()
        # pause()

    def complete_match(self):
        """entrer le score d'un match"""
        cls()
        display_message("\x1b[32m>>> Complete match <<<\x1b[0m")
        if self.turn == None:
            logger.info("No turn in memory")
            pause()
            return None
        elif len(self.turn.matchs) == len(self.generated_matchs):
            print("all matchs defined")
            pause()
            return None
        self.display_current_match(no_number=False)
        match_selected = get_valid_entry(
            input_fonction=entry_request,
            message="> Select a Match: ",
            check_functions=[entry_is_integer_under_max_value],
            max_value=len(self.generated_matchs),
            title="\x1b[32m>>> Generated matchs <<<\x1b[0m\n"
            + self.match.display_matchs(self.generated_matchs, no_number=False),
        )
        players_pair = self.generated_matchs[int(match_selected) - 1]
        print(players_pair)
        pause()
        if self.model_match().match_already_registered(players_pair, self.turn.matchs):
            print("Match already registered")
            return None

        # confirm_result = None
        # while confirm_result != 'y':
        print(players_pair)
        pause()

        match = []
        for player in players_pair:

            player_score = get_valid_entry(
                input_fonction=entry_request,
                message=f"> Enter a score for {' '.join((player.firstname, player.lastname))} (0, 1 or 0.5): ",
                check_functions=[entry_belongs_list],
                allowed_list=["0", "1", "0.5"],
            )
            match.append([player, float(player_score)])
        self.turn.add_match(self.model_match(match=tuple(match)))

    def complete_turn(self):
        """terminer un tour"""
        cls()
        display_message("\x1b[32m>>> Complete turn <<<\x1b[0m")
        if self.turn == None:
            print("No turn in memory")
            return None
        if len(self.turn.matchs) != len(self.generated_matchs):
            message = self.model_match().display_matchs(
                self.turn.list_players_pair_complete(), view_complete=True
            )
            if message == None:
                print(
                    "No match is completed.\nPlease complete the other matchs before finishing the turn."
                )
                pause()
            else:
                print(
                    "Completed matchs:\n"
                    + message
                    + "\nPlease complete the other matchs before finishing the turn."
                )
                pause()

        if len(self.turn.matchs) == len(self.generated_matchs):
            self.turn.stop_turn()
            self.tournament.add_turn(self.turn)
            self.turn = None
            # self.tournament.update_in_database(
            #    self.model_match(),
            #    self.model_turn(),
            #    self.model_player(),
            # )
            print("all matchs registered ")
            self.save_tournament()
            pause()

    def valid_resume(self):
        """menu pour reprendre un tournoi qui a tout le nécéssaire de définit"""

        choice = None
        handler = {
            "1": self.tournament.display_all_info,
            "2": self.start_a_turn,
            "3": self.display_current_match,
            "4": self.complete_match,
            "5": self.complete_turn,
        }
        while (
            choice != "0" and len(self.tournament.turns) != self.tournament.turns_number
        ):
            cls()
            choice = display_menu_tournament_resume()
            if choice_is_valid(choice, handler):
                handler[choice]()
        if len(self.tournament.turns) == self.tournament.turns_number:
            print("all turns defined")
            # self.save_tournament()
        return "0"

    # def get_player(self):
    #    return get_player(self.tournament, self.model_player, self.table_players)

    def lack_player(self):
        """"""
        choice = None
        handler = {
            "1": {
                "function": self.tournament.display_all_info,
                "parameters": [self.model_player(), self.model_turn()],
            },
            "2": {"function": get_player, "parameters": []},
        }
        while (
            choice != "0"
            and len(self.tournament.players) != self.tournament.players_number
        ):
            cls()
            choice = display_menu_tournament_lack_players()
            if choice_is_valid(choice, handler):
                return_value = handler[choice]["function"](
                    *handler[choice]["parameters"]
                )
                self.tournament.add_player(return_value)
        if len(self.tournament.players) == self.tournament.players_number:
            print("all player defined")
            # self.save_tournament()
            # self.resume_tournament()

        return "0"

    def tournament_is_complete(self):
        """"""
        choice = None
        handler = {
            "1": {
                "function": self.tournament.display_all_info,
                "parameters": [self.model_player(), self.model_turn()],
            },
            "2": {"function": get_player, "parameters": []},
        }
        while choice != "0":
            cls()
            choice = display_menu_tournament_lack_players()
            if choice_is_valid(choice, handler):
                return_value = handler[choice]["function"](
                    *handler[choice]["parameters"]
                )
        return "0"

    def resume_tournament(self):
        """reprendre ou non un tournoi en memoire en fonction de ces infos si elle sont complete ou non"""

        if not self.tournament.attributes_are_not_none():
            print("undefined")
            pause()
            return None
        choice = None
        while choice != "0":
            if (
                self.tournament.all_players_defined()
                and len(self.tournament.turns) == self.tournament.turns_number
            ):
                choice = self.tournament_is_complete()

            elif self.tournament.all_players_defined():

                choice = self.valid_resume()
                self.save_tournament()

            elif not self.tournament.all_players_defined():
                print("Need more players")  # temporaire
                choice = self.lack_player()
                self.save_tournament()
            else:
                print("no resume")  # temporaire
                pause()
        # self.tournament.update_in_database(
        #    self.model_match(),
        #    self.model_turn(),
        #    self.model_player(),
        # )

    def save_tournament(self, title=None):
        answer = get_valid_entry(
            input_fonction=entry_request,
            message=f"> Confirm want to save ? (y, n): ",
            check_functions=[entry_belongs_list],
            allowed_list=["y", "n"],
            title=title,
        )
        if answer == "y":
            self.tournament.update_in_database(
                self.model_match(),
                self.model_turn(),
                self.model_player(),
            )


if __name__ == "__main__":
    controller = TournamentController()
    controller.run()
