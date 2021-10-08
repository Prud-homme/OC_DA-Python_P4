import copy


def pause():
    programPause = input("\x1b[35mPress the <ENTER> key to continue...\x1b[0m")


class Match:
    def __init__(self, **kwargs) -> None:
        """"""
        self.match = kwargs.get("match", ([None, None], [None, None]))

    def __str__(self) -> None:
        if self.match == ([None, None], [None, None]):
            return "Undefined match"
        [player1, score1], [player2, score2] = self.match
        return f"""{' '.join((player1.firstname, player1.lastname))} got {score1} point
{' '.join((player2.firstname, player2.lastname))} got {score2} point"""

    def __repr__(self) -> None:
        return f"Match(match={self.match})"

    def attributes_are_not_none(self):
        if self.match == None:
            return False
        [player1, score1], [player2, score2] = self.match
        return None not in (player1, score1, player2, score2)

    def display(self):
        if self.attributes_are_not_none():
            print(f"\x1b[32m>>> Match <<<\x1b[0m\n{self.__str__()}")
        else:
            print(
                "The match is not correctly defined, try again after completing his information"
            )

    def serializing(self, player_object):
        [player1, score1], [player2, score2] = self.match
        return [player1.serializing(), score1], [player2.serializing(), score2]

    @staticmethod
    def serializing_matchs(matchs, player_object):
        # return {"matchs": [match.match for match in matchs]}
        # breakpoint()
        return [match.serializing(player_object) for match in matchs]

    @staticmethod
    def unserializing_matchs(serial_matchs, player_object):
        unserial_matchs = []

        for serial_match in serial_matchs:
            player1 = copy.copy(player_object)
            player2 = copy.copy(player_object)
            [serial_player1, score1], [serial_player2, score2] = serial_match
            ##breakpoint()
            player1.unserializing(serial_player1)
            player2.unserializing(serial_player2)
            ##breakpoint()
            unserial_matchs.append(Match(match=([player1, score1], [player2, score2])))
            # breakpoint()
        return unserial_matchs

    def get_players(self):
        [player1, score1], [player2, score2] = self.match
        return player1, player2

    def get_serial_players(self):
        [player1, score1], [player2, score2] = self.match
        return player1.serializing(), player2.serializing()

    @staticmethod
    def display_matchs(generated_matchs, no_number=False):
        message = ""
        if len(generated_matchs) == 0:
            return None
        number = 1
        for match in generated_matchs:
            (player1, player2) = match
            if None in (
                player1.firstname,
                player1.lastname,
                player2.firstname,
                player2.lastname,
            ):
                return None
            if no_number:
                message += "- "
            else:
                message += f"""{number}: """
            message += f"""[Match] {' '.join((player1.firstname, player1.lastname))} VS {' '.join((player2.firstname, player2.lastname))}\n"""
            number += 1

        return message[:-1]

    @staticmethod
    def match_already_registered(players_pair, matchs_list):
        for match in matchs_list:
            [player1, score1], [player2, score2] = match.match
            match_players_pair = (player1.serializing(), player2.serializing())
            if (
                players_pair[0].serializing() in match_players_pair
                and players_pair[1].serializing() in match_players_pair
            ):
                return True
        return False

    @staticmethod
    def display_only_matchs(turns_list):
        for turn in turns_list:
            print(f"\x1b[32m>>> {turn.name} <<<\x1b[0m")
            for match in turn.matchs:
                match.display()
        pause()
