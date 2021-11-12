def display_menu_report() -> str:
    """Display the report menu and return the choice"""
    menu = f"""\x1b[32m♟️ Report and statistics ♟️\x1b[0m
1: List of all players
2: List of all tournaments
3: About a tournament
0: Main menu
\x1b[32m> Select an option: \x1b[0m"""
    return input(menu)


def display_menu_report_player_filter() -> str:
    """Display the filter menu for player and return the choice"""
    menu = """\x1b[32m♟️ Filter by ♟️\x1b[0m
1: Rank
2: Alphabetical order
0: Return to the previous menu
\x1b[32m> Select an option: \x1b[0m"""
    return input(menu)


def display_menu_report_tournament() -> str:
    """Display the menu for a specific tournament and return the choice"""
    menu = f"""\x1b[32m♟️ Report and statistics - Tournament ♟️\x1b[0m
1: List of all player
2: List of all turns
3: List of all matchs
4: See the final ranking
0: Report menu
\x1b[32m> Select an option: \x1b[0m"""
    return input(menu)
