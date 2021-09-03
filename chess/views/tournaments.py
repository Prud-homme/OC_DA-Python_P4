from textwrap import dedent

from .date import enter_a_day, enter_a_month, enter_a_year


def display_tournament_menu(tournament_in_memory: bool) -> int:
    """Display the tournament menu and return the choice"""
    resume = {True: '\n\t3: Resume a tournament', False: ''}
    last_choice = {True: 3, False: 2}

    menu = f'''
	---  Tournaments menu ---
	1: New tournament
	2: Load a tournament{resume[tournament_in_memory]}
	0: Main menu
	> Select an option: '''
    menu = dedent(menu)
    choice = input(menu)

    if choice.isdecimal() and int(choice) <= last_choice:
        if int(choice) == 0:
            print('>>> Return to main menu <<<')
        return int(choice)
    else:
        print('Incorrect entry, please try again.')
        return display_tournament_menu(tournament_in_memory)


def display_menu_load_tournament() -> int:
    """Display the load menu and return the choice"""
    menu = '''\t>>> Load a tournament <<<
	1: Search by name
	2: Search by location
	0: Cancel
	> Select an option: '''
    menu = dedent(menu)
    choice = input(menu)

    if choice.isdecimal() and int(choice) <= 2:
        if int(choice) == 0:
            print('>>> Return to tournament menu <<<')
        return int(choice)
    else:
        print('Incorrect entry, please try again.')
        return display_menu_load_tournament()


def display_menu_resume_tournament(
        tournament_name: str,
        all_players_defined: bool,
        turn_in_memory: bool,
        exist_turns: bool) -> int:
    """Display the resume menu and return the choice"""
    menu_state = {
        (True, True, True): f'\n3: View turns complete\n4: View current matchs\n5: Complete a turn',
        (True, True, False): f'\n3: View current matchs\n4: Complete a turn',
        (True, False, True): f'\n3: View turns complete\n4: Start a turn',
        (True, False, False): f'\n3: Start a turn',
        (False, False, False): 'already defined\n3: Add players'
    }
    menu = f'''
	--- Tournament: {tournament_name} ---
	1: View tournament informations
	2: View players {menu_state[(all_players_defined, turn_in_memory, exist_turns)]}
	0: Return to tournament menu
	> Select an option: '''
    menu = dedent(menu)
    choice = input(menu)

    last_choice = {(True, True): 5, (True, False): 3, (False, False): 3}
    if choice.isdecimal() and int(
            choice) <= last_choice[(all_players_defined, exist_turns)]:
        if int(choice) == 0:
            print('>>> Return to tournament menu <<<')
        return int(choice)
    else:
        print('Incorrect entry, please try again.')
        return display_menu_resume_tournament()


def display_search_result(result) -> int:
    """Display the tournaments found from a search and return the selected tournament number"""
    if len(result) == 0:
        print('No tournament found.')
        return -1
    print(f'Number of tournaments found: {len(result)}')
    i = 0
    for elt in result:
        print(f'{i}: {elt["name"]}, {elt["location"]}, {elt["date"]}')
        i += 1
    choice = input('> Select a tournament: ')
    if choice.isdecimal() and int(choice) < i:
        return int(choice)
    else:
        print('Incorrect entry, please try again.')
        return display_search_result(result)


def display_tournament_info(
        tournament_name,
        tournament_location,
        tournament_date,
        tournament_description,
        tournament_time_control):
    info = f'''
    Tournament name: {tournament_name}
    Location: {tournament_location}
    Date: {tournament_date}
    Time control: {tournament_time_control}
    Description: {tournament_description}
    '''
    print(dedent(info))


def enter_tournament_name() -> str:
    """Ask and return the tournament name"""
    name = input('> Enter a tournament name: ')
    if len(name) > 0:
        return name
    else:
        print('Incorrect entry, please try again.')
        return enter_tournament_name()


def enter_tournament_location() -> str:
    """Ask and return the tournament location"""
    location = input('> Enter a location: ')
    if len(location) > 0:
        return location
    else:
        print('Incorrect entry, please try again.')
        return enter_tournament_location()


def enter_tournament_description() -> str:
    """Ask and return the tournament description"""
    description = input('> Enter a description: ')
    return description


def enter_tournament_time_control(TIME_CONTROL: list) -> str:
    """Ask and return the tournament time control"""
    time_control = input(
        f'> Enter a time control ({", ".join(TIME_CONTROL)}): ')

    if time_control.lower() in TIME_CONTROL:
        return time_control.lower()
    else:
        print('Incorrect entry, please try again.')
        return enter_tournament_time_control(TIME_CONTROL)


def enter_tournament_turns_number() -> int:
    """Ask and return the number of turns of the tournament"""
    turns_number = input(
        '> Enter a number of turns (press Enter for 4 turns): ')
    if len(turns_number) == 0:
        return 4
    elif turns_number.isdecimal():
        return int(turns_number)
    else:
        print('Incorrect entry, please try again.')
        return enter_tournament_turns_number()


def enter_tournament_players_number() -> int:
    """Ask and return the number of players of the tournament"""
    players_number = input(
        '> Enter a number of players (press Enter for 8 players): ')
    if len(players_number) == 0:
        return 8
    elif players_number.isdecimal():
        return int(players_number)
    else:
        print('Incorrect entry, please try again.')
        return enter_tournament_players_number()


def define_new_tournament(TIME_CONTROL: list[str]):  # -> tuple ?
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
    time_control = enter_tournament_time_control(TIME_CONTROL)
    turns_number = enter_tournament_turns_number()
    players_number = enter_tournament_players_number()

    return name, location, date, description, time_control, turns_number, players_number
