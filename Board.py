from Exceptions import EndOfGameException
from typing import List
from Piece import *
from Node import Node
from itertools import product


class Board:
    def __init__(self, players: List[Player]):
        self.players = players
        self.board: List[List[Node]] = []
        self.kings = {players[0]: (0, 3), players[1]: (7, 3)}
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

    def restricted_check(self, player, other_player):
        rest = []
        king_loc = self.kings.get(other_player)
        for src in self.pieces.get(player):
            if isinstance(self.board[src[0]][src[1]].top, (Queen, Bishop, Rook)):
                piece = self.board[src[0]][src[1]].top
                i, j = src
                if isinstance(piece, Rook):
                    if i == king_loc[0] or j == king_loc[1]:
                        rest.append(src)
                if isinstance(piece, Bishop):
                    if (i + j) % 2 == (king_loc[0] + king_loc[1]) % 2:
                        rest.append(src)
                if isinstance(piece, Queen):
                    if (i + j) % 2 == (king_loc[0] + king_loc[1]) % 2 or i == king_loc[0] or j == king_loc[1]:
                        rest.append(src)
        return rest

    def pre_processing(self, player: Player):
        other_player = self.players[1] if player.name == 'WHITE' else self.players[0]
        restricted = self.restricted_check(player, other_player)
        impossible = []
        pinned = []
        check = False
        for src_piece in restricted:
            tmp_impossible, tmp_pinned = self.board[src_piece[0]][src_piece[1]].top.check_move(self.board, src_piece, True)
            impossible.extend(tmp_impossible)
            pinned.extend(tmp_pinned)
        moves = []
        for src_piece in self.pieces.get(player):
            moves.extend(self.board[src_piece[0]][src_piece[1]].top.check_move(self.board, src_piece, False))
        # remove any movement (in moves list) that has a src equal to pinned.values()
        # remove any king move with dst that exist in impossible.values()
        # if king src in impossible.values(): keep movement with king src,
        #       keep movement with dst equal to hunter src, keep movement with dst placed in ghost list.
        #           Except these, remove any movement.
        # now check the opponent's knight and pawn.
        # if there is any pawn or knight attack to the king, keep movement with king src,
        #       keep movement with dst equal to hunter src
        if len(moves) == 0:
            if check:
                raise EndOfGameException(player.name + ' Lose the Game')
            else:
                raise EndOfGameException('DRAW')
        return moves

    def post_processing(self, player, src, dst):
        self.move(src, dst)
        expand = {self.players[0]: 7, self.players[1]: 0}
        if isinstance(self.board[dst[0]][dst[1]].top, Pawn) and expand.get(self.board[dst[0]][dst[1]].top.owner) == dst[0]:
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
            line_buffer += '\n' + str(i+1) + '  '
            for j in range(8):
                tmp = self.board[i][j].top
                if tmp is None:
                    if (i+j) % 2 == 0:
                        line_buffer += u'\u25FB'
                    else:
                        line_buffer += u'\u25FC'
                else:
                    line_buffer += tmp.shape
                line_buffer += '  '
        return line_buffer
