class MyException(Exception):
    def __init__(self, msg):
        self.msg = msg


class EndOfGame(MyException):
    pass


class MoveException(MyException):
    pass


class InputException(MyException):
    pass
