import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
chessdir = os.path.dirname(currentdir)
sys.path.append(chessdir)

cls = lambda: os.system('cls')
def pause():
    programPause = input("\x1b[35mPress the <ENTER> key to continue...\x1b[0m")

from views.view_master import entry_request, display_message

from controllers.checks.check import (
    choice_is_valid,
    entry_is_positive_integer,
    entry_is_not_empty,
    entry_is_valid_date,
    entry_belongs_list,
)

from controllers.controller_master import get_valid_entry
from models import Player
from settings import PLAYERS_TABLE, TIME_CONTROL, TOURNAMENTS_TABLE, SCORE_VALUES

from views.view_player import display_menu_add_player 

# def check_player_id(**kwargs):
#     """verifier id saisie  existe"""
#     tournament = kwargs.get("tournament", None)
#     table_players = kwargs.get("table_players", None)
#     if tournament == None or table_players == None:
#         return None

#     player_id = get_valid_entry(
#         input_fonction=entry_request,
#         message="> Enter a player id: ",
#         check_functions=[entry_is_positive_integer],
#     )
#     player_id = int(player_id)

#     if table_players.exist_id(player_id):
#         #return player_id

#         player_serial_data = table_players.get_item_with_id(player_id)
#         return player_serial_data

#     return None


def search_player():
    """chercher un id dans la bdd"""
    #table_players = kwargs.get("table_players", None)
    #if table_players == None:
    #    return None

    cls()    
    display_message('\x1b[32m>>> Search a player <<<\x1b[0m')

    firstname = get_valid_entry(
        input_fonction=entry_request,
        message="\x1b[35mPress Enter to not filter by first name.\x1b[0m\n> Enter a first name: ",
    )
    lastname = get_valid_entry(
        input_fonction=entry_request,
        message="\x1b[35mPress Enter to not filter by last name.\x1b[0m\n> Enter a last name: ",
    )
    results = PLAYERS_TABLE.search_by_first_and_last_name(firstname, lastname)

    if results != None and len(results) != 0:

        message = f"\x1b[35mNumber of player found: {len(results)}\x1b[0m"
        i = 1
        for result in results:
            message += f'\n{i}: {result["firstname"]}, {result["lastname"]}, {result["birthdate"]}, {result["gender"]}'
            i += 1
        message += "\n\x1b[32m> Select a player: \x1b[0m"

        player_selected = get_valid_entry(
            input_fonction=entry_request,
            message=message,
            check_funtions=[entry_is_positive_integer],
            max_value=len(results),
            title='\x1b[32m>>> Search a player <<<\x1b[0m',
        )

        # if player_selected != None:
        player_serial_data = results[int(player_selected) - 1]

        #player_id = table_players.get_id(player_serial_data)
        #return player_id
        player = Player(**player_serial_data)
        pause()
        return player

    else:
        print("No player")  # temporaire
        pause()
        return None


def create_player():
    """creer un joueur et recuperer son id"""
    #model_player = kwargs.get("model_player", None)
    #table_players = kwargs.get("table_players", None)
    #if model_player == None or table_players == None:
    #    return None

    cls()    
    display_message('\x1b[32m>>> Create a player <<<\x1b[0m')

    firstname = get_valid_entry(
        input_fonction=entry_request,
        message="> Enter a first name: ",
        check_functions=[entry_is_not_empty],
        title='\x1b[32m>>> Create a player <<<\x1b[0m',
    )
    lastname = get_valid_entry(
        input_fonction=entry_request,
        message="> Enter a last name: ",
        check_functions=[entry_is_not_empty],
        title='\x1b[32m>>> Create a player <<<\x1b[0m',
    )
    birthdate = get_valid_entry(
        input_fonction=entry_request,
        message="> Enter a birth date (yyyy-mm-dd): ",
        check_functions=[entry_is_valid_date],
        title='\x1b[32m>>> Create a player <<<\x1b[0m',
    )
    gender = get_valid_entry(
        input_fonction=entry_request,
        message=f"> Enter a gender (M/F): ",
        check_functions=[entry_belongs_list],
        allowed_list=["M", "F"],
        title='\x1b[32m>>> Create a player <<<\x1b[0m',
    )
    ranking = get_valid_entry(
        input_fonction=entry_request,
        message="> Enter a ranking: ",
        check_functions=[entry_is_positive_integer],
        title='\x1b[32m>>> Create a player <<<\x1b[0m',
    )

    player = Player(
        firstname=firstname,
        lastname=lastname,
        birthdate=birthdate,
        gender=gender,
        ranking=ranking,
    )

    player.insert_in_database()
    #player_id = player.get_id_in_database(table_players)

    #return player_id  # Renvoi None ou l'id
    pause()
    return player

def get_player(**kwargs):
#    tournament, model_player, table_players
#):  # , players_table, views_player, player):
    """menu pour ajouter un joueur a un tournoi"""
#     menu = """>>> Add a player <<<
# 1: Add by id
# 2: Add by name
# 3: Create a new player and add it
# 0: Don't add any more players
# > Select an option: """

    tournament = kwargs.get("tournament", None)

    choice = None
    # handler = {
    #     "1": check_player_id,
    #     "2": search_player_id,
    #     "3": create_player_id,
    # }
    handler = {
        "1": search_player,
        "2": create_player,
    }
    #kwargs = {
    #    "tournament": tournament,
    #    "model_player": model_player,
    #    "table_players": table_players,
    #}
    while choice != "0":
        cls()
        if tournament != None and len(tournament.players) == tournament.players_number:
            print('all player defined')
            pause()
            return None 
        choice = display_menu_add_player()
        if choice_is_valid(choice, handler):
            player = handler[choice]()
            if tournament != None:
                tournament.add_player(player)
        '''
        if len(tournament.players) == tournament.players_number:
            print('all player defined')
            pause()
            return None 

        if choice_is_valid(choice, handler):
            player = handler[choice]()

            if player != None and player.player_not_in_list(tournament.players):
                pause()

                tournament.add_player(player)
        '''

        # if len(self.tournament.players) == self.tournament.players_number:#temporaire
        #    print('The list of players for this tournament is complete.')#temporaire


# if __name__ == "__main__":
#     from database import Table
#     from models import Match, Turn, Player, Tournament

#     tournament = Tournament(
#         name="a",
#         location="a",
#         date="2020-01-01 15:00",
#         description="",
#         time_control="blitz",
#         turns_number=4,
#         players_number=8,
#     )
#     table = Table("players", "test.json")
#     append_players(tournament, Player, table)
#     #breakpoint()

#     serial = {'name': 'a', 'location': 'a', 'date': '2020-01-01 15:00', 'description': '', 'time_control': 'blitz', 'turns_number': 4, 'players_number': 8, 'players': [{'firstname': 'John', 'lastname': 'Doe', 'birthdate': '1970-01-01', 'gender': 'M', 'ranking': '45'}, {'firstname': 'Jeanne', 'lastname': 'Doe', 'birthdate': '1975-01-01', 'gender': 'F', 'ranking': '20'}], 'turns': []}
#     #breakpoint()
#     tou=Tournament()
#     print('\n\n',tou.players,'\n\n')
#     tou.unserializing(Match(),Turn(),Player(),serial)
#     print('\n\n',tou.players,'\n\n')
#     #breakpoint()
