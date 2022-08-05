from Piece import Piece


class Node:
    def __init__(self, name, piece: Piece = None):
        self.name = name
        self.top = piece
        self.down = None

    def add(self, piece: Piece):
        self.down = self.top
        self.top = piece

    def pick_up(self):
        self.down = self.top
        self.top = None

    def back(self):
        self.top = self.down
        self.down = None
