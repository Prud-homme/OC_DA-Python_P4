from typing import Optional  # , NewType, Tuple, List
from datetime import datetime

# TournamentMatch = NewType('TournamentMatch', Tuple[List[int,int],List[int,int]])


class Turn:
    def __init__(self, **kwargs) -> None:
        ''''''
        self.name = kwargs.get('name', None)
        self.start_date = kwargs.get('start_date', self.get_current_time())
        self.end_date = kwargs.get('end_date', None)
        self.matchs = kwargs.get('matchs', [])

    def __str__(self) -> None:
        return f'''The turn is called {self.name} and started on {self.start_date}.
The turn ended on {self.end_date} and the matchs are: {str(self.matchs)[1:-1]}.'''

    def __repr__(self) -> None:
        return f'''Turn(name='{self.name}', start_date='{self.start_date}', end_date='{self.end_date}', matchs={self.matchs})'''

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

    @staticmethod
    def serializing_turns(match_object,turns):
        return {'turns': [turn.serializing(match_object.serializing_matchs(self.matchs)) for turn in turns]}

    @staticmethod
    def unserializing_turns(match_object,serial_turns):
        turns = []        
        for serial_turn in serial_turns:
            name, start_date, end_date = serial_turn['name'], serial_turn['start_date'], serial_turn['end_date']
            matchs = match_object.unserializing_matchs(serial_turn['matchs'])
            turns.append(Turn(name=name,start_date=start_date,end_date=end_date,matchs=matchs))

        return turns