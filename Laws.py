from Player import Player


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


def diagonal_move(board, player: Player, src: tuple, check_pinned):
    result = []
    ghost = []
    tmp_result, tmp_ghost1 = direct_move(player, board, src, plus, plus, check_pinned)
    result.extend(tmp_result)
    tmp_result, tmp_ghost2 = direct_move(player, board, src, plus, minus, check_pinned)
    result.extend(tmp_result)
    tmp_result, tmp_ghost3 = direct_move(player, board, src, minus, plus, check_pinned)
    result.extend(tmp_result)
    tmp_result, tmp_ghost4 = direct_move(player, board, src, minus, minus, check_pinned)
    result.extend(tmp_result)
    if check_pinned:
        for node in (tmp_ghost1, tmp_ghost2, tmp_ghost3, tmp_ghost4):
            if node:
                ghost.append(node)
                break
    return result, ghost


def polar_move(board, player: Player, src: tuple, check_pinned):
    result = []
    tmp_result, tmp_ghost1 = direct_move(player, board, src, plus, feedback, check_pinned)
    result.extend(tmp_result)
    tmp_result, tmp_ghost2 = direct_move(player, board, src, feedback, plus, check_pinned)
    result.extend(tmp_result)
    tmp_result, tmp_ghost3 = direct_move(player, board, src, minus, feedback, check_pinned)
    result.extend(tmp_result)
    tmp_result, tmp_ghost4 = direct_move(player, board, src, feedback, minus, check_pinned)
    result.extend(tmp_result)
    if check_pinned:
        for node in (tmp_ghost1, tmp_ghost2, tmp_ghost3, tmp_ghost4):
            if node is not None:
                return result, node
    return result, None


def direct_move(player: Player, board, src: tuple, update_i, update_j, check_pinned):
    i, j = src
    result = []
    while True:
        i = update_i(i)
        j = update_j(j)
        if i < 0 or i > 7 or j < 0 or j > 7:
            return result, None
        if board[i][j].top is None:
            result.append((src, (i, j)))
        elif board[i][j].top.owner != player:
            result.append((src, (i, j)))
            if check_pinned:
                return result, find_ghost(player, board, (i, j), update_i, update_j)
            return result, None
        else:
            return result, None


def find_ghost(player: Player, board, src: tuple, update_i, update_j):
    i, j = src
    while True:
        i = update_i(i)
        j = update_j(j)
        if i < 0 or i > 7 or j < 0 or j > 7:
            return None
        if board[i][j].top is None:
            continue
        elif board[i][j].top.owner != player and board[i][j].top.name.endswith('KING'):
            return src
        else:
            return None


def check_range(input_list, board, player):
    result = []
    for node in input_list:
        i, j = node
        if 0 <= node[0] <= 7 and 0 <= node[1] <= 7 and board[i][j].top is None or board[i][j].top.owner != player:
            result.append(node)
    return result


def king_move(board, player, src: tuple):
    i, j = src
    result = []
    return check_range([(i, j+1), (i, j-1), (i+1, j), (i-1, j),
                        (i+1, j+1), (i-1, j-1), (i-1, j+1), (i+1, j-1)], board, player)


def knight_move(board, player, src: tuple):
    result = []
    i, j = src
    return check_range([(i+2, j+1), (i+2, j-1), (i-2, j+1), (i-2, j-1),
                        (i+1, j+2), (i-1, j+2), (i+1, j-2), (i-1, j-2)], board, player)


def pawn_move(board, player, src: tuple):
    if player.name == 'WHITE':
        return pawn_generator_moves(board, player, src, plus, plus2)
    return pawn_generator_moves(board, player, src, minus, minus2)


def pawn_generator_moves(board, player, src, update1, update2):
    result = []
    i, j = src

    if (i == 1 and player.name == 'WHITE') or (i == 6 and player.name == 'BLACK'):
        if board[update1(i)][j].top is None and board[update2(i)][j].top is None:
            result.append((update2(i), j))

    if (i < 7 and player.name == 'WHITE') or (i > 1 and player.name == 'BLACK'):
        if board[update1(i)][j].top is None:
            result.append((update1(i), j))
    try:
        if j == 0:
            raise IndexError
        owner = board[update1(i)][j - 1].top.owner
        if owner != player:
            result.append((update1(i), j - 1))
    except (AttributeError, IndexError):
        pass
    try:
        if j == 7:
            raise IndexError
        owner = board[update1(i)][j + 1].top.owner
        if owner != player:
            result.append((update1(i), j + 1))
    except (AttributeError, IndexError):
        pass
    return result
