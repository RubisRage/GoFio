import unittest
from game_logic.stone import Stone
from game_logic.exceptions import GoRuleException as GoEx
from game_logic.data_module import TeamController as t
from game_logic.data_module import BLACK
from game_logic.data_module import WHITE
import game_logic.data_module as data_module

class GroupTests(unittest.TestCase):

    def setUp(self):
        data_module.board = [[0 for _ in range(0, 19)] for _ in range(0, 19)]

    def test_simple_group_liberties(self):

        upper_left = t.Group(Stone(0, 0), BLACK)
        upper_right = t.Group(Stone(0, 18), BLACK)
        lower_left = t.Group(Stone(18, 0), BLACK)
        lower_right = t.Group(Stone(18, 18), BLACK)

        top = t.Group(Stone(0, 15), BLACK)
        bottom = t.Group(Stone(18, 15), BLACK)
        left = t.Group(Stone(15, 0), BLACK)
        right = t.Group(Stone(15, 18), BLACK)

        interior = t.Group(Stone(15, 15), BLACK)

        self.assertEqual(upper_left.process_liberties(), 2)
        self.assertEqual(upper_right.process_liberties(), 2)
        self.assertEqual(lower_left.process_liberties(), 2)
        self.assertEqual(lower_right.process_liberties(), 2)

        self.assertEqual(top.process_liberties(), 3)
        self.assertEqual(bottom.process_liberties(), 3)
        self.assertEqual(left.process_liberties(), 3)
        self.assertEqual(right.process_liberties(), 3)

        self.assertEqual(interior.process_liberties(), 4)


    def test_compound_group_liberties(self):

        group = t.Group([Stone(0, x) for x in range(0, 19)], BLACK)
        self.assertEqual(group.process_liberties(), 19)

        group = t.Group([Stone(5, x) for x in range(0, 19)], BLACK)
        self.assertEqual(group.process_liberties(), 19*2)

        group = t.Group([Stone(7, x) for x in range(1, 18)], BLACK)
        self.assertEqual(group.process_liberties(), (17*2 + 2))
    
        group = t.Group([Stone(15, x) for x in range(0, 19)], BLACK)
        t.Group([Stone(16, x) for x in range(0, 19)], WHITE)
        self.assertEqual(group.process_liberties(), 19)


    def test_pre_check_liberties(self):
        
        group = t.Group(Stone(0, 0), BLACK)
        self.assertEqual(group.pre_check_liberties(Stone(0,1)), 1)




class TeamControllerTests(unittest.TestCase):
    
    def setUp(self):
        data_module.board =  [[0 for _ in range(0, 19)] for _ in range(0, 19)]
        self.test_board = [[0 for _ in range(0, 19)] for _ in range(0, 19)]
        self.black = t(BLACK)
        self.white = t(WHITE, self.black)
        self.black.other = self.white

    def test_simple_process_throw(self):
        self.test_board[1][1] = BLACK
        self.black.process_throw(Stone(1, 1))
        self.assertEqual(data_module.board, self.test_board)
        self.assertEqual(self.black.groups[0], t.Group(Stone(1,1), BLACK))

        self.test_board[1][2] = BLACK
        self.black.process_throw(Stone(1, 2))
        self.assertEqual(data_module.board, self.test_board)
        self.assertEqual(self.black.groups[0], t.Group([Stone(1, x) for x in range(1, 3)], BLACK))
        
        self.test_board[2][2] = BLACK
        self.black.process_throw(Stone(2,2))
        self.assertEqual(data_module.board, self.test_board)
        temp_stones = [Stone(1, x) for x in range(1, 3)]
        temp_stones.append(Stone(2,2))
        self.assertEqual(self.black.groups[0], t.Group(temp_stones, BLACK))

    
    def test_elimination_process_throw(self):
        
        #Single group elimination
        self.black.process_throw(Stone(1,0))
        self.black.process_throw(Stone(1,2))
        self.black.process_throw(Stone(2,1))
        self.white.process_throw(Stone(1,1))

        #Elimination throw
        self.black.process_throw(Stone(0,1))

        self.test_board[1][0] = BLACK
        self.test_board[1][2] = BLACK
        self.test_board[2][1] = BLACK
        self.test_board[0][1] = BLACK
        
        self.assertEqual(data_module.board, self.test_board)
        self.assertEqual(len(self.white.groups), 0)
        self.assertEqual(len(self.black.groups), 4)


        #Compound group elimination
        self.black.process_throw(Stone(17,0))
        self.black.process_throw(Stone(18,0))
        self.black.process_throw(Stone(18,1))
        self.black.process_throw(Stone(18,2))
        self.white.process_throw(Stone(16,0))
        self.white.process_throw(Stone(17,1))
        self.white.process_throw(Stone(17,2))

        #Elimination throw
        self.white.process_throw(Stone(18,3))
        self.assertEqual(len(self.black.groups), 4)
        self.assertEqual(len(self.white.groups), 3)


    def test_suicide_throw(self):
        
        #Corner group suicide situation
        self.black.process_throw(Stone(0,17))
        self.black.process_throw(Stone(1,18))
        
        self.test_board[0][17] = BLACK
        self.test_board[1][18] = BLACK

        #Corner group suicide attempt
        with self.assertRaises(GoEx) as contex:
            self.white.process_throw(Stone(0, 18))
        self.assertEqual(contex.exception.error_code, GoEx.SUICIDE_EXCEPTION)
        self.assertEqual(data_module.board, self.test_board)
        self.assertEqual(len(self.black.groups), 2)
        self.assertEqual(len(self.white.groups), 0)


        #Simple suicide situation
        self.black.process_throw(Stone(1,0))
        self.black.process_throw(Stone(1,2))
        self.black.process_throw(Stone(2,1))
        self.black.process_throw(Stone(0,1))

        self.test_board[1][0] = BLACK
        self.test_board[1][2] = BLACK
        self.test_board[2][1] = BLACK
        self.test_board[0][1] = BLACK

        #Suicide attempt
        with self.assertRaises(GoEx) as context:
            self.white.process_throw(Stone(1,1))
        self.assertEqual(contex.exception.error_code, GoEx.SUICIDE_EXCEPTION)
        self.assertEqual(data_module.board, self.test_board)
        self.assertEqual(len(self.black.groups), 6)
        self.assertEqual(len(self.white.groups), 0)


        #Compound group suicide situacion
        self.white.process_throw(Stone(16,0))
        self.white.process_throw(Stone(16,1))
        self.white.process_throw(Stone(17,1))
        self.white.process_throw(Stone(17,2))
        self.white.process_throw(Stone(18,3))

        self.black.process_throw(Stone(17,0))
        self.black.process_throw(Stone(18,0))
        self.black.process_throw(Stone(18,1))

        self.test_board[16][0] = WHITE
        self.test_board[16][1] = WHITE
        self.test_board[17][1] = WHITE
        self.test_board[17][2] = WHITE
        self.test_board[18][3] = WHITE

        self.test_board[17][0] = BLACK
        self.test_board[18][0] = BLACK
        self.test_board[18][1] = BLACK

        #Compound group suicide attempt
        with self.assertRaises(GoEx) as context:
            self.black.process_throw(Stone(18,2))
        self.assertEqual(contex.exception.error_code, GoEx.SUICIDE_EXCEPTION)
        self.assertEqual(data_module.board, self.test_board)
        self.assertEqual(len(self.black.groups), 7)
        self.assertEqual(len(self.white.groups), 2)
        

    def test_fake_suicide_throw(self):
        
        #Corner fake suicide
        self.white.process_throw(Stone(0,16))
        self.white.process_throw(Stone(1,17))

        self.black.process_throw(Stone(0,17))
        self.black.process_throw(Stone(1,18))

        self.test_board[0][16] = WHITE
        self.test_board[1][17] = WHITE
        self.test_board[0][18] = WHITE

        self.test_board[1][18] = BLACK
        
        #Corner elimination success
        self.white.process_throw(Stone(0,18))
        self.assertEqual(data_module.board, self.test_board)
        self.assertEqual(len(self.black.groups), 1)
        self.assertEqual(len(self.white.groups), 3)


        #Interior fake suicide
        self.white.process_throw(Stone(0,2))
        self.white.process_throw(Stone(1,1))
        self.white.process_throw(Stone(1,3))

        self.black.process_throw(Stone(2,1))
        self.black.process_throw(Stone(3,1))
        self.black.process_throw(Stone(2,3))
        self.black.process_throw(Stone(3,3))
        self.black.process_throw(Stone(4,2))

        self.test_board[0][2] = WHITE
        self.test_board[1][1] = WHITE
        self.test_board[1][3] = WHITE
        
        self.test_board[1][2] = BLACK
        self.test_board[2][1] = BLACK
        self.test_board[3][1] = BLACK
        self.test_board[2][3] = BLACK
        self.test_board[3][3] = BLACK
        self.test_board[4][2] = BLACK

        #Interior elimination success
        self.black.process_throw(Stone(1,2))
        self.assertEqual(data_module.board, self.test_board)
        self.assertEqual(len(self.black.groups), 5)
        self.assertEqual(len(self.white.groups), 6)


        #Compound fake suicide
        self.black.process_throw(Stone(18,0))
        self.black.process_throw(Stone(17,2))
        self.black.process_throw(Stone(17,3))
        self.black.process_throw(Stone(18,4))

        self.white.process_throw(Stone(17,0))
        self.white.process_throw(Stone(17,1))
        self.white.process_throw(Stone(18,2))
        self.white.process_throw(Stone(18,3))

        self.test_board[18][0] = BLACK
        self.test_board[18][1] = BLACK
        self.test_board[17][2] = BLACK
        self.test_board[17][3] = BLACK
        self.test_board[18][4] = BLACK

        self.test_board[17][0] = WHITE
        self.test_board[17][1] = WHITE

        #Compound elimination success
        self.black.process_throw(Stone(18,1))
        self.assertEqual(data_module.board, self.test_board)
        self.assertEqual(len(self.black.groups), 8)
        self.assertEqual(len(self.white.groups), 7)

from game_logic.data_module import GameController

class GameControllerTests(unittest.TestCase):

    def setUp(self):
        self.game = GameController()
        data_module.board = [[0 for _ in range(0,19)] for _ in range(0,19)]

    def test_pass_turn(self):
        
        self.game.pass_turn()
        self.game.throw(0,0)
        self.assertTrue(not self.game.ended())
        
        self.game.pass_turn()
        self.game.pass_turn()
        self.assertTrue(self.game.ended())

    def test_occupied_throw(self):

        self.game.throw(0,0)
        with self.assertRaises(GoEx) as context:
            self.game.throw(0,0)
        self.assertEqual(context.exception.error_code, GoEx.OCCUPIED_EXCEPTION)

    def test_ko_throw(self):
        test_board = [[0 for _ in range(0,19)] for _ in range(0,19)]

        test_board[0][0] = BLACK
        test_board[1][1] = BLACK
        test_board[2][0] = BLACK
        test_board[0][1] = WHITE
        
        self.game.throw(2,0)
        self.game.throw(1,0)
        self.game.throw(1,1)
        self.game.throw(0,1)
        self.game.throw(0,0)

        with self.assertRaises(GoEx) as context:
            self.game.throw(1,0)
        self.assertEqual(data_module.board, test_board)
        self.assertEqual(context.exception.error_code, GoEx.KO_EXCEPTION)

        test_board[2][3] = WHITE
        test_board[1][4] = WHITE
        test_board[2][5] = WHITE
        test_board[3][4] = WHITE
        test_board[3][3] = BLACK
        test_board[3][5] = BLACK
        test_board[4][4] = BLACK

        self.game.throw(2,3) #w
        self.game.throw(3,3)
        self.game.throw(1,4) #w
        self.game.throw(4,4)
        self.game.throw(2,5) #w
        self.game.throw(3,5)
        self.game.pass_turn() #w
        self.game.throw(2,4)
        self.game.throw(3,4) #w

        with self.assertRaises(GoEx) as context:
            self.game.throw(2,4)
        self.assertEqual(data_module.board, test_board)
        self.assertEqual(context.exception.error_code, GoEx.KO_EXCEPTION)

if __name__ == "__main__":
    unittest.main()