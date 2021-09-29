import re
from typing import Optional  # , NewType, Tuple, List, Dict, Union


# from chess.settings import TIME_CONTROL

# TournamentMatch = NewType('TournamentMatch', Tuple[List[int,int],List[int,int]])
# TournamentTurn = NewType('TournamentTurn', Union[str,str,str,List[TournamentMatch]])


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
        return f"""The tournament is called {self.name}
and takes place in {self.location} on {self.date}.
It will take place in {self.turns_number} turns
with {self.players_number} players
and {self.time_control} as time control.
Description of the tournament: {self.description}.""".replace(
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

    def add_player(self, player_id) -> None:
        """"""
        self.players.append(player_id)

    def serializing(self, match_object, turn_object, player_object) -> None:
        """"""
        return {
            "name": self.name,
            "location": self.location,
            "date": self.date,
            "description": self.description,
            "time_control": self.time_control,
            "turns_number": self.turns_number,
            "players_number": self.players_number,
            "players": player_object.serializing_players_list(self.players),
            "turns": turn_object.serializing_turns(match_object, self.turns),
        }

    def unserializing(self, match_object, turn_object, player_object, serial_tournament: dict) -> None:
        """"""
        self.name = serial_tournament["name"]
        self.location = serial_tournament["location"]
        self.date = serial_tournament["date"]
        self.description = serial_tournament["description"]
        self.time_control = serial_tournament["time_control"]
        self.turns_number = serial_tournament["turns_number"]
        self.players_number = serial_tournament["players_number"]
        #breakpoint()
        self.players = player_object.unserializing_players_list(serial_tournament["players"])
        self.turns = turn_object.unserializing_turns(
            match_object, serial_tournament["turns"]
        )

    def load_scores(self) -> list:
        scores = [0] * len(self.players)
        for turn in self.turns:
            for match in turn.matchs:
                ([player1, score1], [player2, score2]) = match.match
                index1 = self.players.index(player1)
                index2 = self.players.index(player2)
                scores[index1] += float(score1)
                scores[index2] += float(score2)
        return scores

    def load_rankings(self, players_table) -> list:
        ranking = []
        for player_id in self.players:
            player_data = players_table.get_item_with_id(player_id)
            ranking.append(int(player_data["ranking"]))
        return ranking

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

    def exist_in_database(self, tournaments_table) -> bool:
        if self.attributes_are_not_none():
            return tournaments_table.exist_serial_data(
                self.serialised_information_for_research()
            )
        return False

    def get_id_in_database(self, tournaments_table) -> Optional[int]:
        if self.attributes_are_not_none():
            return tournaments_table.get_id(self.serialised_information_for_research())
        return None

    def insert_in_database(self, tournaments_table, match_object, turn_object) -> None:
        if not self.exist_in_database(tournaments_table):
            tournaments_table.create_item(self.serializing(match_object, turn_object))
            # print('Successful insert.')
        else:
            print(
                "Insertion impossible, the tournament already exists in the database."
            )

    def load_from_database_with_id(self, tournaments_table, tournament_id: int) -> None:
        if tournaments_table.exist_id(tournament_id):
            self.unserializing(tournaments_table.get_item_with_id(tournament_id))
            # print('Successful load.')
        else:
            print("Load impossible, player does not exist in the database.")

    def load_from_database_with_serial_data(
        self, tournaments_table, serial_tournament: dict, unserial_turns
    ) -> None:
        if tournaments_table.exist_serial_data(serial_tournament):
            self.unserializing(serial_tournament, unserial_turns)
            # print('Successful load.')
        else:
            print("Load impossible, tournament does not exist in the database.")

    def update_in_database(self, tournaments_table) -> None:
        tournament_id = self.get_id_in_database()
        if tournament_id != None:
            tournaments_table.update_item(self.serializing(), tournament_id)
            # print('Successful update.')
        else:
            print("Update impossible, tournament does not exist in the database.")

    def display(self) -> None:
        if self.attributes_are_not_none():
            print(f"{self.__str__()}")
        else:
            print(
                "The tournament is not correctly defined, try again after completing his information"
            )

    def display_turns(self):
        if len(self.turns) > 0:
            for turn in self.turns:
                turn.display()
        else:
            print("No turn is defined")

    def display_players(self):
        if len(self.players) > 0:
            for player in self.players:
                player.display()
        else:
            print("No turn is defined")

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
