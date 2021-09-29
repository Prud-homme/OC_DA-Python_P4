def generate_pairs_swiss_system(players, **kwargs):
    """generation des pairs"""
    rankings = kwargs.get("rankings", None)
    scores = kwargs.get("scores", None)
    previous_matches = kwargs.get("previous_matches", [])

    if scores != None and len(players) == len(scores) and len(players) % 2 == 0:
        sort_scores, sort_players = zip(*sorted(zip(scores, players), reverse=True))

    elif rankings != None and len(players) == len(rankings) and len(players) % 2 == 0:
        sort_rankings, sort_players = zip(
            *sorted(zip(rankings, players), reverse=False)
        )

    else:
        return None

    nb_matchs = int(len(players) / 2)
    top_players_list = players[:nb_matchs]
    bottom_players_list = players[nb_matchs:]

    pair_players_matchs = []
    player_paired = []

    top_index = list(range(nb_matchs))
    bottom_index = list(range(nb_matchs))
    position_top = position_bottom = 0

    while len(pair_players_matchs) != nb_matchs and position_top < nb_matchs:
        for i in top_index:
            for j in [player for player in bottom_index if player not in player_paired]:
                pair_players = (top_players_list[i], bottom_players_list[j])

                if pair_players not in previous_matches:
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


if __name__ == "__main__":
    players = [1, 2, 3, 4, 5, 6, 7, 8]
    rankings = [10, 20, 30, 40, 50, 60, 70, 80]

    print(">> No previous match <<")
    generate_pairs_swiss_system(players, rankings=rankings)

    previous_matches = [(1, 5)]
    print(">> ", previous_matches, " <<")
    generate_pairs_swiss_system(
        players, rankings=rankings, previous_matches=previous_matches
    )

    previous_matches = [(2, 6)]
    print(">> ", previous_matches, " <<")
    generate_pairs_swiss_system(
        players, rankings=rankings, previous_matches=previous_matches
    )

    previous_matches = [(3, 7)]
    print(">> ", previous_matches, " <<")
    generate_pairs_swiss_system(
        players, rankings=rankings, previous_matches=previous_matches
    )

    previous_matches = [(4, 8)]
    print(">> ", previous_matches, " <<")
    generate_pairs_swiss_system(
        players, rankings=rankings, previous_matches=previous_matches
    )

    previous_matches = [(1, 5), (2, 6)]
    print(">> ", previous_matches, " <<")
    generate_pairs_swiss_system(
        players, rankings=rankings, previous_matches=previous_matches
    )

    previous_matches = [(1, 5), (2, 6), (3, 7)]
    print(">> ", previous_matches, " <<")
    generate_pairs_swiss_system(
        players, rankings=rankings, previous_matches=previous_matches
    )

    previous_matches = [(1, 5), (2, 6), (3, 7), (4, 8)]
    print(">> ", previous_matches, " <<")
    generate_pairs_swiss_system(
        players, rankings=rankings, previous_matches=previous_matches
    )

    previous_matches = [(1, 5), (1, 6), (1, 7), (1, 8)]
    print(">> ", previous_matches, " <<")
    generate_pairs_swiss_system(
        players, rankings=rankings, previous_matches=previous_matches
    )

    previous_matches = [(4, 5), (4, 6), (4, 7), (4, 8)]
    print(">> ", previous_matches, " <<")
    generate_pairs_swiss_system(
        players, rankings=rankings, previous_matches=previous_matches
    )

    previous_matches = [(2, 5), (2, 6), (2, 8)]
    print(">> ", previous_matches, " <<")
    generate_pairs_swiss_system(
        players, rankings=rankings, previous_matches=previous_matches
    )

    previous_matches = [(3, 5), (3, 7), (3, 8)]
    print(">> ", previous_matches, " <<")
    generate_pairs_swiss_system(
        players, rankings=rankings, previous_matches=previous_matches
    )

    previous_matches = [(4, 5), (4, 7), (4, 8)]
    print(">> ", previous_matches, " <<")
    generate_pairs_swiss_system(
        players, rankings=rankings, previous_matches=previous_matches
    )
