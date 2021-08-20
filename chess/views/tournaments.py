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

def display_menu_new(): #Type hint
	print('''
	--- New tournament ---
	If you want to enter information later, just press enter.
	Otherwise please enter the information before pressing enter.''')
	name = input('> Enter a name: ')
	location = input('> Enter a location: ')
	date = input('> Enter a date: ')
	description = input('> Enter a description: ')
	time_control = input('> Enter a time control: ')
	turns_number = int(input('> Enter a turns number: '))
	players_number = int(input('> Enter a players number: '))
	
	
	return name, location, date, description, time_control, turns_number, players_number

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
	0: Save and return to main menu
	> Select an option: '''
	return input(menu)

def display_menu_add_player():
	menu = '''\t>>> Add a player <<<
	1: Add by id
	2: Add by name
	3: Create a new player and add it
	0: Save and return to main menu
	> Select an option: '''
	return input(menu)
	#4: Remove a registered player -> archiver

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
