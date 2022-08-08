from Player import Player
from Exceptions import EndOfGameException, IllegalMoveException
from typing import List
from Piece import *
from Node import Node


class Board:
    def __init__(self, players: List[Player]):
        self.players = players
        self.board: List[List[Node]] = []
        self.kings = [(0, 3), (7, 3)]
        self.white_pieces = []
        self.black_pieces = []
        self.create_board()
        self.find_lists()

    def find_lists(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j].top is not None:
                    if self.board[i][j].top.owner == self.players[0]:
                        self.white_pieces.append((i, j))
                    else:
                        self.black_pieces.append((i, j))

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
        for i in range(0, 8, 7):
            self.board[0][i].add(Rook(self.players[0]))
        for i in range(0, 8, 7):
            self.board[7][i].add(Rook(self.players[1]))
        for i in range(1, 7, 5):
            self.board[0][i].add(Knight(self.players[0]))
        for i in range(1, 7, 5):
            self.board[7][i].add(Knight(self.players[1]))
        for i in range(2, 6, 3):
            self.board[0][i].add(Bishop(self.players[0]))
        for i in range(2, 6, 3):
            self.board[7][i].add(Bishop(self.players[1]))
        self.board[0][3].add(Queen(self.players[0]))
        self.board[7][3].add(Queen(self.players[1]))
        self.board[0][4].add(King(self.players[0]))
        self.board[7][4].add(King(self.players[1]))

    def back(self, src, dst):
        if self.board[dst[0]][dst[1]].top.name == 'WHITE KING':
            self.kings[0] = src
        elif self.board[dst[0]][dst[1]].top.name == 'BLACK KING':
            self.kings[1] = src
        if self.board[src[0]][src[1]].down.owner == self.players[0]:
            self.white_pieces.append(src)
            self.white_pieces.remove(dst)
            if self.board[dst[0]][dst[1]].down is not None:
                self.black_pieces.append(dst)
        else:
            self.black_pieces.append(src)
            self.black_pieces.remove(dst)
            if self.board[dst[0]][dst[1]].down is not None:
                self.white_pieces.append(dst)
        self.board[src[0]][src[1]].back()
        self.board[dst[0]][dst[1]].back()

    def move(self, src: tuple, dst: tuple):
        if self.board[src[0]][src[1]].top.name == 'WHITE KING':
            self.kings[0] = dst
        elif self.board[src[0]][src[1]].top.name == 'BLACK KING':
            self.kings[1] = dst
        if self.board[src[0]][src[1]].top.owner == self.players[0]:
            self.white_pieces.remove(src)
            self.white_pieces.append(dst)
            if dst in self.black_pieces:
                self.black_pieces.remove(dst)
        if self.board[src[0]][src[1]].top.owner == self.players[1]:
            self.black_pieces.remove(src)
            self.black_pieces.append(dst)
            if dst in self.white_pieces:
                self.white_pieces.remove(dst)
        tmp = self.board[src[0]][src[1]].pick_up()
        self.board[dst[0]][dst[1]].add(tmp)

    def check(self, player):
        if player == self.players[0]:
            pieces = self.black_pieces
            king = self.kings[0]
        else:
            pieces = self.white_pieces
            king = self.kings[1]
        for piece in pieces:
            i, j = piece
            tmp = self.board[i][j].top.check_move(self.board, (i, j))
            if king in tmp:
                return True
        return False

    def outer_section(self, a, b):
        temp = set(a)
        result = [value for value in b if value not in temp]
        return result

    def achmaz_detection(self, player, src, dst_s):
        result = []
        for dst in dst_s:
            self.move(src, dst)
            if not self.check(player):
                result.append(dst)
                # calling a function that gives heuristic score to this situation
            self.back(src, dst)
        return result

    def pre_processing(self, player: Player):
        result = {}
        stick = []
        if player.name == 'WHITE':
            pieces = self.white_pieces[:]
        else:
            pieces = self.black_pieces[:]
        for piece in pieces:
            i, j = piece
            tmp = self.board[i][j].top.check_move(self.board, (i, j))
            if tmp is not None:
                tmp = self.achmaz_detection(player, (i, j), tmp)
                stick.extend(tmp)
                result[(i, j)] = tmp
        if len(stick) == 0:
            if self.check(player):
                raise EndOfGameException(player.name + ' Lose the Game')
            else:
                raise EndOfGameException('DRAW')
        return result

    def post_processing(self, player, src, dst):
        if self.board[dst[0]][dst[1]].top is not None and self.board[dst[0]][dst[1]].top.name.endswith('KING'):
            raise IllegalMoveException("Don't Hit The King")
        else:
            self.move(src, dst)
        expand = {self.players[0]: 7, self.players[1]: 0}
        if isinstance(self.board[dst[0]][dst[1]].top, Pawn) and expand.get(self.board[dst[0]][dst[1]].top.owner) == dst[0]:
            self.board[dst[0]][dst[1]].down = None
            while True:
                try:
                    list_pieces = {'Q': Queen, 'R': Rook, 'K': Knight, 'B': Bishop}
                    promoted_piece = input('Q: queen R: rook K: knight B: bishop\n')
                    tmp = list_pieces.get(promoted_piece)
                    self.board[dst[0]][dst[1]].top = tmp(player)
                    break
                except Exception:
                    continue

    def weight_of_board(self):
        white_score = 0
        black_score = 0
        for src in self.white_pieces:
            i, j = src
            white_score += self.board[i][j].top.weight
        for src in self.black_pieces:
            i, j = src
            black_score += self.board[i][j].top.weight
        return white_score, black_score

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
