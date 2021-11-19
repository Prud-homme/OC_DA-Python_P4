from __future__ import annotations

from typing import Any, Optional

# from chess.chess_typeddict import SerializedPartialPlayer, SerializedPlayer
from ..logger import logger
from ..settings import PLAYERS_TABLE
from ..utils import autopause, pause


class Player:
    """
    A player is composed of 5 atttributes, 4 strings
    about the name, first name, date of birth and gender
    and an integer corresponding to the player's ranking.
    """

    def __init__(self, **kwargs) -> None:
        """"""
        self.firstname: str = kwargs.get("firstname", None)
        self.lastname: str = kwargs.get("lastname", None)
        self.birthdate: str = kwargs.get("birthdate", None)
        self.gender: str = kwargs.get("gender", None)
        self.ranking: int = kwargs.get("ranking", None)

    def __str__(self) -> None:
        if self.attributes_are_not_none():
            gender_equivalent = {"M": "man", "F": "woman"}
            return f"""{self.firstname} {self.lastname}
is a {gender_equivalent[self.gender]} born on {self.birthdate}.
His ranking is {self.ranking}.""".replace(
                "\n", " "
            )
        else:
            return self.__repr__()

    def __repr__(self) -> None:
        return f"""Player(firstname='{self.firstname}', lastname='{self.lastname}',
birthdate='{self.birthdate}', gender='{self.gender}',
ranking={self.ranking})""".replace(
            "\n", " "
        )

    def serializing(self) -> SerializedPlayer:
        """Serialization of the player instance in order to export it to json format"""
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "ranking": int(self.ranking),
        }

    def serialised_information_for_research(self) -> SerializedPartialPlayer:
        """
        Serialization of the player instance in order to use it
        to search in the player database
        """
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "birthdate": self.birthdate,
            "gender": self.gender,
        }

    def unserializing(self, serial_player: SerializedPlayer) -> None:
        """Transform the serialized data of a player into a player instance"""
        self.firstname = serial_player["firstname"]
        self.lastname = serial_player["lastname"]
        self.birthdate = serial_player["birthdate"]
        self.gender = serial_player["gender"]
        self.ranking = int(serial_player["ranking"])

    def attributes_are_not_none(self) -> bool:
        """Check that the data set of a player is well defined and not left to None"""
        return None not in (
            self.firstname,
            self.lastname,
            self.birthdate,
            self.gender,
            self.ranking,
        )

    def exist_in_database(self) -> bool:
        """
        Checks if the player has any missing data
        before checking his presence in the player database
        """
        if self.attributes_are_not_none():
            return PLAYERS_TABLE.exist_serial_data(self.serializing())
        return False

    def get_id_in_database(self) -> Optional[int]:
        """
        Checks if the player has any missing data
        retrieving his id from the player database
        """
        if self.attributes_are_not_none():
            return PLAYERS_TABLE.get_id(self.serialised_information_for_research())
        return None

    def insert_in_database(self) -> None:
        """
        Checks if the player does not exist in the player database
        before inserting it to avoid duplicates
        """
        if not self.exist_in_database():
            PLAYERS_TABLE.create_item(self.serializing())
            logger.info("Success: the player has been added to the database.")
            autopause()
        else:
            logger.error(
                "Insertion impossible, the player already exists in the database."
            )
            pause()

    def load_from_database_with_id(self, player_id: int) -> None:
        """
        Checks if the player id exists in the player database
        before retrieving its serialized data from its id
        and transforming it into a player instance
        """
        if PLAYERS_TABLE.exist_id(player_id):
            self.unserializing(PLAYERS_TABLE.get_item_with_id(player_id))
            logger.info("Successful load.")
        else:
            logger.error("Load impossible, player does not exist in the database.")
            pause()

    def load_from_database_with_serial_data(
        self, serial_player: SerializedPlayer
    ) -> None:
        """
        Checks if the serialized data of the player exists in the player database
        before transforming its serialized data into a player instance
        """
        if PLAYERS_TABLE.exist_serial_data(serial_player):
            self.unserializing(serial_player)
            logger.info("Successful load.")
        else:
            logger.error("Load impossible, player does not exist in the database.")
            pause()

    def update_in_database(self) -> None:
        """
        Retrieves the player id from the database and updates its information
        after serializing the player instance data
        """
        player_id = self.get_id_in_database()
        if player_id is not None:
            PLAYERS_TABLE.update_item(self.serializing(), player_id)
            logger.info("Successful update.")
        else:
            logger.error("Update impossible, player does not exist in the database.")
            pause()

    def display(self) -> Optional[str]:
        """Return a string containing a printable description of the object"""
        if self.attributes_are_not_none():
            return f"\n{self.__str__()}"
        else:
            logger.error(
                "The player is not correctly defined, try again after completing his information"
            )
            pause()

    def player_not_in_list(self, players_list: list[Player]) -> bool:
        """Checks if the instance belongs to a list of players"""
        for player in players_list:
            if self.serializing() == player.serializing():
                return False
        return True

    @staticmethod
    def unserializing_players_list(
        serial_players_list: list[SerializedPlayer],
    ) -> list[Player]:
        """
        From a list of players, the function serializes the players
        and creates a new list containing the players serialized.
        """
        return [Player(**serial_data) for serial_data in serial_players_list]

    @staticmethod
    def serializing_players_list(players_list: list[Player]) -> list[SerializedPlayer]:
        """
        From a list of unserialized players, the function unserializes
        the players and creates a new list containing the player instances.
        """
        return [player.serializing() for player in players_list]

    @staticmethod
    def display_players(players_list: list[Player], **kwargs) -> str:
        """
        Return a string containing a printable message
        containing the players of a list provided
        keeping only those that meet the criteria
        """
        sort_field: str = kwargs.get("sort_field", None)
        if len(players_list) == 0:
            return "\x1b[32m♟️ No player is defined ♟️\x1b[0m"

        message = "\x1b[32m♟️ List of players ♟️\x1b[0m"
        if sort_field is not None:
            zipped = zip(
                [player.serializing()[sort_field] for player in players_list],
                range(len(players_list)),
            )
            unsorted_list = list(zipped)
            sorted_list = sorted(unsorted_list)
            sort_value, sort_index = zip(*sorted_list)
            display_list = [players_list[i] for i in sort_index]
        else:
            display_list = players_list

        for player in display_list:
            message += player.display()
        return message

    @staticmethod
    def is_serializedplayer(elt: Any) -> bool:
        """Checks if the provided element is a serialized player"""
        try:
            return (
                len(elt) == 5
                and isinstance(elt["firstname"], str)
                and isinstance(elt["lastname"], str)
                and isinstance(elt["birthdate"], str)
                and isinstance(elt["gender"], str)
                and isinstance(elt["ranking"], int)
            )
        except Exception as e:
            logger.error(e)
            return False

    @staticmethod
    def is_list_of_serializedplayer(list_elt: list[Any]) -> bool:
        """Checks if the provided list is a list of serialized player"""
        for elt in list_elt:
            if not Player().is_serializedplayer(elt):
                return False
        return True

    @staticmethod
    def display_players_choice(results: list) -> str:
        """
        Return a string containing a printable menu
        requesting the selection of a player from the displayed list
        """
        if type(results) != list:
            return None
        if not Player().is_list_of_serializedplayer(results):
            return None
        if len(results) == 0:
            return None
        message = f"\x1b[35mNumber of player found: {len(results)}\x1b[0m\n0: Cancel"
        i = 1
        for result in results:
            message += f'\n{i}: {result["firstname"]}, {result["lastname"]}, {result["birthdate"]}, {result["gender"]}'
            i += 1
        message += "\n\x1b[32m> Select a player: \x1b[0m"
        return message
