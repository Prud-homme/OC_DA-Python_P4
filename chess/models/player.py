import re

from chess.settings import PLAYERS_TABLE


class Player:
    def __init__(
            self,
            firstname=None,
            lastname=None,
            birthdate=None,
            gender=None,
            ranking=None):
        """"""
        self.firstname = firstname
        self.lastname = lastname
        self.birthdate = birthdate
        self.gender = gender
        self.ranking = ranking

    def well_defined(self):
        return None not in (
            self.firstname,
            self.lastname,
            self.birthdate,
            self.gender,
            self.ranking)

    def serializing(self):
        """"""
        return {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'birthdate': self.birthdate,
            'gender': self.gender,
            'ranking': self.ranking
        }

    def unserializing(self, player_data):
        """"""
        self.firstname = player_data['firstname']
        self.lastname = player_data['lastname']
        self.birthdate = player_data['birthdate']
        self.gender = player_data['gender']
        self.ranking = player_data['ranking']

    def exist_in_database(self):
        if self.well_defined():
            return PLAYERS_TABLE.exist_serial_data(self.serializing())
        return False

    def get_id_in_database(self):
        if self.well_defined():
            return PLAYERS_TABLE.get_id(self.serializing())
        return -1

    def get_player_name_with_id(self, player_id):
        if PLAYERS_TABLE.exist_id(player_id):
            self.unserializing(PLAYERS_TABLE.get_item_with_id(player_id))
            return ' '.join((self.firstname, self.lastname))
        else:
            return ''

    def insert_in_database(self):
        if self.well_defined():
            PLAYERS_TABLE.create_item(self.serializing())
            return 'Success'
        else:
            return 'Fail: player is not well defined'

    def load_from_database_with_id(self, player_id):
        if PLAYERS_TABLE.exist_id(player_id):
            self.unserializing(PLAYERS_TABLE.get_item_with_id(player_id))
            return 'Success'
        else:
            return 'Fail: no player exists with this id in the database'

    def load_from_database_with_serial_data(self, serial_data):
        if PLAYERS_TABLE.exist_serial_data(serial_data):
            self.unserializing(serial_data)
            return 'Success'
        else:
            return 'Fail: no player exists with this data in the database'

    def update_in_database(self):
        player_id = self.get_id_in_database()
        if player_id != -1:
            PLAYERS_TABLE.update_item(self.serializing(), player_id)
            return 'Success'
        else:
            return 'Fail: no player exists with this data in the database'
