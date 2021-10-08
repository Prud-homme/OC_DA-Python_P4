# from chess.settings import PLAYERS_TABLE
import os
import re
import sys
from typing import Optional

currentdir = os.path.dirname(os.path.realpath(__file__))
chessdir = os.path.dirname(currentdir)
sys.path.append(chessdir)
from settings import PLAYERS_TABLE


class Player:
    def __init__(self, **kwargs) -> None:
        """"""
        self.firstname = kwargs.get("firstname", None)
        self.lastname = kwargs.get("lastname", None)
        self.birthdate = kwargs.get("birthdate", None)
        self.gender = kwargs.get("gender", None)
        self.ranking = kwargs.get("ranking", None)

    def __str__(self) -> None:
        gender_equivalent = {"M": "man", "F": "woman"}
        return f"""{self.firstname} {self.lastname}
is a {gender_equivalent[self.gender]} born on {self.birthdate}.
His ranking is {self.ranking}.""".replace(
            "\n", " "
        )

    def __repr__(self) -> None:
        return f"""Player(firstname='{self.firstname}', lastname='{self.lastname}',
birthdate='{self.birthdate}', gender='{self.gender}',
ranking={self.ranking})""".replace(
            "\n", " "
        )

    def serializing(self) -> dict:
        """"""
        return {
            "firstname": self.firstname,
            "lastname": self.lastname,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "ranking": int(self.ranking),
        }

    def unserializing(self, serial_player: dict) -> None:
        """"""
        self.firstname = serial_player["firstname"]
        self.lastname = serial_player["lastname"]
        self.birthdate = serial_player["birthdate"]
        self.gender = serial_player["gender"]
        self.ranking = int(serial_player["ranking"])

    def attributes_are_not_none(self) -> bool:
        return None not in (
            self.firstname,
            self.lastname,
            self.birthdate,
            self.gender,
            self.ranking,
        )

    def exist_in_database(self) -> bool:
        if self.attributes_are_not_none():
            # breakpoint()
            return PLAYERS_TABLE.exist_serial_data(self.serializing())
        return False

    def get_id_in_database(self) -> Optional[int]:
        if self.attributes_are_not_none():
            return PLAYERS_TABLE.get_id(self.serializing())
        return None

    def insert_in_database(self):
        if not self.exist_in_database():
            PLAYERS_TABLE.create_item(self.serializing())
            # print('Successful insert.')
        else:
            print("Insertion impossible, the player already exists in the database.")

    def load_from_database_with_id(self, player_id):
        if PLAYERS_TABLE.exist_id(player_id):
            self.unserializing(PLAYERS_TABLE.get_item_with_id(player_id))
            # print('Successful load.')
        else:
            print("Load impossible, player does not exist in the database.")

    def load_from_database_with_serial_data(self, serial_player):
        if PLAYERS_TABLE.exist_serial_data(serial_player):
            self.unserializing(serial_player)
            # print('Successful load.')
        else:
            print("Load impossible, player does not exist in the database.")

    def update_in_database(self):
        player_id = self.get_id_in_database()
        if player_id != None:
            PLAYERS_TABLE.update_item(self.serializing(), player_id)
            # print('Successful update.')
        else:
            print("Update impossible, player does not exist in the database.")

    def display(self):
        if self.attributes_are_not_none():
            print(f"{self.__str__()}")
        else:
            print(
                "The player is not correctly defined, try again after completing his information"
            )

    def player_not_in_list(self, players_list):
        # breakpoint()
        for player in players_list:
            if self.serializing() == player.serializing():
                return False
        return True

    @staticmethod
    def unserializing_players_list(serial_players_list):
        return [Player(**serial_data) for serial_data in serial_players_list]

    @staticmethod
    def serializing_players_list(players_list):
        # breakpoint()
        return [player.serializing() for player in players_list]

    # @staticmethod
    # def get_id_players_list(PLAYERS_TABLE, players_list):
    #     return [Player().get_id_in_database(player.serializing()) for player in players_list]

    # @staticmethod
    # def get_player_name_with_id(PLAYERS_TABLE, player_id):
    #     if PLAYERS_TABLE.exist_id(player_id):
    #         player_serial_data = PLAYERS_TABLE.get_item_with_id(player_id)
    #         return " ".join(
    #             (player_serial_data["firstname"], player_serial_data["lastname"])
    #         )
    #     else:
    #         print("Load impossible, player does not exist in the database.")
    #         return None
    @staticmethod
    def display_players(players_list, **kwargs):
        sort_field = kwargs.get("sort_field", None)
        if len(players_list) > 0:
            print("\x1b[32m>>> List of players <<<\x1b[0m")
            if sort_field != None:
                unsorted_list = [
                    (player.serializing()[sort_field], player)
                    for player in players_list
                ]
                unsorted_list.sort()
                display_list = [player for (field_value, player) in unsorted_list]
            else:
                display_list = players_list

            for player in display_list:
                player.display()
        else:
            print("\n\x1b[32m>>> No player is defined <<<\x1b[0m")
