import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(currentdir)

from controller_tournament import TournamentController
#from pair_generation import generate_pairs_swiss_system