from chess.settings import PLAYERS_TABLE, TIME_CONTROL, TOURNAMENTS_TABLE, SCORE_VALUES
from chess.models import Match, Player, Table, Tournament, Turn
from chess.views import (
    views_menu,
    views_match,
    views_player,
    views_tournament,
    views_turn,
)


class TournamentController:
    def __init__(self, **kwargs):
        # models
        self.models_tournament = kwargs.get("models_tournament", Tournament)
        self.models_turn = kwargs.get("models_turn", Turn)
        self.models_match = kwargs.get("models_match", Match)
        self.models_player = kwargs.get("models_player", Player)
        self.models_table = kwargs.get("models_table", Table)

        # views
        self.views_menu = kwargs.get("views_menu", views_menu)
        self.views_tournament = kwargs.get("views_tournament", views_tournament)
        self.views_turn = kwargs.get("views_turn", views_turn)
        self.views_match = kwargs.get("views_match", views_match)
        self.views_player = kwargs.get("views_player", views_player)

        self.players_table = kwargs.get("players_table", PLAYERS_TABLE)
        self.tournaments_table = kwargs.get("tournaments_table", TOURNAMENTS_TABLE)
        self.time_controls = kwargs.get("time_controls", TIME_CONTROL)
        self.score_values = kwargs.get("score_values", SCORE_VALUES)

        self.tournament = self.models_tournament()
        self.tournament_id = None
        self.player = self.models_player()

    def run(self):
        choice = -1
        while choice != 0:
            can_resume_tournament = self.tournament.attributes_are_not_none()
            choice = self.views_tournament.display_tournament_menu(
                can_resume_tournament
            )

            # New tournament
            if choice == 1 and not tournament_in_memory:
                tournament = self.new_tournament()

            # Load a tournament
            elif choice == 2:
                tournament = load_tournament(tournament)
                tournament = resume_tournament(tournament, tournament_id)

            # Resume a tournament
            elif choice == 3 and tournament_in_memory:
                tournament = resume_tournament(tournament, tournament_id)

        return tournament, tournament_id

    def new_tournament():
        (
            name,
            location,
            date,
            description,
            time_control,
            turns_number,
            players_number,
        ) = self.views_tournament.define_new_tournament(self.time_controls)
        self.tournament = self.models_tournament(
            name=name,
            location=location,
            date=date,
            description=description,
            time_control=time_control,
            turns_number=turns_number,
            players_number=players_number,
        )
        self.tournament.add_players(self.players_table, self.views_player, self.player)

    def load_tournament():
        choice = -1
        while choice != 0:
            result = None
            choice = self.views_tournament.display_menu_load_tournament()

            # Name search
            if choice == 1:
                name = self.views_tournament.enter_tournament_name()
                result = self.tournaments_table.search_by_name(name)

            # Location search
            elif choice == 2:
                location = self.views_tournament.enter_tournament_location()
                result = self.tournaments_table.search_by_location(location)

            if result != None:
                tournament_selected = self.views_tournament.display_search_result(result)
                if tournament_selected != None:
                    self.tournament.unserializing(result[tournament_selected])

    def resume_tournament():
        current_turn = None
        current_matchs = None
        choice = -1
        while choice != 0:
            all_players_defined = len(self.tournament.players) == self.tournament.players_number
            turn_in_memory = current_turn is not None
            exist_turns = len(self.tournament.turns) > 0

            choice = self.views_tournament.display_menu_resume_tournament(
                self.tournament.name, all_players_defined, turn_in_memory, exist_turns
            )

            # Informations
            if choice == 1:
                self.tournament.display()

            # Players defined
            elif choice == 2:
                for player_id in tournament.players:
                    self.player.load_from_database_with_id(player_id)
                    self.player.display()

            # Add player
            elif choice == 3 and not all_players_defined:
                self.tournament.add_players(self.players_table, self.views_player, self.player)

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
                            number, player1_name, score1, player2_name, score2
                        )
                        number += 1

            # Current matchs
            elif (
                turn_in_memory
                and choice == 3
                and not exist_turns
                or choice == 4
                and exist_turns
            ):
                number = 1
                for match in current_matchs:
                    (player1, player2) = match
                    player = Player()
                    player1_name = player.get_player_name_with_id(player1)
                    player2_name = player.get_player_name_with_id(player2)
                    match_view.display_match_info(number, player1_name, player2_name)
                    number += 1

            # Start Turn
            elif (
                not turn_in_memory
                and choice == 3
                and not exist_turns
                or choice == 4
                and exist_turns
            ):
                pass

            # Complete Turn
            elif choice == 4 and not exist_turns or choice == 5 and exist_turns:
                pass
