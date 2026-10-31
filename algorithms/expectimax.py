"""3. Expectimax: node lawan diganti chance node. Lawan diasumsikan memilih langkah secara
acak (seragam), sehingga nilainya adalah rata-rata semua kemungkinan langkah lawan."""
from .common import other, moves, terminal_score, root_search


def value(b, turn, d, ctx, me):
    ctx["nodes"] += 1
    s = terminal_score(b, me, d)
    if s is not None:
        return s
    vals = []
    for r, c in moves(b):
        b[r][c] = turn
        vals.append(value(b, other(turn), d + 1, ctx, me))
        b[r][c] = ""
    return max(vals) if turn == me else sum(vals) / len(vals)  # MAX atau CHANCE


def get_move(board, me, **_):
    return root_search(board, me, value)
