from chess.models import Tournament, Player, Turn, Match, Table
#from .controllers import tournaments as t_c
from chess.views import main_menu as mm_v, tournaments as t_v
#, players as p_v, reports as r_v
t_table = Table('tournaments', 'test.json')

def run(tournament):
	choice = -1
	while choice!='0':
		ongoing = tournament!=None
		choice = t_v.display_menu(ongoing)

		if choice not in ['0', '1', '2', '3']:
			mm_v.display_try_again()

		elif choice=='1' and not ongoing:
			print('[IN PROGRESS] New tournament')
			name, location, date, description, time_control, turns_number, players_number = t_v.display_menu_new()
			tournament = Tournament(name, location, date, description, time_control, turns_number, players_number)
			while len(tournament.players)<int(players_number):
				tournament.add_player(t_v.prompt_player())
			breakpoint()
			t_table.create_item(tournament.serializing())
			breakpoint()
		elif choice=='1' and ongoing:
			all_players_defined = len(tournament.players)==tournament.players_number
			exist_turns = len(tournament.turns)>0
			#breakpoint()
			subchoice = -1
			print('[IN PROGRESS] Resume a tournament')
			while subchoice!='0':
				subchoice = t_v.display_menu_resume(tournament.name, all_players_defined, exist_turns)

				if subchoice=='0':
					print('Saved')
					#return tournament

				elif subchoice=='1':
					print('[IN PROGRESS] View informations')

				elif subchoice=='2':
					print('[IN PROGRESS] View players')

				elif subchoice=='3' and not all_players_defined:
					print('[IN PROGRESS] Add players')
					subsubchoice = -1
					while subsubchoice!='0':
						subsubchoice = t_v.display_menu_add_player()

						if subsubchoice=='0':
							print('Saved')
							#return tournament

						elif subsubchoice=='1':
							print('[IN PROGRESS] Add id')

						elif subsubchoice=='2':
							print('[IN PROGRESS] Add name')

						elif subsubchoice=='3':
							print('[IN PROGRESS] Create')

						else:
							mm_v.display_try_again()

				elif subchoice=='3' and exist_turns:
					print('[IN PROGRESS] View turns')

				elif subchoice=='4' and all_players_defined:
					print('[IN PROGRESS] View matchs')

				elif subchoice in ['3', '5'] and all_players_defined:
					print('[IN PROGRESS] Start turn')
					turn = Turn(t_v.prompt_turn())
					breakpoint()
					subsubchoice = -1
					while subsubchoice!='0':
						subsubchoice = t_v.display_menu_new_turn(turn.name)

						if subsubchoice=='0':
							print('Saved')
							#return tournament

						elif subsubchoice=='1':
							print('[IN PROGRESS] View matchs')

						elif subsubchoice=='2':
							print('[IN PROGRESS] End turn')
							turn.close_turn()
							tournament.add_turn(turn)
							breakpoint()
							subsubchoice = '0'

						elif subsubchoice=='3':
							print('[IN PROGRESS] Rank')

						elif subsubchoice=='4':
							print('[IN PROGRESS] Score')

						else:
							mm_v.display_try_again()

				else:
					mm_v.display_try_again()

			if ongoing:
				tempid = t_table.get_id({'name': tournament.name, 'location': tournament.location})
				print('Update ID: ',tempid)
				#t_table.update_item(tournament.serializing(),tempid)

		elif choice=='2':
			print('[IN PROGRESS] Load a tournament')

		elif choice=='3':
			print('[IN PROGRESS] Update a tournament')

	