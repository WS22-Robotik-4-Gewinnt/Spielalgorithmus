
COLUMNS = 7
ROWS = 6

HUMAN_PIECE = 'X'
AI_PIECE = 'O'

def check_win(board, player_piece):
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

def full_board(board):
    for row in range(ROWS):
        for col in range(COLUMNS):
            if board[row][col] == ' ':
                return False

    return True

def make_move(curr_board, col, piece):
    piece_placed = False

    # five because counting starts by zero
    x = 5

    while not piece_placed and x >= 0:
        if curr_board[x][col-1] == " ":
            curr_board[x][col-1] = piece
            piece_placed = True
        x -= 1
