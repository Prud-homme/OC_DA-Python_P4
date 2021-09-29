from datetime import datetime

import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
chessdir = os.path.dirname(currentdir)
sys.path.append(chessdir)

# appdir = os.path.dirname(chessdir)
# sys.path.append(appdir)
# import chess.views

# from chess.settings import PLAYERS_TABLE, TIME_CONTROL, TOURNAMENTS_TABLE, SCORE_VALUES
# from chess.models import Match, Player, Tournament, Turn
# from chess.database import Table

from settings import PLAYERS_TABLE, TIME_CONTROL, TOURNAMENTS_TABLE, SCORE_VALUES
from models import Match, Player, Tournament, Turn
from database import Table

"""
from chess.views import (
    views_menu,
    views_match,
    views_player,
    views_tournament,
    views_turn,
)
"""
# from chess.views import menu as views_menu
# import chess.views as views
import views
from controllers.controller_master import get_valid_entry

# print(views.views_tournament)
from controllers.pair_generation import generate_pairs_swiss_system

# from chess.logger import logger
# import chess.check_entry as check_entry
# from controllers.pair_generation import generate_pairs_swiss_system
from logger import logger
from controllers.checks.check import (
    choice_is_valid,
    entry_is_not_empty,
    entry_is_positive_integer,
    entry_is_integer_under_max_value,
    entry_belongs_list,
    entry_is_valid_datetime,
    entry_is_valid,
)
from controllers.checks import check

from views.view_master import entry_request

from controllers.controller_player import append_players


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
        self.table_tournaments = kwargs.get("table_tournaments", TOURNAMENTS_TABLE)

        self.time_controls = kwargs.get("time_controls", TIME_CONTROL)
        self.score_values = kwargs.get("score_values", SCORE_VALUES)

        self.tournament = self.model_tournament()
        self.turn = None
        self.match = None
        self.player = self.model_player()
        self.generated_matchs = None

    #######################################################################################
    def run(self):
        """menu principal des tournoi"""
        menu = f"""---  Tournaments menu ---
1: New tournament
2: Load a tournament
3: Resume a tournament
0: Main menu
> Select an option: """
        choice = None
        handler = {
            "1": self.new_tournament,
            "2": self.load_tournament,
            "3": self.resume_tournament,
        }

        while choice != "0":
            #breakpoint()
            choice = entry_request(menu)
            if choice_is_valid(choice, handler):
                handler[choice]()

    ####################################################################################### ? erreur kwargs >>> kwargs=**kwargs

    def new_tournament(self):
        """creation d'un tournoi et ajout a la bdd"""
        name = get_valid_entry(
            input_fonction=entry_request,
            message="> Enter a tournament name: ",
            check_functions=[check.entry_is_not_empty],
        )
        location = get_valid_entry(
            input_fonction=entry_request,
            message="> Enter a tournament location: ",
            check_functions=[entry_is_not_empty],
        )
        date = get_valid_entry(
            input_fonction=entry_request,
            message="> Enter a tournament date (yyyy-mm-dd hh:mm): ",
            check_functions=[entry_is_valid_datetime],
        )

        description = get_valid_entry(
            input_fonction=entry_request,
            message="> Enter a tournament description: ",
        )

        time_control = get_valid_entry(
            input_fonction=entry_request,
            message=f'> Enter a time control ({", ".join(self.time_controls)}): ',
            check_functions=[entry_belongs_list],
            allowed_list=self.time_controls,
        )

        turns_number = get_valid_entry(
            input_fonction=entry_request,
            message="> Enter a number of turns (press Enter for 4 turns): ",
            check_functions=[entry_is_positive_integer],
            default_value=4,
        )
        players_number = get_valid_entry(
            input_fonction=entry_request,
            message="> Enter a number of players (press Enter for 8 players): ",
            check_functions=[entry_is_positive_integer],
            default_value=8,
        )
        self.tournament = self.model_tournament(
            name=name,
            location=location,
            date=date,
            description=description,
            time_control=time_control,
            turns_number=int(turns_number),
            players_number=int(players_number),
        )
        append_players(self.tournament, self.model_player, self.table_players)
        self.tournament.insert_in_database(
            self.table_tournaments, self.model_match(), self.model_turn()
        )
        self.resume_tournament()

    #######################################################################################

    def load_tournament(self):
        """chargement d'un tournoi depuis bdd"""
        if self.table_tournaments == None:
            return None

        name = get_valid_entry(
            input_fonction=entry_request,
            message="Press Enter to not filter by name.\n> Enter a tournament name: ",
        )
        location = get_valid_entry(
            input_fonction=entry_request,
            message="Press Enter to not filter by location.\n> Enter a tournament location: ",
        )
        results = self.table_tournaments.search_by_name_and_location(name, location)

        if results != None and len(results) != 0:

            message = f"Number of tournament found: {len(results)}"
            i = 1
            for result in results:
                message += (
                    f'\n{i}: {result["name"]}, {result["location"]}, {result["date"]}'
                )
                i += 1
            message += "\n> Select a tournament: "
            print(len(results))
            tournament_selected = get_valid_entry(
                input_fonction=entry_request,
                message=message,
                check_functions=[entry_is_integer_under_max_value],
                max_value=len(results),
            )
            ###breakpoint()
            # if tournament_selected != None:
            self.tournament.unserializing(
                self.model_match(),
                self.model_turn(),
                self.model_player(),
                results[int(tournament_selected) - 1],
            )
            ###breakpoint()
            self.resume_tournament()

        else:
            print("No tournament")  # temporaire
            return None

    #######################################################################################
    def request_display_info(self):
        """afficher info d'un tournoi"""
        self.tournament.display()
        self.tournament.display_turns()
        self.tournament.display_players()

        # for player_id in self.tournament.players:
        #     self.player.load_from_database_with_id(self.table_players, player_id)
        #     self.player.display(player_id)
        # self.player = self.model_player()

    def display_current_match(self):
        """affiche les matchs généré"""
        if self.turn == None:
            print("No turn in memory")
            return None
        print("Generated matchs:")
        message = self.turn.display_matchs(
            self.table_players, self.model_player(), self.generated_matchs
        )
        print(message)  # temporaire

    def start_a_turn(self):
        """demarer un nouveau tour"""
        # start
        ##breakpoint()
        if self.turn != None:
            print("Turn in memory")
            return None
        name = get_valid_entry(
            input_fonction=entry_request,
            message="> Enter a turn name: ",
            check_functions=[check.entry_is_not_empty],
        )
        self.turn = self.model_turn(name=name)
        if len(self.tournament.turns) == 0:
            self.generated_matchs = generate_pairs_swiss_system(
                self.tournament.players,
                rankings=self.tournament.load_rankings(self.table_players),
            )
        else:
            self.generated_matchs = generate_pairs_swiss_system(
                self.tournament.players, scores=self.tournament.load_scores()
            )
        self.display_current_match()

    def complete_match(self):
        """entrer le score d'un match"""
        if self.turn == None:
            print("No turn in memory")
            return None
        self.display_current_match()
        match_selected = get_valid_entry(
            input_fonction=entry_request,
            message="> Select a Match: ",
            check_functions=[entry_is_integer_under_max_value],
            max_value=len(self.generated_matchs),
        )
        match = []
        for player_id in self.generated_matchs[int(match_selected) - 1]:
            player_name = self.model_player().get_player_name_with_id(
                self.table_players, player_id
            )
            player_score = get_valid_entry(
                input_fonction=entry_request,
                message=f"> Enter a score for [{player_id}] {player_name} (0, 1 or 0.5): ",
                check_functions=[entry_belongs_list],
                allowed_list=["0", "1", "0.5"],
            )
            match.append([player_id, float(player_score)])
        # breakpoint()
        self.turn.add_match(self.model_match(match=tuple(match)))
        # breakpoint()

    def complete_turn(self):
        """terminer un tour"""
        if self.turn == None:
            print("No turn in memory")
            return None
        if len(self.turn.matchs) != len(self.generated_matchs):
            message = self.turn.display_matchs(
                self.table_players,
                self.model_player(),
                self.model_match().list_players(self.turn.matchs),
                display_number=False,
            )
            if message == None:
                print(
                    "No match is completed.\nPlease complete the other matchs before finishing the turn."
                )
            else:
                print(
                    "Completed matchs:\n"
                    + message
                    + "\nPlease complete the other matchs before finishing the turn."
                )
            self.complete_match()

        if len(self.turn.matchs) == len(self.generated_matchs):
            # breakpoint()
            self.turn.stop_turn()
            self.tournament.add_turn(self.turn)
            # breakpoint()
            self.turn = None
            self.tournament.serializing(self.model_match(), self.model_turn())

    def valid_resume(self):
        """menu pour reprendre un tournoi qui a tout le nécéssaire de définit"""
        choice = None
        handler = {
            "1": self.request_display_info,
            "2": self.start_a_turn,
            "3": self.display_current_match,
            "4": self.complete_match,
            "5": self.complete_turn,
        }
        menu = f"""--- Tournament: {self.tournament.name} ---
1: View tournament informations
2: Start a turn
3: Current matchs
4: Complete a match
5: Complete a turn
0: Return to tournament menu
> Select an option: """
        while choice != "0":
            breakpoint()
            choice = entry_request(menu)
            if choice_is_valid(choice, handler):
                handler[choice]()

    def resume_tournament(self):
        """reprendre ou non un tournoi en memoire en fonction de ces infos si elle sont complete ou non"""
        ##breakpoint()
        if (
            self.tournament.attributes_are_not_none()
            and self.tournament.all_players_defined()
        ):
            self.valid_resume()

        elif (
            self.tournament.attributes_are_not_none()
            and not self.tournament.all_players_defined()
        ):
            print("Need more players")  # temporaire
            append_players(self.tournament, self.model_player, self.table_players)
        else:
            print("no resume")  # temporaire


if __name__ == "__main__":
    controller = TournamentController()
    controller.run()
