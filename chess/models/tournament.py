# from chess.settings import TIME_CONTROL
# TournamentMatch = NewType('TournamentMatch', Tuple[List[int,int],List[int,int]])
# TournamentTurn = NewType('TournamentTurn', Union[str,str,str,List[TournamentMatch]])
import os
import re
import sys
import time
from typing import Optional  # , NewType, Tuple, List, Dict, Union

currentdir = os.path.dirname(os.path.realpath(__file__))
chessdir = os.path.dirname(currentdir)
sys.path.append(chessdir)
from logger import logger
from settings import TOURNAMENTS_TABLE

cls = lambda: os.system("cls")


def pause():
    programPause = input("\x1b[35mPress the <ENTER> key to continue...\x1b[0m")


class Tournament:
    def __init__(self, **kwargs) -> None:
        self.name = kwargs.get("name", None)
        self.location = kwargs.get("location", None)
        self.date = kwargs.get("date", None)
        self.description = kwargs.get("description", None)
        self.time_control = kwargs.get("time_control", None)
        self.turns_number = kwargs.get("turns_number", 4)
        self.players_number = kwargs.get("players_number", 8)
        self.players = []
        self.turns = []

    def __str__(self) -> None:
        return f"""{self.name} is a tournament that
takes place in {self.location} on {', '.join(self.date)}.
It take place in {self.turns_number} turns
with {self.players_number} players
whose time control is {self.time_control}.
Description of the tournament: {self.description}""".replace(
            "\n", " "
        )

    def __repr__(self) -> None:
        return f"""Tournament(name='{self.name}', location='{self.location}',
date='{self.date}', description='{self.description}',
time_control='{self.time_control}', turns_number={self.turns_number},
players_number={self.players_number})""".replace(
            "\n", " "
        )

    def add_turn(self, turn) -> None:
        """"""
        self.turns.append(turn)

    def add_player(self, new_player) -> None:
        """"""
        if new_player == None:
            return None
        if new_player.serializing() not in [
            player.serializing() for player in self.players
        ]:
            self.players.append(new_player)
            print("insertion reussie")
            time.sleep(1)
        else:
            print("insertion echouee")
            time.sleep(1)

    def serializing(self, match_object, turn_object, player_object) -> None:
        """"""
        ##breakpoint()
        return {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "description": self.description,
            "time_control": self.time_control,
            "turns_number": self.turns_number,
            "players_number": self.players_number,
            "players": player_object.serializing_players_list(self.players),
            "turns": turn_object.serializing_turns(
                match_object, player_object, self.turns
            ),
        }

    def unserializing(
        self, match_object, turn_object, player_object, serial_tournament: dict
    ) -> None:
        """"""
        self.name = serial_tournament["name"]
        self.location = serial_tournament["location"]
        self.date = serial_tournament["date"]
        self.description = serial_tournament["description"]
        self.time_control = serial_tournament["time_control"]
        self.turns_number = serial_tournament["turns_number"]
        self.players_number = serial_tournament["players_number"]
        ##breakpoint()
        self.players = player_object.unserializing_players_list(
            serial_tournament["players"]
        )
        self.turns = turn_object.unserializing_turns(
            match_object, player_object, serial_tournament["turns"]
        )

    def load_scores(self) -> list:
        scores = [0] * len(self.players)
        serial_players = [player.serializing() for player in self.players]
        for turn in self.turns:
            for match in turn.matchs:
                [player1, score1], [player2, score2] = match.match
                index1 = serial_players.index(player1.serializing())
                index2 = serial_players.index(player2.serializing())
                scores[index1] += float(score1)
                scores[index2] += float(score2)
        return scores

    def load_rankings(self) -> list:
        return [player.ranking for player in self.players]

    def serialised_information_for_research(self) -> dict:
        """"""
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
        return None not in (
            self.name,
            self.location,
            self.date,
            self.description,
            self.time_control,
        )

    def all_players_defined(self):
        return len(self.players) == self.players_number

    def exist_in_database(self) -> bool:
        if self.attributes_are_not_none():
            return TOURNAMENTS_TABLE.exist_serial_data(
                self.serialised_information_for_research()
            )
        return False

    def get_id_in_database(self) -> Optional[int]:
        if self.attributes_are_not_none():
            return TOURNAMENTS_TABLE.get_id(self.serialised_information_for_research())
        return None

    def insert_in_database(self, match_object, turn_object, player_object) -> None:
        if not self.exist_in_database():
            TOURNAMENTS_TABLE.create_item(
                self.serializing(match_object, turn_object, player_object)
            )
            # print('Successful insert.')
        else:
            print(
                "Insertion impossible, the tournament already exists in the database."
            )

    def load_from_database_with_id(self, tournament_id: int) -> None:
        if TOURNAMENTS_TABLE.exist_id(tournament_id):
            self.unserializing(TOURNAMENTS_TABLE.get_item_with_id(tournament_id))
            # print('Successful load.')
        else:
            print("Load impossible, player does not exist in the database.")

    def load_from_database_with_serial_data(
        self, serial_tournament: dict, unserial_turns
    ) -> None:
        if TOURNAMENTS_TABLE.exist_serial_data(serial_tournament):
            self.unserializing(serial_tournament, unserial_turns)
            # print('Successful load.')
        else:
            print("Load impossible, tournament does not exist in the database.")

    def update_in_database(self, match_object, turn_object, player_object) -> None:
        tournament_id = self.get_id_in_database()
        if tournament_id != None:
            ##breakpoint()
            TOURNAMENTS_TABLE.update_item(
                self.serializing(match_object, turn_object, player_object),
                tournament_id,
            )
            # print('Successful update.')
        else:
            print("Update impossible, tournament does not exist in the database.")

    def display(self) -> None:
        if self.attributes_are_not_none():
            print(f"\x1b[32m>>> Tournament - Information <<<\x1b[0m\n{self.__str__()}")
        else:
            print(
                "The tournament is not correctly defined, try again after completing his information"
            )

    def display_all_info(self, player_object, turn_object):
        cls()
        self.display()
        turn_object.display_turns(self.turns)
        player_object.display_players(self.players, sort_field="ranking")
        pause()

    def associate_player_ids_with_their_name(self, players_table):
        players_id_with_name = {}
        for player_id in self.players:
            player_data = players_table.get_item_with_id(player_id)
            if player_data != None:
                players_id_with_name[player_id] = " ".join(
                    (player_data["firstname"], player_data["lastname"])
                )
        if len(players_id_with_name) == len(self.players):
            return players_id_with_name
        else:
            return None

    def all_previous_matches(self):
        return [
            (player1, player2)
            for turn in self.turns
            for ([player1, score1], [player2, score2]) in turn.matchs
        ]

    def list_previous_matchs(self):
        return [
            match.get_serial_players() for turn in self.turns for match in turn.matchs
        ]

    @staticmethod
    def display_all_tournaments():
        tournaments_list = [
            Tournament(**serial_data) for serial_data in TOURNAMENTS_TABLE.table.all()
        ]
        for tournament in tournaments_list:
            print(tournament)
        pause()


if __name__ == "__main__":
    tournament1 = Tournament(
        "Tournament 1",
        "Paris",
        "2019/09/22",
        "Qualification for Tournament 2.",
        "bullet",
        8,
        16,
    )
    print(f"__str__:\n{tournament1.__str__()}\n")
    print(f"__repr__:\n{tournament1.__repr__()}\n")

    tournament2 = Tournament(
        "Tournament 2", "Paris", "2019/10/12", "Regional championship", "bullet"
    )
    print(f"__str__:\n{tournament2.__str__()}\n")
    print(f"__repr__:\n{tournament2.__repr__()}\n")
