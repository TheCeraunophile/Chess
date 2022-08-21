from time import time
from Exceptions import EndOfGameException
from typing import List
from Piece import *
from Node import Node
from itertools import product
from copy import copy


class Board:
    def __init__(self, players: List[Player]):
        self.players = players
        self.board: List[List[Node]] = []
        self.kings = {players[0]: (0, 4), players[1]: (7, 4)}
        columns = [0, 1, 2, 3, 4, 5, 6, 7]
        white_row = [0, 1]
        black_row = [6, 7]
        self.pieces = {players[0]: [], players[1]: []}
        for i, j in product(white_row, columns):
            self.pieces[players[0]].append((i, j))
        for i, j in product(black_row, columns):
            self.pieces[players[1]].append((i, j))
        self.board_weight = {self.players[0]: 1290, self.players[1]: 1290}
        self.create_board()

    def create_board(self):
        tmp: List[List[Node]] = []
        for i in range(8):
            column: List[Node] = []
            for j in range(8):
                column.append(Node(str(i) + chr(j + 65), (i, j)))
            tmp.append(column)
        self.board = tmp
        self.initialization_board()

    def initialization_board(self):
        for i in range(0, 8):
            self.board[1][i].add(Pawn(self.players[0]))
        for i in range(0, 8):
            self.board[6][i].add(Pawn(self.players[1]))
        self.board[0][0].add(Rook(self.players[0]))
        self.board[0][7].add(Rook(self.players[0]))
        self.board[7][0].add(Rook(self.players[1]))
        self.board[7][7].add(Rook(self.players[1]))
        self.board[0][4].add(King(self.players[0]))
        self.board[7][4].add(King(self.players[1]))
        self.board[0][3].add(Queen(self.players[0]))
        self.board[7][3].add(Queen(self.players[1]))
        self.board[0][1].add(Knight(self.players[0]))
        self.board[0][6].add(Knight(self.players[0]))
        self.board[7][1].add(Knight(self.players[1]))
        self.board[7][6].add(Knight(self.players[1]))
        self.board[0][2].add(Bishop(self.players[0]))
        self.board[0][5].add(Bishop(self.players[0]))
        self.board[7][2].add(Bishop(self.players[1]))
        self.board[7][5].add(Bishop(self.players[1]))

    def back(self, src, dst):
        i, j = dst
        player = self.board[i][j].top.owner
        if isinstance(self.board[i][j].top, King):
            self.kings[player] = src
        self.pieces[player].remove(dst)
        self.pieces[player].append(src)
        if self.board[i][j].get_down() is not None:
            other_player = self.board[i][j].get_down().owner
            self.board_weight[other_player] += self.board[i][j].get_down().weight
            self.pieces[other_player].append(dst)
        self.board[i][j].back()
        self.board[src[0]][src[0]].back()

    def move(self, src: tuple, dst: tuple):
        p1 = time()
        i, j = src
        player = self.board[i][j].top.owner
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
        p2 = time()
        print(p2-p1)

    def status(self, opponent):
        reserved_nodes = []
        pinned_nodes = []
        detected_check = []
        n_k_p = []
        for src in self.pieces.get(opponent):
            if not isinstance(self.board[src[0]][src[1]].top, (Knight, Pawn, King)):
                reserved, pinned, check = self.board[src[0]][src[1]].top.check_move(self.board, src, True)
                reserved_nodes.extend(reserved)
                if pinned is not None:
                    pinned_nodes.append(pinned)
                if check is not None:
                    detected_check.append(check)
                continue
            if isinstance(self.board[src[0]][src[1]].top, Pawn):
                tmp, reserved = self.board[src[0]][src[1]].top.check_move(self.board, src, True)
                if reserved:
                    reserved_nodes.extend(reserved)
                continue
            reserved = self.board[src[0]][src[1]].top.check_move(self.board, src, True)
            n_k_p.extend(reserved)
        return reserved_nodes, pinned_nodes, detected_check, n_k_p

    def pre_processing(self, player: Player):
        p1 = time()
        opponent = self.players[1] if player.name == 'WHITE' else self.players[0]
        reserved, pinned, check_path, nkp = self.status(opponent)
        # print('reserved modes ', reserved)
        # print('pinned', pinned)
        # print('check - path', check_path)
        # print('nkp', nkp)
        check = False
        moves = []
        for src_piece in self.pieces.get(player):
            result = self.board[src_piece[0]][src_piece[1]].top.check_move(self.board, src_piece, False)
            if isinstance(self.board[src_piece[0]][src_piece[1]].top, (Pawn, Bishop, Rook, Queen)):
                moves.extend(result[0])
                continue
            if isinstance(self.board[src_piece[0]][src_piece[1]].top, (King, Knight)):
                moves.extend(result)
        # moves_src = list(set([move[0] for move in moves]))
        # moves_dst = list(set([move[1] for move in moves]))
        tmp_moves = moves[:]
        jj = list(set(move[1] for move in reserved))
        for move in tmp_moves:
            if move[0] == self.kings.get(player) and move[1] in jj:
                moves.remove(move)
        tmp_moves = moves[:]
        for pin in pinned:
            if pin:
                pinned_piece = pin[0][len(pin[0])-1]
                for move in tmp_moves:
                    if move[0] == pinned_piece and move[1] not in pin[0]:
                        moves.remove(move)
        tmp_moves = moves[:]
        for path in check_path:
            if path:
                check = True
                for move in tmp_moves:
                    if move[0] == self.kings.get(player) or move[1] in [x[1] for x in path] or move[1] == path[0][0]:
                        continue
                    else:
                        moves.remove(move)
        tmp_moves = moves[:]
        for move in nkp:
            if move[1] == self.kings.get(player):
                check = True
                for path in tmp_moves:
                    if path[0] != self.kings.get(player) and path[1] != move[0]:
                        moves.remove(path)
        # print('moves', moves)
        p2 = time()
        print(p2 - p1)
        if len(moves) == 0:
            if check:
                raise EndOfGameException(opponent.name + ' Won the game')
            else:
                raise EndOfGameException(':/')
        return moves

    def post_processing(self, player, src, dst):
        self.move(src, dst)
        expand = {self.players[0]: 7, self.players[1]: 0}
        if isinstance(self.board[dst[0]][dst[1]].top, Pawn) \
                and expand.get(self.board[dst[0]][dst[1]].top.owner) == dst[0]:
            self.board[dst[0]][dst[1]].down.pop()
            while True:
                try:
                    list_pieces = {'Q': Queen, 'R': Rook, 'K': Knight, 'B': Bishop}
                    promoted_piece = input('Q: queen R: rook K: knight B: bishop\n')
                    tmp = list_pieces.get(promoted_piece)
                    self.board[dst[0]][dst[1]].top = tmp(player)
                    break
                except Exception:
                    continue

    def __str__(self):
        line_buffer = '   A  B  C  D  E  F  G  H'
        for i in range(7, -1, -1):
            line_buffer += '\n' + str(i + 1) + '  '
            for j in range(8):
                tmp = self.board[i][j].top
                if tmp is None:
                    if (i + j) % 2 == 0:
                        line_buffer += u'\u25FB'
                    else:
                        line_buffer += u'\u25FC'
                else:
                    line_buffer += tmp.shape
                line_buffer += '  '
        return line_buffer
