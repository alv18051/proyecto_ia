import random
import numpy as np

ROWS, COLS = 6, 7

def evaluate_board(board, player_turn_id):
    opponent_id = 2 if player_turn_id == 1 else 1
    score = 0

    for row in range(ROWS):
        for col in range(COLS - 3):
            window = [board[row][col + i] for i in range(4)]
            score += evaluate_window(window, player_turn_id, opponent_id)

    for row in range(ROWS - 3):
        for col in range(COLS):
            window = [board[row + i][col] for i in range(4)]
            score += evaluate_window(window, player_turn_id, opponent_id)

    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [board[row - i][col + i] for i in range(4)]
            score += evaluate_window(window, player_turn_id, opponent_id)

    for row in range(3, ROWS):
        for col in range(3, COLS):
            window = [board[row - i][col - i] for i in range(4)]
            score += evaluate_window(window, player_turn_id, opponent_id)

    return score

def evaluate_window(window, player_turn_id, opponent_id):
    score = 0
    count_player = window.count(player_turn_id)
    count_opponent = window.count(opponent_id)

    if count_player == 4:
        score += 10

    elif count_player == 3 and window.count(0) == 1:
        score += 5

    elif count_player == 2 and window.count(0) == 2:
        score += 2

    if count_opponent == 3 and window.count(0) == 1:
        score -= 4

    return score

def minMax(board, depth, alpha, beta, maximizing_player, player_turn_id):
    available_moves = [i for i in range(COLS) if board[0][i] == 0]

    if depth == 0 or not available_moves:
        score = evaluate_board(board, player_turn_id)
        return None, score

    if maximizing_player:
        max_score = -1000000000000000000000000000
        best_move = None

        for move in available_moves:
            new_board = generate(board, move, player_turn_id)
            _, score = minMax(new_board, depth - 1, alpha, beta, False, player_turn_id)

            if score > max_score:
                max_score = score
                best_move = move

            alpha = max(alpha, max_score)

            if alpha >= beta:
                break

        return best_move, max_score
    else:
        min_score = 1000000000000000000000000000
        best_move = None

        for move in available_moves:
            new_board = generate(board, move, 2 if player_turn_id == 1 else 1)
            _, score = minMax(new_board, depth - 1, alpha, beta, True, player_turn_id)

            if score < min_score:
                min_score = score
                best_move = move

            beta = min(beta, min_score)

            if alpha >= beta:
                break

        return best_move, min_score

def generate(board, column_index, player_turn_id):
    new_board = [row.copy() for row in board]

    for row in range(ROWS - 1, -1, -1):
        if new_board[row][column_index] == 0:
            new_board[row][column_index] = player_turn_id
            break

    return new_board

def move(board, player_turn_id):
    max_depth = 4
    alpha = -1000000000000000000000000000
    betha = 1000000000000000000000000000
    board_burner = [row.copy() for row in board]
    column_best_move, _ = minMax(board_burner, max_depth, alpha, betha, True, player_turn_id)
    # num = random.randint(0,6)
    # return num
    return column_best_move

