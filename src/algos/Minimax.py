

class Minimax():
    def __init__(self, curr_board, row_count, column_count, ai_piece, human_piece):
        self.board = curr_board
        self.rows = row_count
        self.columns = column_count
        self.ai_piece = ai_piece
        self.human_piece = human_piece

    def choose_column(self):
        col, minimax_score = self.mini_max(5, True)
        print(minimax_score)
        return col

    def get_valid_locations(self):
        valid_locations = []
        
        for column in range(self.columns):
            if self.board[0][column] == 0:
                valid_locations.append(column)

        return valid_locations

    def open_row(self, col):
        for r in range(self.rows-1, -1, -1):
            if self.board[r][col] == 0:
                return r

    def make_move(self, board, col, piece):
        piece_placed = False

        # five because counting starts by zero
        x = 5

        while not piece_placed:
            if board[x][col-1] == " ":
                board[x][col-1] = piece
                piece_placed = True
            x -= 1

    # look at a part that contains 4 locations and rate as score
    def calc_area(self, area, player):
        score = 0
        opponent = self.human_piece

        if player == self.human_piece:
            opponent = self.ai_piece

        if area.count(player) == 4:
            score += 15
        if area.count(player) == 3 and area.count('') == 1:
            score += 3
        if area.count(player) == 2 and area.count('') == 2:
            score += 1
        if area.count(opponent) == 3 and area.count('') == 1:
            score -= 2

        return score

    def calc_utility(self):
        score = 0
        area = []
        ## TODO: Score center column

        ## Score Horizontal
        for row in range(self.rows):
            for col in range(self.rows - 3):
                score += self.calc_area(self.board[row,col:col+4])

        for col in range(self.columns):
            for row in range(self.rows - 3):
                score += self.calc_area(self.board[row:row+4,col])

        for row in range(self.rows - 3):
            for col in range(self.columns - 3):
                for x in range(4):
                    area.append(self.board[row-x,col-x])

                score += self.calc_area(area)
                area = []

        for row in range(3, self.rows):
            for col in range(self.columns-3):
                for x in range(4):
                    area.append(self.board[row-x,col+x])
                
                score += self.calc_area(area)
                area = []

    # depth first search
    def mini_max(self, depth, maximizing_player):

        possible_cols = self.get_valid_locations()

        print(len(possible_cols))

        # TODO: return current value
        if depth == 0:
            return 10, 123

        if maximizing_player:
            value = -1000
            column = 1
            # iterate over possible columns
            for col in possible_cols:
                board_cp = self.board.copy()
                self.make_move(board_cp, col, self.ai_piece)

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
                self.make_move(board_cp, col, self.human_piece)
                new_score = self.mini_max(board_cp, depth-1, True)[1]

                if new_score < value:
                    value = new_score
                    column = col

                # some debug prints
                print("minimize")
                print(value)
                print(new_score)
            return column, value
