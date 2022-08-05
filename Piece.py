from Player import Player


class Piece:
    def __init__(self, owner: Player):
        self.owner = owner
        self.name = ''

    def check_move(self, player: Player, src: tuple, dst: tuple):
        pass


class Knight(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE KNIGHT' if owner.name == 'WHITE' else 'BLACK KNIGHT'

    def check_move(self, player: Player, src: tuple, dst: tuple):
        pass


class King(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE KING' if owner.name == 'WHITE' else 'BLACK KING'

    def check_move(self, player: Player, src: tuple, dst: tuple):
        pass


class Rook(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE QUEEN' if owner.name == 'WHITE' else 'BLACK QUEEN'

    def check_move(self, player: Player, src: tuple, dst: tuple):
        pass


class Bishop(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE BISHOP' if owner.name == 'WHITE' else 'BLACK BISHOP'

    def check_move(self, player: Player, src: tuple, dst: tuple):
        pass


class Queen(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE QUEEN' if owner.name == 'WHITE' else 'BLACK QUEEN'

    def check_move(self, player: Player, src: tuple, dst: tuple):
        pass


class Pawn(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE PAWN' if owner.name == 'WHITE' else 'BLACK PAWN'

    def check_move(self, player: Player, src: tuple, dst: tuple):
        if self.owner.name == 'WHITE':
            return self.check_white_move(src, dst)
        return self.check_black_move(src, dst)

    def check_white_move(self, src: tuple, dst: tuple):
        pass

    def check_black_move(self, src: tuple, dst: tuple):
        pass
