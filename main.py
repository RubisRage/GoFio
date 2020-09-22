from exceptions import GoRuleException
import GameController as gc
import Point as p
import os

crossValue = ["-", "B", "W"]
g = gc.GameController()


def main():
    
    print("/pass to pass the turn.")
    print("x y coords to throw.")

    while True:
        #os.system("clear")
        print(f"{g.get_player()} plays")
        print_board()

        if (s := input())[0] == 'p' or s == 'e':
            process_command(s)
        else:
            try:
                coords = s.split(' ')
                g.process_throw(p.Point(int(coords[0]), int(coords[1])))
            except GoRuleException as e:
                print(str(e))
 

def process_command(command):
        if command == "p":
            g.pass_turn()
            exit() if g.end_game() else None
        elif command == "e":
            exit()


def print_board():
    board = g.get_board()
    
    rows_num = iter(range(0,19))

    for row in board:
        s = (row_num:=str(next(rows_num))) + ("  " if len(row_num) == 1 else " ")
        print(f"{s}", end='')
        for x in row:
            print(f"{crossValue[x]} ", end='')
        print()


if __name__ == "__main__":
    main()