from LoadData import Load


class Report:
    check = False
    attacker_to_king_path_pinned = []
    attacker_piece = []
    attacker_to_king_path = []

    @staticmethod
    def initialize():
        Report.check = False
        Report.attacker_to_king_path_pinned = []
        Report.attacker_piece = []
        Report.attacker_to_king_path = []


ins = Load()


def king_knight(board, src, piece_type):
    player = board.board[src[0]][src[1]].top.owner
    resource = ins.king[src] if piece_type == 12 else ins.knight[src]
    return [x for x in resource if board.board[x[1][0]][x[1][1]].top is None or board.board[x[1][0]][x[1][1]].top.owner != player]


def get_pawn(board, src, check_pawn):
    player = board.board[src[0]][src[1]].top.owner
    p1, p2 = ins.pawn[player][src]
    if check_pawn:
        return [x for x in p2 if board.board[x[1][0]][x[1][1]].top is None or board.board[x[1][0]][x[1][1]].top.owner != player]
    front = []
    for move in p1:
        dst = move[1]
        if board.board[dst[0]][dst[1]].top is None:
            front.append(move)
        else:
            break
    p2 = [x for x in p2 if board.board[x[1][0]][x[1][1]].top is not None and board.board[x[1][0]][x[1][1]].top.owner != player]
    return front[::-1] + p2[::-1]


def rook_bishop_queen(board, src, piece_type, check):
    """
    if check happened, we have to create an array, starts from attacker piece and ends to the player king
    without any exceptions, we should save a path starts from attacker piece goes throw the one player piece
        and finally ends to the player king,
    so we should save any path from attacker piece to the player king
    :param check:
    :param piece_type:
    :param board:
    :param src:
    :return:
    """

    player = board.board[src[0]][src[1]].top.owner
    resource = ins.bishop[src] if piece_type == 3 else ins.rook[src] if piece_type == 5 else ins.queen[src]
    result = []

    for middle in resource:
        path = []
        if not middle:
            continue
        dsts = [x[1] for x in middle]
        ptr = 0
        while ptr < len(dsts):
            node = dsts[ptr]
            dst_tile = board.board[node[0]][node[1]].top
            ptr += 1
            if dst_tile is None:
                path.append((src, node))
                continue
            if dst_tile.owner != player:
                path.append((src, node))
                if not check:
                    break
                if dst_tile.weight == 12:
                    Report.attacker_piece.append(src)
                    Report.attacker_to_king_path.append(path)
                    Report.check = True
                    break
                if not board.kings.get((player+1) % 2) in dsts:
                    break
                ghost(src, path[:], dsts, ptr, player, board)
            break
        result += path[::-1]
    return result


def ghost(src, path, dsts, ptr, player, board):
    while ptr < len(dsts):
        node = dsts[ptr]
        dst_tile = board.board[node[0]][node[1]].top
        ptr += 1
        if dst_tile is None:
            path.append((src, node))
            continue
        if dst_tile.owner != player and dst_tile.weight == 12:
            # add pinned piece in last index of attacker_to_king_path_pinned sublist
            Report.attacker_to_king_path_pinned.append(path)
        break
