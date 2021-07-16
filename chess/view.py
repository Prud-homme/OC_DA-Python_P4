import re
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
			"7: Edit a player\n"
			"10: View player in memory\n"
			"11: View tournament in memory\n"
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

		state = True
		while state:
			selection = input(f"Select a {keyword}: ")
			selection = re.sub("[^0-9]", "", selection) # only numeric
			if len(selection)>0 and int(selection) in range(len(data)):
				state = False
			else:
				print('Incorrect entry, please try again.\n')

		return selection


	def prompt_date(self, event="date"):
		print(f"Enter {event}")
		# Prompt year
		state = True
		while state:
			year = input("Enter a year: ")
			year = re.sub("[^0-9]", "", year) # only numeric
			if len(year)==4:
				year = int(year)
				state = False
			else:
				print('Incorrect entry, please try again.\n')
		# Leap year: the year is divisible by 4 and not divisible by 100; the year is divisible by 400
		leap_year = year%4==0 and year%100!=0 or year%400==0

		# Prompt month
		state = True
		while state:
			month = input("Enter a month between 1 and 12: ")
			month = re.sub("[^0-9]", "", month) # only numeric
			if len(month)>0 and int(month)>=1 and int(month)<=12:
				month = month.zfill(2)
				state = False
			else:
				print('Incorrect entry, please try again.\n')
		# Last day of the month
		if leap_year and int(month)==2:
			last_day = 29
		elif int(month)==2:
			last_day = 28
		elif int(month) in [1,3,5,7,8,10,12]:
			last_day = 31
		else:
			last_day = 30

		state = True
		while state:
			day = input(f"Enter a day between 1 and {last_day}: ")
			day = re.sub("[^0-9]", "", day) # only numeric
			if len(day)>0 and int(day)>=1 and int(day)<=last_day:
				day = day.zfill(2)
				state = False
			else:
				print('Incorrect entry, please try again.\n')
		return f"{day}/{month}/{year}"

	def prompt_time_control(self):
		state = True
		while state:
			time_control = input('Time control: ')
			if time_control in ['bullet', 'blitz', 'coup rapide']:
				state = False
			else:
				print("Incorrect entry, please enter 'bullet', 'blitz' or 'coup rapide'.\n")
		return time_control

	def prompt_turns_number(self):
		state = True
		while state:
			turns_number = input('Turns number: ')
			turns_number = re.sub("[^0-9]", "", turns_number) # only numeric
			if len(turns_number)>0 and int(turns_number) > 0 :
				state = False
			else:
				print("Incorrect entry, please try again.\n")
		return turns_number

	def prompt_tournament_info(self):
		print("--- Add a tournament ---")
		name = input('Name: ')
		location = input('Location: ')
		date = self.prompt_date("tournament date")
		description = input('Description: ')
		time_control = self.prompt_time_control()
		turns_number = self.prompt_turns_number()
		return name, location, date, description, time_control, turns_number

	def prompt_gender(self):
		state = True
		while state:
			gender = input('Gender: ')
			if gender in ['M', 'F']:
				state = False
			else:
				print("Incorrect entry, please enter 'M' or 'F'.\n")
		return gender

	def prompt_ranking(self):
		state = True
		while state:
			ranking = input('Ranking: ')
			ranking = re.sub("[^0-9]", "", ranking) # only numeric
			if len(ranking)>0 and int(ranking)>0:
				state = False
			else:
				print("Incorrect entry, please enter a positive integer.\n")
		return ranking

	def prompt_player_info(self):
		print("--- Add a player ---")
		name = input('Name: ')
		birth_date = self.prompt_date('birth date')
		gender = self.prompt_gender()
		ranking = self.prompt_ranking()
		return name, birth_date, gender, ranking

	def prompt_edit_player(self, player):
		menu = (
			"--- Edit a player ---\n"
			f"0: Edit name: {player.name}\n"
			f"1: Edit birth_date: {player.birth_date}\n"
			f"2: Edit gender: {player.gender}\n"
			f"3: Edit ranking: {player.ranking}\n"
			"Select an option: "
			)

		state = True
		while state:
			selection = input(menu)
			selection = re.sub("[^0-9]", "", selection) # only numeric
			if len(selection)>0 and int(selection) in range(4):
				state = False
			else:
				print('Incorrect entry, please try again.\n')
		
		if selection=="0":
			update = input('Name: ')
		elif selection=="1":
			update = self.prompt_date('birth date')
		elif selection=="2":
			update = self.prompt_gender()
		elif selection=="3":
			update = self.prompt_ranking()

		return selection, update

	def prompt_edit_tournament(self, tournament):
		menu = (
			"--- Edit a tournament ---\n"
			f"0: Edit name: {tournament.name}\n"
			f"1: Edit location: {tournament.location}\n"
			f"2: Edit date: {tournament.date}\n"
			f"3: Edit description: {tournament.description}\n"
			f"4: Edit time control: {tournament.time_control}\n"
			f"5: Edit turns_number: {tournament.turns_number}\n"
			"Select an option: "
			)

		state = True
		while state:
			selection = input(menu)
			selection = re.sub("[^0-9]", "", selection) # only numeric
			if len(selection)>0 and int(selection) in range(6):
				state = False
			else:
				print('Incorrect entry, please try again.\n')
		
		if selection=="0":
			update = input('Name: ')
		elif selection=="1":
			update = input('Location: ')
		elif selection=="2":
			update = self.prompt_date("tournament date")
		elif selection=="3":
			update = input('Description: ')
		elif selection=="4":
			update = self.prompt_time_control()
		elif selection=="5":
			update = self.prompt_turns_number()
		return selection, update

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