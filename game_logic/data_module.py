import copy
from game_logic.stone import Stone
from game_logic.exceptions import GoRuleException as GoEx


EMPTY = 0
BLACK = 1
WHITE = 2

board  = [[0 for _ in range(0, 19)] for _ in range(0, 19)]

class GameController:
    
    def __init__(self):
        self.current_turn = BLACK
        self.black = TeamController(BLACK)
        self.white = TeamController(WHITE, self.black)
        self.black.other = self.white


    def throw(self, x, y):

        throw = Stone(x,y)
        if board[throw.x][throw.y] != EMPTY:
            raise GoEx(GoEx.OCCUPIED_EXCEPTION)
        self.__get_player().process_throw(throw)
        self.black.has_passed = self.white.has_passed = False
        self.current_turn = BLACK if self.current_turn == WHITE else WHITE

    
    def get_player_str(self):
        return "black" if self.current_turn == BLACK else "white"

    
    def get_board(self):
        return board


    def pass_turn(self):
        self.__get_player().has_passed = True
        self.current_turn = BLACK if self.current_turn == WHITE else WHITE


    def ended(self):
        return self.black.has_passed and self.white.has_passed


    def __get_player(self):
        return self.black if self.current_turn == BLACK else self.white


class TeamController:

    def __init__(self, team, other = None):
        self.team = team
        self.other = other
        self.groups = list()
        self.last_board_state = None
        self.has_passed = False


    def process_throw(self, stone):
        enem_tangent = list()
        ally_tangent = list()

        for g in self.other.groups:
            if g.is_tangent(stone):
                enem_tangent.append(g)

        for g in self.groups:
            if g.is_tangent(stone):
                ally_tangent.append(g)

        for enemy_group in enem_tangent:
            if enemy_group.pre_check_liberties(stone) == 0:
                self.other.remove(enemy_group)
        
        if len(ally_tangent) == 0:
            temp = TeamController.Group(stone, self.team)
        else:
            temp = self.create_compound_group(ally_tangent, stone)

        if self.last_board_state == board:
            del temp
            self.handle_ko_exception(stone, enem_tangent)

        if temp.process_liberties() == 0:
            del temp
            board[stone.x][stone.y] = EMPTY
            raise GoEx(GoEx.SUICIDE_EXCEPTION)

        for old_groups in ally_tangent:
            self.groups.remove(old_groups)

        self.last_board_state = copy.deepcopy(board)
        self.groups.append(temp)


    def __repr__(self):
        return "BLACK" if self.team == BLACK else "WHITE"
    
    def handle_ko_exception(self,stone, enem_tangent):
        board[stone.x][stone.y] = EMPTY
        for enem_group in enem_tangent:
            if enem_group not in self.other.groups:
                enem_group.process_liberties()
                enem_group.print_stones()
                self.groups.append(enem_group)

        raise GoEx(GoEx.KO_EXCEPTION)

    def create_compound_group(self, groups, stone):
        stones = list()
        
        for g in groups:
            for s in g.stones:
                stones.append(s)

        stones.append(stone)
        return TeamController.Group(stones, self.team)


    def remove(self, group):
        
        for stone in group.stones:
            board[stone.x][stone.y] = EMPTY

        self.groups.remove(group)


    class Group:
        
        def __init__(self, stones, team):
            self.team = team
            self.liberties = set()
            
            if isinstance(stones, list):
                self.stones = set(stones)
            else:
                self.stones = {stones}

            for stone in self.stones:
                board[stone.x][stone.y] = self.team

            self.process_liberties()


        def is_tangent(self, stone):
            return stone in self.liberties

        def pre_check_liberties(self, stone):
            board[stone.x][stone.y] = (BLACK if self.team == WHITE else WHITE)
            temp = self.process_liberties()
            board[stone.x][stone.y] = EMPTY
            return temp


        def __eq__(self, other):
            return (isinstance(other, TeamController.Group) and
                self.team == other.team and self.stones == other.stones 
                and self.liberties == other.liberties)

        def print_stones(self):
            for s in self.stones:
                board[s.x][s.y] = self.team

        def process_liberties(self):
            
            del self.liberties
            self.liberties = set()

            for stone in self.stones:
                if stone.x %18 == 0 and stone.y %18 == 0:
                    self.__process_corner_liberties(stone)
                elif stone.x %18 == 0 or stone.y %18 == 0:
                    self.__process_side_liberties(stone)
                else:
                    self.__process_interior_liberties(stone)

            return len(self.liberties)
                    

        def __process_corner_liberties(self, stone):
            
            if stone.x == 0 and stone.y == 0:
                if board[stone.x+1][stone.y] == EMPTY:
                    self.liberties.add(Stone(stone.x+1, stone.y))
                if board[stone.x][stone.y+1] == EMPTY:
                    self.liberties.add(Stone(stone.x, stone.y+1))
            elif stone.x == 0 and stone.y == 18:
                if board[stone.x+1][stone.y] == EMPTY:
                    self.liberties.add(Stone(stone.x+1, stone.y))
                if board[stone.x][stone.y-1] == EMPTY:
                    self.liberties.add(Stone(stone.x, stone.y-1))
            elif stone.x == 18 and stone.y == 0:
                if board[stone.x-1][stone.y] == EMPTY:
                    self.liberties.add(Stone(stone.x-1, stone.y))
                if board[stone.x][stone.y+1] == EMPTY:
                    self.liberties.add(Stone(stone.x, stone.y+1))
            else:
                if board[stone.x-1][stone.y] == EMPTY:
                    self.liberties.add(Stone(stone.x-1, stone.y))
                if board[stone.x][stone.y-1] == EMPTY:
                    self.liberties.add(Stone(stone.x, stone.y-1))

        
        def __process_side_liberties(self, stone):

            if stone.x == 0:
                if board[stone.x+1][stone.y] == EMPTY:
                    self.liberties.add(Stone(stone.x+1, stone.y))
                
                for i in range(-1, 2, 2):
                    if board[stone.x][stone.y+i] == EMPTY:
                        self.liberties.add(Stone(stone.x, stone.y+i))
            elif stone.x == 18:
                if board[stone.x-1][stone.y] == EMPTY:
                    self.liberties.add(Stone(stone.x+1, stone.y))
                
                for i in range(-1, 2, 2):
                    if board[stone.x][stone.y+i] == EMPTY:
                        self.liberties.add(Stone(stone.x, stone.y+i))
            elif stone.y == 0:
                if board[stone.x][stone.y+1] == EMPTY:
                    self.liberties.add(Stone(stone.x, stone.y+1))
                
                for i in range(-1, 2, 2):
                    if board[stone.x+i][stone.y] == EMPTY:
                        self.liberties.add(Stone(stone.x+i, stone.y))
            else:
                if board[stone.x][stone.y-1] == EMPTY:
                    self.liberties.add(Stone(stone.x, stone.y-1))
                
                for i in range(-1, 2, 2):
                    if board[stone.x+i][stone.y] == EMPTY:
                        self.liberties.add(Stone(stone.x+i, stone.y))


        def __process_interior_liberties(self, stone):

            for i in range(-1, 2, 2):
                if board[stone.x+i][stone.y] == EMPTY:
                    self.liberties.add(Stone(stone.x+i, stone.y))
                if board[stone.x][stone.y+i] == EMPTY:
                    self.liberties.add(Stone(stone.x, stone.y+i))




