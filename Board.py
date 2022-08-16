from Exceptions import EndOfGameException, IllegalMoveException
from typing import List
from Piece import *
from Node import Node


class Board:
    def __init__(self, players: List[Player]):
        self.players = players
        self.board: List[List[Node]] = []
        self.board_weight = {self.players[0]: 1290, self.players[1]: 1290}
        self.l_to_p = {players[0]: {(0, 0): Rook(players[0], 0), (0, 7): Rook(players[0], 1),
                                    (0, 1): Knight(players[0], 0), (0, 6): Knight(players[0], 1),
                                    (0, 2): Bishop(players[0], 0), (0, 5): Bishop(players[0], 1),
                                    (0, 3): Queen(players[0], 0), (0, 4): King(players[0], 0),
                                    (1, 0): Pawn(players[0], 0), (1, 1): Pawn(players[0], 1),
                                    (1, 2): Pawn(players[0], 2), (1, 3): Pawn(players[0], 3),
                                    (1, 4): Pawn(players[0], 4), (1, 5): Pawn(players[0], 5),
                                    (1, 6): Pawn(players[0], 6), (1, 7): Pawn(players[0], 7)},
                       players[1]: {(7, 0): Rook(players[1], 0), (7, 7): Rook(players[1], 1),
                                    (7, 1): Knight(players[1], 0), (7, 6): Knight(players[1], 1),
                                    (7, 2): Bishop(players[1], 0), (7, 5): Bishop(players[1], 1),
                                    (7, 3): Queen(players[1], 0), (7, 4): King(players[1], 0),
                                    (6, 0): Pawn(players[1], 0), (6, 1): Pawn(players[1], 1),
                                    (6, 2): Pawn(players[1], 2), (6, 3): Pawn(players[1], 3),
                                    (6, 4): Pawn(players[1], 4), (6, 5): Pawn(players[1], 5),
                                    (6, 6): Pawn(players[1], 6), (6, 7): Pawn(players[1], 7)}}
        self.p_to_l = {players[0]: {Rook(players[0], 0): (0, 0), Rook(players[0], 1): (0, 7),
                                    Knight(players[0], 0): (0, 1), Knight(players[0], 1): (0, 6),
                                    Bishop(players[0], 0): (0, 2), Bishop(players[0], 1): (0, 5),
                                    Queen(players[0], 0): (0, 3), King(players[0], 0): (0, 4),
                                    Pawn(players[0], 0): (1, 0), Pawn(players[0], 1): (1, 1),
                                    Pawn(players[0], 2): (1, 2), Pawn(players[0], 3): (1, 3),
                                    Pawn(players[0], 4): (1, 4), Pawn(players[0], 5): (1, 5),
                                    Pawn(players[0], 6): (1, 6), Pawn(players[0], 7): (1, 7)},
                       players[1]: {Rook(players[1], 0): (7, 0), Rook(players[1], 1): (7, 7),
                                    Knight(players[1], 0): (7, 1), Knight(players[1], 1): (7, 6),
                                    Bishop(players[1], 0): (7, 2), Bishop(players[1], 1): (7, 5),
                                    Queen(players[1], 0): (7, 3), King(players[1], 0): (7, 4),
                                    Pawn(players[1], 0): (6, 0), Pawn(players[1], 1): (6, 1),
                                    Pawn(players[1], 2): (6, 2), Pawn(players[1], 3): (6, 3),
                                    Pawn(players[1], 4): (6, 4), Pawn(players[1], 5): (6, 5),
                                    Pawn(players[1], 6): (6, 6), Pawn(players[1], 7): (6, 7)}}
        self.create_board()

    def create_board(self):
        tmp: List[List[Node]] = []
        for i in range(8):
            column: List[Node] = []
            for j in range(8):
                column.append(Node(str(i) + chr(j + 65), (i, j)))
            tmp.append(column)
        self.board = tmp
        self.initialization_board()

    def initialization_board(self):
        for i in range(0, 8):
            self.board[1][i].add(Pawn(self.players[0], i))
        for i in range(0, 8):
            self.board[6][i].add(Pawn(self.players[1], i))
        self.board[0][0].add(Rook(self.players[0], 0))
        self.board[0][7].add(Rook(self.players[0], 1))
        self.board[7][0].add(Rook(self.players[1], 0))
        self.board[7][7].add(Rook(self.players[1], 1))
        self.board[0][4].add(King(self.players[0], 0))
        self.board[7][4].add(King(self.players[1], 0))
        self.board[0][3].add(Queen(self.players[0], 0))
        self.board[7][3].add(Queen(self.players[1], 0))
        self.board[0][1].add(Knight(self.players[0], 0))
        self.board[0][6].add(Knight(self.players[0], 1))
        self.board[7][1].add(Knight(self.players[1], 0))
        self.board[7][6].add(Knight(self.players[1], 1))
        self.board[0][2].add(Bishop(self.players[0], 0))
        self.board[0][5].add(Bishop(self.players[0], 1))
        self.board[7][2].add(Bishop(self.players[1], 0))
        self.board[7][5].add(Bishop(self.players[1], 1))

    def back(self, src: tuple, dst: tuple):
        i, j = dst
        piece = self.board[i][j].top
        player = piece.owner
        self.l_to_p[player][src] = piece
        self.l_to_p[player].pop(dst)
        self.p_to_l[player][piece] = src

        i, j = dst
        if self.board[i][j].get_down() is not None:
            piece = self.board[i][j].get_down()
            player = piece.owner
            self.l_to_p[player][dst] = piece
            self.p_to_l[player][piece] = dst
            self.board_weight[player] = self.board_weight.get(player) + piece.weight
        self.board[src[0]][src[1]].back()
        self.board[dst[0]][dst[1]].back()

    def move(self, src: tuple, dst: tuple):
        i, j = src
        piece = self.board[i][j].top
        player = piece.owner
        self.l_to_p[player][dst] = piece
        self.l_to_p[player].pop(src)
        self.p_to_l[player][piece] = dst

        i, j = dst
        if self.board[i][j].top is not None:
            piece = self.board[i][j].top
            player = piece.owner
            self.l_to_p[player].pop(dst)
            self.p_to_l[player].pop(piece)
            self.board_weight[player] = self.board_weight.get(player) - piece.weight
        tmp = self.board[src[0]][src[1]].pick_up()
        self.board[dst[0]][dst[1]].add(tmp)

    def check(self, player, restricted):
        for piece in restricted:
            i, j = piece
            tmp = self.board[i][j].top.check_move(self.board, (i, j))
            if self.p_to_l.get(player).get(King(player, 0)) in tmp:
                return True
        return False

    def achmaz_detection(self, player, src, dst_s, restricted):
        result = []
        for dst in dst_s:
            self.move(src, dst)
            if not self.check(player, restricted):
                result.append(dst)
            self.back(src, dst)
        return result

    def restricted_check(self, player, other_player):
        """
        find opponent's pieces with check potential
        :param player: find king location like i, j by player object
        :param other_player:
        :return: any location contain an object that can check the king
        """
        pieces = []
        king_loc = self.p_to_l.get(player).get(King(player, 0))
        i, j = king_loc
        k1 = self.p_to_l.get(other_player).get(Knight(other_player, 0), None)
        k2 = self.p_to_l.get(other_player).get(Knight(other_player, 1), None)
        k3 = self.p_to_l.get(other_player).get(Knight(other_player, 2), None)
        b1 = self.p_to_l[other_player].get(Bishop(other_player, 0), None)
        b2 = self.p_to_l[other_player].get(Bishop(other_player, 1), None)
        b3 = self.p_to_l[other_player].get(Bishop(other_player, 2), None)
        r1 = self.p_to_l[other_player].get(Rook(other_player, 0), None)
        r2 = self.p_to_l[other_player].get(Rook(other_player, 1), None)
        r3 = self.p_to_l[other_player].get(Rook(other_player, 2), None)
        q1 = self.p_to_l[other_player].get(Queen(other_player, 0), None)
        q2 = self.p_to_l[other_player].get(Queen(other_player, 1), None)
        for node in (k1, k2, k3, b1, b2, b3, q1, q2):
            if node is not None:
                if (node[0] + node[1]) % 2 == (i + j) % 2:
                    pieces.append(node)
        for node in (r1, r2, r3, q1, q2):
            if node is not None:
                if node[0] == i or node[1] == j:
                    if node not in pieces:
                        pieces.append(node)
        if player.name == 'WHITE' and i < 7:
            if j > 0 and self.board[i+1][j-1].top is not None and self.board[i+1][j-1].top.owner.name == 'BLACK PAWN':
                pieces.append((i+1, j-1))
            if j < 7 and self.board[i+1][j+1].top is not None and self.board[i+1][j+1].top.owner.name == 'BLACK PAWN':
                pieces.append((i+1, j+1))
        elif player.name == 'BLACK' and i > 0:
            if j > 0 and self.board[i-1][j-1].top is not None and self.board[i-1][j-1].top.owner.name == 'WHITE PAWN':
                pieces.append((i-1, j-1))
            if j < 7 and self.board[i-1][j+1].top is not None and self.board[i-1][j+1].top.owner.name == 'WHITE PAWN':
                pieces.append((i-1, j+1))
        return pieces

    def pre_processing(self, player: Player):
        other_player = self.players[1] if player.name == 'WHITE' else self.players[0]
        restricted = list(set(self.restricted_check(player, other_player)))
        p_to_l = self.p_to_l.get(player)
        result = []
        pieces = list(p_to_l.keys())
        for piece in pieces:
            if isinstance(piece, King):
                i, j = p_to_l.get(piece)
                nodes = self.board[i][j].top.check_move(self.board, (i, j))
                if nodes is not None:
                    first = [(i, j)] * len(nodes)
                    nodes = self.achmaz_detection(player, (i, j), nodes, self.p_to_l[other_player].values())
                    result.extend((zip(first, nodes)))
            else:
                i, j = p_to_l.get(piece)
                nodes = self.board[i][j].top.check_move(self.board, (i, j))
                if nodes is not None:
                    first = [(i, j)] * len(nodes)
                    nodes = self.achmaz_detection(player, (i, j), nodes, restricted)
                    result.extend((zip(first, nodes)))
        if len(result) == 0:
            if self.check(player, restricted):
                raise EndOfGameException(player.name + ' Lose the Game')
            else:
                raise EndOfGameException('DRAW')
        return result

    def post_processing(self, player, src, dst):
        self.move(src, dst)
        expand = {self.players[0]: 7, self.players[1]: 0}
        if isinstance(self.board[dst[0]][dst[1]].top, Pawn) and expand.get(self.board[dst[0]][dst[1]].top.owner) == dst[0]:
            self.board[dst[0]][dst[1]].down.pop()
            while True:
                try:
                    list_pieces = {'Q': Queen, 'R': Rook, 'K': Knight, 'B': Bishop}
                    promoted_piece = input('Q: queen R: rook K: knight B: bishop\n')
                    tmp = list_pieces.get(promoted_piece)
                    if isinstance(tmp, Queen):
                        count = 0 if self.p_to_l.get(player).get(Queen(player, 0), None) is None else 1
                        self.p_to_l[player][Queen(player, count)] = dst
                        self.l_to_p[player][dst] = Queen(player, count)
                    else:
                        count = 0 if self.p_to_l.get(player).get(tmp(player, 0), None) is None \
                            else 1 if self.p_to_l.get(player).get(tmp(player, 1), None) is None else 2
                        self.p_to_l[player][tmp(player, count)] = dst
                        self.l_to_p[player][dst] = tmp(player, count)
                    break
                except Exception:
                    continue

    def __str__(self):
        line_buffer = '   A  B  C  D  E  F  G  H'
        for i in range(7, -1, -1):
            line_buffer += '\n' + str(i+1) + '  '
            for j in range(8):
                tmp = self.board[i][j].top
                if tmp is None:
                    if (i+j) % 2 == 0:
                        line_buffer += u'\u25FB'
                    else:
                        line_buffer += u'\u25FC'
                else:
                    line_buffer += tmp.shape
                line_buffer += '  '
        return line_buffer
