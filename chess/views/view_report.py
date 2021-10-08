def display_menu_report():
    menu = f"""\x1b[32m>>> Report and statistics <<<\x1b[0m
1: List of all players
2: List of all tournaments
3: About a tournament
0: Main menu
\x1b[32m> Select an option: \x1b[0m"""
    return input(menu)


def display_menu_report_player_filter():
    menu = """\x1b[32m>>> Filter by <<<\x1b[0m
1: Rank
2: Alphabetical order
0: Show report
\x1b[32m> Select an option: \x1b[0m"""
    return input(menu)


# def display_menu_report_tournament_filter():
#     menu = """>>> Filter by <<<
# 	1: Rank
# 	2: Alphabetical order
# 	0: Show report
# 	"""
# 	return input(menu)


# def display_menu_search_tournament():
#     menu = """ >>> Search a tournament <<<
# 	> Research: """
#     return input(menu)


def display_menu_report_tournament():
    menu = f"""\x1b[32m>>> Report and statistics - Tournament <<<\x1b[0m
1: List of all player
2: List of all turns
3: List of all matchs
0: Main menu
\x1b[32m> Select an option: \x1b[0m"""
    return input(menu)
