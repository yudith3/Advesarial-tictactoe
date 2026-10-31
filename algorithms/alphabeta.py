"""2. Alpha-Beta Pruning: hasil sama dengan Minimax, tetapi cabang yang tidak berpengaruh dipangkas."""
from .common import other, moves, terminal_score, root_search

INF = float("inf")


def value(b, turn, d, ctx, me, alpha=-INF, beta=INF):
    ctx["nodes"] += 1
    s = terminal_score(b, me, d)
    if s is not None:
        return s
    if turn == me: 
        v = -INF
        for r, c in moves(b):
            b[r][c] = turn
            v = max(v, value(b, other(turn), d + 1, ctx, me, alpha, beta))
            b[r][c] = ""
            alpha = max(alpha, v)
            if alpha >= beta:  
                break
        return v
    v = INF  
    for r, c in moves(b):
        b[r][c] = turn
        v = min(v, value(b, other(turn), d + 1, ctx, me, alpha, beta))
        b[r][c] = ""
        beta = min(beta, v)
        if alpha >= beta:
            break
    return v


def get_move(board, me, **_):
    return root_search(board, me, value)
