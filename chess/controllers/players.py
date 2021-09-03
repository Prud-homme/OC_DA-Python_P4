from chess.models import Player, Table
from chess.views import main_menu as mm_v
from chess.views import players as p_v

p_table = Table('players', 'test.json')


def update_player(players_table):
    result = t_table.search_by_name(p_v.prompt_player_name())
    choice = p_v.display_search_result(result)
    if len(result) > 0:
        player = Player()
        player_id = players_table.get_id(result[choice])
        serial_data = players_table.get_item_with_id(player_id)
        player.unserializing(serial_data)
    print('''Only load, don't update''')


def add_player(players_table):
    firstname, lastname, birthdate, gender, ranking = p_v.prompt_new_player()
    player = Player(firstname, lastname, birthdate, gender, ranking)
    players_table.create_item(player.serializing())


def run():
    choice = -1
    while choice != 0:
        choice = p_v.display_menu()
        if choice == 1:
            add_player(p_table)
        elif choice == 2:
            update_player(p_table)
