"""1. Minimax: menelusuri seluruh pohon permainan, lawan dianggap bermain optimal."""
from .common import other, moves, terminal_score, root_search


def value(b, turn, d, ctx, me):
    ctx["nodes"] += 1
    s = terminal_score(b, me, d)
    if s is not None:
        return s
    best = None
    for r, c in moves(b):
        b[r][c] = turn
        v = value(b, other(turn), d + 1, ctx, me)
        b[r][c] = ""
        if best is None or (v > best if turn == me else v < best):  # MAX untuk AI, MIN untuk lawan
            best = v
    return best


def get_move(board, me, **_):
    return root_search(board, me, value)
