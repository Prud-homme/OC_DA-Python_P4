import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
chessdir = os.path.dirname(currentdir)
sys.path.append(chessdir)

from views.view_master import entry_request

from controllers.checks.check import (
    choice_is_valid,
    entry_is_positive_integer,
    entry_is_not_empty,
    entry_is_valid_date,
    entry_belongs_list,
)

from controllers.controller_master import get_valid_entry
from models import Player

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


def search_player(**kwargs):
    """chercher un id dans la bdd"""
    table_players = kwargs.get("table_players", None)
    if table_players == None:
        return None

    firstname = get_valid_entry(
        input_fonction=entry_request,
        message="Press Enter to not filter by first name.\n> Enter a first name: ",
    )
    lastname = get_valid_entry(
        input_fonction=entry_request,
        message="Press Enter to not filter by last name.\n> Enter a last name: ",
    )
    results = table_players.search_by_first_and_last_name(firstname, lastname)

    if results != None and len(results) != 0:

        message = f"Number of player found: {len(results)}"
        i = 1
        for result in results:
            message += f'\n{i}: {result["firstname"]}, {result["lastname"]}, {result["birthdate"]}, {result["gender"]}'
            i += 1
        message += "\n> Select a player: "

        player_selected = get_valid_entry(
            input_fonction=entry_request,
            message=message,
            check_funtions=[entry_is_positive_integer],
            max_value=len(results),
        )

        # if player_selected != None:
        player_serial_data = results[int(player_selected) - 1]

        #player_id = table_players.get_id(player_serial_data)
        #return player_id
        player = Player(**player_serial_data)
        return player

    else:
        print("No player")  # temporaire
        return None


def create_player(**kwargs):
    """creer un joueur et recuperer son id"""
    model_player = kwargs.get("model_player", None)
    table_players = kwargs.get("table_players", None)
    if model_player == None or table_players == None:
        return None

    firstname = get_valid_entry(
        input_fonction=entry_request,
        message="> Enter a first name: ",
        check_functions=[entry_is_not_empty],
    )
    lastname = get_valid_entry(
        input_fonction=entry_request,
        message="> Enter a last name: ",
        check_functions=[entry_is_not_empty],
    )
    birthdate = get_valid_entry(
        input_fonction=entry_request,
        message="> Enter a birth date (yyyy-mm-dd): ",
        check_functions=[entry_is_valid_date],
    )
    gender = get_valid_entry(
        input_fonction=entry_request,
        message=f"> Enter a gender (M/F): ",
        check_functions=[entry_belongs_list],
        allowed_list=["M", "F"],
    )
    ranking = get_valid_entry(
        input_fonction=entry_request,
        message="> Enter a ranking: ",
        check_functions=[entry_is_positive_integer],
    )

    player = model_player(
        firstname=firstname,
        lastname=lastname,
        birthdate=birthdate,
        gender=gender,
        ranking=ranking,
    )

    player.insert_in_database(table_players)
    #player_id = player.get_id_in_database(table_players)

    #return player_id  # Renvoi None ou l'id
    return player

def append_players(
    tournament, model_player, table_players
):  # , players_table, views_player, player):
    """menu pour ajouter un joueur a un tournoi"""
#     menu = """>>> Add a player <<<
# 1: Add by id
# 2: Add by name
# 3: Create a new player and add it
# 0: Don't add any more players
# > Select an option: """
    menu = """>>> Add a player <<<
1: Add by name
2: Create a new player and add it
0: Don't add any more players
> Select an option: """
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
    kwargs = {
        "tournament": tournament,
        "model_player": model_player,
        "table_players": table_players,
    }
    while choice != "0" and len(tournament.players) != tournament.players_number:
        choice = entry_request(menu)

        if choice_is_valid(choice, handler):
            player = handler[choice](**kwargs)

            if player != None and player.player_not_in_list(tournament.players):

                tournament.add_player(player)

        # if len(self.tournament.players) == self.tournament.players_number:#temporaire
        #    print('The list of players for this tournament is complete.')#temporaire


if __name__ == "__main__":
    from database import Table
    from models import Match, Turn, Player, Tournament

    tournament = Tournament(
        name="a",
        location="a",
        date="2020-01-01 15:00",
        description="",
        time_control="blitz",
        turns_number=4,
        players_number=8,
    )
    table = Table("players", "test.json")
    append_players(tournament, Player, table)
    #breakpoint()

    serial = {'name': 'a', 'location': 'a', 'date': '2020-01-01 15:00', 'description': '', 'time_control': 'blitz', 'turns_number': 4, 'players_number': 8, 'players': [{'firstname': 'John', 'lastname': 'Doe', 'birthdate': '1970-01-01', 'gender': 'M', 'ranking': '45'}, {'firstname': 'Jeanne', 'lastname': 'Doe', 'birthdate': '1975-01-01', 'gender': 'F', 'ranking': '20'}], 'turns': []}
    #breakpoint()
    tou=Tournament()
    print('\n\n',tou.players,'\n\n')
    tou.unserializing(Match(),Turn(),Player(),serial)
    print('\n\n',tou.players,'\n\n')
    #breakpoint()
