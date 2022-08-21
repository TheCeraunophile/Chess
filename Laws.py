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
    tmp_result, tmp_ghost1, tmp_path1 = direct_move(player, board, src, plus, plus, check_pinned)
    result.extend(tmp_result)
    tmp_result, tmp_ghost2, tmp_path2 = direct_move(player, board, src, plus, minus, check_pinned)
    result.extend(tmp_result)
    tmp_result, tmp_ghost3, tmp_path3 = direct_move(player, board, src, minus, plus, check_pinned)
    result.extend(tmp_result)
    tmp_result, tmp_ghost4, tmp_path4 = direct_move(player, board, src, minus, minus, check_pinned)
    result.extend(tmp_result)
    if check_pinned:
        for node in (tmp_ghost1, tmp_ghost2, tmp_ghost3, tmp_ghost4):
            if node is not None:
                return result, node, None
        for node in (tmp_path1, tmp_path2, tmp_path3, tmp_path4):
            if node is not None:
                return result, None, node
    return result, None, None


def polar_move(board, player: Player, src: tuple, check_pinned):
    reserved = []
    tmp_result, tmp_ghost1, tmp_path1 = direct_move(player, board, src, plus, feedback, check_pinned)
    reserved.extend(tmp_result)
    tmp_result, tmp_ghost2, tmp_path2 = direct_move(player, board, src, feedback, plus, check_pinned)
    reserved.extend(tmp_result)
    tmp_result, tmp_ghost3, tmp_path3 = direct_move(player, board, src, minus, feedback, check_pinned)
    reserved.extend(tmp_result)
    tmp_result, tmp_ghost4, tmp_path4 = direct_move(player, board, src, feedback, minus, check_pinned)
    reserved.extend(tmp_result)
    if check_pinned:
        for node in (tmp_ghost1, tmp_ghost2, tmp_ghost3, tmp_ghost4):
            if node is not None:
                return reserved, node, None
        for node in (tmp_path1, tmp_path2, tmp_path3, tmp_path4):
            if node is not None:
                return reserved, None, node
    return reserved, None, None


def direct_move(player: Player, board, src: tuple, update_i, update_j, check_pinned):
    i, j = src
    reserved = []
    ghost = [src]
    while True:
        i = update_i(i)
        j = update_j(j)
        if i < 0 or i > 7 or j < 0 or j > 7:
            return reserved, None, None
        if board[i][j].top is None:
            reserved.append((src, (i, j)))
            ghost.append((i, j))
        elif board[i][j].top.owner != player:
            reserved.append((src, (i, j)))
            if check_pinned:
                if board[i][j].top.name.endswith('KING'):
                    return reserved, None, reserved
                ghost.append((i, j))
                return reserved, find_ghost(player, board, (i, j), update_i, update_j, ghost), None
            return reserved, None, None
        else:
            return reserved, None, None


def find_ghost(player: Player, board, src: tuple, update_i, update_j, ghost):
    i, j = src
    while True:
        i = update_i(i)
        j = update_j(j)
        if i < 0 or i > 7 or j < 0 or j > 7:
            return None
        if board[i][j].top is None:
            ghost.append((i, j))
        elif board[i][j].top.owner != player and board[i][j].top.name.endswith('KING'):
            ghost.append(src)
            return ghost
        else:
            return None


def check_range(input_list, board, player, src):
    result = []
    for node in input_list:
        i, j = node
        if 0 <= i <= 7 and 0 <= j <= 7:
            if board[i][j].top is None or board[i][j].top.owner != player:
                result.append((src, node))
    return result


def king_move(board, player, src: tuple):
    i, j = src
    return check_range([(i, j+1), (i, j-1), (i+1, j), (i-1, j),
                        (i+1, j+1), (i-1, j-1), (i-1, j+1), (i+1, j-1)], board, player, src)


def knight_move(board, player, src: tuple):
    i, j = src
    return check_range([(i+2, j+1), (i+2, j-1), (i-2, j+1), (i-2, j-1),
                        (i+1, j+2), (i-1, j+2), (i+1, j-2), (i-1, j-2)], board, player, src)


def pawn_move(board, player, src: tuple):
    if player.name == 'WHITE':
        return pawn_generator_moves(board, player, src, plus, plus2)
    return pawn_generator_moves(board, player, src, minus, minus2)


def pawn_generator_moves(board, player, src, update1, update2):
    result = []
    reserved = []
    i, j = src

    if (i == 1 and player.name == 'WHITE') or (i == 6 and player.name == 'BLACK'):
        if board[update1(i)][j].top is None and board[update2(i)][j].top is None:
            result.append((src, (update2(i), j)))

    if (i < 7 and player.name == 'WHITE') or (i > 1 and player.name == 'BLACK'):
        if board[update1(i)][j].top is None:
            result.append((src, (update1(i), j)))
    try:
        if j == 0:
            raise IndexError
        owner = board[update1(i)][j - 1].top.owner
        if owner != player:
            result.append((src, (update1(i), j - 1)))
    except AttributeError:
        reserved.append((src, (update1(i), j - 1)))
    except IndexError:
        pass
    try:
        if j == 7:
            raise IndexError
        owner = board[update1(i)][j + 1].top.owner
        if owner != player:
            result.append((src, (update1(i), j + 1)))
    except AttributeError:
        reserved.append((src, (update1(i), j + 1)))
    except IndexError:
        pass
    return result, reserved
