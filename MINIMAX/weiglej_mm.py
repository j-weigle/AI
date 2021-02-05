#-----------------------------------#
#       Author: Justin Weigle       #
#       Edited: 16 Oct 2019         #
#-----------------------------------#
#       Minimax Algorithm           #
#-----------------------------------#

import platform
import time
import random
from math import inf
from os import system

class Board ():
    """ Creates a board for playing tic tac toe
    methods:
        move: places given player on the board at x,y
        random_move: places player on the board at a random x,y
        minimax: implementation of the recursive AI algorithm Minimax which
                    decides the best move for a given player
        won: checks if a given player won the game
        tied: checks if there are no empty cells left after no one has won,
                    which would mean a tied game
        empty_cells: checks if there are any empty cells left
    """
    def __init__ (self):
        self.max_player = 'X'
        self.min_player = 'O'
        self.empty = ' '
        self.cells = {}
        for y in range(3):
            for x in range(3):
                self.cells[x,y] = self.empty

    def move (self, x, y, player):
        """ Puts the player given on the board at x,y
        params:
            x: row 0, 1, or 2
            y: col 0, 1, or 2
            player: 'X' or 'O'
        """
        if (self.cells[x,y] == self.empty):
            self.cells[x,y] = player

    def random_move (self, player):
        """ Chooses a random cell from the empty cells as player's move
        params:
            player: 'X' or 'O'
        returns:
            random move chosen, (None, (move_x, move_y))
        """
        choices = []
        for cell in self.cells.keys():
            if (self.cells[cell] == self.empty):
                choices.append(cell)
        n_choices = len(choices) - 1
        rand_move = random.randint(0, n_choices)
        return (None, choices[rand_move])

    def minimax (self, player):
        """ Recursive AI algorithm Minimax applied to tic tac toe
        params:
            player: 'X' or 'O'
        returns:
            best move determined by algorithm, (score, (move_x, move_y))
        """
        if self.won(self.max_player):
            return (+1, None)
        if self.won(self.min_player):
            return (-1, None)
        elif self.tied():
            return (0, None)

        if (player == self.max_player):
            best = (-inf, None)
        else:
            best = (+inf, None)

        for x, y in self.cells:
            if (self.cells[x,y] == self.empty):
                self.cells[x,y] = player
                if (player == self.max_player):
                    score = self.minimax(self.min_player)[0]
                    if (score > best[0]):
                        best = (score, (x,y))
                else:
                    score = self.minimax(self.max_player)[0]
                    if (score < best[0]):
                        best = (score, (x,y))
                self.cells[x,y] = self.empty
        return best

    def won (self, player):
        """ Returns True if the given player won the game
        params:
            player: 'X' or 'O'
        """
        winning_states = [
            [self.cells[0,0], self.cells[0,1], self.cells[0,2]],    #row 0
            [self.cells[1,0], self.cells[1,1], self.cells[1,2]],    #row 1
            [self.cells[2,0], self.cells[2,1], self.cells[2,2]],    #row 2
            [self.cells[0,0], self.cells[1,0], self.cells[2,0]],    #col 0
            [self.cells[0,1], self.cells[1,1], self.cells[2,1]],    #col 1
            [self.cells[0,2], self.cells[1,2], self.cells[2,2]],    #col 2
            [self.cells[0,0], self.cells[1,1], self.cells[2,2]],    #diag\
            [self.cells[2,0], self.cells[1,1], self.cells[0,2]],    #diag/
        ]
        if [player, player, player] in winning_states:
            return True
        else:
            return False

    def tied (self):
        """ Returns False if any empty cells are found """
        if (self.empty_cells()):
            return False
        return True

    def empty_cells (self):
        """ Returns True if any empty cells are found """
        for y in range(3):
            for x in range(3):
                if (self.cells[x,y] == self.empty):
                    return True
        return False


def max_turn(board, chance = False):
    """ Runs the max players turn in minimax
    params:
        board: class Board()
        chance: True or False on whether to use 50 50 chance
                to use minimax or pick a random move
    """
    if not run_checks(board):
        return

    print("X turn")
    if (chance):
        use_minimax = random.choice([0,1])
    else:
        use_minimax = 1

    if (use_minimax):
        print("Using Minimax")
        best_move = board.minimax('X')
    else:
        print("Choosing random")
        best_move = board.random_move('X')
    time.sleep(1)

    if (best_move[1]):
        board.move(best_move[1][0], best_move[1][1], 'X')
    clear_screen()
    show_board(board)
    time.sleep(1)


def min_turn(board, chance = False):
    """ Runs the min players turn in minimax
    params:
        board: class Board()
        chance: True or False on whether to use 50 50 chance
                to use minimax or pick a random move
    """
    if not run_checks(board):
        return

    print("O turn")
    if (chance):
        use_minimax = random.choice([0,1])
    else:
        use_minimax = 1

    if (use_minimax):
        print("Using Minimax")
        best_move = board.minimax('O')
    else:
        print("Choosing random")
        best_move = board.random_move('O')
    time.sleep(1)

    if (best_move[1]):
        board.move(best_move[1][0], best_move[1][1], 'O')
    clear_screen()
    show_board(board)
    time.sleep(1)


def run_checks(board):
    """ Checks if the board is empty, X won, or O won
    params:
        board: class Board()
    """
    if not board.empty_cells():
        return False
    if board.won('X'):
        return False
    if board.won('O'):
        return False
    return True


def show_board (board):
    """ Renders the board to the console
    params:
        board: class Board()
    """
    horz_line = "-------------"
    print(horz_line)
    for y in range(3):
        for x in range(3):
            x_o = board.cells[x,y]
            print(f"| {x_o} ", end = '')
            if (x == 2):
                print('|')
        print(horz_line)


def clear_screen ():
    """ Clears Console so board can be displayed """
    os_name = platform.system().lower()
    if "windows" in os_name:
        system("cls")
    else:
        system("clear")


def get_choice():
    """ Gets and returns choice for mode to use when running minimax """
    choice = input(
        "Please enter a number (1 - 4)\n 1. Both players use minimax correctly at every turn\n 2. The starting player (X) is an expert and the opponent (0) only has a 50% chance to use minimax\n\t at each turn\n 3. The starting player (X) only has a 50% chance to use minimax at each turn and the opponent (0)\n\t is an expert.\n 4. Both players only have a 50% chance to use minimax at each turn.\n"
    )
    while (choice != '1' and choice != '2' and choice != '3' and choice != '4'):
        choice = input("Not a choice. Go agane: (1 - 4)\n")

    return choice


def main ():
    clear_screen()
    # get the mode choice for running minimax tictactoe
    choice = get_choice()
    print("You chose option: ", choice)
    time.sleep(3)

    # set the mode chosen
    if (choice == '1'):
        max_use_rand = False
        min_use_rand = False
    if (choice == '2'):
        max_use_rand = False
        min_use_rand = True
    if (choice == '3'):
        max_use_rand = True
        min_use_rand = False
    if (choice == '4'):
        max_use_rand = True
        min_use_rand = True

    clear_screen()
    board = Board()
    show_board(board)
    
    # run the minimax algorithm, alternating turns
    while run_checks(board):
        max_turn(board, max_use_rand)
        min_turn(board, min_use_rand)

    if (board.won('X')):
        print("X won!")
    elif (board.won('O')):
        print("O won!")
    else:
        print("Draw!")


if __name__ == "__main__":
    main()
