from datetime import datetime

from chess.models import Match


class Turn:
    def __init__(self, name=None):
        """"""
        self.name = name
        self.start_date = self.get_current_time()
        self.matchs = []
        self.end_date = None

    def add_match(self, match):
        """"""
        self.matchs.append(match)

    def close_turn(self):
        """"""
        self.end_date = self.get_current_time()

    def serializing(self):
        """"""
        matchs = []
        for match in self.matchs:
            matchs.append(match.serializing())
        return {
            'name': self.name,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'matchs': matchs
        }

    def unserializing(self, turn_data):
        """"""
        matchs = []
        for match in turn_data['matchs']:
            ([player1, score1], [player2, score2]) = match
            matchs.append(Match(player1, score1, player2, score2))

        self.name = turn_data['name']
        self.start_date = turn_data['start_date']
        self.matchs = matchs
        self.end_date = turn_data['end_date']

    @staticmethod
    def get_current_time():
        """"""
        now = datetime.now()
        return now.strftime("Date: %d/%m/%Y, Time: %H:%M")  # :%S")
