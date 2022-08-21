from Piece import Piece
from typing import List


class Node:
    def __init__(self, name, index, piece: Piece = None):
        self.name = name
        self.top = piece
        self.down = []
        self.index = index

    def add(self, piece: Piece):
        self.down.append(self.top)
        self.top = piece

    def pick_up(self):
        self.down.append(self.top)
        tmp = self.top
        self.top = None
        return tmp

    def back(self):
        try:
            self.top = self.down.pop()
        except IndexError:
            print('error :/\n')

    def get_down(self):
        return self.down[len(self.down)-1]
