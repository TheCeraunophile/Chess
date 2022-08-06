from Player import Player


def nothing(a):
    return a


def minus(a):
    return a - 1


def plus(a):
    return a + 1


def diagonal_move(player: Player, board, src: tuple):
    result = []
    result.extend(direct_move(player, board, src, plus, plus))
    result.extend(direct_move(player, board, src, plus, minus))
    result.extend(direct_move(player, board, src, minus, plus))
    result.extend(direct_move(player, board, src, minus, minus))
    return result


def polar_move(player: Player, board, src: tuple):
    result = []
    result.extend(direct_move(player, board, src, plus, nothing))
    result.extend(direct_move(player, board, src, nothing, plus))
    result.extend(direct_move(player, board, src, minus, nothing))
    result.extend(direct_move(player, board, src, nothing, minus))
    return result


def direct_move(player: Player, board, src: tuple, update_i, update_j):
    i, j = src
    result = []
    while True:
        try:
            i = update_i(i)
            j = update_j(j)
            if i < 0 or i > 7 or j < 0 or j > 7:
                raise Exception
            if board[i][j].top is None:
                result.append((i, j))
            elif board[i][j].top.owner != player and \
                    not board[i][j].top.name.endswith('KING'):
                result.append((i, j))
                break
            else:
                break
        except Exception:
            break
    return result


def king_move(board, src: tuple):
    i, j = src
    result = []
    un_checked_result = [(i, j+1), (i, j-1), (i+1, j), (i-1, j), (i+1, j+1), (i-1, j-1), (i-1, j+1), (i+1, j-1)]
    for i in un_checked_result:
        if board[i[0]][i[1]].top is None:
            result.append(i)
    return result
