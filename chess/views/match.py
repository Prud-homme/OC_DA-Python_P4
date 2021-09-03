from textwrap import dedent


def display_match_info(
        number,
        player1_name,
        score1,
        player2_name,
        score2) -> None:
    info = f'''
    Match {number}:
    > Player: {player1_name}
    Score: {score1}
    > Player: {player2_name}
    Score: {score2}
    '''
    print(dedent(info))


def display_match_generation(number, player1_name, player2_name) -> None:
    print(f'Match {number}: {player1_name} <> {player2_name}')
