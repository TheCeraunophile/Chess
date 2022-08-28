from Board import Board
from Exceptions import EndOfGameException
from typing import List


def evaluate(board: Board):
    white = board.board_weight.get(0)
    black = board.board_weight.get(1)
    return black - white


def minimax(board: Board, players: List[int], current: int, depth, is_max, alpha, beta):
    player = (current+1) % 2
    if depth == 0:
        return evaluate(board)
    try:
        ways = board.pre_processing(player)
    except EndOfGameException as e:
        if e.msg == 'DRAW':
            return 0
        else:
            if player == 0:
                return 1000
            return -1000
    if is_max:
        best_value = float('-inf')
        for src, dst in ways:
            board.move(src, dst)
            value = minimax(board, players, player, depth - 1, False, alpha, beta)
            board.back(src, dst)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value
    else:
        best_value = float('+inf')
        for src, dst in ways:
            board.move(src, dst)
            value = minimax(board, players, player, depth - 1, True, alpha, beta)
            board.back(src, dst)
            best_value = min(best_value, value)
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value


def find_best_move(board, players: List[int], current: int, ways):
    best_value = float('-inf')
    best_move = None
    for src, dst in ways:
        board.move(src, dst)
        move_value = minimax(board, players, current, 3, False, float('-inf'), float('inf'))
        board.back(src, dst)
        if move_value > best_value:
            best_value = move_value
            best_move = (src, dst)
    return best_move
