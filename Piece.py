from Player import Player
from Laws import diagonal_move, polar_move, king_move


class Piece:
    def __init__(self, owner: Player):
        self.owner = owner
        self.name = ''

    def check_move(self, board, player: Player, src: tuple):
        pass


class Knight(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE KNIGHT' if owner.name == 'WHITE' else 'BLACK KNIGHT'

    def check_move(self, board, player: Player, src: tuple):
        pass


class King(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE KING' if owner.name == 'WHITE' else 'BLACK KING'

    def check_move(self, board, player: Player, src: tuple):
        king_move(player, board, src)


class Rook(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE QUEEN' if owner.name == 'WHITE' else 'BLACK QUEEN'

    def check_move(self, board, player: Player, src: tuple):
        return polar_move(player, src)


class Bishop(Piece):
    def __init__(self, board, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE BISHOP' if owner.name == 'WHITE' else 'BLACK BISHOP'

    def check_move(self, board, player: Player, src: tuple):
        return diagonal_move(player, src)


class Queen(Piece):
    def __init__(self, board, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE QUEEN' if owner.name == 'WHITE' else 'BLACK QUEEN'

    def check_move(self, player: Player, src: tuple):
        tmp = []
        tmp.extend(polar_move(player, src))
        tmp.extend(direct_move(player, src))
        return tmp


class Pawn(Piece):
    def __init__(self, owner: Player):
        super().__init__(owner)
        self.name = 'WHITE PAWN' if owner.name == 'WHITE' else 'BLACK PAWN'

    def check_move(self, board, player: Player, src: tuple):
        if self.owner.name == 'WHITE':
            return self.check_white_move(src, dst)
        return self.check_black_move(src, dst)

    def check_white_move(self, src: tuple):
        pass

    def check_black_move(self, src: tuple):
        pass
