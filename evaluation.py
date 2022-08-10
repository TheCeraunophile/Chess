from Board import Board
from Player import Player
from Exceptions import EndOfGameException
from typing import List


def evaluate(board: Board, player):
    white, black = board.weight_of_board()
    return white - black if player.name == 'WHITE' else black - white


def minimax(board: Board, players: List[Player], current: Player, depth, is_max, alpha, beta, max_depth):
    if depth == max_depth:
        return evaluate(board, current)

    player = players[0] if current.name == 'BLACK' else players[1]

    if is_max:
        best_value = float('-inf')
        try:
            piece_to_moves = board.pre_processing(player)
        except EndOfGameException as e:
            if e.msg == 'DRAW':
                return 0
            else:
                return 10000  # maybe -100000
        else:
            ways = []
            for src in piece_to_moves.keys():
                dsts = piece_to_moves.get(src)
                for dst in dsts:
                    ways.append((src, dst))
            for src, dst in ways:
                board.move(src, dst)
                value = minimax(board, players, player, depth+1, False, alpha, beta, max_depth)
                board.back(src, dst)
                best_value = max(best_value, value)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value
    else:
        best_value = float('inf')
        try:
            piece_to_moves = board.pre_processing(player)
        except EndOfGameException as e:
            if e.msg == 'DRAW':
                return 0
            else:
                return 10000  # maybe -100000
        else:
            ways = []
            for src in piece_to_moves.keys():
                dsts = piece_to_moves.get(src)
                for dst in dsts:
                    ways.append((src, dst))
            for src, dst in ways:
                board.move(src, dst)
                value = minimax(board, players, player, depth+1, False, alpha, beta, max_depth)
                board.back(src, dst)
                best_value = min(best_value, value)
                beta = min(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value


def find_best_move(board, players: List[Player], current: Player,  ways):
    best_value = float('-inf')
    best_move = ways[0]
    for src, dst in ways:
        board.move(src, dst)
        move_value = minimax(board, players, current, 0, False, float('-inf'), float('inf'), 6)
        board.back(src, dst)
        if move_value > best_value:
            best_value = move_value
            best_move = (src, dst)
    return best_move


def move_detection(board: Board, players: List[Player], current: Player, valid_nodes):
    result = []
    for src in valid_nodes.keys():
        dsts = valid_nodes.get(src)
        for dst in dsts:
            result.append((src, dst))
    return find_best_move(board, players, current, result)
