"""4. Depth-Limited Search: Minimax dengan batas kedalaman. Di batas, papan dinilai dengan heuristik."""
from .common import LINES, other, moves, terminal_score, root_search


def heuristic(b, me):
    """Jumlah baris yang masih terbuka bagi AI dikurangi bagi lawan (bobot 1 untuk 1 tanda, 5 untuk 2)."""
    opp, h, w = other(me), 0, (0, 1, 5, 0)
    for line in LINES:
        cells = [b[r][c] for r, c in line]
        m, o = cells.count(me), cells.count(opp)
        if o == 0:
            h += w[m]
        elif m == 0:
            h -= w[o]
    return h


def make_value(limit):
    def value(b, turn, d, ctx, me):
        ctx["nodes"] += 1
        s = terminal_score(b, me, d)
        if s is not None:
            return s
        if d >= limit:  # cutoff: batas kedalaman tercapai
            return heuristic(b, me)
        best = None
        for r, c in moves(b):
            b[r][c] = turn
            v = value(b, other(turn), d + 1, ctx, me)
            b[r][c] = ""
            if best is None or (v > best if turn == me else v < best):
                best = v
        return best
    return value


def get_move(board, me, limit=3, **_):
    return root_search(board, me, make_value(max(1, int(limit))))
