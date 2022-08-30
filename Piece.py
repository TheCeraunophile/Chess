from SetPin import rook_bishop_queen, get_pawn, knight, king
from termcolor import colored


class Piece:
    def __init__(self, owner: int):
        self.owner = owner
        self.name = ''
        self.shape = ''
        self.weight = 0

    def check_move(self, board, src: tuple, check):
        pass

    def __eq__(self, other):
        if other.owner == self.owner and self.name == other.name:
            return True
        return False

    def __hash__(self):
        return hash(self.owner) + hash(self.name)


class King(Piece):
    def __init__(self, owner: int):
        super().__init__(owner)
        self.name, self.shape = ('WHITE KING', colored(u'\u265A', 'white')) if owner == 0 \
            else ('BLACK KING', colored(u'\u265A', 'cyan'))
        self.weight = 12

    def check_move(self, board, src: tuple, check):
        return king(board, src, self.owner, check)


class Queen(Piece):
    def __init__(self, owner: int):
        super().__init__(owner)
        self.name, self.shape = ('WHITE QUEEN', colored(u'\u265B', 'white')) if owner == 0 \
            else ('BLACK QUEEN', colored(u'\u265B', 'cyan'))
        self.weight = 9

    def check_move(self, board, src: tuple, check):
        return rook_bishop_queen(board, src, 9, check, self.owner)


class Rook(Piece):
    def __init__(self, owner: int):
        super().__init__(owner)
        self.name, self.shape = ('WHITE ROOK', colored(u'\u265C', 'white')) if owner == 0 \
            else ('BLACK ROOK', colored(u'\u265C', 'cyan'))
        self.weight = 5

    def check_move(self, board, src: tuple, check):
        return rook_bishop_queen(board, src, 5, check, self.owner)


class Knight(Piece):
    def __init__(self, owner: int):
        super().__init__(owner)
        self.name, self.shape = ('WHITE KNIGHT', colored(u'\u265E', 'white')) if owner == 0 \
            else ('BLACK KNIGHT', colored(u'\u265E', 'cyan'))
        self.weight = 3

    def check_move(self, board, src: tuple, check):
        return knight(board, src, self.owner, check)


class Bishop(Piece):
    def __init__(self, owner: int):
        super().__init__(owner)
        self.name, self.shape = ('WHITE BISHOP', colored(u'\u265D', 'white')) if owner == 0 \
            else ('BLACK BISHOP', colored(u'\u265D', 'cyan'))
        self.weight = 3

    def check_move(self, board, src: tuple, check):
        return rook_bishop_queen(board, src, 3, check, self.owner)


class Pawn(Piece):
    def __init__(self, owner: int):
        super().__init__(owner)
        self.name, self.shape = ('WHITE PAWN', colored(u'\u265F', 'white')) if owner == 0 \
            else ('BLACK PAWN', colored(u'\u265F', 'cyan'))
        self.weight = 1

    def check_move(self, board, src: tuple, check):
        return get_pawn(board, src, check, self.owner)
