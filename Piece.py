from Player import Player
from Laws import diagonal_move, polar_move, king_move, knight_move, pawn_move


class Piece:
    def __init__(self, owner: Player):
        self.owner = owner
        self.name = ''
        self.shape = ''
        self.weight = 10

    def check_move(self, board, src: tuple):
        pass


class Knight(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE KNIGHT' if owner.name == 'WHITE' else 'BLACK KNIGHT'
        self.shape = u'\u265E' if owner.name == 'WHITE' else u'\u2658'
        self.weight = 30

    def check_move(self, board, src: tuple):
        return knight_move(board, self.owner, src)


class King(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE KING' if owner.name == 'WHITE' else 'BLACK KING'
        self.shape = u'\u265A' if owner.name == 'WHITE' else u'\u2654'
        self.weight = 900

    def check_move(self, board, src: tuple):
        return king_move(board, self.owner, src)


class Rook(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE ROOK' if owner.name == 'WHITE' else 'BLACK ROOK'
        self.shape = u'\u265C' if owner.name == 'WHITE' else u'\u2656'
        self.weight = 50

    def check_move(self, board, src: tuple):
        return polar_move(board, self.owner, src)


class Bishop(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE BISHOP' if owner.name == 'WHITE' else 'BLACK BISHOP'
        self.shape = u'\u265D' if owner.name == 'WHITE' else u'\u2657'
        self.weight = 30

    def check_move(self, board, src: tuple):
        return diagonal_move(board, self.owner, src)


class Queen(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE QUEEN' if owner.name == 'WHITE' else 'BLACK QUEEN'
        self.shape = u'\u265B' if owner.name == 'WHITE' else u'\u2655'
        self.weight = 90

    def check_move(self, board, src: tuple):
        tmp = []
        tmp.extend(polar_move(board, self.owner, src))
        tmp.extend(diagonal_move(board, self.owner, src))
        return tmp


class Pawn(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE PAWN' if owner.name == 'WHITE' else 'BLACK PAWN'
        self.shape = u'\u265F' if owner.name == 'WHITE' else u'\u2659'
        self.weight = 10

    def check_move(self, board, src: tuple):
        result = pawn_move(board, self.owner, src)
        return result
