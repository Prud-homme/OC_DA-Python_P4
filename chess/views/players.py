from .date import prompt_date_year, prompt_date_month, prompt_date_day

def display_menu():
	menu = '''
	--- Players menu ---
	1: Add a player
	2: Update a player informations
	0: Main menu
	> Select an option: '''
	choice = input(menu)
	if choice.isdecimal() and int(choice)<=2:
		return int(choice)
	else:
		print('Incorrect entry, please try again.')
		return display_menu_load_tournament()

def prompt_firstname():
	firstname = input('> Enter a first name: ')
	if len(firstname)>0:
		return firstname
	else:
		print('Incorrect entry, please try again.')
		return prompt_firstname()

def prompt_lastname():
	lastname = input('> Enter a last name: ')
	if len(lastname)>0:
		return lastname
	else:
		print('Incorrect entry, please try again.')
		return prompt_lastname()

def prompt_gender():
	gender = input('> Enter a gender (M/F): ')
	if len(gender)==0:
		return None
	elif gender.upper() in ['M', 'F']:
		return gender.upper()
	else:
		print('Incorrect entry, please try again.')
		return prompt_gender()

def prompt_ranking():
	ranking = input('> Enter a ranking: ')
	if len(ranking)==0:
		return None
	elif ranking.isdecimal() and int(ranking)>1:
		return int(ranking)
	else:
		print('Incorrect entry, please try again.')
		return prompt_ranking()

def prompt_new_player(): #Type hint
	print('''
	--- Add a new Player ---
	Required information: firstname, lastname.
	If you want to enter information later, just press enter.
	Otherwise please enter the information before pressing enter.''')
	firstname = prompt_firstname()
	lastname = prompt_lastname()
	print('> Enter birth date')
	year = prompt_date_year()
	month = prompt_date_month()
	if None not in (year, month):
		day = prompt_date_day(year, month)
		birthdate = '/'.join((year, month, day))
	else:
		birthdate = None
	gender = prompt_gender()
	ranking = prompt_ranking()
	return firstname, lastname, birthdate, gender, ranking


def prompt_player_name():
	print('''
	--- Search a player with name ---
	If you are entering a first and last name,
	please enter the last name before the first name,
	making sure to separate them with a space.
	You can also enter only the first or last name''')
	name = input('> Enter a name: ')
	if len(name)>0:
		return name
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
