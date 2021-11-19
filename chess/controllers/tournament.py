from __future__ import annotations

from ..logger import logger
from ..models import Match, Tournament, Turn
from ..settings import TIME_CONTROL, TOURNAMENTS_TABLE
from ..utils import autopause, clear_display, pause
from ..views import (
    display_menu_tournament_complete,
    display_menu_tournament_lack_players,
    display_menu_tournament_main,
    display_menu_tournament_resume,
    display_message,
    entry_request,
)
from .checks import (
    choice_is_valid,
    entry_belongs_list,
    entry_is_integer_under_max_value,
    entry_is_not_empty,
    entry_is_valid_datetime,
    get_valid_entry,
)
from .player import get_player


class TournamentController:
    """ """

    def __init__(self):
        self.tournament = Tournament()
        self.turn = None

    def run(self) -> None:
        """
        Selection of a choice from the tournament menu.
        After a choice among the selection, it launches the function associated
        with this choice (new, load, resume)
        """
        choice = None
        handler = {
            "1": self.new_tournament,
            "2": self.load_tournament,
            "3": self.resume_tournament,
        }
        while choice != "0":
            clear_display()
            choice = display_menu_tournament_main()
            if choice_is_valid(choice, handler):
                handler[choice]()

    @staticmethod
    def new_tournament_get_name(title: str) -> str:
        """Retrieves the tournament name after the user input has been verified"""
        name = get_valid_entry(
            input_function=entry_request,
            message="> Enter a tournament name: ",
            check_functions=[entry_is_not_empty],
            title=title,
        )
        return name

    @staticmethod
    def new_tournament_get_location(title: str) -> str:
        """Retrieves the tournament location after the user input has been verified"""
        location = get_valid_entry(
            input_function=entry_request,
            message="> Enter a tournament location: ",
            check_functions=[entry_is_not_empty],
            title=title,
        )
        return location

    @staticmethod
    def new_tournament_get_dates(title: str) -> dict[str]:
        """Retrieves the tournament date (start and end) after the user input has been verified"""
        dates = {}
        date = get_valid_entry(
            input_function=entry_request,
            message="> Enter a tournament date (yyyy-mm-dd hh:mm): ",
            check_functions=[entry_is_valid_datetime],
            min_date_str="2000-01-01 00:00",
            title=title,
        )
        dates["starts"] = date

        choice = get_valid_entry(
            input_function=entry_request,
            message="> Enter a end date (y, n): ",
            check_functions=[entry_belongs_list],
            allowed_list=["y", "n"],
            title=title,
        )
        if choice == "y":
            date = get_valid_entry(
                input_function=entry_request,
                message="> Enter a tournament date (yyyy-mm-dd hh:mm): ",
                check_functions=[entry_is_valid_datetime],
                min_date_str="2000-01-01 00:00",
                title=title,
            )
            dates["finished"] = date
        return dates

    @staticmethod
    def new_tournament_get_description(title: str) -> str:
        """Retrieves the tournament name after the user input has been verified"""
        description = get_valid_entry(
            input_function=entry_request,
            message="> Enter a tournament description: ",
            title=title,
        )
        return description

    @staticmethod
    def new_tournament_get_time_control(title: str) -> str:
        """Retrieves the tournament time control after the user input has been verified"""
        time_control = get_valid_entry(
            input_function=entry_request,
            message=f'> Enter a time control ({", ".join(TIME_CONTROL)}): ',
            check_functions=[entry_belongs_list],
            allowed_list=TIME_CONTROL,
            title=title,
        )
        return time_control

    @staticmethod
    def new_tournament_get_turns_number(title: str) -> int:
        """Retrieves the tournament turns number after the user input has been verified"""
        turns_number = get_valid_entry(
            input_function=entry_request,
            message="> Enter a number of turns (press Enter for 4 turns): ",
            check_functions=[entry_is_integer_under_max_value],
            default_value=4,
            title=title,
        )
        return int(turns_number)

    @staticmethod
    def new_tournament_get_players_number(title: str) -> int:
        """Retrieves the tournament players number after the user input has been verified"""
        players_number = get_valid_entry(
            input_function=entry_request,
            message="> Enter a number of players (press Enter for 8 players): ",
            check_functions=[entry_is_integer_under_max_value],
            default_value=8,
            title=title,
        )
        return int(players_number)

    def tournament_get_players(self) -> None:
        """Request the user to add a player as many times as he wants or up to the maximum number of players"""
        continue_add = None
        while continue_add != "n":
            if len(self.tournament.players) == self.tournament.players_number:
                logger.info("All players are defined")
                autopause()
                return None
            player = get_player()
            if player is not None:
                self.tournament.add_player(player)
                continue_add = get_valid_entry(
                    input_function=entry_request,
                    message="> Want to add another player ? (y, n): ",
                    check_functions=[entry_belongs_list],
                    allowed_list=["y", "n"],
                    title="\x1b[32m♟️ Tournament - Add player ♟️\x1b[0m",
                )
            else:
                continue_add = "n"

    def new_tournament(self) -> None:
        """Creation of a tournament by recovering the data entered and adding to the database"""
        clear_display()
        title = "\x1b[32m♟️ Create a Tournament ♟️\x1b[0m"
        display_message(title)
        self.tournament = Tournament()
        self.tournament.name = self.new_tournament_get_name(title)
        self.tournament.location = self.new_tournament_get_location(title)
        self.tournament.date = self.new_tournament_get_dates(title)
        self.tournament.description = self.new_tournament_get_description(title)
        self.tournament.time_control = self.new_tournament_get_time_control(title)
        self.tournament.turns_number = self.new_tournament_get_turns_number(title)
        self.tournament.players_number = self.new_tournament_get_players_number(title)
        self.tournament_get_players()
        self.tournament.insert_in_database()
        self.resume_tournament()

    def load_tournament(self) -> None:
        """Loading of a tournament among a list proposed according to the data entered for the search"""
        clear_display()
        title = "\x1b[32m♟️ Load a Tournament ♟️\x1b[0m"
        display_message(title)
        name = get_valid_entry(
            input_function=entry_request,
            message="\x1b[35mPress Enter to not filter by name.\x1b[0m\n> Enter a tournament name: ",
            title=title,
        )
        location = get_valid_entry(
            input_function=entry_request,
            message="\x1b[35mPress Enter to not filter by location.\x1b[0m\n> Enter a tournament location: ",
            title=title,
        )
        results = TOURNAMENTS_TABLE.search_by_name_and_location(name, location)

        if results is not None and len(results) != 0:

            message = f"\x1b[35mNumber of tournament found: {len(results)}\x1b[0m\n0: Cancel load"
            i = 1
            for result in results:
                message += f"""\n{i}: {result["name"]}, {result["location"]},
    {" and ".join([f"{key} on {value}" for key, value in result["date"].items()])}"""
                i += 1
            message += "\n\x1b[32m> Select a tournament: \x1b[0m"
            tournament_selected = get_valid_entry(
                input_function=entry_request,
                message=message,
                check_functions=[entry_is_integer_under_max_value],
                max_value=len(results),
                title=title,
            )

            if tournament_selected == "0":
                logger.info("cancel ok")
                autopause()
                return None

            self.tournament.unserializing(results[int(tournament_selected) - 1])
            autopause()
            self.resume_tournament()

        else:
            logger.info("No tournament")
            autopause()
            return None

    def display_current_match(self, number: bool = False) -> None:
        """Displays the latest matches generated according to the Swiss system"""
        clear_display()
        if self.turn is None:
            logger.info("No turn in memory")
            autopause()
        else:
            message = Match().display_matches_choice(self.turn)
            display_message(message)
            if not number:
                pause()

    def start_a_turn(self) -> None:
        """
        Start of a new turn with the generation of matches according to
        the Swiss system and the display of these matches
        """
        clear_display()
        display_message("\x1b[32m♟️ New turn ♟️\x1b[0m")
        if self.turn is not None:
            logger.info("Turn in memory")
            autopause()
            return None
        if len(self.tournament.turns) == self.tournament.turns_number:
            logger.info("All turns are defined")
            autopause()
            return None
        name = f"Round {len(self.tournament.turns)+1}"
        self.turn = Turn(name=name)

        if len(self.tournament.turns) == 0:
            self.turn.matches = self.turn.generate_pairs_swiss_system(
                self.tournament.players,
                rankings=self.tournament.load_rankings(),
            )
        else:
            self.turn.matches = self.turn.generate_pairs_swiss_system(
                self.tournament.players,
                scores=self.tournament.load_scores(),
                turns_list=self.tournament.turns,
            )

        self.display_current_match()

    def complete_match(self) -> None:
        """
        Display of the current matches, the user selects one of
        these matches and has to enter the scores of it
        """
        clear_display()
        display_message("\x1b[32m♟️ Complete match ♟️\x1b[0m")
        if self.turn is None:
            logger.info("No turn in memory")
            autopause()
            return None
        elif self.turn.all_matches_defined():
            logger.info("all matches defined")
            autopause()
            return None
        self.display_current_match(number=True)
        match_selected = get_valid_entry(
            input_function=entry_request,
            message="\x1b[32m> Select a Match: \x1b[0m",
            check_functions=[entry_is_integer_under_max_value],
            max_value=len(self.turn.matches),
            title=Match().display_matches_choice(self.turn),
        )

        if self.turn.matches[int(match_selected) - 1].attributes_are_not_none():
            logger.info("Match already registered")
            autopause()
            return None

        player = self.turn.matches[int(match_selected) - 1].get_players()[
            0
        ]  # players_pair[0]
        player_score = get_valid_entry(
            input_function=entry_request,
            message=f"> Enter a score for {' '.join((player.firstname, player.lastname))} (0, 1 or 0.5): ",
            check_functions=[entry_belongs_list],
            allowed_list=["0", "1", "0.5"],
            title=self.turn.matches[int(match_selected) - 1].display(),
        )
        self.turn.matches[int(match_selected) - 1].edit_scores(
            float(player_score), 1 - float(player_score)
        )
        display_message(self.turn.matches[int(match_selected) - 1].display())
        register = get_valid_entry(
            input_function=entry_request,
            message="> Confirm match registration ? (y/n)\nAnswer : ",
            check_functions=[entry_belongs_list],
            allowed_list=["y", "n"],
            title=self.turn.matches[int(match_selected) - 1].display(),
        )
        if register == "n":
            self.turn.matches[int(match_selected) - 1].edit_scores(None, None)

    def complete_turn(self) -> None:
        """
        Checks if all the matches of the round have been recorded with scores
        and records the round if it is complete
        """
        clear_display()
        display_message("\x1b[32m♟️ Complete turn ♟️\x1b[0m")
        if self.turn is None:
            logger.info("No turn in memory")
            return None
        if not self.turn.all_matches_defined():
            message = Match().display_matches_choice(self.turn)
            display_message(
                f"{message}\n\x1b[32mPlease complete matches without scores\x1b[0m"
            )
            pause()

        if self.turn.all_matches_defined():
            logger.info("all matches registered ")
            message = Match().display_matches_choice(self.turn)
            display_message(message)
            register = get_valid_entry(
                input_function=entry_request,
                message="> Confirm matches registration ? (y/n)\nAnswer : ",
                check_functions=[entry_belongs_list],
                allowed_list=["y", "n"],
                title=f"\x1b[32m♟️ Complete turn ♟️\x1b[0m{Match().display_matches_choice(self.turn)}",
            )
            if register == "y":
                self.turn.stop_turn()
                self.tournament.add_turn(self.turn)
                self.save_tournament()
            self.turn = None
            autopause()

    def valid_resume(self) -> None:
        """
        Selection of a choice from the resume menu.
        After a choice among the selection, it launches the function associated
        with this choice
        """
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
            clear_display()
            choice = display_menu_tournament_resume()
            if choice == "1":
                message = handler[choice]()
                display_message(message)
                pause()

            elif choice_is_valid(choice, handler):
                handler[choice]()
            autopause()

        if len(self.tournament.turns) == self.tournament.turns_number:
            logger.info("All turns defined")
            autopause()

    def lack_player(self) -> None:
        """
        Menu to register a new player in a tournament
        After a choice among the selection, it launches the function associated
        with this choice
        """
        choice = None
        handler = {
            "1": self.tournament.display_all_info,
            "2": self.tournament_get_players,
        }
        while (
            choice != "0"
            and len(self.tournament.players) != self.tournament.players_number
        ):
            clear_display()
            choice = display_menu_tournament_lack_players()
            if choice == "1":
                message = handler[choice]()
                display_message(message)
                pause()
            elif choice_is_valid(choice, handler):
                handler[choice]()
        if len(self.tournament.players) == self.tournament.players_number:
            logger.info("all player defined")
            self.resume_tournament()

    def tournament_is_complete(self) -> None:
        """
        Menu to display all the information of a finished tournament
        After a choice among the selection, it launches the function associated
        with this choice
        """
        choice = None
        handler = {
            "1": self.tournament.display_all_info,
        }
        while choice != "0":
            clear_display()
            choice = display_menu_tournament_complete()
            if choice_is_valid(choice, handler):
                message = handler[choice]()
                display_message(message)
                pause()

    def resume_tournament(self) -> None:
        """
        Checks if a tournament is well in memory before resuming it and adapts
        the menu according to the state of the tournament (lack of players,
        tournament not finished, finished tournament)
        """
        if not self.tournament.attributes_are_not_none():
            logger.info("Can not resume with a undefined tournament")
            autopause()
            return None
        if (
            self.tournament.all_players_defined()
            and len(self.tournament.turns) == self.tournament.turns_number
        ):
            self.tournament_is_complete()

        elif (
            self.tournament.all_players_defined()
            and len(self.tournament.turns) != self.tournament.turns_number
        ):
            self.valid_resume()
            # self.save_tournament()

        elif not self.tournament.all_players_defined():
            logger.info("Need more players")
            autopause()
            self.lack_player()
            # self.save_tournament()
        else:
            logger.info("Please create or load a tournament to access this menu")
            autopause()

    def save_tournament(self, title: str = None) -> None:
        """Allows the user to register the tournament in the database"""
        answer = get_valid_entry(
            input_function=entry_request,
            message="> Confirm want to save ? (y, n): ",
            check_functions=[entry_belongs_list],
            allowed_list=["y", "n"],
            title=title,
        )
        if answer == "y":
            self.tournament.update_in_database()
            autopause()
