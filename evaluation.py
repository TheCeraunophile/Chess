from Piece import Piece
from Node import Node
from Board import Board


def evaluate(board: Board, valid_nodes):
    pass


def heuristic(board: Board, player):
    white, black = board.weight_of_board()
    return white - black if player.name == 'WHITE' else black - white
    # score = white - black if player.name == 'WHITE' else black - white
    # white_center = 0
    # black_center = 0
    # for i in range(4, 6):
    #     for j in range(4, 6):
    #         try:
    #             name = board.board[i][j].top.owner.name
    #             if name == 'WHITE':
    #                 white_center += 5
    #             else:
    #                 black_center += 5
    #         except Exception:
    #             continue
    # score += white_center - black_center if player.name == 'WHITE' else black_center - white_center


