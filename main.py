from chess.views.view_menu import display_menu
#from chess.controllers.checks.check import choice_is_valid
#from chess.controllers.controller_tournament import TournamentController
#from chess.controllers.controller_report import launch_report
import os, sys
cls = lambda: os.system('cls')
def run():
	#controller = TournamentController()
	cls()
	choice = None
	handler = {
		"1": exit,
		"2": exit,
	}
	choice = display_menu()
	# while choice != "0":
	# 	cls()
	# 	choice = display_menu()
	# 	if choice_is_valid(choice, handler):
	# 		player = handler[choice]()

if __name__ == "__main__":
	run()
