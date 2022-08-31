from LoadData import Load


class Report:
    check = False
    attacker_to_king_path_pinned = []
    attacker_piece = []
    attacker_to_king_path = []
    check_two_way = False
    attacker_piece_two_way = None

    @staticmethod
    def initialize():
        Report.check = False
        Report.attacker_to_king_path_pinned = []
        Report.attacker_piece = []
        Report.attacker_to_king_path = []
        Report.check_two_way = False
        Report.attacker_piece_two_way = None

    @staticmethod
    def b_q_r_state():
        if Report.check and len(Report.attacker_piece) == 1:
            return True, True
        if Report.check and len(Report.attacker_piece) > 1:
            return True, False
        return False, None


ins = Load()


def king(board, src, player, check):
    resource = ins.king[src]
    if check:
        return resource
    else:
        reserved = [x for x in resource if board.board[x[1][0]][x[1][1]].top is None
                    or board.board[x[1][0]][x[1][1]].top.owner != player]
        return reserved


def knight(board, src, player, check):
    resource = ins.knight[src]
    if check:
        if board.kings.get((player + 1) % 2) in [x[1] for x in resource]:
            Report.check_two_way = True
            Report.attacker_piece_two_way = src
        return resource
    else:
        reserved = [x for x in resource if board.board[x[1][0]][x[1][1]].top is None
                    or board.board[x[1][0]][x[1][1]].top.owner != player]
        return reserved


def get_pawn(board, src, check_pawn, player):
    p1, p2 = ins.pawn[player][src]
    if check_pawn:
        return p2
    front = []
    for move in p1:
        dst = move[1]
        if board.board[dst[0]][dst[1]].top is None:
            front.append(move)
        else:
            break
    p2 = [x for x in p2 if board.board[x[1][0]][x[1][1]].top is not None
          and board.board[x[1][0]][x[1][1]].top.owner != player]
    if board.kings.get((player + 1) % 2) in [x[1] for x in p2]:
        Report.check_two_way = True
        Report.attacker_piece_two_way = src
    return front[::-1] + p2[::-1]


def rook_bishop_queen(board, src, piece_type, check, player):
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
                    Report.attacker_to_king_path.append(path[:])
                    Report.check = True
                    if check:
                        continue
                    break
                if not board.kings.get((player+1) % 2) in dsts:
                    break
                ghost(src, path[:], dsts, ptr, player, board)
            if not check:
                break
            else:
                path.append((src, node))
                break
        result += path[::-1]
    return result


def ghost(src, path, dsts, ptr, player, board):
    pinned_piece = path[len(path)-1][1]
    while ptr < len(dsts):
        node = dsts[ptr]
        dst_tile = board.board[node[0]][node[1]].top
        ptr += 1
        if dst_tile is None:
            path.append((src, node))
            continue
        if dst_tile.owner != player and dst_tile.weight == 12:
            path.append(pinned_piece)
            Report.attacker_to_king_path_pinned.append(path)
        break
