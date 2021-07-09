class View:
	def display_menu(self):
		menu = (
			"\n--- Menu ---\n"
			"1: Add a tournament in db\n"
			"2: Load a tournament from db\n"
			"3: Add a player in db\n"
			"4: Load a player from db\n"
			"5: Start a turn\n"
			#"6: Turn end\n"
			"0: Exit\n"
			"Select an option: "
			)
		return input(menu)

	def prompt_research(self):
		return input("Research: ")

	def prompt_research_result(self, data, keyword):
		print("--- Results of research ---")
		for i in range(len(data)):
			if keyword == 'tournament':
				info = (
					f"{i}: "
					f"Name: {data[i]['name']}, "
					f"Location: {data[i]['location']}, "
					f"Date: {data[i]['date']}, "
					f"Time control: {data[i]['time_control']}, "
					f"Description: {data[i]['description']}"
					)
				print(info)

			elif keyword == 'player':
				info = (
					f"{i}: "
					f'Name: {data[i]["name"]}\n'
					f'Birth date: {data[i]["birth_date"]}\n'
					f'Gender: {data[i]["gender"]}\n'
					f'Ranking: {data[i]["ranking"]}\n'
					)
				print(info)
		return input(f"Select a {keyword}: ")


	def prompt_tournament_info(self):
		print("--- Add a tournament ---")
		name = input('Name: ')
		location = input('Location: ')
		date = input('Date: ')
		description = input('Description: ')
		time_control = input('Time control: ')
		turns_number = input('Turns number: ')
		return name, location, date, description, time_control, turns_number

	def prompt_player_info(self):
		print("--- Add a player ---")
		name = input('Name: ')
		birth_date = input('Birth date: ')
		gender = input('Gender: ')
		ranking = input('Ranking: ')
		return name, birth_date, gender, ranking

	def prompt_turn_info(self):
		print("--- Start a turn ---")
		return input('Name: ')
	# # Tournament
	# def prompt_tournament_name()

	# def prompt_tournament_location()

	# def prompt_tournament_date()

	# def prompt_tournament_description()

	# def prompt_tournament_time_control()

	# def prompt_tournament_turns_number()

	# # Player
	# def prompt_player_name()

	# def prompt_player_birth_date()

	# def prompt_player_gender()

	# def prompt_player_ranking()

	# def display_menu_player()

	# # Turn
	# def prompt_turn_name()



	# def display_matchs(matchs_list)
		
	# # Match
	# def prompt_match_result()

	# # Global
	# def display_action()
	# 	#Creer tournoi
	# 	#Debuter un tour
	# 	#Terminer un tour
	# 	#...

	# def update_rankings()

	# def display_report()

	# def load_data()

	# def save_data()