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




def enter_player(players_id)->int:
    player_id = input(f'''Enter the player id (accepted id: {', '.join([str(p_id) for p_id in players_id])}): ''')
    if player_id.isdecimal() and player_id in players_id:
        return int(player_id)
    else:
        print('Incorrect entry, please try again.')
        return enter_player(players_id)


def enter_score(score_values)->int:
    score = input(f'''Enter the score (accepted value: {', '.join(score_values)}): ''')
    if score.isdecimal():
        return int(score)
    elif score in score_values:
        return 0.5
    else:
        print('Incorrect entry, please try again.')
        return enter_score(score_values)

def enter_match_result_1(players_id:list, score_values:list):
    accepted_players = players_id

    player1 = enter_player(accepted_players)
    score1 = enter_score(score_values)
    accepted_players.remove(player1)

    player2 = enter_player(accepted_players)
    accepted_players.remove(player2)
    score2 = enter_score(score_values)
'''
def enter_match_result_1(players_id:list, players_id_with_name:dict, score_values:list):
    accepted_players = players_id

    player1 = enter_player(accepted_players)
    score1 = enter_score(score_values)
    accepted_players.remove(player1)

    player2 = enter_player(accepted_players)
    accepted_players.remove(player2)
    score2 = enter_score(score_values)
'''
