"""Fungsi bersama untuk semua algoritma. Papan = matriks 2D 3x3 berisi 'X', 'O', atau ''."""
import time

LINES = [[(r, c) for c in range(3)] for r in range(3)] + \
        [[(r, c) for r in range(3)] for c in range(3)] + \
        [[(i, i) for i in range(3)], [(i, 2 - i) for i in range(3)]]
WIN = 100  


def other(p):
    return "O" if p == "X" else "X"


def winner(b):
    for line in LINES:
        a, c, d = (b[r][k] for r, k in line)
        if a and a == c == d:
            return a
    return None


def moves(b):
    return [(r, c) for r in range(3) for c in range(3) if b[r][c] == ""]


def full(b):
    return not moves(b)


def terminal_score(b, me, depth):
    """Nilai dari sudut pandang `me`; None jika papan belum selesai."""
    w = winner(b)
    if w:
        return WIN - depth if w == me else depth - WIN
    return 0 if full(b) else None


def root_search(board, me, value_fn):
    """Evaluasi setiap langkah `me` di akar pohon, lalu pilih nilai tertinggi.
    value_fn(b, giliran, kedalaman, ctx, me) -> nilai papan."""
    b = [row[:] for row in board]
    ctx, scores = {"nodes": 0}, {}
    t0 = time.perf_counter()
    if not winner(b):
        for r, c in moves(b):
            b[r][c] = me
            scores[f"{r},{c}"] = round(value_fn(b, other(me), 1, ctx, me), 2)
            b[r][c] = ""
    ms = (time.perf_counter() - t0) * 1000
    best = max(scores, key=scores.get) if scores else None
    return {"move": [int(x) for x in best.split(",")] if best else None,
            "scores": scores, "nodes": ctx["nodes"], "time_ms": round(ms, 3)}
