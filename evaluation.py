from Board import Board
from Player import Player
from Exceptions import EndOfGameException
from typing import List


def evaluate(board: Board):
    white, black = board.board_weight
    return black - white


def minimax(board: Board, players: List[Player], current: Player, depth, is_max, alpha, beta):
    print('minimax')
    player = players[0] if current.name == 'BLACK' else players[1]
    if depth == 0:
        return evaluate(board)
    try:
        ways = board.pre_processing(player)
    except EndOfGameException as e:
        if e.msg == 'DRAW':
            return 0
        else:
            if player.name == 'WHITE':
                return 10000
            return -10000
    if is_max:
        best_value = float('-inf')
        for src, dst in ways:
            board.move(src, dst)
            board.post_processing(player, src, dst)
            value = minimax(board, players, player, depth - 1, False, alpha, beta)
            board.back(src, dst)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                return best_value
        return best_value
    else:
        best_value = float('+inf')
        for src, dst in ways:
            board.move(src, dst)
            value = minimax(board, players, player, depth - 1, True, alpha, beta)
            board.back(src, dst)
            best_value = min(best_value, value)
            beta = min(alpha, best_value)
            if beta <= alpha:
                return best_value
        return best_value


def find_best_move(board, players: List[Player], current: Player, ways):
    # print(board.board[7][1].top.name)
    best_value = float('-inf')
    best_move = None
    for src, dst in ways:
        # print('find best move')
        # print(src, dst)
        board.move(src, dst)
        board.post_processing(current, src, dst)
        move_value = minimax(board, players, current, 1, True, float('-inf'), float('inf'))
        board.back(src, dst)
        if move_value > best_value:
            best_value = move_value
            best_move = (src, dst)
    return best_move
