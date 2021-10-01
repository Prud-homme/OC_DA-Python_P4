from datetime import datetime
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
chessdir = os.path.dirname(currentdir)
sys.path.append(chessdir)

from settings import PLAYERS_TABLE, TIME_CONTROL, TOURNAMENTS_TABLE, SCORE_VALUES
from models import Match, Player, Tournament, Turn
from database import Table
import views
from controllers.controller_master import get_valid_entry
from controllers.pair_generation import generate_pairs_swiss_system
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
        self.match = self.model_match()
        self.player = self.model_player()
        self.generated_matchs = None
        self.previous_matchs = None

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
            breakpoint()
            choice = entry_request(menu)
            if choice_is_valid(choice, handler):
                handler[choice]()

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
            self.table_tournaments,
            self.model_match(),
            self.model_turn(),
            self.model_player(),
        )
        self.previous_matchs = []
        self.resume_tournament()

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

            self.tournament.unserializing(
                self.model_match(),
                self.model_turn(),
                self.model_player(),
                results[int(tournament_selected) - 1],
            )

            self.previous_matchs = self.tournament.list_previous_matchs()
            self.resume_tournament()

        else:
            print("No tournament")  # temporaire
            return None

    def request_display_info(self):
        """afficher info d'un tournoi"""
        self.tournament.display()
        self.tournament.display_turns()
        self.tournament.display_players()

    def display_current_match(self):
        """affiche les matchs généré"""
        if self.turn == None:
            print("No turn in memory")
            return None
        print("Generated matchs:")
        message = self.match.display_matchs(self.generated_matchs)
        print(message)  # temporaire

    def start_a_turn(self):
        """demarer un nouveau tour"""
        if self.turn != None:
            print("Turn in memory")
            return None
        if len(self.tournament.turns) == self.tournament.turns_number:
            print("all turns defined")
            self.run()
            return None
        # name = get_valid_entry(
        #    input_fonction=entry_request,
        #    message="> Enter a turn name: ",
        #    check_functions=[check.entry_is_not_empty],
        # )
        name = f"Round {len(self.tournament.turns)+1}"
        self.turn = self.model_turn(name=name)

        if len(self.tournament.turns) == 0:
            self.generated_matchs = generate_pairs_swiss_system(
                self.tournament.players,
                rankings=self.tournament.load_rankings(),
            )
        else:
            self.generated_matchs = generate_pairs_swiss_system(
                self.tournament.players,
                scores=self.tournament.load_scores(),
                previous_matchs=self.previous_matchs,
            )
        self.previous_matchs.extend(self.generated_matchs)
        self.display_current_match()

    def complete_match(self):
        """entrer le score d'un match"""
        if self.turn == None:
            print("No turn in memory")
            return None
        elif len(self.turn.matchs) == len(self.generated_matchs):
            print("all matchs defined")
            return None
        self.display_current_match()
        match_selected = get_valid_entry(
            input_fonction=entry_request,
            message="> Select a Match: ",
            check_functions=[entry_is_integer_under_max_value],
            max_value=len(self.generated_matchs),
        )
        players_pair = self.generated_matchs[int(match_selected) - 1]
        if self.model_match().match_already_registered(players_pair, self.turn.matchs):
            print("Match already registered")
            return None

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
            else:
                print(
                    "Completed matchs:\n"
                    + message
                    + "\nPlease complete the other matchs before finishing the turn."
                )

        if len(self.turn.matchs) == len(self.generated_matchs):
            self.turn.stop_turn()
            self.tournament.add_turn(self.turn)
            self.turn = None
            self.tournament.update_in_database(
                self.table_tournaments,
                self.model_match(),
                self.model_turn(),
                self.model_player(),
            )

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
            choice = entry_request(menu)
            if choice_is_valid(choice, handler):
                handler[choice]()

    def resume_tournament(self):
        """reprendre ou non un tournoi en memoire en fonction de ces infos si elle sont complete ou non"""
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
