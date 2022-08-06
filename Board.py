from Player import Player
from Exceptions import EndOfGameException
from typing import List
from Piece import *
from Node import Node


class Board:
    def __init__(self, players: List[Player]):
        self.players = players
        self.board: List[List[Node]] = []
        self.create_board()

    def create_board(self):
        tmp: List[List[Node]] = []
        for i in range(8):
            column: List[Node] = []
            for j in range(8):
                column.append(Node(str(i) + chr(j + 65)))
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

    def give_piece(self, src: tuple):
        pass

    def back(self, src: tuple, dst: tuple):
        pass

    def move(self, player: Player, src: tuple, dst: tuple):
        pass

    def pre_processing(self, player: Player):
        result = {}
        stick = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j].top is not None and self.board[i][j].top.owner == player:
                    tmp = self.board[i][j].top.check_move(self.board, player, (i, j))
                    if tmp is not None:
                        stick.extend(tmp)
                        result[(i, j)] = tmp
        if len(stick) == 0:
            raise EndOfGameException('END Game')
        return result
