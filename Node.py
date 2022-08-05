from Piece import Piece

class Node:
    def __init__(self, name, piece: Piece = None):
        """
        down contains a piece that killed by another piece,
        so if player hit your piece by a piece that be Achmez,
        your killed piece should back from down of Node into top of Node
        :param name: like 1A or 5H
        :param piece: like king
        """
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
