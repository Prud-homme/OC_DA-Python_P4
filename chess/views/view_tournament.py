def display_tournament_menu():
    """Display the tournament menu and return the choice"""
    menu = f"""---  Tournaments menu ---
1: New tournament
2: Load a tournament
3: Resume a tournament
0: Main menu
> Select an option: """
    choice = input(menu)
    return choice


def display_menu_load_tournament():
    """Display the load menu and return the choice"""
    menu = """>>> Load a tournament <<<
1: Search by name
2: Search by location
0: Cancel
> Select an option: """
    choice = input(menu)
    return choice


# def display_menu_resume_tournament(
#         tournament_name: str,
#         all_players_defined: bool,
#         turn_in_memory: bool,
#         exist_turns: bool):
#     """Display the resume menu and return the choice"""
#     menu_state = {
#         (True, True, True): f'\n3: View turns complete\n4: View current matchs\n5: Complete a turn',
#         (True, True, False): f'\n3: View current matchs\n4: Complete a turn',
#         (True, False, True): f'\n3: View turns complete\n4: Start a turn',
#         (True, False, False): f'\n3: Start a turn',
#         (False, False, False): 'already defined\n3: Add players'
#     }
#     menu = f'''
# 	--- Tournament: {tournament_name} ---
# 	1: View tournament informations
# 	2: View players {menu_state[(all_players_defined, turn_in_memory, exist_turns)]}
# 	0: Return to tournament menu
# 	> Select an option: '''
#     menu = dedent(menu)
#     choice = input(menu)

#     last_choice = {(True, True): 5, (True, False): 3, (False, False): 3}
#     if choice.isdecimal() and int(
#             choice) <= last_choice[(all_players_defined, exist_turns)]:
#         if int(choice) == 0:
#             print('>>> Return to tournament menu <<<')
#         return int(choice)
#     else:
#         print('Incorrect entry, please try again.')
#         return display_menu_resume_tournament()


def display_menu_resume_tournament(tournament_name: str):
    """Display the resume menu and return the choice"""
    menu = f"""--- Tournament: {tournament_name} ---
1: View tournament informations
2: Start a turn
3: Current matchs
4: Complete a turn
0: Return to tournament menu
> Select an option: """
    choice = input(menu)
    return choice


def enter_tournament_choice(result):
    """Display the tournaments found from a search and return the selected tournament number"""
    """
    if len(result) == 0:
        print('No tournament found.')
        return None
    """
    print(f"Number of tournaments found: {len(result)}")
    i = 0
    for elt in result:
        print(f'{i}: {elt["name"]}, {elt["location"]}, {elt["date"]}')
        i += 1

    return input("> Select a tournament: ")
    """
    if choice.isdecimal() and int(choice) < i:
        return int(choice)
    else:
        print('Incorrect entry, please try again.')
        return display_search_result(result)
    """


def entry_request(message):
    return input(message)


def enter_tournament_name():
    """Ask and return the tournament name"""
    return input("> Enter a tournament name: ")
    """
    if len(name) > 0:
        return name
    else:
        print('Incorrect entry, please try again.')
        return enter_tournament_name()
    """


def enter_tournament_location():
    """Ask and return the tournament location"""
    return input("> Enter a location: ")

    """
    if len(location) > 0:
        return location
    else:
        print('Incorrect entry, please try again.')
        return enter_tournament_location()
    """


"""
def enter_tournament_date():
    print('> Enter a tournament date')
    year = enter_a_year()
    month = enter_a_month()
    day = enter_a_day(year, month)
    date = '/'.join((year, month, day))
"""


def enter_tournament_description():
    """Ask and return the tournament description"""
    return input("> Enter a description: ")


def enter_tournament_time_control(time_controls: list):
    """Ask and return the tournament time control"""
    return input(f'> Enter a time control ({", ".join(time_controls)}): ')
    """
    if time_control.lower() in time_controls:
        return time_control.lower()
    else:
        print('Incorrect entry, please try again.')
        return enter_tournament_time_control(time_controls)
    """


def enter_tournament_turns_number():
    """Ask and return the number of turns of the tournament"""
    return input("> Enter a number of turns (press Enter for 4 turns): ")
    """
    if len(turns_number) == 0:
        return 4
    elif turns_number.isdecimal():
        return int(turns_number)
    else:
        print('Incorrect entry, please try again.')
        return enter_tournament_turns_number()
    """


def enter_tournament_players_number():
    """Ask and return the number of players of the tournament"""
    return input("> Enter a number of players (press Enter for 8 players): ")

    """
    if len(players_number) == 0:
        return 8
    elif players_number.isdecimal():
        return int(players_number)
    else:
        print('Incorrect entry, please try again.')
        return enter_tournament_players_number()
    """


def enter_tournament_date():
    return input("> Enter a tournament date(yyyy-mm-dd hh:mm): ")


'''
def define_new_tournament(time_controls: list):  # -> tuple ?
    """Ask and return all the information necessary for the creation of a tournament"""
    print('--- New tournament ---')
    name = enter_tournament_name()
    location = enter_tournament_location()

    print('> Enter a tournament date')
    year = enter_a_year()
    month = enter_a_month()
    day = enter_a_day(year, month)
    date = '/'.join((year, month, day))

    description = enter_tournament_description()
    time_control = enter_tournament_time_control(time_controls)
    turns_number = enter_tournament_turns_number()
    players_number = enter_tournament_players_number()

    return name, location, date, description, time_control, turns_number, players_number
'''

# display_menu_load_tournament()
# print('hello')
