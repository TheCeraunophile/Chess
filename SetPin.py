from LoadData import Load


class Report:
    check = False
    pinned_movements = []
    piece_checker = []
    check_path = []

    @staticmethod
    def initialize():
        Report.check = False
        Report.pinned_movements = []
        Report.piece_checker = []
        Report.check_path = []


ins = Load()


def king_knight(board, src, piece_type):
    player = board[src[0]][src[1]].top.owner
    resource = ins.king[src] if piece_type == 12 else ins.knight[src]
    return [x for x in resource if board[x[1][0]][x[1][1]].top is None or board[x[1][0]][x[1][1]].top.owner != player]


def get_pawn(board, src, check_pawn):
    player = board[src[0]][src[1]].top.owner
    p1, p2 = ins.pawn[player][src]
    if check_pawn:
        return [x for x in p2 if board[x[1][0]][x[1][1]].top is None or board[x[1][0]][x[1][1]].top.owner != player]
    p1 = [x for x in p1 if board[x[1][0]][x[1][1]].top is None]
    p2 = [x for x in p2 if board[x[1][0]][x[1][1]].top is not None and board[x[1][0]][x[1][1]].top.owner != player]
    return p1 + p2


def rook_bishop_queen(board, src, piece_type, check):
    """
    in this function if check equals True, we should detect all the pinned pieces with its valid movements
        and check detections with its path,
    :param check:
    :param piece_type:
    :param board:
    :param src:
    :return:
    """

    player = board[src[0]][src[1]].top.owner
    resource = ins.bishop[src] if piece_type == 3 else ins.rook[src] if piece_type == 5 else ins.queen[src]
    result = []

    for middle in resource:
        path = []
        for node in [x[1] for x in middle]:
            if board[node[0]][node[1]].top is None:
                result.append((src, node))
                continue
            if board[node[0]][node[1]].top.owner != player:
                result.append((src, node))
                if not check:
                    break
                if board[node[0]][node[1]].top.weight == 12:
                    Report.check = True
                    Report.check_path.append(path)
                    ghost()
            break
        result += path
    return result


def ghost():
    pass

        # i = update_i(i)
        # j = update_j(j)
        # if i < 0 or i > 7 or j < 0 or j > 7:
        #     return None
        # if board[i][j].top is None:
        #     ghost.append((i, j))
        # elif board[i][j].top.owner != player and board[i][j].top.name.endswith('KING'):
        #     ghost.append(src)
        #     return ghost
        # else:
        #     return None
