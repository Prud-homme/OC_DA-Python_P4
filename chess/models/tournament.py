import re
from textwrap import dedent

from chess.models import Turn
from chess.settings import PLAYERS_TABLE, TIME_CONTROL, TOURNAMENTS_TABLE


class Tournament:

    def __init__(
            self,
            name=None,
            location=None,
            date=None,
            description=None,
            time_control=None,
            turns_number=4,
            players_number=8):
        self.name = name
        self.location = location
        self.date = date
        self.description = description
        self.time_control = time_control
        self.turns_number = turns_number
        self.players_number = players_number
        self.players = []
        self.turns = []

    def __str__(self):
        info = f'''Tournament informations:
		Name: {self.name}
		Location: {self.location}
		Date: {self.date}
		Description: {self.description}
		Time control: {self.time_control}
		Turns number: {self.turns_number}
		Players number: {self.players_number}
		Players defined: {self.players}'''
        return dedent(info)

    def add_turn(self, turn):
        """"""
        self.turns.append(turn)

    def add_player(self, player_id):
        """"""
        self.players.append(player_id)

    def partial_serializing(self):
        """"""
        return {
            'name': self.name,
            'location': self.location,
            'date': self.date,
            'description': self.description,
            'time_control': self.time_control,
            'turns_number': self.turns_number,
            'players_number': self.players_number
        }

    def partial_well_defined(self):
        return None not in (
            self.name,
            self.location,
            self.date,
            self.description,
            self.time_control)

    def serializing(self):
        """"""
        turns = []
        for turn in self.turns:
            turns.append(turn.serializing)
        return {
            'name': self.name,
            'location': self.location,
            'date': self.date,
            'description': self.description,
            'time_control': self.time_control,
            'turns_number': self.turns_number,
            'players_number': self.players_number,
            'players': self.players,
            'turns': turns
        }

    def unserializing(self, tournament_data):
        """"""
        turns = []
        for serial_turn in tournament_data['turns']:
            turn = Turn()
            turn.unserializing(serial_turn)
            turns.append(turn)

        self.name = tournament_data['name']
        self.location = tournament_data['location']
        self.date = tournament_data['date']
        self.description = tournament_data['description']
        self.time_control = tournament_data['time_control']
        self.turns_number = tournament_data['turns_number']
        self.players_number = tournament_data['players_number']
        self.players = tournament_data['players']
        self.turns = turns

    def load_scores(self):
        scores = [0] * len(self.players)
        for turn in self.turns:
            for match in turn.matchs:
                ([player1, score1], [player2, score2]) = match.match
                index1 = self.players.index(player1)
                index2 = self.players.index(player2)
                scores[index1] += float(score1)
                scores[index2] += float(score2)
        return scores

    def load_ranking(self):
        ranking = []
        for player_id in self.players:
            player_data = PLAYERS_TABLE.get_item_with_id(player_id)
            ranking.append(int(player_data['ranking']))
        return ranking

    def exist_in_database(self):
        if self.partial_well_defined():
            return TOURNAMENTS_TABLE.exist_serial_data(
                self.partial_serializing())
        return False

    def get_id_in_database(self):
        if self.partial_well_defined():
            return TOURNAMENTS_TABLE.get_id(self.partial_serializing())
        return -1

    def insert_in_database(self):
        if self.partial_well_defined():
            TOURNAMENTS_TABLE.create_item(self.serializing())
            return 'Success'
        else:
            return 'Fail: tournament is not well defined'

    def load_from_database_with_serial_data(self, serial_data):
        if TOURNAMENTS_TABLE.exist_serial_data(serial_data):
            self.unserializing(serial_data)
            return 'Success'
        else:
            return 'Fail: no tournament exists with this data in the database'

    def update_in_database(self):
        tournament_id = self.get_id_in_database()
        if tournament_id != -1:
            TOURNAMENTS_TABLE.update_item(self.serializing(), tournament_id)
            return 'Success'
        else:
            return 'Fail: no tournament exists with this data in the database'
