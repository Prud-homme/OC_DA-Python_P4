def display_menu_tournament_main() -> str:
    """Display the tournament menu and return the choice"""
    menu = """\x1b[32m♟️  Tournament - Menu ♟️\x1b[0m
1: New tournament
2: Load a tournament
3: Resume a tournament
0: Main menu
\x1b[32m> Select an option: \x1b[0m"""
    return input(menu)


def display_menu_tournament_resume() -> str:
    """Display the load menu and return the choice"""
    menu = """\x1b[32m♟️ Tournament - Resume ♟️\x1b[0m
1: View tournament informations
2: Start a turn
3: Current matches
4: Complete a match
5: Complete a turn
0: Save and return to tournament menu
\x1b[32m> Select an option: \x1b[0m"""
    return input(menu)


def display_menu_tournament_lack_players() -> str:
    """Display the load menu and return the choice"""
    menu = """\x1b[32m♟️ Tournament - Resume ♟️\x1b[0m
1: View tournament informations
2: Add players to the tournament
0: Save and return to tournament menu
\x1b[32m> Select an option: \x1b[0m"""
    return input(menu)


def display_menu_tournament_complete() -> str:
    """Display the load menu and return the choice"""
    menu = """\x1b[32m♟️ Tournament - Resume ♟️\x1b[0m
1: View tournament informations
0: Return to tournament menu
\x1b[32m> Select an option: \x1b[0m"""
    return input(menu)
