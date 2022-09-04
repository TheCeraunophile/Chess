from Board import Board
from Exceptions import EndOfGameException, InputException, MoveException, IllegalMoveException
import random
from evaluation import find_best_move


class Game:

    def __init__(self):
        self.colors = {0: 'WHITE', 1: 'BLACK'}
        self.players = [1, 0]
        self.board = Board()
        self.turn = 0
        self.controls = []
        self.inv_columns = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        self.inv_rows = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5, '7': 6, '8': 7, }
        self.columns = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
        self.count = 0
        self.max_depth = 2

    def control(self, *param):
        try:
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
        except IndexError:
            self.control()

    def update_turn(self):
        self.turn = self.players[self.turn]

    def select_starter(self, funcs):
        rand = random.randint(0, 1)
        self.controls.append(funcs[0])
        self.controls.append(funcs[1])

    def select_mode(self):
        while True:
            try:
                question = '1: ' + u'\U0001F464' + ' VS ' + u'\U0001F464' +\
                           '\n\n' +\
                           '2: ' + u'\U0001F464' + ' VS ' + u'\U0001F418' + \
                           '\n\n' + \
                           '3: ' + u'\U0001F418' + ' VS ' + u'\U0001F418'
                print(question)
                answer = {
                    '1': (self.control, self.control),
                    '2': (self.control, find_best_move),
                    '3': (find_best_move, find_best_move)
                }
                mode = input()
                self.select_starter(answer.get(mode))
                break
            except Exception:
                continue

    def main_loop(self):
        while True:
            try:
                self.count += 1
                if self.count >= 5:
                    self.max_depth = 3
                if self.count >= 180:
                    self.max_depth = 4
                if self.count >= 250:
                    self.max_depth = 5
                print(self.count)
                print(self.colors.get(self.turn), ' TURN')
                print(self.board)
                piece_to_node = self.board.pre_processing(self.turn)
                src, dst = self.controls[self.turn](self.board, self.players, self.turn, piece_to_node, self.max_depth)
                if (src, dst) not in piece_to_node:
                    raise IllegalMoveException('Illegal Move')
                else:
                    human_or_robot = True if self.controls[self.turn] == self.control else False
                    self.board.post_processing(self.turn, src, dst, human_or_robot)
                    self.board.castle_stack_pop()
            except (MoveException, InputException, IllegalMoveException) as e:
                print(e.msg)
            except EndOfGameException as e:
                print(e.msg)
                break
            except (KeyboardInterrupt, EOFError):
                break
            except IndexError:
                print('INVALID INPUT')
            else:
                self.update_turn()
        exit(0)
