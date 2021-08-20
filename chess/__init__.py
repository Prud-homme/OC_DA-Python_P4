from .models import Tournament, Player, Turn, Match, Table
from .controllers import tournaments as t_c
from .views import main_menu as mm_v, tournaments as t_v, players as p_v, reports as r_v
from .settings import DATABASE