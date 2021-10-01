import operator


def generate_pairs_swiss_system(players, **kwargs):
    """generation des pairs"""
    rankings = kwargs.get("rankings", None)
    scores = kwargs.get("scores", None)
    previous_matchs = kwargs.get("previous_matchs", [])

    players_index = [*range(len(players))]
    if scores != None and len(players) == len(scores) and len(players) % 2 == 0:
        sort_scores, sort_index = zip(*sorted(zip(scores, players_index), reverse=True))

    elif rankings != None and len(players) == len(rankings) and len(players) % 2 == 0:
        sort_rankings, sort_index = zip(
            *sorted(zip(rankings, players_index), reverse=False)
        )

    else:
        return None

    sort_players = operator.itemgetter(*sort_index)(players)

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
            for j in [player for player in bottom_index if player not in player_paired]:
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

        elif len(pair_players_matchs) != nb_matchs and position_bottom == nb_matchs - 1:
            position_top += 1
            position_bottom = 0
            pair_players_matchs = []
            player_paired = []
            bottom_index = list(range(nb_matchs))
            top_index = list(range(nb_matchs))
            top_index.insert(0, top_index.pop(position_top))

    return pair_players_matchs
