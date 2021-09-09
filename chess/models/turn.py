from typing import Optional  # , NewType, Tuple, List
from datetime import datetime

# TournamentMatch = NewType('TournamentMatch', Tuple[List[int,int],List[int,int]])


class Turn:
    def __init__(self, **kwargs) -> None:
        ''''''
        self.name = kwargs.get('name', None)
        self.start_date = self.get_current_time()
        self.end_date = None
        self.matchs = []

    def __str__(self) -> None:
        return f'''The tour is called {self.name} and started on {self.start_date}.'''

    def __repr__(self) -> None:
        return f'''Turn(name='{self.name}')'''

    def add_match(self, match: tuple) -> None:
        ''''''
        self.matchs.append(match)

    def stop_turn(self) -> None:
        ''''''
        self.end_date = self.get_current_time()

    def serializing(self, serial_matchs: dict) -> dict:
        ''''''
        return {
            'name': self.name,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'matchs': serial_matchs,
        }

    def unserializing(self, serial_turn: dict, unserial_matchs: list) -> None:
        ''''''
        self.name = serial_turn['name']
        self.start_date = serial_turn['start_date']
        self.matchs = unserial_matchs
        self.end_date = serial_turn['end_date']

    def display(self)
        if self.name != None:
            print(f'\n{self.__str__()}\n')
        else:
            print('The turn is not correctly defined, try again after completing his information')

    @staticmethod
    def get_current_time() -> str:
        ''''''
        now = datetime.now()
        return now.strftime('Date: %d/%m/%Y, Time: %H:%M')
