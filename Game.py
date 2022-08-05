from Player import Player
from Board import Board
from Exceptions import EndOfGame, InputException, MoveException


class Game:
    """
    game class has a board and a function named: control, that gives
    one move from the user and implement it.
    every move specified by a source and destination, your piece located
    in src and goes to the des.
    """
    def __init__(self):
        self.players = [Player('WHITE'), Player('BLACK')]
        self.board = Board()
        self.turn = 0
        """
        each one of 64 chess houses defined by a number in range 1-8
        and a character in range A-H, so we should convert the input into
        our 2D Array indexes from (0, 0)-(7, 7).
        """
        self.inv_columns = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        self.inv_rows = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, }
        self.columns = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}

    def control(self):
        src = input('source:    ')
        src = self.inv_rows.get(src[0], None), self.inv_columns.get(src[1], None)
        if None in src:
            raise InputException('invalid src')
        dst = input('destination:    ')
        dst = self.inv_rows.get(
            dst[0], None), self.inv_columns.get(dst[1], None)
        if None in dst:
            raise InputException('invalid dst')
        return src, dst

    def main_loop(self):
        while True:
            try:
                src, dst = self.control()
            except (MoveException, InputException) as e:
                print('error ' + e.msg)
            except EndOfGame as e:
                print('error ' + e.msg)
                break
            except KeyboardInterrupt:
                break
        exit(0)
