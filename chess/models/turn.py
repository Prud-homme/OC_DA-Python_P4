from typing import Optional  # , NewType, Tuple, List
from datetime import datetime

# TournamentMatch = NewType('TournamentMatch', Tuple[List[int,int],List[int,int]])


class Turn:
    def __init__(self, **kwargs) -> None:
        """"""
        self.name = kwargs.get("name", None)
        self.start_date = kwargs.get("start_date", self.get_current_time())
        self.end_date = kwargs.get("end_date", None)
        self.matchs = kwargs.get("matchs", [])

    def __str__(self) -> None:
        end_string = {True: f"The turn ended on {self.end_date}.", False: ""}
        return f"""The turn is called {self.name} and started on {self.start_date}. {end_string[self.end_date!=None]}"""

    def __repr__(self) -> None:
        return f"""Turn(name='{self.name}', start_date='{self.start_date}', end_date='{self.end_date}', matchs={self.matchs})"""

    def add_match(self, match: tuple) -> None:
        """"""
        self.matchs.append(match)

    def stop_turn(self) -> None:
        """"""
        self.end_date = self.get_current_time()

    def serializing(self, serial_matchs: dict) -> dict:
        """"""
        return {
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "matchs": serial_matchs,
        }

    def unserializing(self, serial_turn: dict, unserial_matchs: list) -> None:
        """"""
        self.name = serial_turn["name"]
        self.start_date = serial_turn["start_date"]
        self.matchs = unserial_matchs
        self.end_date = serial_turn["end_date"]

    def display(self):
        if self.name != None:
            end_string = {True: f"The turn ended on {self.end_date}.", False: ""}
            print(f"{self.__str__()} {end_string[self.end_date!=None]}")

            if len(self.matchs) > 0:
                match_number = 1
                for match in self.matchs:
                    match.display()
                    match_number += 1

        else:
            print(
                "The turn is not correctly defined, try again after completing his information"
            )

    @staticmethod
    def get_current_time() -> str:
        """"""
        now = datetime.now()
        return now.strftime("Date: %d/%m/%Y, Time: %H:%M")

    @staticmethod
    def serializing_turns(match_object, turns):
        # return {
        #     "turns": [
        #         turn.serializing(match_object.serializing_matchs(turn.matchs))
        #         for turn in turns
        #     ]
        # }
        return [
            turn.serializing(match_object.serializing_matchs(turn.matchs))
            for turn in turns
        ]
        

    @staticmethod
    def unserializing_turns(match_object, serial_turns):
        turns = []
        for serial_turn in serial_turns:
            # breakpoint()
            name, start_date, end_date = (
                serial_turn["name"],
                serial_turn["start_date"],
                serial_turn["end_date"],
            )
            matchs = match_object.unserializing_matchs(serial_turn["matchs"])
            turns.append(
                Turn(name=name, start_date=start_date, end_date=end_date, matchs=matchs)
            )
        return turns

    @staticmethod
    def display_matchs(
        players_table, player_object, generated_matchs, display_number=True
    ):
        message = ""
        if len(generated_matchs) == 0:
            return None
        number = 0
        for match in generated_matchs:
            (player1_id, player2_id) = match
            player1_name = player_object.get_player_name_with_id(
                players_table, player1_id
            )
            player2_name = player_object.get_player_name_with_id(
                players_table, player2_id
            )

            if None in (player1_name, player2_name):
                return None
            if not display_number:
                number = ""
            else:
                number += 1
            message += f"""Match {number}: [{player1_id}] {player1_name} VS [{player2_id}] {player2_name}\n"""

        return message
