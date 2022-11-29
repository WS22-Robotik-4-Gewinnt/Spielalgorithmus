from utils import check_win

HUMAN_PIECE = 'X'
AI_PIECE = 'O'

class Minimax():
    def __init__(self, curr_board, row_count, column_count, ai_piece, human_piece):
        self.board = curr_board
        self.rows = row_count
        self.columns = column_count
        self.ai_piece = ai_piece
        self.human_piece = human_piece

    def choose_column(self):
        col, minimax_score = self.mini_max(self.board, 5, True)
        print(minimax_score)
        return col

    def get_valid_locations(self, board):
        valid_locations = []

        for column in range(self.columns):
            if board[0][column] == ' ':
                valid_locations.append(column)

        return valid_locations

    def open_row(self, col):
        for r in range(self.rows-1, -1, -1):
            if self.board[r][col] == 0:
                return r
    
    def terminal(self, board):
        return check_win(board, HUMAN_PIECE) or check_win(board, AI_PIECE) or len(self.get_valid_locations(board)) == 0

    # look at a part that contains 4 locations and rate as score
    def calc_area(self, area):
        score = 0
        opponent = self.human_piece
        player = self.ai_piece

        if area.count(player) == 4:
            score += 15
        if area.count(player) == 3 and area.count('') == 1:
            score += 3
        if area.count(player) == 2 and area.count('') == 2:
            score += 1
        if area.count(opponent) == 3 and area.count('') == 1:
            score -= 2

        return score

    def calc_utility(self, board):
        score = 0
        area = []
        
        # TODO: Score center column
        #center_array = [int(i) for i in list(self.board[:,COLS//2])]
        #center_count = center_array.count(piece)
        #score += center_count * 6

        # score horizontal 24
        for row in range(self.rows):
            for col in range(self.columns - 3):
                score += self.calc_area(board[row][col:col+4])
        
        # score vertical 21
        for col in range(self.columns):
            for row in range(self.rows - 3):
                for x in range(4):
                    area.append(board[row][col])
                score += self.calc_area(area)

        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                for x in range(4):
                    area.append(board[row-x][col-x])

                score += self.calc_area(area)
                area = []

        for row in range(3, self.rows):
            for col in range(self.columns-3):
                for x in range(4):
                    area.append(board[row-x][col+x])
                
                score += self.calc_area(area)
                area = []
    
        return score

    # depth first search
    def mini_max(self, board, depth, maximizing_player):

        possible_cols = self.get_valid_locations(board)
        is_terminal = self.terminal(board)

        # TODO: return current value
        if depth == 0:
            if is_terminal:
                if check_win(self.board, AI_PIECE):
                    return None, 123456
                elif check_win(self.board, HUMAN_PIECE):
                    return None, -123456
                else: # Game is over, no more valid moves
                    return None, 0
            else:
                return None, self.calc_utility(board)

        if maximizing_player:
            value = -1000
            column = 1
            # iterate over possible columns
            for col in possible_cols:
                board_cp = board.copy()
                make_move(board_cp, col, self.ai_piece)
                new_score = self.mini_max(board_cp, depth - 1, False)[1]

                if new_score > value:
                    value = new_score
                    column = col

                # some debug prints
                print("maximize")
                print(value)
                print(new_score)
            return column, value

        # minimizing player
        else:
            value = +1000
            column = 1

            for col in possible_cols:
                board_cp = self.board.copy()
                make_move(board_cp, col, self.human_piece)
                new_score = self.mini_max(board_cp, depth-1, True)[1]

                if new_score < value:
                    value = new_score
                    column = col

                # some debug prints
                print("minimize")
                print(value)
                print(new_score)
            return column, value
