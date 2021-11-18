def display_menu() -> str:
    """Display the app main menu and return the choice"""
    menu = """\x1b[32m♟️ Main menu ♟️\x1b[0m
1: Tournaments menu
2: Report and statistics
3: Edit a player rank
0: Exit
\x1b[32m> Select an option: \x1b[0m"""
    return input(menu)
