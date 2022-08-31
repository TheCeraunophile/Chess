from Board import Board
from Exceptions import EndOfGameException
from typing import List
import random


def evaluate(board: Board, id):
    white = board.board_weight.get(0)
    black = board.board_weight.get(1)
    return black - white if id else white - black


def minimax(board: Board, players: List[int], current: int, depth, is_max, alpha, beta, id):
    player = (current+1) % 2
    if depth == 0:
        return evaluate(board, id)
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
            value = minimax(board, players, player, depth - 1, False, alpha, beta, id)
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
            value = minimax(board, players, player, depth - 1, True, alpha, beta, id)
            board.back(src, dst)
            best_value = min(best_value, value)
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value


def find_best_move(board, players: List[int], current: int, ways):
    best_value = float('-inf')
    best_move = None
    stack = []
    for src, dst in ways:
        board.move(src, dst)
        move_value = minimax(board, players, current, 3, False, float('-inf'), float('inf'), current)
        board.back(src, dst)
        if move_value > best_value:
            stack = []
            best_value = move_value
            best_move = (src, dst)
            stack.append(best_move)
        elif move_value == best_value:
            stack.append((src, dst))
    if len(stack) == 0:
        return stack[0]
    return stack[random.randrange(len(stack))]


def find_middle_move(board, players: List[int], current: int, ways):
    best_value = float('-inf')
    best_move = None
    stack = []
    for src, dst in ways:
        board.move(src, dst)
        move_value = minimax(board, players, current, 2, False, float('-inf'), float('inf'), current)
        board.back(src, dst)
        if move_value > best_value:
            best_value = move_value
            best_move = (src, dst)
            stack = []
            stack.append(best_move)
        elif move_value == best_value:
            stack.append((src, dst))
    if len(stack) == 0:
        return stack[0]
    return stack[random.randrange(len(stack))]
