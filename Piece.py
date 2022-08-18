from Player import Player
from Laws import diagonal_move, polar_move, king_move, knight_move, pawn_move


class Piece:
    def __init__(self, owner: Player):
        self.owner = owner
        self.name = ''
        self.shape = ''
        self.weight = 10

    def check_move(self, board, src: tuple, check_pinned):
        pass

    def __eq__(self, other):
        if other.owner.name == self.owner.name and self.name == other.name:
            return True
        return False

    def __hash__(self):
        return hash(self.owner) + hash(self.name)


class Knight(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE KNIGHT' if owner.name == 'WHITE' else 'BLACK KNIGHT'
        self.shape = u'\u265E' if owner.name == 'WHITE' else u'\u2658'
        self.weight = 30

    def check_move(self, board, src: tuple, check_pinned):
        return knight_move(board, self.owner, src)


class King(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE KING' if owner.name == 'WHITE' else 'BLACK KING'
        self.shape = u'\u265A' if owner.name == 'WHITE' else u'\u2654'
        self.weight = 900

    def check_move(self, board, src: tuple, check_pinned):
        return king_move(board, self.owner, src)


class Rook(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE ROOK' if owner.name == 'WHITE' else 'BLACK ROOK'
        self.shape = u'\u265C' if owner.name == 'WHITE' else u'\u2656'
        self.weight = 50

    def check_move(self, board, src: tuple, check_pinned):
        return polar_move(board, self.owner, src, check_pinned)


class Bishop(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE BISHOP' if owner.name == 'WHITE' else 'BLACK BISHOP'
        self.shape = u'\u265D' if owner.name == 'WHITE' else u'\u2657'
        self.weight = 30

    def check_move(self, board, src: tuple, check_pinned):
        return diagonal_move(board, self.owner, src, check_pinned)


class Queen(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE QUEEN' if owner.name == 'WHITE' else 'BLACK QUEEN'
        self.shape = u'\u265B' if owner.name == 'WHITE' else u'\u2655'
        self.weight = 90

    def check_move(self, board, src: tuple, check_pinned):
        reserved = []
        pinned = None
        check_path = None
        reserved1, pinned1, check_path1 = polar_move(board, self.owner, src, check_pinned)
        reserved.extend(reserved1)
        if pinned1:
            pinned = [pinned1]
        if check_path1:
            check_path = [check_path1]
        reserved2, pinned2, check_path2 = diagonal_move(board, self.owner, src, check_pinned)
        reserved.extend(reserved2)
        if pinned2:
            pinned.append(pinned2)
        if check_path2:
            if check_path is None:
                check_path = [check_path2]
            else:
                check_path.append(check_path2)
        return reserved, pinned, check_path


class Pawn(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE PAWN' if owner.name == 'WHITE' else 'BLACK PAWN'
        self.shape = u'\u265F' if owner.name == 'WHITE' else u'\u2659'
        self.weight = 10

    def check_move(self, board, src: tuple, check_pinned):
        return pawn_move(board, self.owner, src)
