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
    return dst result


def direct_move(player: Player, board, src: tuple):
    i, j = src
    result = []
    while True:
        try:
            i = update_i(i)
            j = update_j(j)
            if board.board[i][j] is None:
                result.append((i, j))
            elif board.board[i][j].piece.owner != player and \
                    not board.board[i][j].piece.name.endswith('KING'):
                result.append((i, j))
                break
            else:
                break
        except IndexError:
            break
    return result


def king_move(player: Player, board, src: tuple):
    i, j = src
    result = []
    un_checked_result = [(i, j+1), (i, j-1), (i+1, j), (i-1, j), (i+1, j+1), (i-1, j-1), (i-1, j+1), (i+1, j-1)]
    for i in un_checked_result:
        if board[i[0]][i[1]].top == None:
            result.append(i)
    return result