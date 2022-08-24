def _move(func):
    def wrapper(src, dst):
        value = func(src, dst)
        # something else
        return value
    return wrapper


def _back(func):
    def wrapper(src, dst):
        value = func(src, dst)
        # something else
        return value
    return wrapper


@_move
def move(src, dst, player, otherplayer, ):
    pass


@_back
def back():
    pass


def status():
    pass
