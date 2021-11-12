def display_menu_add_player() -> str:
    """
    Selection menu for adding a player.
    Returns the choice between searching the player database
    or inserting a new player.
    """
    menu = """\x1b[32m♟️ Add a player ♟️\x1b[0m
1: Search by name
2: Create a new player and add it
0: Don't add any more players
\x1b[32m> Select an option: \x1b[0m"""
    return input(menu)
