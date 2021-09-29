def display_menu_add_player() -> int:
    menu = """>>> Add a player <<<
1: Add by id
2: Add by name
3: Create a new player and add it
0: Don't add any more players
> Select an option: """
    choice = input(menu)

    if choice.isdecimal() and int(choice) <= 3:
        return int(choice)
    else:
        print("Incorrect entry, please try again.")
        return display_menu_add_player()


def display_search_result(result) -> int:
    """Display the players found from a search and return the selected player number"""
    if len(result) == 0:
        print("No players found.")
        return None
    print(f"Number of players found: {len(result)}")
    i = 0
    for elt in result:
        print(f'{i}: {elt["name"]}, {elt["birthdate"]}')
        i += 1
    choice = input("> Select a player: ")
    if choice.isdecimal() and int(choice) < i:
        return int(choice)
    else:
        print("Incorrect entry, please try again.")
        return display_search_result(result)


def enter_player_id() -> int:
    """Ask and return the player ranking"""
    player_id = input("> Enter a player id: ")
    if player_id.isdecimal() and int(player_id) > 0:
        return int(player_id)
    else:
        print("Incorrect entry, please try again.")
        return enter_player_id()


def enter_player_firstname(search=False) -> str:
    """Ask and return the player firstname"""
    info = {True: "Press Enter to not filter by firstname.\n", False: ""}
    firstname = input(f"{info[search]}> Enter a first name: ")

    if len(firstname) > 0 or search:
        return firstname
    else:
        print("Incorrect entry, please try again.")
        return enter_player_firstname()


def enter_player_lastname(search=False) -> str:
    """Ask and return the player lastname"""
    info = {True: "Press Enter to not filter by lastname.\n", False: ""}
    lastname = input(f"{info[search]}> Enter a last name: ")

    if len(lastname) > 0 or search:
        return lastname
    else:
        print("Incorrect entry, please try again.")
        return enter_player_lastname()


def enter_player_gender() -> str:
    """Ask and return the player gender"""
    gender = input("> Enter a gender (M/F): ")
    if gender.upper() in ["M", "F"]:
        return gender.upper()
    else:
        print("Incorrect entry, please try again.")
        return enter_player_gender()


def enter_player_ranking() -> int:
    """Ask and return the player ranking"""
    ranking = input("> Enter a ranking: ")
    if ranking.isdecimal() and int(ranking) > 0:
        return int(ranking)
    else:
        print("Incorrect entry, please try again.")
        return enter_player_ranking()


def define_new_player():  # -> tuple ?
    print("--- Add a new Player ---")
    firstname = prompt_firstname()
    lastname = prompt_lastname()

    print("> Enter birth date")
    year = enter_a_year()
    month = enter_a_month()
    day = enter_a_day(year, month)
    birthdate = "/".join((year, month, day))

    gender = prompt_gender()
    ranking = prompt_ranking()
    return firstname, lastname, birthdate, gender, ranking
