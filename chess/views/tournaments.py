from .date import prompt_date_year, prompt_date_month, prompt_date_day


def display_menu(ongoing: bool) -> str:
	state = {True: 'Resume a', False: 'New'}
	menu = f'''
	---  Tournaments menu ---
	1: {state[ongoing]} tournament
	2: Load a tournament
	3: Update informations of a tournament
	0: Main menu
	> Select an option: '''
	return input(menu)


def prompt_name():
	name = input('> Enter a name: ')
	if len(name)>0:
		return name
	else:
		print('Incorrect entry, please try again.')
		return prompt_name()

def prompt_location():
	location = input('> Enter a location: ')
	if len(location)==0:
		return None
	else:
		return location

def prompt_description():
	description = input('> Enter a description: ')
	if len(description)==0:
		return None
	else:
		return description

def prompt_time_control(TIME_CONTROL):
	time_control = input(f'> Enter a time control ({", ".join(TIME_CONTROL)}): ')
	if len(time_control)==0:
		return None
	elif time_control.lower() in TIME_CONTROL:
		return time_control.lower()
	else:
		print('Incorrect entry, please try again.')
		return prompt_time_control(TIME_CONTROL)

def prompt_turns_number():
	turns_number = input('> Enter a turns number (4 by default): ')
	if len(turns_number)==0:
		return 4
	elif turns_number.isdecimal():
		return int(turns_number)
	else:
		print('Incorrect entry, please try again.')
		return prompt_turns_number()

def prompt_players_number():
	players_number = input('> Enter a players number (8 by default): ')
	if len(players_number)==0:
		return 8
	elif players_number.isdecimal():
		return int(players_number)
	else:
		print('Incorrect entry, please try again.')
		return prompt_players_number()

def prompt_new_tournament(TIME_CONTROL): #Type hint
	print('''
	--- New tournament ---
	Required information: name
	If you want to enter information later, just press enter.
	Otherwise please enter the information before pressing enter.''')
	name = prompt_name()
	location = prompt_location()
	print('> Enter tournament date')
	year = prompt_date_year()
	month = prompt_date_month()
	if None not in (year, month):
		day = prompt_date_day(year, month)
		date = '/'.join((year, month, day))
	else:
		print('No date will be defined.')
		date = None
	description = prompt_description()
	time_control = prompt_time_control(TIME_CONTROL)
	turns_number = prompt_turns_number()
	players_number = prompt_players_number()
	return name, location, date, description, time_control, turns_number, players_number





def display_tournament_info(tournament_name, tournament_location, tournament_date, tournament_description, tournament_time_control):
	info = f'''--- Tournament information ---
	Name: {tournament_name}
	Location: {tournament_location}
	Date: {tournament_date}
	Time control: {tournament_time_control}
	Description: {tournament_description}
	'''
	print(info)

def display_tournament_player(player_id, player_name, player_birthdate):
	print(f'{player_id}: {player_name}, {player_birthdate}')






def display_menu_resume(tournament_name: str, all_players_defined: bool, exist_turns: bool): #Type hint tournament = tournament object
	state = {
	(True, True): '\n\t3: View turns\n\t4: View matchs\n\t5: Start a turn',
	(True, False): '\n\t3: Start a turn',
	(False, False): 'already defined\n\t3: Add players'
	}
	menu = f'''
	--- Tournament: {tournament_name} ---
	1: View tournament informations
	2: View players {state[(all_players_defined, exist_turns)]}
	0: Return to tournament menu
	> Select an option: '''
	choice = input(menu)
	max_choice = {(True, True): 5, (True, False): 3, (False, False): 3}
	if choice.isdecimal() and int(choice)<=max_choice[(all_players_defined, exist_turns)]:
		return int(choice)
	else:
		print('Incorrect entry, please try again.')
		return display_menu_load_tournament()






def prompt_tournament_name():
	t_name = input('> Enter a tournament name: ')
	if len(t_name)>0:
		return t_name
	else:
		print('Incorrect entry, please try again.')
		return prompt_player_name()

def prompt_tournament_location():
	t_loc = input('> Enter a tournament location: ')
	if len(t_loc)>0:
		return t_loc
	else:
		print('Incorrect entry, please try again.')
		return prompt_tournament_location()


def display_menu_load_tournament():
	menu = '''\t>>> Load a tournament <<<
	1: Search by name
	2: Search by location
	0: Cancel
	> Select an option: '''
	choice = input(menu)
	#4: Remove a registered player -> archiver
	if choice.isdecimal() and int(choice)<=2:
		return int(choice)
	else:
		print('Incorrect entry, please try again.')
		return display_menu_load_tournament()






def display_menu_add_player():
	menu = '''\t>>> Add a player <<<
	1: Add by id
	2: Add by name
	3: Create a new player and add it
	0: Don't add any more players
	> Select an option: '''
	choice = input(menu)
	#4: Remove a registered player -> archiver
	if choice.isdecimal() and int(choice)<=3:
		return int(choice)
	else:
		print('Incorrect entry, please try again.')
		return display_menu_add_player()

def prompt_player_id():
	player_id = input('> Enter a player id: ')
	if player_id.isdecimal():
		return int(player_id)
	else:
		print('Incorrect entry, please try again.')
		return prompt_player_id()

def prompt_player_name():
	player_name = input('> Enter a player name: ')
	if len(player_name)>0:
		return player_name
	else:
		print('Incorrect entry, please try again.')
		return prompt_player_name()

def display_search_result(result):
	if len(result)==0:
		print('No players found.')
		return -1
	print('List of players')
	i = 0
	for elt in result:
		print(f'{i}: {elt["name"]}, {elt["birthdate"]}')
		i += 1
	choice = input('> Select a player: ')
	if choice.isdecimal() and int(choice)<i:
		return choice
	else:
		print('Incorrect entry, please try again.')
		return display_search_result(result)


def display_search_result_t(result):
	if len(result)==0:
		print('No tournament found.')
		return -1
	print('List of tournaments')
	i = 0
	for elt in result:
		print(f'{i}: {elt["name"]}, {elt["location"]}, {elt["date"]}')
		i += 1
	choice = input('> Select a tournament: ')
	if choice.isdecimal() and int(choice)<i:
		return int(choice)
	else:
		print('Incorrect entry, please try again.')
		return display_search_result_t(result)

def tournament_choice(result):
	menu = f'''
	Multiple tournaments match.
	0: Load a tournament
	1: Save as a new tournament
	> Select an option: '''

	choice = input(menu)
	if choice.isdecimal and int(choice)<=1:
		return int(choice)
	else:
		print('Incorrect entry, please try again.')
		return tournament_choice(result)








def display_menu_new_turn(turn_name: str):
	menu = f'''\t>>> Turn: {turn_name} <<<
	1: View matchs
	2: End turn
	3: View players ranking (current tournament)
	4: View players score
	0: Save and return to main menu
	> Select an option: '''
	return input(menu)



def prompt_turn():
	return input('Turn name: ')

def prompt_player():#Sera remplacée par display_menu_add_player()
	return input('Add a player id: ')
