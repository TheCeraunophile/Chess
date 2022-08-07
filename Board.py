from Player import Player
from Exceptions import EndOfGameException
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
        try:
            if self.board[src[0]][src[1]].down.name == 'WHITE KING':
                self.kings[0] = src
            elif self.board[src[0]][src[1]].down.name == 'BLACK KING':
                self.kings[1] = src
        except Exception:
            pass

        if self.board[src[0]][src[1]].down is not None and self.board[src[0]][src[1]].down.owner == self.players[0]:
            self.white_pieces.append(src)
            self.white_pieces.remove(dst)
            if self.board[dst[0]][dst[1]].down == self.players[1]:
                self.black_pieces.append(dst)
        elif self.board[src[0]][src[1]].down is not None:
            self.black_pieces.append(src)
            self.black_pieces.remove(dst)
            if self.board[dst[0]][dst[1]].down == self.players[0]:
                self.white_pieces.append(dst)

        self.board[src[0]][src[1]].back()
        self.board[dst[0]][dst[1]].back()

    def move(self, src: tuple, dst: tuple):
        # print('check movement from ' + str(src[0]) + ' ' + str(src[1]) + ' to ' + str(dst[0]) + ' ' + str(dst[1]))
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
        stick = []
        for piece in pieces:
            i, j = piece
            tmp = self.board[i][j].top.check_move(self.board, (i, j))
            if tmp is not None:
                stick.extend(tmp)
        return king in stick

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
            self.back(src, dst)
        return result

    def pre_processing(self, player: Player):
        result = {}
        stick = []
        pieces = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j].top is not None:
                    if self.board[i][j].top.owner == player:
                        pieces.append((i, j))
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
        # for i in result.keys():
        #     print(str(i) + "    " + str(result.get(i)))
        return result

    def __str__(self):
        print('   A  B  C  D  E  F  G  H')
        for i in range(8):
            line_buffur = str(i+1) + '  '
            for j in range(8):
                tmp = self.board[i][j].top
                if tmp is None:
                    if (i+j) % 2 == 0:
                        line_buffur += u'\u25FB'
                    else:
                        line_buffur += u'\u25FC'
                else:
                    line_buffur += tmp.shape
                line_buffur += '  '
            print(line_buffur)
        return ''
