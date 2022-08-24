from LoadData import Load


ins = Load()


def king_knight(board, src, piece):
    player = board[src[0]][src[1]].top.owner
    resource = ins.king[src] if piece == 'king' else ins.knight[src]
    result = []
    for node in [x[1] for x in resource]:
        if board.board[node[0]][node[1]].top.owner == player:
            result.append((src, node))
    return result


def get_pawn(board, src):
    player = board[src[0]][src[1]].top.owner
    p1, p2 = ins.white_pawn[src] if player.name == 'WHITE' else ins.black_pawn[src]
    result1 = []
    result2 = []
    for node in [x[1] for x in p1]:
        if board.board[node[0]][node[1]].top is not None:
            break
        result1.append((src, node))

    for node in [x[1] for x in p2]:
        if board.board[node[0]][node[1]].top is None or board.board[node[0]][node[1]].top.owner != player:
            result2.append((src, node))

    return result1, result2


def rook_bishop_queen(board, src, piece):
    player = board[src[0]][src[1]].top.owner
    resource = ins.bishop[src] if piece == 'bishop' else ins.rook[src] if piece == 'rook' else ins.queen[src]
    result = []
    for middle in resource:
        for node in [x[1] for x in middle]:
            if board[node[0]][node[1]].top is None:
                result.append((src, node))
                continue
            if board[node[0]][node[1]].top.owner != player:
                result.append((src, node))
                break
            break
    return result
