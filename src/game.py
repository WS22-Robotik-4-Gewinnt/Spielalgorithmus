from os import system, name
from random import randint
from algos.Random import Random
from algos.Minimax import Minimax

import sys


# some global variables
COLUMNS = 7
ROWS = 6
board = [[' ' for x in range(COLUMNS)] for y in range(ROWS)]

HUMAN_PIECE = 'X'
AI_PIECE = 'O'

HUMAN_TURN = 1
AI_TURN = 0

# enter game mode here
game_mode = "random"

def clear_terminal():
    # clear for linux / macOS
    if name == 'posix':
        _ = system('clear')
    # clear for windows
    else:
        _ = system('cls')

def print_board():
    clear_terminal()
    print("*************************************")
    print("")
    for row in range(ROWS):
        print('      |', end='')
        for col in range(COLUMNS):
            print(board[row][col] + '|', end='')
        print('\n')
    print('      |1|2|3|4|5|6|7|')

def full_board():
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == ' ':
                return False

    return True

def check_win(player_piece):
    piece = player_piece

    # check for horizontal win
    for col in range(COLUMNS-3):
        for row in range(ROWS):
            if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                print("###horizontal win")
                return True

    # check for vertical win
    for col in range(COLUMNS):
        for row in range(ROWS-3):
            if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                print("###vertical win")
                return True

    # check for rising diagonal win
    for col in range(COLUMNS-3):
        for row in range(ROWS-3):
            if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                print("###rising diagonal win")
                return True

    # check for shrinking diagonal win
    for col in range(COLUMNS-3):
        for row in range(ROWS):
            if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
                print("###shrinking diagonal win")
                return True
    
    return False

def make_move(col, piece):
    piece_placed = False

    # five because counting starts by zero
    x = 5

    while not piece_placed:
        if board[x][col-1] == " ":
            board[x][col-1] = piece
            piece_placed = True
        x -= 1

def main():
    print("*************************************")
    print("Welcome to the game connect four!")
    print("*************************************")
    print_board()

    # check the chosen mode
    if game_mode == "random":
        modus = Random(board, ROWS, COLUMNS, AI_PIECE, HUMAN_PIECE)
    if game_mode == "minimax":
        modus = Minimax(board, ROWS, COLUMNS, AI_PIECE, HUMAN_PIECE)

    # randomly choose who starts the game (turn)
    curr_turn = randint(AI_TURN, HUMAN_TURN)

    # loop as long as there is no winner 
    while not full_board():

        # Human makes a move
        if HUMAN_TURN == curr_turn:
            print("*************************************")
            print("Player HUMAN has to make the next move!")

            chosen_col = int(input("\nInput a number from 1-7 for column\n"))

            make_move(chosen_col, HUMAN_PIECE)

            if check_win(HUMAN_PIECE):
                print_board()
                print("WIN HUMAN")
                break

            curr_turn = AI_TURN

        # AI makes a move
        if AI_TURN == curr_turn:
            print("*************************************")
            print("Player AI has to make the next move!")

            chosen_col = modus.choose_column()

            make_move(chosen_col, AI_PIECE)

            if check_win(AI_PIECE):
                print_board()
                print("WIN AI")
                break

            curr_turn = HUMAN_TURN

        # print updated board after every move
        print_board()
    
    sys.exit(1)


if __name__ == '__main__':
    main()
