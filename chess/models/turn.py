from __future__ import annotations

import operator
from datetime import datetime
from typing import Optional  # , NewType, Tuple, List

# TournamentMatch = NewType('TournamentMatch', Tuple[List[int,int],List[int,int]])
import sys, os
currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(currentdir)
chessdir = os.path.dirname(currentdir)
sys.path.append(chessdir)
from match import Match
from utils import pause
from typing import Optional, NewType, Union, TypedDict
class SerializedTurn(TypedDict):
    name: str
    start_date: str
    end_date: str
    matches: list[Match]

class Turn:
    def __init__(self, **kwargs) -> None:
        """"""
        self.name = kwargs.get('name', None)
        self.start_date = kwargs.get('start_date', self.get_current_time())
        self.end_date = kwargs.get('end_date', None)
        self.matches = kwargs.get('matches', [])

    def __str__(self) -> None:
        end_string = {True: f' and ended on {self.end_date}.', False: '.'}
        return f'{self.name} started on {self.start_date}{end_string[self.end_date!=None]}'

    def __repr__(self) -> None:
        return f'''Turn(name='{self.name}', start_date='{self.start_date}', end_date='{self.end_date}', matches={self.matches})'''

    def add_match(self, match: Match) -> None:
        """"""
        self.matches.append(match)

    def stop_turn(self) -> None:
        """"""
        self.end_date = self.get_current_time()

    def serializing(self) -> dict:
        """"""
        # breakpoint()
        test = {
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "matches": Match().serializing_matches(self.matches),
        }
        # breakpoint()
        return test

    def unserializing(self, serial_turn: dict, unserial_matches: list) -> None:
        """"""
        self.name = serial_turn["name"]
        self.start_date = serial_turn["start_date"]
        self.matches = unserial_matches
        self.end_date = serial_turn["end_date"]

    def display(self):
        message = ''
        if self.name != None:
            print(f"{self.__str__()}")

            if len(self.matches) > 0:
                # match_number = 1
                for match in self.matches:
                    print(match.display())
                    # match_number += 1
            print()  #'\n', end = '')

        else:
            print(
                "The turn is not correctly defined, try again after completing his information"
            )

    @staticmethod
    def get_current_time() -> str:
        """"""
        now = datetime.now()
        return now.strftime("Date: %d/%m/%Y, Time: %H:%M")

    @staticmethod
    def serializing_turns(turns):
        # return {
        #     "turns": [
        #         turn.serializing(match_object.serializing_matches(turn.matches))
        #         for turn in turns
        #     ]
        # }
        ##breakpoint()
        return [turn.serializing() for turn in turns]

    @staticmethod
    def unserializing_turns(serial_turns):
        turns = []
        for serial_turn in serial_turns:
            turns.append(Turn(name=serial_turn["name"],start_date=serial_turn["start_date"], end_date=serial_turn["end_date"], matches=Match().unserializing_matches(serial_turn["matches"])))
        return turns

    def list_players_pair_complete(self):
        return [match.get_players() for match in self.matches]

    @staticmethod
    def sort_players_swiss_system(players, **kwargs):
        rankings = kwargs.get("rankings", None)
        scores = kwargs.get("scores", None)

        players_index = [*range(len(players))]
        if scores != None and len(players) == len(scores) and len(players) % 2 == 0:
            sort_scores, sort_index = zip(
                *sorted(zip(scores, players_index), reverse=True)
            )

        elif (
            rankings != None and len(players) == len(rankings) and len(players) % 2 == 0
        ):
            sort_rankings, sort_index = zip(
                *sorted(zip(rankings, players_index), reverse=False)
            )

        else:
            return None

        return operator.itemgetter(*sort_index)(players)

    @staticmethod
    def pair_not_in_previous_matches(turns_list, pair_players):
        previous_matches = [
            match.get_serial_players() for turn in turns_list for match in turn.matches
        ]
        return (
            pair_players[0].serializing(),
            pair_players[1].serializing(),
        ) not in previous_matches and (
            pair_players[1].serializing(),
            pair_players[0].serializing(),
        ) not in previous_matches

    @staticmethod
    def pairing_swiss_system(
        players,
        top_index,
        bottom_index,
        player_paired,
        top_players_list,
        bottom_players_list,
        turns_list,
        pair_players_matches,
    ):
        for i in top_index:
            for j in [player for player in bottom_index if player not in player_paired]:
                pair_players = (top_players_list[i], bottom_players_list[j])
                if (
                    Turn().pair_not_in_previous_matches(turns_list, pair_players)
                    or len(players) == 2
                ):
                    pair_players_matches.append(Match(match=([top_players_list[i], None],[bottom_players_list[j], None])))
                    player_paired.append(j)
                    break

                elif i == top_index[0] and j == bottom_index[-1] and len(players) > 2:
                    return None
        return pair_players_matches, j

    @staticmethod
    def pairing_failed_swiss_system(
        position_top, position_bottom, pair_players_matches, player_paired, nb_matches, j, bottom_index, top_index
    ):
        if (
            len(pair_players_matches) != nb_matches
            and j == bottom_index[-1]
            and position_bottom < nb_matches - 1
        ):
            position_bottom += 1
            pair_players_matches, player_paired = [], []
            bottom_index = list(range(nb_matches))
            bottom_index.insert(0, bottom_index.pop(position_bottom))

        elif len(pair_players_matches) != nb_matches and position_bottom == nb_matches - 1:
            position_top += 1
            position_bottom = 0
            pair_players_matches, player_paired = [], []
            top_index, bottom_index = list(range(nb_matches)), list(range(nb_matches))
            top_index.insert(0, top_index.pop(position_top))
        return (
            position_top,
            position_bottom,
            pair_players_matches,
            player_paired,
            top_index,
            bottom_index,
        )

    @staticmethod
    def generate_pairs_swiss_system(players, **kwargs):
        """generation des pairs"""
        if len(players) > 0 and len(players) % 2 != 0:
            return None

        turns_list = kwargs.get("turns_list", [])
        sort_players = Turn().sort_players_swiss_system(players, **kwargs)
        nb_matches = int(len(players) / 2)
        top_players_list = sort_players[:nb_matches]
        bottom_players_list = sort_players[nb_matches:]
        breakpoint()
        pair_players_matches, player_paired = [], []
        top_index, bottom_index = list(range(nb_matches)), list(range(nb_matches))
        position_top = position_bottom = 0

        while len(pair_players_matches) != nb_matches and position_top < nb_matches:
            # for i in top_index:
            #     for j in [
            #         player for player in bottom_index if player not in player_paired
            #     ]:
            #         pair_players = (top_players_list[i], bottom_players_list[j])
            #         if (
            #             Turn().pair_not_in_previous_matches(turns_list, pair_players)
            #             or len(players) == 2
            #         ):
            #             pair_players_matches.append(
            #                 (
            #                     [top_players_list[i], None],
            #                     [bottom_players_list[j], None],
            #                 )
            #             )
            #             player_paired.append(j)
            #             break

            result = Turn().pairing_swiss_system(
                players,
                top_index,
                bottom_index,
                player_paired,
                top_players_list,
                bottom_players_list,
                turns_list,
                pair_players_matches,
            )
            if result == None:
                return None

            pair_players_matches, j = result

            (
                position_top,
                position_bottom,
                pair_players_matches,
                player_paired,
                top_index,
                bottom_index,
            ) = Turn().pairing_failed_swiss_system(
                position_top,
                position_bottom,
                pair_players_matches,
                player_paired,
                nb_matches,
                j,
                bottom_index,
                top_index,
            )
            #         elif (
            #             i == top_index[0] and j == bottom_index[-1] and len(players) > 2
            #         ):
            #             return None

            # if (
            #     len(pair_players_matches) != nb_matches
            #     and j == bottom_index[-1]
            #     and position_bottom < nb_matches - 1
            # ):
            #     position_bottom += 1
            #     pair_players_matches, player_paired = [], []
            #     bottom_index = list(range(nb_matches))
            #     bottom_index.insert(0, bottom_index.pop(position_bottom))

            # elif (
            #     len(pair_players_matches) != nb_matches
            #     and position_bottom == nb_matches - 1
            # ):
            #     position_top += 1
            #     position_bottom = 0
            #     pair_players_matches, player_paired = [], []
            #     top_index, bottom_index = list(range(nb_matches)), list(range(nb_matches))
            #     top_index.insert(0, top_index.pop(position_top))

        return pair_players_matches

    @staticmethod
    def display_turns(turns_list):
        if len(turns_list) > 0:
            print("\n\x1b[32m>>> Tournament - List of turns <<<\x1b[0m")
            for turn in turns_list:
                turn.display()
        else:
            print("\n\x1b[32m>>> Tournament - No turn is defined <<<\x1b[0m")

    @staticmethod
    def display_turns_without_match(turns_list):
        if len(turns_list) > 0:
            print("\n\x1b[32m>>> List of turns <<<\x1b[0m")
            for turn in turns_list:
                print(turn.__str__())
            pause()
        else:
            print("\n\x1b[32m>>> No turn is defined <<<\x1b[0m")
        pause()

    def all_matches_defined(self):
        for match in self.matches:
            if not match.attributes_are_not_none():
                return False
        return True
