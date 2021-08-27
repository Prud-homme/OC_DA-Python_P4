from chess import *

def run():
	choice = -1
	tournament = None
	tournament_id = -1
	while choice!=0:
		choice = mm_v.display_menu()
		if choice==0:
			print('Quit...')
		elif choice==1:
			print('[IN PROGRESS] Tournaments')
			tournament, tournament_id = t_c.run(tournament, tournament_id)

		elif choice==2:
			print('[IN PROGRESS] Players')
			#p_c.run()

		elif choice==3:
			print('[IN PROGRESS] Reports')

		else:
			mm_v.display_try_again()

		"""
		if choice not in ['0', '1', '2', '3']:
			mm_v.display_try_again()
		
		elif choice=='1':
			tournament = t_c.run(m_m, t_m, tournament)

		elif choice=='2':
			subchoice = p_m.display_menu()

		elif choice=='3':
			subchoice = r_m.display_menu()
		"""
'''
		if choice=="1":
			subchoice = v.display_submenu_start()

			if subchoice=="1":
				result = v.prompt_tournament_info()
				c.create_tournament(result)
				
			# elif subchoice=="2":

		elif choice=="2":
			subchoice = v.display_submenu_database()

			# if subchoice=="1":

			# elif subchoice=="2":


		elif choice=="3":
			subchoice = v.display_submenu_report()

			# if subchoice=="1":


			# elif subchoice=="2":


		elif choice=="-1":
			subchoice = v.display_submenu_developer()

			# if subchoice=="1":


			# elif subchoice=="2":


'''
if __name__ == "__main__":
	run()
