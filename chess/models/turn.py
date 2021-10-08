import operator
from datetime import datetime
from typing import Optional  # , NewType, Tuple, List

# TournamentMatch = NewType('TournamentMatch', Tuple[List[int,int],List[int,int]])


def pause():
    programPause = input("\x1b[35mPress the <ENTER> key to continue...\x1b[0m")


class Turn:
    def __init__(self, **kwargs) -> None:
        """"""
        self.name = kwargs.get("name", None)
        self.start_date = kwargs.get("start_date", self.get_current_time())
        self.end_date = kwargs.get("end_date", None)
        self.matchs = kwargs.get("matchs", [])

    def __str__(self) -> None:
        end_string = {True: f" and ended on {self.end_date}.", False: "."}
        return f"""{self.name} started on {self.start_date}{end_string[self.end_date!=None]}"""

    def __repr__(self) -> None:
        return f"""Turn(name='{self.name}', start_date='{self.start_date}', end_date='{self.end_date}', matchs={self.matchs})"""

    def add_match(self, match: tuple) -> None:
        """"""
        self.matchs.append(match)

    def stop_turn(self) -> None:
        """"""
        self.end_date = self.get_current_time()

    def serializing(self, match_object, player_object) -> dict:
        """"""
        # breakpoint()
        test = {
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "matchs": match_object.serializing_matchs(self.matchs, player_object),
        }
        # breakpoint()
        return test

    def unserializing(self, serial_turn: dict, unserial_matchs: list) -> None:
        """"""
        self.name = serial_turn["name"]
        self.start_date = serial_turn["start_date"]
        self.matchs = unserial_matchs
        self.end_date = serial_turn["end_date"]

    def display(self):
        if self.name != None:
            print(f"{self.__str__()}")

            if len(self.matchs) > 0:
                # match_number = 1
                for match in self.matchs:
                    match.display()
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
    def serializing_turns(match_object, player_object, turns):
        # return {
        #     "turns": [
        #         turn.serializing(match_object.serializing_matchs(turn.matchs))
        #         for turn in turns
        #     ]
        # }
        ##breakpoint()
        return [turn.serializing(match_object, player_object) for turn in turns]

    @staticmethod
    def unserializing_turns(match_object, player_object, serial_turns):
        turns = []
        # breakpoint()
        for serial_turn in serial_turns:
            # #breakpoint()
            name, start_date, end_date = (
                serial_turn["name"],
                serial_turn["start_date"],
                serial_turn["end_date"],
            )
            matchs = match_object.unserializing_matchs(
                serial_turn["matchs"], player_object
            )
            # breakpoint()
            turns.append(
                Turn(name=name, start_date=start_date, end_date=end_date, matchs=matchs)
            )
        return turns

    def list_players_pair_complete(self):
        return [match.get_players() for match in self.matchs]

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
    def generate_pairs_swiss_system(players, **kwargs):
        """generation des pairs"""
        previous_matchs = kwargs.get("previous_matchs", [])
        sort_players = Turn().sort_players_swiss_system(players, **kwargs)

        nb_matchs = int(len(players) / 2)
        top_players_list = sort_players[:nb_matchs]
        bottom_players_list = sort_players[nb_matchs:]

        pair_players_matchs = []
        player_paired = []

        top_index = list(range(nb_matchs))
        bottom_index = list(range(nb_matchs))
        position_top = position_bottom = 0
        while len(pair_players_matchs) != nb_matchs and position_top < nb_matchs:
            for i in top_index:
                for j in [
                    player for player in bottom_index if player not in player_paired
                ]:
                    pair_players = (top_players_list[i], bottom_players_list[j])

                    if (
                        top_players_list[i].serializing(),
                        bottom_players_list[j].serializing(),
                    ) not in previous_matchs and (
                        bottom_players_list[j].serializing(),
                        top_players_list[i].serializing(),
                    ) not in previous_matchs:
                        pair_players_matchs.append(pair_players)
                        player_paired.append(j)
                        break

                    elif i == top_index[0] and j == bottom_index[-1]:
                        return None

            if (
                len(pair_players_matchs) != nb_matchs
                and j == bottom_index[-1]
                and position_bottom < nb_matchs - 1
            ):
                position_bottom += 1
                pair_players_matchs = []
                player_paired = []
                bottom_index = list(range(nb_matchs))
                bottom_index.insert(0, bottom_index.pop(position_bottom))

            elif (
                len(pair_players_matchs) != nb_matchs
                and position_bottom == nb_matchs - 1
            ):
                position_top += 1
                position_bottom = 0
                pair_players_matchs = []
                player_paired = []
                bottom_index = list(range(nb_matchs))
                top_index = list(range(nb_matchs))
                top_index.insert(0, top_index.pop(position_top))

        return pair_players_matchs

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
