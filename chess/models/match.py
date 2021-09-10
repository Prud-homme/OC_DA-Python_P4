class Match:
    def __init__(self, **kwargs) -> None:
        ''''''
        player1 = kwargs.get('player1', None)
        score1 = kwargs.get('score1', None)
        player2 = kwargs.get('player2', None)
        score2 = kwargs.get('score2', None)
        self.match = ([player1, score1], [player2, score2])

    def __str__(self) -> None:
        [player1, score1], [player2, score2] = self.match
        return f'''The match was between {player1} and {player2}.
{player1} got {score1} point and {player2} got {score2} points.'''.replace('\n', ' ')

    def __repr__(self) -> None:
        [player1, score1], [player2, score2] = self.match
        return f'''Match(player1='{player1}', score1='{score1}', 
player2='{player2}', score1='{score2}')'''.replace('\n', ' ')

    def attributes_are_not_none(self):
        [player1, score1], [player2, score2] = self.match
        return None in (player1, score1, player2, score2)

    def display(self)
        if self.attributes_are_not_none():
            print(f'\n{self.__str__()}\n')
        else:
            print('The match is not correctly defined, try again after completing his information')

    @staticmethod
    def serializing_matchs(matchs):
        return {'matchs': [match.match for match in matchs]}

    @staticmethod
    def unserializing_matchs(serial_matchs):
        return [Match(player1=p1,score1=s1,player2=p2,score2=s2) for ([p1,s1],[p2,s2]) in serial_matchs['matchs']]

