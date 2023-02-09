import random
import pickle # M to load a pre-trained MLP classifier
import pandas as pd # M to create data representation of the playing field (game board)

HUMAN_PIECE = 'h'
AI_PIECE = 'r'
EMPTY_PIECE = '0'

DEBUG_MINIMAX = False

COLUMNS = 7
ROWS = 6

class Minimax_Alpha_Beta_MLP():

    board = []
    difficulty = 0
    
    def __init__(self, board, difficulty):
        self.board = [x[:] for x in board]
        self.difficulty = difficulty
        self.MLP_clf = pickle.load(open('MLP_clf.data', 'rb')) # M uses the pickle library to load a pre-trained MLP-classifier and uses it to determine the best move for the AI player

    def choose_column(self, board):
        winner = "NONE"
        self.board = [x[:] for x in board]
        col, minimax_score = self.mini_max(self.board, self.difficulty, True, -1000, 1000) # M add parameters alpha-beta-pruning
        if col is not None:
            row = self.get_row(self.board, col)

            # Check if the move ends the game
            copy = self.make_move(board, col, AI_PIECE)
            if len(self.get_valid_locations(copy)) == 0:
                winner = "DRAW"
            elif self.check_win(copy, AI_PIECE):
                winner = "ROBOT"
        else:
            row = None
            if minimax_score == 0:
                winner = "DRAW"
            elif minimax_score > 100000:
                winner = "ROBOT"
            elif minimax_score < -100000:
                winner = "HUMAN"


        print("==================")
        print("the winning col: " + str(col))
        print("score for move :" + str(minimax_score))
        self.printBoard(board)

        #return col, row, minimax_score
        return col, row, winner

    def get_row(self, board, col):
        for row in range(ROWS):
            print(row, col)
            if board[row][col] == EMPTY_PIECE:
                return row

    def get_valid_locations(self, board):
        valid_locations = []

        for column in range(COLUMNS):
            if board[5][column] == EMPTY_PIECE:
                valid_locations.append(column)
        return valid_locations

    def check_win(self, board, player_piece):
        piece = player_piece

        # check for horizontal win
        for col in range(COLUMNS-3):
            for row in range(ROWS):
                if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                    if DEBUG_MINIMAX:
                        print("###horizontal win")
                    return True

        # check for vertical win
        for col in range(COLUMNS):
            for row in range(ROWS-3):
                if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                    if DEBUG_MINIMAX:
                        print("###vertical win")
                    return True

        # check for rising diagonal win
        for col in range(COLUMNS-3):
            for row in range(ROWS-3):
                if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                    if DEBUG_MINIMAX:
                        print("###rising diagonal win")
                    return True

        # check for shrinking diagonal win
        for col in range(COLUMNS-3):
            for row in range(ROWS-3):
                row += 3
                if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
                    if DEBUG_MINIMAX:
                        print("###shrinking diagonal win", row, col)
                    return True

        return False

    def make_move(self, state, column, piece):
        temp = [x[:] for x in state]
        i = 0

        while i <= 5:
            if temp[i][column] == EMPTY_PIECE:
                temp[i][column] = piece
                break
            i += 1

        return temp

    def terminal(self, board):
        return self.check_win(board, HUMAN_PIECE) or self.check_win(board, AI_PIECE) or len(self.get_valid_locations(board)) == 0

    # M returns pandas DataFrame representing the playing field, columns are labeled with letters (A to G) and the numbers 1 to 6
    def getState(self, board):                                  
        state = []                                        
        
        for i in range(len(board)): # M the board is split into a list 
            for j in range(len(board[i])):
                state.append(board[i][j])

        state = pd.DataFrame(data = state).T # M converted into a pandas DataFrame

        state[state == "h"] = 1 # M values for "h", "r" and "0" are converted to 1, -1 and 0
        state[state == "0"] = 0
        state[state == "r"] = -1

        width = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        height = range(1, 7)
        cols = []

        for i in width:
            for j in height:
                cols.append(i + str(j))
        state.columns = cols

        return state


    # M mini_max() was extended with alpha-beta pruning, parameters alpha and beta were added and corresponding comparisons/conditions were set
    def mini_max(self, board, depth, maximizing_player, alpha, beta): # M
        possible_cols = self.get_valid_locations(board)
        is_terminal = self.terminal(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if self.check_win(board, AI_PIECE):
                    return None, 123456
                elif self.check_win(board, HUMAN_PIECE):
                    return None, -123456
                else: # game is over, no more valid moves
                    return None, 0
            else:
                predict = self.MLP_clf.predict_proba(self.getState(board)) # M classifier object uses DataFrame to make predictions about the probabilities for each possible game move.
                return None, (predict[0][2] - predict[0][0]) # M determination of the move point: (probability of winning - probability of losing)

        if maximizing_player:
            value = -1000
            column = random.choice(possible_cols)
            # iterate over possible columns
            for col in possible_cols:
                copy = self.make_move(board, col, AI_PIECE)
                new_score = self.mini_max(copy, depth - 1, False, alpha, beta)[1] # M 

                if DEBUG_MINIMAX:
                    print("maximize: " + str(value) + " " + "new_score: " + str(new_score) + " column: " + str(col) + " depth: " + str(depth))

                if new_score > value:
                    value = new_score
                    column = col

                alpha = max(alpha, value) # M
                if beta <= alpha:         # M
                    break                 # M beta cut-off

            return column, value

        # minimizing player
        else:
            value = 1000
            column = random.choice(possible_cols)

            for col in possible_cols:
                copy = self.make_move(board, col, HUMAN_PIECE)
                new_score = self.mini_max(copy, depth-1, True, alpha, beta)[1] # M

                if DEBUG_MINIMAX:
                    print("minimize: " + str(value) + " " + "new_score: " + str(new_score) + " column: " + str(col) + " depth: " + str(depth))

                if new_score < value:
                    value = new_score
                    column = col

                beta = min(beta, value) # M
                if beta <= alpha:       # M
                    break               # M alpha cut-off

            return column, value

    def printBoard(self, board):
        print("*************************************")
        print("")
        for row in range(ROWS):
            #print('      |', end='')
            for col in range(COLUMNS):
                print(board[ROWS-row-1][col] + '|', end='')
            print('')
        print('1|2|3|4|5|6|7|')
