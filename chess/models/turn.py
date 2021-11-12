from __future__ import annotations
import operator
from datetime import datetime
import sys, os

modelsdir = os.path.dirname(os.path.realpath(__file__))
chessdir = os.path.dirname(modelsdir)
sys.path.append(chessdir)
from models.match import Match
from utils import pause
from logger import logger
from typing import Optional


class Turn:
    """
    A turn is composed of 4 atttributes, 3 strings
    about the name, start and end date of the tour
    and a list of matches.
    """

    def __init__(self, **kwargs) -> None:
        self.name: str = kwargs.get("name", None)
        self.start_date: str = kwargs.get("start_date", self.get_current_time())
        self.end_date: str = kwargs.get("end_date", None)
        self.matches: list[Match] = kwargs.get("matches", [])

    def __str__(self) -> str:
        end_string = {True: f" and ended on {self.end_date}.", False: "."}
        return f"{self.name} started on {self.start_date}{end_string[self.end_date!=None]}"

    def __repr__(self) -> str:
        return f"""Turn(name='{self.name}',
start_date='{self.start_date}', end_date='{self.end_date}',
matches={self.matches})""".replace(
            "\n", " "
        )

    def add_match(self, match: Match) -> None:
        """Add a match to turn"""
        self.matches.append(match)

    def stop_turn(self) -> None:
        """Generate and set end date of turn"""
        self.end_date = self.get_current_time()

    def serializing(self) -> SerializedTurn:
        """Serialization of the turn instance in order to export it to json format"""
        return {
            "name": self.name,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "matches": Match().serializing_matches(self.matches),
        }

    def unserializing(self, serial_turn: SerializedTurn, unserial_matches: list[Match]) -> None:
        """Transform the serialized data of a turn into a turn instance"""
        self.name = serial_turn["name"]
        self.start_date = serial_turn["start_date"]
        self.matches = unserial_matches
        self.end_date = serial_turn["end_date"]

    def display(self) -> str:
        """Return a string containing a printable description of the object"""
        if self.name != None:
            message = f"\n{self.__str__()}"

            if len(self.matches) > 0:
                for match in self.matches:
                    message += f"\n{match.display()}"
            else:
                message += "No match defined"
            return message

        else:
            logger.error("The turn is not correctly defined, try again after completing his information")
            pause()

    @staticmethod
    def get_current_time() -> str:
        """Retrieving of the current date and export to a specific str format"""
        now = datetime.now()
        return now.strftime("Date: %d/%m/%Y, Time: %H:%M")

    @staticmethod
    def serializing_turns(turns: list[Turn]) -> list[SerializedTurn]:
        """
        From a list of turns, the function serializes the turns
        and creates a new list containing the turns serialized.
        """
        return [turn.serializing() for turn in turns]

    @staticmethod
    def unserializing_turns(serial_turns: list[SerializedTurn]) -> list[Turn]:
        """
        From a list of unserialized turns, the function unserializes
        the turns and creates a new list containing the turn instances.
        """
        turns = []
        for serial_turn in serial_turns:
            turns.append(
                Turn(
                    name=serial_turn["name"],
                    start_date=serial_turn["start_date"],
                    end_date=serial_turn["end_date"],
                    matches=Match().unserializing_matches(serial_turn["matches"]),
                )
            )
        return turns

    def list_players_pair_complete(self) -> list[tuple[Player, Player]]:
        """Retrieves the player pair of each match from the match list of the instance"""
        return [match.get_players() for match in self.matches]

    @staticmethod
    def sort_players_swiss_system(players: list[Player], **kwargs) -> list[Player]:
        """Sorts a list of players according to their ranking or score"""
        rankings = kwargs.get("rankings", None)
        scores = kwargs.get("scores", None)

        players_index = [*range(len(players))]
        if scores != None and len(players) == len(scores) and len(players) % 2 == 0:
            sort_scores, sort_index = zip(*sorted(zip(scores, players_index), reverse=True))

        elif rankings != None and len(players) == len(rankings) and len(players) % 2 == 0:
            sort_rankings, sort_index = zip(*sorted(zip(rankings, players_index), reverse=False))

        else:
            return None

        return operator.itemgetter(*sort_index)(players)

    @staticmethod
    def pair_not_in_previous_matches(turns_list: list[Turn], pair_players: list[tuple[Player, Player]]) -> bool:
        """Check if the players have not already played against each other"""
        previous_matches = [match.get_serial_players() for turn in turns_list for match in turn.matches]
        return (pair_players[0].serializing(), pair_players[1].serializing(),) not in previous_matches and (
            pair_players[1].serializing(),
            pair_players[0].serializing(),
        ) not in previous_matches

    @staticmethod
    def pairing_swiss_system(
        players: list[Player],
        top_index: list[int],
        bottom_index: list[int],
        player_paired: list[int],
        top_players_list: list[Player],
        bottom_players_list: list[Player],
        turns_list: list[Turn],
        pair_players_matches: list[Match],
    ) -> Optional[tuple[list[Match], int]]:
        """Generates a list of matches according to the Swiss system"""
        for i in top_index:
            for j in [player for player in bottom_index if player not in player_paired]:
                pair_players = (top_players_list[i], bottom_players_list[j])
                if Turn().pair_not_in_previous_matches(turns_list, pair_players) or len(players) == 2:
                    pair_players_matches.append(
                        Match(
                            match=(
                                [top_players_list[i], None],
                                [bottom_players_list[j], None],
                            )
                        )
                    )
                    player_paired.append(j)
                    break

                elif i == top_index[0] and j == bottom_index[-1] and len(players) > 2:
                    return None
        return pair_players_matches, j

    @staticmethod
    def pairing_failed_swiss_system(
        position_top: int,
        position_bottom: int,
        pair_players_matches: list[Match],
        player_paired: list[int],
        nb_matches: int,
        j: int,
        bottom_index: list[int],
        top_index: list[int],
    ) -> tuple[int, int, list[Match], list[int], list[int], list[int]]:
        """
        Checks if the list of matches provided by the method pairing_swiss_system()
        contains the expected number of matches and if not, shifts a player
        to test new possibilities by making sure to respect the Swiss system
        as much as possible
        """
        if len(pair_players_matches) != nb_matches and j == bottom_index[-1] and position_bottom < nb_matches - 1:
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
    def generate_pairs_swiss_system(players: list[Player], **kwargs) -> Optional[list[Match]]:
        """
        Use methods sort_players_swiss_system(), pairing_swiss_system()
        and pairing_failed_swiss_system() to generate the match list
        according to the Swiss system if possible
        """
        if len(players) > 0 and len(players) % 2 != 0:
            return None

        turns_list = kwargs.get("turns_list", [])
        sort_players = Turn().sort_players_swiss_system(players, **kwargs)
        nb_matches = int(len(players) / 2)
        top_players_list = sort_players[:nb_matches]
        bottom_players_list = sort_players[nb_matches:]
        pair_players_matches, player_paired = [], []
        top_index, bottom_index = list(range(nb_matches)), list(range(nb_matches))
        position_top = position_bottom = 0

        while len(pair_players_matches) != nb_matches and position_top < nb_matches:

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
        return pair_players_matches

    @staticmethod
    def display_turns(turns_list: list[Turn]) -> str:
        """
        Return a string containing a printable message
        containing the information given by the display method of each turn
        """
        if len(turns_list) > 0:
            message = "\n\x1b[32m♟️ Tournament - List of turns ♟️\x1b[0m"
            for turn in turns_list:
                message += turn.display()
            return message
        else:
            return "\n\x1b[32m♟️ Tournament - No turn is defined ♟️\x1b[0m"

    @staticmethod
    def display_turns_without_match(turns_list: list[Turn]) -> str:
        """
        Return a string containing a printable message
        containing the information given by the __str__ method of each turn
        """
        if len(turns_list) > 0:
            message = f"\n\x1b[32m♟️ List of turns ♟️\x1b[0m"
            for turn in turns_list:
                message += turn.__str__()
            return message
        else:
            return f"\n\x1b[32m♟️ No turn is defined ♟️\x1b[0m"

    def all_matches_defined(self) -> bool:
        """Checks if the list of matches of the instance does not contain undefined data"""
        for match in self.matches:
            if not match.attributes_are_not_none():
                return False
        return True
