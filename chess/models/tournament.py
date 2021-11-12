from __future__ import annotations
import os
import sys
from typing import Optional

modelsdir = os.path.dirname(os.path.realpath(__file__))
chessdir = os.path.dirname(modelsdir)
sys.path.append(chessdir)
from models.turn import Turn
from models.player import Player
from models.match import Match
from logger import logger
from settings import TOURNAMENTS_TABLE, ICONS
from utils import clear_display, autopause


class Tournament:
    """
    A tournament is composed of 9 attributes, 4 strings
    about the name, location, description and time control.
    The tournament date is a two-key dictionary 'starts'
    and 'finished' with str value.
    The number of turns and players in this tournament are stored as int.
    The players attributes is a list of Player instance.
    The turns attributes is a list of Turn instance.
    """

    def __init__(self, **kwargs) -> None:
        self.name: str = kwargs.get("name", None)
        self.location: str = kwargs.get("location", None)
        self.date: dict[str] = kwargs.get("date", None)
        self.description: str = kwargs.get("description", None)
        self.time_control: str = kwargs.get("time_control", None)
        self.turns_number: int = kwargs.get("turns_number", 4)
        self.players_number: int = kwargs.get("players_number", 8)
        self.players: list[Player] = []
        self.turns: list[Turn] = []

    def __str__(self) -> None:
        return f"""{self.name} is a tournament that takes place in {self.location}.
It {' and '.join([f'{key} on {value}' for key, value in self.date.items()])}.
It takes place in {self.turns_number} turns with {self.players_number} players.
whose time control is {self.time_control}.

Description of the tournament: {self.description}
"""

    def __repr__(self) -> None:
        return f"""Tournament(name='{self.name}', location='{self.location}',
date='{self.date}', description='{self.description}',
time_control='{self.time_control}', turns_number={self.turns_number},
players_number={self.players_number})""".replace(
            "\n", " "
        )

    def add_turn(self, turn: Turn) -> None:
        """Check if the provided parameter is a turn instance and, if true, add the turn to tournament"""
        if type(turn) != Turn:
            logger.error("Operation cancelled: the provided parameter is not a turn instance")
            autopause()
        else:
            self.turns.append(turn)
            logger.info("Success: the turn has been added to the tournament")
            autopause()

    def add_player(self, new_player: Player) -> None:
        """Check if the provided parameter is a player instance and, if true, add the player to tournament"""
        if type(new_player) != Player:
            logger.error("Operation cancelled: the provided parameter is not a player instance")
            autopause()

        elif new_player.serializing() not in [player.serializing() for player in self.players]:
            self.players.append(new_player)
            logger.info("Success: the player has been added to the tournament")
            autopause()

        else:
            logger.error("Operation cancelled: the player has already been added")
            autopause()

    def serializing(self) -> SerializedTournament:
        """Serialization of the tournament instance in order to export it to json format"""
        return {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "description": self.description,
            "time_control": self.time_control,
            "turns_number": self.turns_number,
            "players_number": self.players_number,
            "players": Player().serializing_players_list(self.players),
            "turns": Turn().serializing_turns(self.turns),
        }

    def unserializing(self, serial_tournament: SerializedTournament) -> None:
        """Transform the serialized data of a tournament into a tournament instance"""
        self.name = serial_tournament["name"]
        self.location = serial_tournament["location"]
        self.date = serial_tournament["date"]
        self.description = serial_tournament["description"]
        self.time_control = serial_tournament["time_control"]
        self.turns_number = serial_tournament["turns_number"]
        self.players_number = serial_tournament["players_number"]
        self.players = Player().unserializing_players_list(serial_tournament["players"])
        self.turns = Turn().unserializing_turns(serial_tournament["turns"])

    def load_scores(self) -> list[int]:
        """
        Browse each match in each turn of the tournament
        and retrieves the scores of the players in those matches
        and stores them in a list
        """
        scores = [0] * len(self.players)
        serial_players = [player.serializing() for player in self.players]
        for turn in self.turns:
            for match in turn.matches:
                [player1, score1], [player2, score2] = match.match
                index1 = serial_players.index(player1.serializing())
                index2 = serial_players.index(player2.serializing())
                scores[index1] += float(score1)
                scores[index2] += float(score2)
        return scores

    def load_rankings(self) -> list[int]:
        """Retrieves the ranking of the players of the tournament and stores them in a list"""
        return [player.ranking for player in self.players]

    def serialised_information_for_research(self) -> SerializedPartialTournament:
        """
        Serialization of the tournament instance in order to use it
        to search in the tournament database
        """
        return {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "description": self.description,
            "time_control": self.time_control,
            "turns_number": self.turns_number,
            "players_number": self.players_number,
        }

    def attributes_are_not_none(self) -> bool:
        """Check that the data set of a tournament is well defined and not left to None"""
        return None not in (
            self.name,
            self.location,
            self.date,
            self.description,
            self.time_control,
        )

    def all_players_defined(self) -> bool:
        """Checks if the list of players of the tournament is complete"""
        return len(self.players) == self.players_number

    def exist_in_database(self) -> bool:
        """
        Checks if the tournament has any missing data
        before checking his presence in the tournament database
        """
        if self.attributes_are_not_none():
            return TOURNAMENTS_TABLE.exist_serial_data(self.serialised_information_for_research())
        return False

    def get_id_in_database(self) -> Optional[int]:
        """
        Checks if the tournament has any missing data
        retrieving his id from the tournament database
        """
        if self.attributes_are_not_none():
            return TOURNAMENTS_TABLE.get_id(self.serialised_information_for_research())
        return None

    def insert_in_database(self) -> None:
        """
        Checks if the tournament does not exist in the tournament database
        before inserting it to avoid duplicates
        """
        if not self.exist_in_database():
            TOURNAMENTS_TABLE.create_item(self.serializing())
            logger.info("Successful insert.")
            autopause()
        else:
            logger.error("Insertion impossible, the tournament already exists in the database.")

    def load_from_database_with_id(self, tournament_id: int) -> None:
        """
        Checks if the tournament id exists in the tournament database
        before retrieving its serialized data from its id
        and transforming it into a tournament instance
        """
        if TOURNAMENTS_TABLE.exist_id(tournament_id):
            self.unserializing(TOURNAMENTS_TABLE.get_item_with_id(tournament_id))
            logger.info("Successful load.")
        else:
            logger.error("Load impossible, player does not exist in the database.")

    def load_from_database_with_serial_data(
        self, serial_tournament: SerializedTournament, unserial_turns: list[Turn]
    ) -> None:
        """
        Checks if the serialized data of the tournament exists in the tournament database
        before transforming its serialized data into a tournament instance
        """
        if TOURNAMENTS_TABLE.exist_serial_data(serial_tournament):
            self.unserializing(serial_tournament, unserial_turns)
            logger.info("Successful load.")
        else:
            logger.error("Load impossible, tournament does not exist in the database.")

    def update_in_database(self) -> None:
        """
        Retrieves the tournament id from the database and updates its information
        after serializing the tournament instance data
        """
        tournament_id = self.get_id_in_database()
        if tournament_id != None:
            TOURNAMENTS_TABLE.update_item(
                self.serializing(),
                tournament_id,
            )
            logger.info("Successful update.")
        else:
            logger.error("Update impossible, tournament does not exist in the database.")

    def display(self) -> Optional[str]:
        """Return a string containing a printable description of the object"""
        if self.attributes_are_not_none():
            return f"\x1b[32m♟️ Tournament - Information ♟️\x1b[0m\n{self.__str__()}"
        else:
            logger.error("The tournament is not correctly defined, try again after completing his information")

    def display_all_info(self) -> str:
        """
        Return a string containing a printable message
        contening all information of the tournament
        """
        clear_display()
        message = ""
        msg = self.display()
        if msg == None:
            logger.warning("Can not obtain tournament information")
            autopause()
        else:
            message += msg

        msg = Turn().display_turns(self.turns)
        if msg == None:
            logger.warning("Can not obtain turns information")
            autopause()
        else:
            message += msg

        msg = Player().display_players(self.players, sort_field="ranking")
        if msg == None:
            logger.warning("Can not obtain players information")
            autopause()
        else:
            message += msg

        return message

    def list_previous_matches(self) -> list[tuple[Player, Player]]:
        """Return the pairs of players of each match of the tournament in a list"""
        return [match.get_serial_players() for turn in self.turns for match in turn.matches]

    @staticmethod
    def display_all_tournaments() -> str:
        """
        Return a string containing a printable message
        contening description of each tournament in tournament database
        """
        tournaments_list = [Tournament(**serial_data) for serial_data in TOURNAMENTS_TABLE.table.all()]
        if len(tournaments_list) == 0:
            return f"\n\x1b[32m♟️ No tournaments is defined ♟️\x1b[0m"
        message = f"\n\x1b[32m♟️ List of tournaments ♟️\x1b[0m"
        for tournament in tournaments_list:
            message += f"\n\x1b[32m[Tournament]\x1b[0m {tournament.name}\n{tournament.__str__()}"
        return message

    def display_only_matches(self) -> str:
        """
        Return a string containing a printable message
        containing the information given by the a Match method of each match
        """
        if len(self.turns) == 0:
            return f"\n\x1b[32m♟️ No match is defined ♟️\x1b[0m"
        message = f"\n\x1b[32m♟️ List of matches ♟️\x1b[0m"
        for turn in self.turns:
            message += Match().display_matches_choice(turn)
        return message

    def display_turns_without_match(self) -> str:
        """
        Return a string containing a printable message
        containing the information given by the __str__ method of each turn
        """
        if len(self.turns) == 0:
            return f"\n\x1b[32m♟️ No turn is defined ♟️\x1b[0m"
        message = f"\n\x1b[32m♟️ List of turns ♟️\x1b[0m"
        for turn in self.turns:
            message += f"\n\x1b[32m[Turn]\x1b[0m {turn.__str__()}"
        return message

    def display_final_ranking(self) -> Optional[str]:
        """
        Return a string containing a printable message
        containing the final ranking given by the display method of each player
        """
        if len(self.turns) != self.turns_number:
            logger.info("The tournament is not finished")
            autopause()
            return None

        message = f"\n\x1b[32m♟️ Tournament - Final ranking ♟️\x1b[0m"

        scores = self.load_scores()
        zipped = zip(scores, range(len(scores)))
        unsorted_list = list(zipped)
        sorted_list = sorted(unsorted_list, reverse=True)
        sort_score, sort_index = zip(*sorted_list)
        sort_player = [self.players[i] for i in sort_index]

        nb = 0
        while len(sort_score) == len(sort_player) > 0:
            score_max = max(sort_score)
            nb_score = sort_score.count(score_max)

            for player in sort_player[:nb_score]:
                if nb < 3:
                    message += f"\n{ICONS[nb]} - {player.lastname} {player.firstname} with {score_max} point"
                else:
                    message += f"\n{player.lastname} {player.firstname} with {score_max}"

            sort_score = [score for score in sort_score if score != score_max]
            sort_player = sort_player[nb_score:]
            nb += nb_score
        return message
