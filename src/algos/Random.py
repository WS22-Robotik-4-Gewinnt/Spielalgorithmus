from random import randint

class Random():
    def __init__(self, curr_board, row_count, column_count, ai_piece, human_piece):
        self.board = curr_board
        self.rows = row_count
        self.columns = column_count
        self.ai_piece = ai_piece
        self.human_piece = human_piece

    def choose_column(self):
        return randint(1, 7)
