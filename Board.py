from Player import Player
from Exceptions import EndOfGameException


class Board:
    def __init__(self, players: List[Player]):
        self.players = players
        self.board: List[List[Node]] = []
        self.create_board()

    def create_board(self):
        tmp: List[List[Node]] = []
        for i in range(8):
            column: List[Node] = []
            for j in range(8):
                column.append(Node(str(i) + chr(j + 65)))
            tmp.append(column)
        self.board = tmp
        self.initialization_board()

    def initialization_board(self):
        for i in range(0, 8):
            self.board[1][i].add_piece(Pawn(self.players[0]))
        for i in range(0, 8):
            self.board[6][i].add_piece(Pawn(self.players[1]))
        for i in range(0, 8, 7):
            self.board[0][i].add_piece(Rook(self.players[0]))
        for i in range(0, 8, 7):
            self.board[7][i].add_piece(Rook(self.players[1]))
        for i in range(1, 7, 5):
            self.board[0][i].add_piece(Knight(self.players[0]))
        for i in range(1, 7, 5):
            self.board[7][i].add_piece(Knight(self.players[1]))
        for i in range(2, 6, 3):
            self.board[0][i].add_piece(Bishop(self.players[0]))
        for i in range(2, 6, 3):
            self.board[7][i].add_piece(Bishop(self.players[1]))
        
        self.board[0][3].add_piece(Queen(self.players[0]))
        
        self.board[7][3].add_piece(Queen(self.players[1]))
        
        self.board[0][4].add_piece(King(self.players[0]))
        
        self.board[7][4].add_piece(King(self.players[1]))

    def give_piece(self, src: tuple):
        pass

    def back(self, src: tuple, dst: tuple):
        pass

    def move(self, player: Player, src: tuple, dst: tuple):
        pass

    def pre_processing(self, player: Player):
        result = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j].top.owner == player:
                    result.extend(j.top.chek_move(player, (i, j) ))
        if len(result) == 0:
            raise EndOfGameException
        return result
