from SetPin import king_knight, rook_bishop_queen, get_pawn


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
        self.name, self.shape = ('WHITE KING', u'\u265A') if owner == 0 else ('BLACK KING', u'\u2654')
        self.weight = 12

    def check_move(self, board, src: tuple, check):
        return king_knight(board, src, 12)


class Queen(Piece):
    def __init__(self, owner: int):
        super().__init__(owner)
        self.name, self.shape = ('WHITE QUEEN', u'\u265B') if owner == 0 else ('BLACK QUEEN', u'\u2655')
        self.weight = 9

    def check_move(self, board, src: tuple, check):
        return rook_bishop_queen(board, src, 9, check)


class Rook(Piece):
    def __init__(self, owner: int):
        super().__init__(owner)
        self.name, self.shape = ('WHITE ROOK', u'\u265C') if owner == 0 else ('BLACK ROOK', u'\u2656')
        self.weight = 5

    def check_move(self, board, src: tuple, check):
        return rook_bishop_queen(board, src, 5, check)


class Knight(Piece):
    def __init__(self, owner: int):
        super().__init__(owner)
        self.name, self.shape = ('WHITE KNIGHT', u'\u265E') if owner == 0 else ('BLACK KNIGHT', u'\u2658')
        self.weight = 3

    def check_move(self, board, src: tuple, check):
        return king_knight(board, src, 3)


class Bishop(Piece):
    def __init__(self, owner: int):
        super().__init__(owner)
        self.name, self.shape = ('WHITE BISHOP', u'\u265D') if owner == 0 else ('BLACK BISHOP', u'\u2657')
        self.weight = 3

    def check_move(self, board, src: tuple, check):
        return rook_bishop_queen(board, src, 3, check)


class Pawn(Piece):
    def __init__(self, owner: int):
        super().__init__(owner)
        self.name, self.shape = ('WHITE PAWN', u'\u265F') if owner == 0 else ('BLACK PAWN', u'\u2659')
        self.weight = 1

    def check_move(self, board, src: tuple, check):
        return get_pawn(board, src, check)
