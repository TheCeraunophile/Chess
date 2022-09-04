from Exceptions import EndOfGameException
from typing import List
from Piece import *
from Tile import Tile
from itertools import product
from movements.__init__ import Report
from termcolor import colored


class Board:
    def __init__(self):
        self.players = [0, 1]
        self.board: List[List[Tile]] = []
        self.kings = {0: (0, 4), 1: (7, 4)}
        columns = [0, 1, 2, 3, 4, 5, 6, 7]
        white_row = [0, 1]
        black_row = [6, 7]
        self.pieces = {0: [], 1: []}
        for i, j in product(white_row, columns):
            self.pieces[0].append((i, j))
        for i, j in product(black_row, columns):
            self.pieces[1].append((i, j))
        self.board_weight = {0: 1290, 1: 1290}
        self.create_board()
        self.is_castle = {0: False, 1: False}        
        self.castle_power_king = {0: True, 1: True}
        self.castle_power_rook_left = {0: True, 1: True}
        self.castle_power_rook_right = {0: True, 1: True}
        self.castle_stack = {0: [None, None, None], 1: [None, None, None]}

    def castle_stack_pop(self):
        self.castle_stack = {0: [None, None, None], 1: [None, None, None]}

    def create_board(self):
        tmp: List[List[Tile]] = []
        for i in range(8):
            column: List[Tile] = []
            for j in range(8):
                column.append(Tile())
            tmp.append(column)
        self.board = tmp
        self.initialization_board()

    def initialization_board(self):
        for i in range(0, 8):
            self.board[1][i].add(Pawn(0))
        for i in range(0, 8):
            self.board[6][i].add(Pawn(1))
        self.board[0][0].add(Rook(0))
        self.board[0][7].add(Rook(0))
        self.board[7][0].add(Rook(1))
        self.board[7][7].add(Rook(1))
        self.board[0][4].add(King(0))
        self.board[7][4].add(King(1))
        self.board[0][3].add(Queen(0))
        self.board[7][3].add(Queen(1))
        self.board[0][1].add(Knight(0))
        self.board[0][6].add(Knight(0))
        self.board[7][1].add(Knight(1))
        self.board[7][6].add(Knight(1))
        self.board[0][2].add(Bishop(0))
        self.board[0][5].add(Bishop(0))
        self.board[7][2].add(Bishop(1))
        self.board[7][5].add(Bishop(1))

    def back(self, src, dst):
        i, j = dst
        # ---------------------------------back from castle----------------------------------#
        if self.board[dst[0]][dst[1]].top is None and self.board[src[0]][src[1]].top is None:
            if self.board[src[0]][src[1]].get_down().weight == 12 and self.board[dst[0]][dst[1]].get_down().weight == 5:
                if j == 0 and (i == 0 or i == 7):
                    player = self.board[i][j].get_down().owner
                    self.board[dst[0]][dst[1]].back()
                    self.board[src[0]][src[1]].back()
                    self.pieces[player].append(src)
                    self.pieces[player].append(dst)
                    self.castle_power_king[player] = True
                    self.is_castle[player] = False
                    self.board[i][2].back()
                    self.board[i][3].back()
                    self.pieces[player].remove((i, 2))
                    self.pieces[player].remove((i, 3))
                    self.castle_power_rook_left[player] = True
                    self.kings[player] = src
                    return
                elif j == 7 and (i == 0 or i == 7):
                    player = self.board[i][j].get_down().owner
                    self.board[dst[0]][dst[1]].back()
                    self.board[src[0]][src[1]].back()
                    self.pieces[player].append(src)
                    self.pieces[player].append(dst)
                    self.castle_power_king[player] = True
                    self.is_castle[player] = False
                    self.board[i][6].back()
                    self.board[i][5].back()
                    self.pieces[player].remove((i, 6))
                    self.pieces[player].remove((i, 5))
                    self.castle_power_rook_right[player] = True
                    self.kings[player] = src
                    return
        # -----------------------------------------------main------------------------------------#

        player = self.board[i][j].top.owner
        if self.board[i][j].promote:
            self.board[i][j].promote = False
            self.board_weight[player] -= 9
        if isinstance(self.board[i][j].top, King):
            self.kings[player] = src
        self.pieces[player].remove(dst)
        self.pieces[player].append(src)
        if self.board[i][j].get_down() is not None:
            other_player = self.board[i][j].get_down().owner
            self.board_weight[other_player] += self.board[i][j].get_down().weight
            self.pieces[other_player].append(dst)
        self.board[i][j].back()
        self.board[src[0]][src[1]].back()

        if (src, dst) in self.castle_stack.get(player):
            if (src, dst) == self.castle_stack.get(player)[2]:
                self.castle_stack[player][2] = None
                self.castle_power_rook_right[player] = True
            if (src, dst) == self.castle_stack.get(player)[1]:
                self.castle_stack[player][1] = None
                self.castle_power_rook_left[player] = True
            if (src, dst) == self.castle_stack.get(player)[0]:
                self.castle_stack[player][0] = None
                self.castle_power_king[player] = True

    def move(self, src: tuple, dst: tuple):
        i, j = src
        player = self.board[i][j].top.owner
        # -------------------------------------------------------------------------------------------------------------------
        if self.castle_power_king.get(player) and (self.castle_power_rook_right.get(player) or self.castle_power_rook_left.get(player)):
            if self.board[i][j].top.weight == 5 or (src == self.kings.get(player) and (self.board[dst[0]][dst[1]].top is None or self.board[dst[0]][dst[1]].top.weight != 5)):
                if src == self.kings.get(player):
                    self.castle_power_king[player] = False
                    self.castle_stack[player][0] = (src, dst)
                elif j == 0 and self.castle_power_rook_left.get(player):
                    self.castle_power_rook_left[player] = False
                    self.castle_stack[player][1] = (src, dst)
                elif j == 7 and self.castle_power_rook_right.get(player):
                    self.castle_power_rook_right[player] = False
                    self.castle_stack[player][2] = (src, dst)
        # --------------------------------------------------------------------------------------------------------------
        if self.castle_power_king.get(player) and self.kings.get(player) == src:
            if self.board[dst[0]][dst[1]].top is not None and self.board[dst[0]][dst[1]].top.weight == 5:
                if self.castle_power_rook_right.get(player) or self.castle_power_rook_left.get(player):
                    if dst[1] == 7 and (dst[0] == 0 or dst[0] == 7) and self.castle_power_rook_right.get(player):
                        my_rook = self.board[dst[0]][dst[1]].pick_up()
                        my_king = self.board[i][j].pick_up()
                        self.castle_power_king[player] = False
                        self.is_castle[player] = True
                        self.pieces[player].remove(src)
                        self.pieces[player].remove(dst)
                        self.board[i][j + 2].add(my_king)
                        self.board[i][j + 1].add(my_rook)
                        self.pieces[player].append((i, j + 2))
                        self.pieces[player].append((i, j + 1))
                        self.kings[player] = (i, j + 2)
                        self.castle_power_rook_right[player] = False
                    elif dst[1] == 0 and (dst[0] == 0 or dst[0] == 7) and self.castle_power_rook_left.get(player):
                        my_rook = self.board[dst[0]][dst[1]].pick_up()
                        my_king = self.board[i][j].pick_up()
                        self.castle_power_king[player] = False
                        self.is_castle[player] = True
                        self.pieces[player].remove(src)
                        self.pieces[player].remove(dst)
                        self.board[i][j - 2].add(my_king)
                        self.board[i][j - 1].add(my_rook)
                        self.pieces[player].append((i, j - 2))
                        self.pieces[player].append((i, j - 1))
                        self.kings[player] = (i, j - 2)
                        self.castle_power_rook_left[player] = False
                    return
# ----------------------------------------------------------------------------------------------------------------------
        if isinstance(self.board[i][j].top, King):
            self.kings[player] = dst
        self.pieces[player].remove(src)
        self.pieces[player].append(dst)
        if self.board[dst[0]][dst[1]].top is not None:
            other_player = self.board[dst[0]][dst[1]].top.owner
            self.board_weight[other_player] -= self.board[dst[0]][dst[1]].top.weight
            self.pieces[other_player].remove(dst)
        tmp = self.board[src[0]][src[1]].pick_up()
        self.board[dst[0]][dst[1]].add(tmp)

    def pre_processing(self, player: int):
        Report.initialize()
        moves = []
        reserved = []
        opponent = (player+1) % 2
        king_lock = self.kings.get(player)

        for node in self.pieces.get(opponent):
            try:
                reserved.extend(self.board[node[0]][node[1]].top.check_move(self, node, True))
            except:
                print(node)
                raise

        is_check = Report.check
        for node in self.pieces.get(player):
            try:
                moves.extend(self.board[node[0]][node[1]].top.check_move(self, node, False))
            except:
                print(node)
                raise

        moves = [move for move in moves if move[0] != king_lock or move[1] not in [x[1] for x in reserved]]
        copy = moves[:]
        for pinned_path in Report.attacker_to_king_path_pinned:
            pinned_piece = pinned_path[len(pinned_path) - 1]
            attacker = pinned_path[0][0]
            for move in moves:
                if move[0] == pinned_piece and (move[1] not in [x[1] for x in pinned_path] and move[1] != attacker):
                    copy.remove(move)
        moves = copy
        check, three = Report.b_q_r_state()
        if check:
            if three:
                moves = [move for move in moves if move[0] == king_lock
                         or move[1] == Report.attacker_piece[0]
                         or move[1] in [x[1] for x in Report.attacker_to_king_path[0]]]
            else:
                moves = [move for move in moves if move[0] == king_lock
                         or move[1] == Report.attacker_piece[0]]
        kkp = Report.attacker_piece_two_way
        if kkp is not None:
            moves = [move for move in moves if move[0] == king_lock
                     or move[1] == kkp]

#        ---------------------------------------- castling -------------------------------------------#
        if self.castle_power_king.get(player) and not is_check:
            i = king_lock[0]
            p1 = True
            p2 = True
            rook1 = (i, 0)
            rook2 = (i, 7)
            if self.castle_power_rook_left.get(player):
                for j in [1, 2, 3]:
                    if self.board[i][j].top is not None or (i, j) in [x[1] for x in reserved]:
                        p1 = False
                        break
            if self.castle_power_rook_right.get(player):
                for j in [5, 6]:
                    if self.board[i][j].top is not None or (i, j) in [x[1] for x in reserved]:
                        p2 = False
                        break
            if p1 and self.castle_power_rook_left.get(player):
                moves.append((king_lock, rook1))
            if p2 and self.castle_power_rook_right.get(player):
                moves.append((king_lock, rook2))
#       ----------------------------- detect end game ----------------------------#
#         print(moves)
        if len(moves) == 0:
            if is_check:
                raise EndOfGameException(('Black' if player == 0 else 'White') + ' Won the game')
            else:
                raise EndOfGameException('DRAW')
        return moves

    def post_processing(self, player, src, dst, human):
        self.move(src, dst)
        expand = {0: 7, 1: 0}
        if self.board[dst[0]][dst[1]].top is not None:
            if expand.get(self.board[dst[0]][dst[1]].top.owner) == dst[0] \
                    and isinstance(self.board[dst[0]][dst[1]].top, Pawn):
                if human:
                    while True:
                        try:
                            list_pieces = {'Q': Queen, 'R': Rook, 'K': Knight, 'B': Bishop}
                            promoted_piece = input('Q: queen R: rook K: knight B: bishop\n')
                            tmp = list_pieces.get(promoted_piece)
                            self.board[dst[0]][dst[1]].top = tmp(player)
                            self.board[dst[0]][dst[1]].promote = True
                            break
                        except Exception:
                            continue
                else:
                    self.board[dst[0]][dst[1]].top = Queen(player)
                    self.board[dst[0]][dst[1]].promote = True
                self.board_weight[player] += 9

    def __str__(self):
        line_buffer = '   A  B  C  D  E  F  G  H'
        for i in range(7, -1, -1):
            line_buffer += '\n' + str(i + 1) + '  '
            for j in range(8):
                tmp = self.board[i][j].top
                if tmp is None:
                    if (i + j) % 2 == 0:
                        line_buffer += colored(u'\u25FC', 'white')
                    else:
                        line_buffer += colored(u'\u25FC', 'green')
                else:
                    line_buffer += tmp.shape
                line_buffer += '  '
        return line_buffer
