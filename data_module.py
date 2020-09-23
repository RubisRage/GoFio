from stone import Stone
from exceptions import GoRuleException as GoEx

EMPTY = 0
BLACK = 1
WHITE = 2

board  = [[0 for _ in range(0, 19)] for _ in range(0, 19)]

class GameController:
    
    def __init__(self):
        self.turn = BLACK
        self.last_board_state = deepcopy(board)
        self.black = TeamController(BLACK)
        self.white = TeamController(WHITE, self.black)
        self.black.other = self.white


    def throw(self, x, y):
        throw = Stone(x,y)
        check_error(throw)
        last_board_state = deepcopy(board)
        __get_player().process_throw(throw)
        self.black.has_passed = self.white.has_passed = False
        self.turn = BLACK if self.turn == WHITE else WHITE


    def pass_turn(self):
        get_player().has_passed = True


    def ended(self):
        return self.black.has_passed and self.white.has_passed


    def check_error(self,throw):
        if board[throw.x][throw.y] != EMPTY:
            raise GoEx(GoEx.OCCUPIED_EXCEPTION)
        
        temp = deepcopy(board)
        temp[throw.x][throw.y] = self.turn

        if self.last_board_state == temp:
            raise GoEx(GoEx.KO_EXCEPTION)


    def __get_player():
        return self.black if self.turn == BLACK else self.white


class TeamController:

    def __init__(self, team, other = None):
        self.team = team
        self.other = other
        self.groups = list()
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

        if temp.process_liberties() == 0:
            del temp
            board[stone.x][stone.y] = EMPTY
            raise GoEx(GoEx.SUICIDE_EXCEPTION)

        for old_groups in ally_tangent:
            self.groups.remove(old_groups)

        self.groups.append(temp)

    
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
            if isinstance(other, TeamController.Group):
                #print(f"\n\nself stones: {self.stones}")
                #print(f"self liberties: {self.liberties}")
                #print(f"other stones: {other.stones}")
                #print(f"other liberties: {other.liberties}")
                return self.team == other.team and self.stones == other.stones and self.liberties == other.liberties
            return False

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




