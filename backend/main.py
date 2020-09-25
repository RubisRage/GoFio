from exceptions import GoRuleException
from data_module import GameController
import os

crossValue = ["-", "B", "W"]
g = GameController()


def main():
    

    print("p to pass the turn, e to exit.")
    print("x,y (x y) coords to throw.")
    err_str = ""

    while True:
        os.system("clear")
        print(f"{g.get_player_str()} plays")
        print(err_str)
        err_str = ""
        print_board()

        s = input()
        if s == 'p' or s == 'e':
            process_command(s)
        else:
            try:
                coords = s.split(' ')
                g.throw(int(coords[0]), int(coords[1]))
            except GoRuleException as e:
                err_str = str(e)
            except ValueError:
                err_str = "Couldn't understand, would you try again?"
 

def process_command(command):
        if command == "p":
            g.pass_turn()
            exit() if g.ended() else None
        elif command == "e":
            exit()


def print_board():
    board = g.get_board()

    for row in board:
        for value in row:
            print(crossValue[value], end = " ")
        print()


if __name__ == "__main__":
    main()