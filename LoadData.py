from IndexGenerator import diagonal_move, polar_move, king_move, knight_move, pawn_move


class Load:
    def __init__(self):
        self.band = []
        self.king = {}
        self.knight = {}
        self.bishop = {}
        self.queen = {}
        self.rook = {}
        self.black_pawn = {}
        self.white_pawn = {}
        self.converter()

    def converter(self):
        from itertools import product
        index = [0, 1, 2, 3, 4, 5, 6, 7]
        for i, j in product(index, index):
            self.band.append((i, j))
        for node in self.band:
            self.king[node] = king_move(node)
            self.knight[node] = knight_move(node)
            self.rook[node] = polar_move(node)
            self.bishop[node] = diagonal_move(node)
            self.white_pawn[node], self.black_pawn[node] = pawn_move(node)
            self.king[node] = king_move(node)
            self.queen[node] = polar_move(node) + diagonal_move(node)
