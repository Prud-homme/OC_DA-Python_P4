def display_menu():
	menu = f'''
	--- Report and statistics ---
	1: List of all players
	2: List of all tournaments
	3: List of all players in a tournament
	4: List of all turns in a tournament
	5: List of all matchs in a tournament
	0: Main menu
	> Select an option: '''
	return input(menu)

def display_menu_filter():
	menu = '''>>> Filter by <<<
	1: Rank
	2: Alphabetical order
	0: Show report
	'''

def display_menu_search_tournament():
	menu = ''' >>> Search a tournament <<<
	> Research: '''
	return input(menu)
