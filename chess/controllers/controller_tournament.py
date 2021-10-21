import os
import sys
from datetime import datetime

currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(currentdir)
chessdir = os.path.dirname(currentdir)
sys.path.append(chessdir)

from logger import logger
from utils import cls, pause


#import views
#from controllers.checks import check
#from controllers.checks.check import (choice_is_valid, entry_belongs_list,
from checks.check import (choice_is_valid, entry_belongs_list,
                          entry_is_integer_under_max_value,
                          entry_is_not_empty,
                          entry_is_positive_integer,
                          entry_is_valid, entry_is_valid_datetime,
                          get_valid_entry)
#from controllers.controller_player import get_player
from controller_player import get_player
# from controllers.controller_master import get_valid_entry
#from controllers.pair_generation import generate_pairs_swiss_system
from database import Table
from models import Match, Player, Tournament, Turn
from settings import PLAYERS_TABLE, TOURNAMENTS_TABLE, TIME_CONTROL
from views.view_master import display_message, entry_request
from views.view_tournament import (display_menu_tournament_complete,
                                   display_menu_tournament_lack_players,
                                   display_menu_tournament_main,
                                   display_menu_tournament_resume)


class TournamentController:
    def __init__(self, **kwargs):
        # models
        #self.model_tournament = kwargs.get("model_tournament", Tournament)
        #self.model_turn = kwargs.get("model_turn", Turn)
        #self.model_match = kwargs.get("model_match", Match)
        #self.model_player = kwargs.get("model_player", Player)

        #self.database_table = kwargs.get("database_table", Table)

        # views
        # self.views = kwargs.get("views", views)
        #self.views_menu = kwargs.get("views_menu", views.view_menu)
        #self.views_tournament = kwargs.get("views_tournament", views.view_tournament)
        #self.views_turn = kwargs.get("views_turn", views.view_turn)
        #self.views_match = kwargs.get("views_match", views.view_match)
        #self.views_player = kwargs.get("views_player", views.view_player)

        self.table_players = kwargs.get("table_players", PLAYERS_TABLE)
        # self.table_tournaments = kwargs.get("table_tournaments", TOURNAMENTS_TABLE)

        #self.time_controls = kwargs.get("time_controls", TIME_CONTROL)
        #self.score_values = kwargs.get("score_values", SCORE_VALUES)

        self.tournament = Tournament() #self.model_tournament()
        self.turn = None
        self.match = Match() #self.model_match()
        self.player = Player() #self.model_player()
        #self.generated_matches = None
        #self.previous_matches = None

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

    @staticmethod
    def new_tournament_get_name(title):
        name = get_valid_entry(
            input_fonction=entry_request,
            message="> Enter a tournament name: ",
            check_functions=[entry_is_not_empty],
            title=title,
        )
        return name

    @staticmethod    
    def new_tournament_get_location(title):
        location = get_valid_entry(
            input_fonction=entry_request,
            message="> Enter a tournament location: ",
            check_functions=[entry_is_not_empty],
            title=title,
        )
        return location

    @staticmethod
    def new_tournament_get_dates(title):
        dates = {}
        date = get_valid_entry(
            input_fonction=entry_request,
            message="> Enter a tournament date (yyyy-mm-dd hh:mm): ",
            check_functions=[entry_is_valid_datetime],
            min_date_str="2000-01-01 00:00",
            title=title,
        )
        dates['starts'] = date

        choice = get_valid_entry(
            input_fonction=entry_request,
            message=f"> Enter a end date (y, n): ",
            check_functions=[entry_belongs_list],
            allowed_list=["y", "n"],
            title=title,
        )
        if choice == 'y':
            date = get_valid_entry(
                input_fonction=entry_request,
                message="> Enter a tournament date (yyyy-mm-dd hh:mm): ",
                check_functions=[entry_is_valid_datetime],
                min_date_str="2000-01-01 00:00",
                title=title,
            )
            dates['finished'] = date
        return dates

    @staticmethod
    def new_tournament_get_description(title):
        description = get_valid_entry(
            input_fonction=entry_request,
            message="> Enter a tournament description: ",
            title=title,
        )
        return description

    @staticmethod
    def new_tournament_get_time_control(title):
        time_control = get_valid_entry(
            input_fonction=entry_request,
            message=f'> Enter a time control ({", ".join(TIME_CONTROL)}): ',
            check_functions=[entry_belongs_list],
            allowed_list=TIME_CONTROL,
            title=title,
        )
        return time_control

    @staticmethod
    def new_tournament_get_turns_number(title):
        turns_number = get_valid_entry(
            input_fonction=entry_request,
            message="> Enter a number of turns (press Enter for 4 turns): ",
            check_functions=[entry_is_positive_integer],
            default_value=4,
            title=title,
        )
        return turns_number

    @staticmethod
    def new_tournament_get_players_number(title):
        players_number = get_valid_entry(
            input_fonction=entry_request,
            message="> Enter a number of players (press Enter for 8 players): ",
            check_functions=[entry_is_positive_integer],
            default_value=8,
            title=title,
        )
        return players_number

    def tournament_get_players(self):
        continue_add = None
        while continue_add != 'n':
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

    def new_tournament(self):
        """creation d'un tournoi et ajout a la bdd"""
        cls()
        title = "\x1b[32m>>> Create a Tournament <<<\x1b[0m"
        display_message(title)
        name = self.new_tournament_get_name(title)
        location = self.new_tournament_get_location(title)
        dates = self.new_tournament_get_dates(title)
        description = self.new_tournament_get_description(title)
        time_control = self.new_tournament_get_time_control(title)
        turns_number = self.new_tournament_get_turns_number(title)
        players_number = self.new_tournament_get_players_number(title)
        self.tournament_get_players()
        #self.tournament = self.model_tournament(
        self.tournament = Tournament(
            name=name,
            location=location,
            date=dates,
            description=description,
            time_control=time_control,
            turns_number=int(turns_number),
            players_number=int(players_number),
        )
        

        # self.tournament.add_player(get_player())#self.tournament, self.model_player, self.table_players)
        self.tournament.insert_in_database()
        #self.previous_matches = []
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

            self.tournament.unserializing(results[int(tournament_selected) - 1])
            #self.previous_matches = self.tournament.list_previous_matches()
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

    def display_current_match(self, number=False):
        """affiche les matches généré"""
        cls()
        if self.turn == None:
            print("No turn in memory")
            return None
        message = self.match.display_matches_choice(self.turn)
        print(message)
        #pause()

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
        #self.turn = self.model_turn(name=name)
        self.turn = Turn(name=name)

        if len(self.tournament.turns) == 0:
            self.turn.matches = self.turn.generate_pairs_swiss_system(
                self.tournament.players,
                rankings=self.tournament.load_rankings(),
            )
            #breakpoint()
        else:
            self.turn.matches = self.turn.generate_pairs_swiss_system(
                self.tournament.players,
                scores=self.tournament.load_scores(),
                turns_list=self.tournament.turns,
            )
            #breakpoint()
        #self.turn.matches = [Match(match=match) for match in matches]
        #breakpoint()
        
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
        elif self.turn.all_matches_defined():
            print("all matches defined")
            pause()
            return None
        self.display_current_match(number=True)
        match_selected = get_valid_entry(
            input_fonction=entry_request,
            message="> Select a Match: ",
            check_functions=[entry_is_integer_under_max_value],
            max_value=len(self.turn.matches),
            title=self.match.display_matches_choice(self.turn),
        )
        #players_pair = self.generated_matches[int(match_selected) - 1]
        #print(players_pair)
        #pause()
        if self.turn.matches[int(match_selected) -1].attributes_are_not_none():
            print("Match already registered")
            return None

        # confirm_result = None
        # while confirm_result != 'y':
        #print(players_pair)
        #pause()
        #breakpoint()
        player = self.turn.matches[int(match_selected) -1].get_players()[0] #players_pair[0]
        player_score = get_valid_entry(
            input_fonction=entry_request,
            message=f"> Enter a score for {' '.join((player.firstname, player.lastname))} (0, 1 or 0.5): ",
            check_functions=[entry_belongs_list],
            allowed_list=["0", "1", "0.5"],
            title=self.turn.matches[int(match_selected) -1].display(),
        )
        # #match = []
        # if player_score == '0.5':
        #     self.turn.matches[int(match_selected) -1].edit_scores(0.5, 0.5)
        # #    match = self.model_match(match=([self.turn.matches[int(match_selected) -1].get_players()[0], 0.5], [self.turn.matches[int(match_selected) -1].get_players()[1], 0.5]))
        # else:
        #     self.turn.matches[int(match_selected) -1].edit_scores(int(player_score), 1-int(player_score))
        # #    match = self.model_match(match=([self.turn.matches[int(match_selected) -1].get_players()[0], int(player_score)], [self.turn.matches[int(match_selected) -1].get_players()[1], 1-int(player_score)]))
        self.turn.matches[int(match_selected) -1].edit_scores(float(player_score), 1-float(player_score))

        register = get_valid_entry(
            input_fonction=entry_request,
            message=f"> Confirm match registration ? (y/n)\nAnswer : ",
            check_functions=[entry_belongs_list],
            allowed_list=["y", "n"],
            title=self.turn.matches[int(match_selected) -1].display()
        )
        #breakpoint()
        if register == "n":
            self.turn.matches[int(match_selected) -1].edit_scores(None, None)
        #breakpoint()

    def complete_turn(self):
        """terminer un tour"""
        cls()
        display_message("\x1b[32m>>> Complete turn <<<\x1b[0m")
        if self.turn == None:
            print("No turn in memory")
            return None
        if not self.turn.all_matches_defined():
            # message = self.model_match().display_matches_choice(
            #     self.turn.list_players_pair_complete(), view_complete=True
            # )
            # if message == None:
            #     print(
            #         "No match is completed.\nPlease complete the other matches before finishing the turn."
            #     )
            #     pause()
            # else:
            #     print(
            #         "Completed matches:\n"
            #         + message
            #         + "\nPlease complete the other matches before finishing the turn."
            #     )
            #    pause()
            #message = self.model_match().display_matches_choice(self.turn)
            message = Match().display_matches_choice(self.turn)
            print(message)
            print("please complete without point")
            pause()

        if self.turn.all_matches_defined():
            
            # self.tournament.update_in_database(
            #    self.model_match(),
            #    self.model_turn(),
            #    self.model_player(),
            # )
            print("all matches registered ")
            #message = self.model_match().display_matches_choice(self.turn)
            message = Match().display_matches_choice(self.turn)
            print(message)
            # register = get_valid_entry(
            # input_fonction=entry_request,
            # message=f"> Confirm match registration ? (y/n)\nAnswer : ",
            # check_functions=[entry_belongs_list],
            # allowed_list=["y", "n"],
            # title="\x1b[32m>>> Complete turn <<<\x1b[0m\n"+self.model_match().display_matches_choice(self.turn)
            # )
            register = get_valid_entry(
            input_fonction=entry_request,
            message=f"> Confirm match registration ? (y/n)\nAnswer : ",
            check_functions=[entry_belongs_list],
            allowed_list=["y", "n"],
            title="\x1b[32m>>> Complete turn <<<\x1b[0m\n"+Match().display_matches_choice(self.turn)
            )
            #breakpoint()
            if register == "y":
                self.turn.stop_turn()
                self.tournament.add_turn(self.turn)
                self.save_tournament()
            self.turn = None
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
            pause()
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
            "1": self.tournament.display_all_info,
            "2": self.tournament_get_players,
        }
        while (
            choice != "0"
            and len(self.tournament.players) != self.tournament.players_number
        ):
            cls()
            choice = display_menu_tournament_lack_players()
            if choice_is_valid(choice, handler):
                handler[choice]()
        if len(self.tournament.players) == self.tournament.players_number:
            print("all player defined")
            # self.save_tournament()
            # self.resume_tournament()

        return "0"

    def tournament_is_complete(self):
        """"""
        choice = None
        handler = {
            "1": self.tournament.display_all_info,
        }
        while choice != "0":
            cls()
            choice = display_menu_tournament_complete()
            if choice_is_valid(choice, handler):
                return_value = handler[choice]()
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
            self.tournament.update_in_database()


if __name__ == "__main__":
    controller = TournamentController()
    controller.run()
