class Match:
    def __init__(self, **kwargs) -> None:
        """"""
        self.match = kwargs.get("match", ([None, None], [None, None]))

    def __str__(self) -> None:
        if self.match == ([None, None], [None, None]):
            return "Undefined match"
        [player1, score1], [player2, score2] = self.match
        return f"""{player1} got {score1} point and {player2} got {score2} points."""

    def __repr__(self) -> None:
        return f"Match(match={self.match})"

    def attributes_are_not_none(self):
        if self.match == None:
            return False
        [player1, score1], [player2, score2] = self.match
        return None not in (player1, score1, player2, score2)

    def display(self):
        if self.attributes_are_not_none():
            print(f"Match: {self.__str__()}")
        else:
            print(
                "The match is not correctly defined, try again after completing his information"
            )

    @staticmethod
    def serializing_matchs(matchs):
        #return {"matchs": [match.match for match in matchs]}
        return [match.match for match in matchs]

    @staticmethod
    def unserializing_matchs(serial_matchs):
        return [Match(match=match) for match in serial_matchs["matchs"]]

    @staticmethod
    def list_players(matchs):
        players_list = []
        for match in matchs:
            [player1, score1], [player2, score2] = match.match
            players_list.append((player1, player2))

        return players_list
