from Player import Player
from Board import Board
from Exceptions import EndOfGameException, InputException, MoveException, IllegalMoveException
from evaluation import move_detection
import random


class Game:
    """
    game class has a board and a function named: control, that gives
    one move from the user and implement it.
    every move specified by a source and destination, your piece located
    in src and goes to the des.
    """

    def __init__(self):
        self.players = [Player('WHITE'), Player('BLACK')]
        self.current = self.players[0]
        self.board = Board(self.players)
        self.turn = 0
        self.controls = []
        """
        each one of 64 chess houses defined by a number in range 1-8
        and a character in range A-H, so we should convert the input into
        our 2D Array indexes from (0, 0)-(7, 7).
        """
        self.inv_columns = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        self.inv_rows = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, }
        self.columns = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}

    def control(self):
        src = input('source:    ')
        src = self.inv_rows.get(src[0], None), self.inv_columns.get(src[1], None)
        if None in src:
            raise InputException('invalid src')
        dst = input('destination:    ')
        dst = self.inv_rows.get(
            dst[0], None), self.inv_columns.get(dst[1], None)
        if None in dst:
            raise InputException('invalid dst')
        return src, dst

    def update_turn(self):
        """
        Always player White starts the game
        :return: next player
        """
        self.turn = (self.turn + 1) % 2
        self.current = self.players[self.turn]

    def select_starter(self, funcs):
        rand = random.randint(0, 1)
        self.controls.append(funcs[rand])
        self.controls.append(funcs[rand-1])

    def select_mode(self):
        while True:
            try:
                question = '1: ' + u'\U0001F464' + ' VS ' + u'\U0001F464' + '\n\n' + '2: ' + u'\U0001F464' + ' VS ' + u'\U0001f47a'
                answer = {'1': (self.control, self.control), '2': (self.control, move_detection)}
                print(question)
                mode = input()
                self.select_starter(answer.get(mode))
                break
            except Exception:
                continue

    def main_loop(self):
        while True:
            try:
                print(self.current.name + ' TURN')
                print(self.board)
                piece_to_node = self.board.pre_processing(self.current)
                src, dst = self.controls[self.turn]() if self.controls[self.turn] == self.control else self.controls[self.turn](self.board, self.current, piece_to_node)
                if dst not in piece_to_node.get(src, []):
                    raise IllegalMoveException('Illegal Move')
                else:
                    self.board.post_processing(self.current, src, dst)
            # src should contain player's piece -> MoveException
            # dst shouldn't contain player's piece -> MoveException
            # after piece moving, player's king shouldn't be in check, king in check or only the piece be achmaz
            # maybe with every movement the player's king still be in check so player lose the game

            # we should be sure that the player can choose at least one movement (before
            # getting src and dst from the player, called pre-processing)
            # if yes: game continue if not: player lose the game, or draw

            # Instead of post-processing, we use a pre-processing approach
            # so that we don't need to analyze the movement of both players' pieces
            # This approach makes Min-Max tree easier for us

            except (MoveException, InputException, IllegalMoveException) as e:
                print(e.msg)
            except EndOfGameException as e:
                print(e.msg)
                break
            except KeyboardInterrupt:
                break
            except IndexError:
                print('INVALID INPUT')
            else:
                self.update_turn()
        exit(0)
