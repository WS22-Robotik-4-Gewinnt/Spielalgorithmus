import random

HUMAN_PIECE = 'h'
AI_PIECE = 'r'
EMPTY_PIECE = '0'

DEBUG_MINIMAX = False

COLUMNS = 7
ROWS = 6

class Minimax():

    board = []
    
    def __init__(self, board):
        self.board = [x[:] for x in board]

    def choose_column(self, board):
        self.board = [x[:] for x in board]
        col, minimax_score = self.mini_max(self.board, 4, True)
        print("==================")
        print("the winning col: " + str(col))
        print("score for move :" + str(minimax_score))
        return col

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
            for row in range(ROWS):
                if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
                    if DEBUG_MINIMAX:
                        print("###shrinking diagonal win")
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

    # look at a part that contains 4 locations and rate as score
    def calc_area(self, area):
        score = 0

        if area.count(AI_PIECE) == 4:
            score += 15
        if area.count(AI_PIECE) == 3 and area.count(EMPTY_PIECE) == 1:
            score += 3
        if area.count(AI_PIECE) == 2 and area.count(EMPTY_PIECE) == 2:
            score += 1
        if area.count(HUMAN_PIECE) == 3 and area.count(EMPTY_PIECE) == 1:
            score -= 2

        return score

    def calc_utility(self, board):
        score = 0
        area = []

        # extra score for the center column
        center_col = [board[row][3] for row in range(6)]
        center_score = center_col.count(AI_PIECE)
        score += center_score * 3.5

        # score horizontal 24
        for row in range(ROWS):
            for col in range(COLUMNS - 3):
                score += self.calc_area(board[row][col:col+4])

        # score vertical 21
        for col in range(COLUMNS):
            for row in range(ROWS - 3):
                for x in range(4):
                    area.append(board[row+x][col])
                score += self.calc_area(area)
                area = []

        for row in range(ROWS - 3):
            for col in range(COLUMNS - 3):
                for x in range(4):
                    area.append(board[row-x][col-x])

                score += self.calc_area(area)
                area = []

        for row in range(3, ROWS):
            for col in range(COLUMNS-3):
                for x in range(4):
                    area.append(board[row-x][col+x])

                score += self.calc_area(area)
                area = []

        #print("current score for whole board: " + str(score))
        return score

    # depth first search
    def mini_max(self, board, depth, maximizing_player):
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
                return None, self.calc_utility(board)

        if maximizing_player:
            value = -1000
            column = random.choice(possible_cols)
            # iterate over possible columns
            for col in possible_cols:
                copy = self.make_move(board, col, AI_PIECE)
                new_score = self.mini_max(copy, depth - 1, False)[1]

                if DEBUG_MINIMAX:
                    print("maximize: " + str(value) + " " + "new_score: " + str(new_score) + " column: " + str(col) + " depth: " + str(depth))

                if new_score > value:
                    value = new_score
                    column = col

            return column, value

        # minimizing player
        else:
            value = 1000
            column = random.choice(possible_cols)

            for col in possible_cols:
                copy = self.make_move(board, col, HUMAN_PIECE)
                new_score = self.mini_max(copy, depth-1, True)[1]

                if DEBUG_MINIMAX:
                    print("minimize: " + str(value) + " " + "new_score: " + str(new_score) + " column: " + str(col) + " depth: " + str(depth))

                if new_score < value:
                    value = new_score
                    column = col

            return column, value
