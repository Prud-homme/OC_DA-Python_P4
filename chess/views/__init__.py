import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(currentdir)
import view_match
import view_menu
import view_player
import view_tournament
import view_turn
from view_master import entry_request
