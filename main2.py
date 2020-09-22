from stone import Stone
from data_module import TeamController as t
from data_module import BLACK
from data_module import WHITE
import data_module

black = t(BLACK)
white = t(WHITE, black)
black.other = white

black.process_throw(Stone(1, 1))
black.process_throw(Stone(1, 2))