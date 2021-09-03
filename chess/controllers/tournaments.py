from chess.models import Match, Player, Table, Tournament, Turn
from chess.settings import PLAYERS_TABLE, TIME_CONTROL, TOURNAMENTS_TABLE
from chess.views import main_menu as main_menu_view
from chess.views import match as match_view
from chess.views import players as players_view
from chess.views import tournaments as tournaments_view
from chess.views import turn as turn_view


def add_player(tournament):
    choice = -1
    while choice != 0 or len(tournament.players) != tournament.players_number:
        choice = players_view.display_menu_add_player()

        # Add by id
        if choice == 1:
            tournament.add_player(players_view.enter_player_id())

        # Add by name
        elif choice == 2:
            firstname = players_view.enter_player_firstname(search=True)
            lastname = players_view.enter_player_lastname(search=True)
            result = PLAYERS_TABLE.search_by_first_and_last_name(
                firstname, lastname)
            player_selected = players_view.display_search_result(result)
            if player_selected != -1:
                tournament.add_player(
                    PLAYERS_TABLE.get_id(
                        result[player_selected]))

        # Create and add
        elif choice == 3:
            firstname, lastname, birthdate, gender, ranking = players_view.define_new_player()
            player = Player(firstname, lastname, birthdate, gender, ranking)
            PLAYERS_TABLE.create_item(player.serializing())
            tournament.add_player(player.get_id_in_database())
    return tournament


def new_tournament(tournament):
    name, location, date, description, time_control, turns_number, players_number = tournaments_view.define_new_tournament(
        TIME_CONTROL)
    tournament = Tournament(
        name,
        location,
        date,
        description,
        time_control,
        turns_number,
        players_number)
    # if tournament.exist_in_database():
    tournament = add_player(tournament)

    return tournament


def load_tournament(tournament):
    choice = -1
    while choice != 0:
        choice = tournaments_view.display_menu_load_tournament()

        if choice in [1, 2]:
            # Name search
            if choice == 1:
                name = tournaments_view.enter_tournament_name()
                result = TOURNAMENTS_TABLE.search_by_name(name)

            # Location search
            elif choice == 2:
                location = tournaments_view.enter_tournament_location()
                result = TOURNAMENTS_TABLE.search_by_location(location)

            tournament_selected = tournaments_view.display_search_result(
                result)
            if tournament_selected != -1:
                tournament = Tournament()
                tournament.unserializing(result[tournament_selected])

    return tournament


def resume_tournament(tournament):
    current_turn = None
    current_matchs = None
    choice = -1
    while choice != 0:
        all_players_defined = len(
            tournament.players) == tournament.players_number
        turn_in_memory = current_turn is not None
        exist_turns = len(tournament.turns) > 0

        choice = tournaments_view.display_menu_resume_tournament(
            tournament.name, all_players_defined, turn_in_memory, exist_turns)
        # Informations
        if choice == 1:
            tournaments_view.display_tournament_info(
                tournament.name,
                tournament.location,
                tournament.date,
                tournament.description,
                tournament.time_control)

        # Players defined
        elif choice == 2:
            for player_id in tournament.players:
                player = Player()
                player.load_from_database_with_id(player_id)
                players_view.display_player_info(
                    player.firstname,
                    player.lastname,
                    player.birthdate,
                    player.gender,
                    player.ranking)

        # Add player
        elif choice == 3 and not all_players_defined:
            tournament = add_player(tournament)

        # Turns complete
        elif choice == 3 and exist_turns:
            for turn in tounament.turns:
                turn_view.display_turn_info(turn.name)
                number = 1
                for match in turn.matchs:
                    ([player1, score1], [player2, score2]) = match.match
                    player = Player()
                    player1_name = player.get_player_name_with_id(player1)
                    player2_name = player.get_player_name_with_id(player2)
                    match_view.display_match_info(
                        number, player1_name, score1, player2_name, score2)
                    number += 1

        # Current matchs
        elif turn_in_memory and choice == 3 and not exist_turns or choice == 4 and exist_turns:
            number = 1
            for match in current_matchs:
                (player1, player2) = match
                player = Player()
                player1_name = player.get_player_name_with_id(player1)
                player2_name = player.get_player_name_with_id(player2)
                match_view.display_match_info(
                    number, player1_name, player2_name)
                number += 1

        # Start Turn
        elif not turn_in_memory and choice == 3 and not exist_turns or choice == 4 and exist_turns:
            pass

        # Complete Turn
        elif choice == 4 and not exist_turns or choice == 5 and exist_turns:
            pass


def run(tournament):
    choice = -1
    while choice != 0:
        tournament_in_memory = tournament is not None
        choice = tournaments_view.display_tournament_menu(tournament_in_memory)

        # New tournament
        if choice == 1 and not tournament_in_memory:
            tournament = new_tournament(tournament)

        # Load a tournament
        elif choice == 2:
            tournament = load_tournament(tournament)
            tournament = resume_tournament(tournament, tournament_id)

        # Resume a tournament
        elif choice == 3 and tournament_in_memory:
            tournament = resume_tournament(tournament, tournament_id)

    return tournament, tournament_id
