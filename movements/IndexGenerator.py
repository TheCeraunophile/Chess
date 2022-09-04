def feedback(a):
    return a


def minus(a):
    return a - 1


def plus(a):
    return a + 1


def plus2(a):
    return a + 2


def minus2(a):
    return a - 2


def diagonal_move(src: tuple):
    t1 = direct_move(src, plus, plus)
    t2 = direct_move(src, plus, minus)
    t3 = direct_move(src, minus, plus)
    t4 = direct_move(src, minus, minus)
    return t1, t2, t3, t4


def polar_move(src: tuple):
    t1 = direct_move(src, plus, feedback)
    t2 = direct_move(src, feedback, plus)
    t3 = direct_move(src, minus, feedback)
    t4 = direct_move(src, feedback, minus)
    return t1, t2, t3, t4


def direct_move(src: tuple, update_i, update_j):
    i, j = src
    reserved = []
    while True:
        i = update_i(i)
        j = update_j(j)
        if i < 0 or i > 7 or j < 0 or j > 7:
            return reserved
        else:
            reserved.append((src, (i, j)))


def check_range(src, input_list):
    result = []
    for node in input_list:
        i, j = node
        if 0 <= i <= 7 and 0 <= j <= 7:
            result.append((src, node))
    return result


def king_move(src: tuple):
    i, j = src
    return check_range(src, [(i, j+1), (i, j-1), (i+1, j), (i-1, j), (i+1, j+1), (i-1, j-1), (i-1, j+1), (i+1, j-1)])


def knight_move(src: tuple):
    i, j = src
    return check_range(src, [(i+2, j+1), (i+2, j-1),
                             (i-2, j+1), (i-2, j-1), (i+1, j+2), (i-1, j+2), (i+1, j-2), (i-1, j-2)])


def pawn_move(src: tuple):
    i, j = src
    if src[0] == 1:
        white_steps_ahead = check_range(src, [(i + 1, j), (i + 2, j)])
    else:
        white_steps_ahead = check_range(src, [(i + 1, j)])
    white_steps_diagonal = check_range(src, [(i + 1, j + 1), (i + 1, j - 1)])
    if src[0] == 6:
        black_steps_ahead = check_range(src, [(i - 1, j), (i - 2, j)])
    else:
        black_steps_ahead = check_range(src, [(i - 1, j)])
    black_steps_diagonal = check_range(src, [(i - 1, j + 1), (i - 1, j - 1)])
    return (white_steps_ahead, white_steps_diagonal), (black_steps_ahead, black_steps_diagonal)
