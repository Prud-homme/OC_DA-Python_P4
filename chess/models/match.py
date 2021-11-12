from __future__ import annotations
import sys
import os

modelsdir = os.path.dirname(os.path.realpath(__file__))
chessdir = os.path.dirname(modelsdir)
sys.path.append(chessdir)
from logger import logger
from models.player import Player
from typing import Optional, Union


class Match:
    """
    A match is a tuple of two elements.
    Each element is a list containing the instance of a player
    and his score in this match.
    """

    def __init__(self, **kwargs) -> None:
        self.match: tuple[list[Union[Player, float], list[Union[Player, float]]]] = kwargs.get(
            "match", ([None, None], [None, None])
        )

    def __str__(self) -> Optional[str]:
        if not self.is_well_defined():
            logger.error("Match not well defined: unable to create a readable string")
            return f"Match(match={self.match})"
        [player1, score1], [player2, score2] = self.match
        player1_name = " ".join((player1.firstname, player1.lastname))
        player2_name = " ".join((player2.firstname, player2.lastname))
        score_display = {0.0: 0, 1.0: 1, 0.5: 0.5}

        if None in (score1, score2):
            return f"{player1_name} VS {player2_name}"
        return f"""{player1_name} got {score_display[score1]} point and
{player2_name} got {score_display[score2]} point""".replace(
            "\n", " "
        )

    def __repr__(self) -> str:
        return f"Match(match={self.match})"

    def attributes_are_not_none(self) -> bool:
        """Return a bool linked to the presence of a None in the information of a match"""
        [player1, score1], [player2, score2] = self.match
        return None not in (player1, score1, player2, score2)

    def is_well_defined(self) -> bool:
        """
        Assigning scores and player instances of a match in variables.
        Checks if the players are player instances and the scores are float or int.
        The score can also be None if the match did not take place.
        Return a boolean according to the result of the checks.
        """
        try:
            well_defined = True
            [player1, score1], [player2, score2] = self.match

            if not type(player1) == Player:
                logger.error("Match not well defined: the first player must be a player instance.")
                well_defined = False

            if type(score1) not in (float, int) and score1 is not None:
                logger.error(
                    """Match not well defined:
the first score must be a float or int or defined as None."""
                ).replace("\n", " ")
                well_defined = False

            if not type(player2) == Player:
                logger.error("Match not well defined: the second player must be a player instance.")
                well_defined = False

            if type(score2) not in (float, int) and score2 is not None:
                logger.error(
                    """Match not well defined:
the second score must be a float or int or defined as None"""
                ).replace("\n", " ")
                well_defined = False

            return well_defined

        except Exception as e:
            logger.error(e)
            return False

    def display(self) -> Optional[str]:
        """Return a string containing a printable description of the object"""
        if not self.is_well_defined():
            logger.error("Match not well defined: unable to display")
            return None
        [player1, score1], [player2, score2] = self.match
        return f"\x1b[32m[Match] \x1b[0m{self.__str__()}"

    def serializing(self) -> Optional[SerializedMatch]:
        """Serialization of the object for export in json"""
        if not self.is_well_defined():
            logger.error("Match not well defined: unable to serialize")
            return None
        [player1, score1], [player2, score2] = self.match
        return [player1.serializing(), score1], [player2.serializing(), score2]

    def get_players(self) -> tuple[Player, Player]:
        """
        Assigning scores and player instances of a match in variables.
        Returns the instance of each of the two players
        """
        if not self.is_well_defined():
            logger.error("Match not well defined: impossible to return player instances")
            return None
        [player1, score1], [player2, score2] = self.match
        return player1, player2

    def edit_scores(self, score1: float, score2: float) -> None:
        """
        From two input scores, the function changes the score of the match instance.
        score1 is the score of the first player (cf. first element of the tuple).
        score2 is the score of the second player (cf. second element of the tuple).
        """
        if not self.is_well_defined():
            logger.error("Match not well defined: impossible to return player instances")
            return None
        self.match[0][1] = score1
        self.match[1][1] = score2
        logger.info("The scores have been modified")

    def get_serial_players(self) -> Optional[tuple[SerializedPlayer, SerializedPlayer]]:
        """
        Assigning scores and player instances of a match in variables.
        Returns the serialized instance of each of the two players.
        """
        if not self.is_well_defined():
            logger.error("Match not well defined: impossible to return serialized player instances")
            return None
        [player1, score1], [player2, score2] = self.match
        return player1.serializing(), player2.serializing()

    @staticmethod
    def serializing_matches(matches: list[Match]) -> Optional[list[SerializedMatch]]:
        """
        From a list of matches, the function serializes the matches
        and creates a new list containing the matches serialized.
        """
        serial_matches = []
        for match in matches:
            if type(match) != Match and not match.is_well_defined():
                logger.error("Match not well defined: impossible to return the list of serialized matches")
                return None
            serial_matches.append(match.serializing())
        return serial_matches

    @staticmethod
    def unserializing_matches(
        serial_matches: list[SerializedMatch],
    ) -> Optional[list[Match]]:
        """
        From a list of unserialized matches, the function unserializes
        the matches and creates a new list containing the match instances.
        """
        unserial_matches = []

        for serial_match in serial_matches:
            player1 = Player()
            player2 = Player()

            [serial_player1, score1], [serial_player2, score2] = serial_match
            player1.unserializing(serial_player1)
            player2.unserializing(serial_player2)
            match = Match(match=([player1, score1], [player2, score2]))

            if type(match) != Match and not match.is_well_defined():
                logger.error(
                    """Match not well defined:
impossible to unserialized a match and return the unserialized match list."""
                ).replace("\n", " ")
                return None

            unserial_matches.append(match)
        return unserial_matches

    @staticmethod
    def display_matches_choice(turn: Turn) -> str:
        """
        Create and return a printable menu to select a match
        via its associated number.
        """
        message = f"\n\x1b[32m♟️ {turn.name} ♟️\x1b[0m"
        cpt = 1
        for match in turn.matches:
            message += f"\n{cpt}: {match.__str__()}"
            cpt += 1
        return message

    @staticmethod
    def match_already_registered(players_pair: tuple[Player, Player], matches_list: list[Match]) -> bool:
        """Checks if the proposed match has been played previously or not"""
        for match in matches_list:
            [player1, score1], [player2, score2] = match.match
            match_players_pair = (player1.serializing(), player2.serializing())
            if (
                players_pair[0].serializing() in match_players_pair
                and players_pair[1].serializing() in match_players_pair
            ):
                return True
        return False

    @staticmethod
    def display_only_matches(turns_list: list[Turn]) -> str:
        """
        Create and return a printable message
        that contains the list of matches already defined
        """
        message = ""
        for turn in turns_list:
            message += Match().display_matches_choice(turn)
        return message
