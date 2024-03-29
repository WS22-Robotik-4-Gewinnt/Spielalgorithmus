import numpy as np
import random
import pygame
import sys
import math

BLUE = (0, 20, 200)
BLACK = (0, 20, 0)
RED = (200, 20, 0)
YELLOW = (200, 200, 20)

Reihen = 6
Spalten = 7

PLAYER = 0
COMP = 1

EMPTY = 0
PLAYER_PIECE = 1
COMP_PIECE = 2

WINDOW_LENGTH = 4


#Initialising
def createBoard():
    board = np.zeros((Reihen, Spalten))
    return board


def dropPiece(board, row, col, piece):
    board[row][col] = piece


def isValidLocation(board, col):
    return board[Reihen - 1][col] == 0


def getNextOpenRow(board, col):
    for r in range(Reihen):
        if board[r][col] == 0:
            return r


def printBoard(board):
    print(np.flip(board, 0))


def winningMove(board, piece):
    # übebprüfung hor. gewinnen
    for c in range(Spalten - 3):
        for r in range(Reihen):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # übebprüfung ver. gewinnen
    for c in range(Spalten):
        for r in range(Reihen - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # überprüfen positiv geneigte Diagonalen
    for c in range(Spalten - 3):
        for r in range(Reihen - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # überprüfen negativ geneigte Diagonalen
    for c in range(Spalten - 3):
        for r in range(3, Reihen):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def evaluateWindow(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = COMP_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def scoreByposition(board, piece):
    score = 0

    center_array = [int(i) for i in list(board[:, Spalten // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    for r in range(Reihen):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(Spalten - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluateWindow(window, piece)

    for c in range(Spalten):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(Reihen - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluateWindow(window, piece)

    for r in range(Reihen - 3):
        for c in range(Spalten - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluateWindow(window, piece)

    for r in range(Reihen - 3):
        for c in range(Spalten - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluateWindow(window, piece)

    return score


def isNode(board):
    return winningMove(board, PLAYER_PIECE) or winningMove(board, COMP_PIECE) or len(getGoodLocations(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = getGoodLocations(board)
    is_terminal = isNode(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winningMove(board, COMP_PIECE):
                return (None, 100000000000000)
            elif winningMove(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, scoreByposition(board, COMP_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = getNextOpenRow(board, col)
            b_copy = board.copy()
            dropPiece(b_copy, row, col, COMP_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = getNextOpenRow(board, col)
            b_copy = board.copy()
            dropPiece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def getGoodLocations(board):
    valid_locations = []
    for col in range(Spalten):
        if isValidLocation(board, col):
            valid_locations.append(col)
    return valid_locations


def pickMove(board, piece):
    valid_locations = getGoodLocations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = getNextOpenRow(board, col)
        temp_board = board.copy()
        dropPiece(temp_board, row, col, piece)
        score = scoreByposition(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def boardDraw(board):
    for c in range(Spalten):
        for r in range(Reihen):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(Spalten):
        for r in range(Reihen):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == COMP_PIECE:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


board = createBoard()
printBoard(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = Spalten * SQUARESIZE
height = (Reihen + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
boardDraw(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, COMP)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if isValidLocation(board, col):
                    row = getNextOpenRow(board, col)
                    dropPiece(board, row, col, PLAYER_PIECE)

                    if winningMove(board, PLAYER_PIECE):
                        label = myfont.render("Spieler 1 gewinnt!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    printBoard(board)
                    boardDraw(board)

    if turn == COMP and not game_over:

        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

        if isValidLocation(board, col):
            row = getNextOpenRow(board, col)
            dropPiece(board, row, col, COMP_PIECE)

            if winningMove(board, COMP_PIECE):
                label = myfont.render("Spieler 2 gewinnt!", 1, YELLOW)
                screen.blit(label, (40, 10))
                game_over = True

            printBoard(board)
            boardDraw(board)

            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(3000)