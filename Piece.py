from Player import Player
from Laws import diagonal_move, polar_move, king_move, knight_move, pawn_move


class Piece:
    def __init__(self, owner: Player):
        self.owner = owner
        self.name = ''

    def check_move(self, board, src: tuple):
        pass


class Knight(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE KNIGHT' if owner.name == 'WHITE' else 'BLACK KNIGHT'

    def check_move(self, board, src: tuple):
        return knight_move(board, self.owner, src)


class King(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE KING' if owner.name == 'WHITE' else 'BLACK KING'

    def check_move(self, board, src: tuple):
        return king_move(board, self.owner, src)


class Rook(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE ROOK' if owner.name == 'WHITE' else 'BLACK ROOK'

    def check_move(self, board, src: tuple):
        return polar_move(board, self.owner, src)


class Bishop(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE BISHOP' if owner.name == 'WHITE' else 'BLACK BISHOP'

    def check_move(self, board, src: tuple):
        return diagonal_move(board, self.owner, src)


class Queen(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE QUEEN' if owner.name == 'WHITE' else 'BLACK QUEEN'

    def check_move(self, board, src: tuple):
        tmp = []
        tmp.extend(polar_move(board, self.owner, src))
        tmp.extend(diagonal_move(board, self.owner, src))
        return tmp


class Pawn(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE PAWN' if owner.name == 'WHITE' else 'BLACK PAWN'

    def check_move(self, board, src: tuple):
        result = pawn_move(board, self.owner, src)
        return result
