"""5. Monte Carlo Tree Search (UCT): selection, expansion, simulation, backpropagation."""
import math
import random
import time
from .common import winner, moves, full, other


class Node:
    def __init__(self, board, turn, parent=None, move=None):
        self.board, self.turn, self.parent, self.move = board, turn, parent, move
        self.children, self.n, self.w = [], 0, 0.0
        self.untried = [] if winner(board) else moves(board)


def get_move(board, me, sims=1000, c_uct=1.41, **_):
    t0 = time.perf_counter()
    root = Node([r[:] for r in board], me)
    if not root.untried:
        return {"move": None, "scores": {}, "nodes": 0, "time_ms": 0}
    nodes = 1
    for _i in range(max(int(sims), len(root.untried))):
        node = root
        while not node.untried and node.children: 
            node = max(node.children, key=lambda ch: ch.w / ch.n +
                       c_uct * math.sqrt(math.log(node.n) / ch.n))
        if node.untried: 
            m = node.untried.pop(random.randrange(len(node.untried)))
            nb = [r[:] for r in node.board]
            nb[m[0]][m[1]] = node.turn
            child = Node(nb, other(node.turn), node, m)
            node.children.append(child)
            node, nodes = child, nodes + 1
        b, t = [r[:] for r in node.board], node.turn 
        while not winner(b) and not full(b):
            r, c = random.choice(moves(b))
            b[r][c] = t
            t = other(t)
        win = winner(b)
        while node:  
            mover = other(node.turn)
            node.n += 1
            node.w += 1.0 if win == mover else 0.5 if win is None else 0.0
            node = node.parent
    best = max(root.children, key=lambda ch: (ch.n, ch.w / ch.n))
    scores = {f"{ch.move[0]},{ch.move[1]}": round(ch.w / ch.n, 2) for ch in root.children}
    return {"move": list(best.move), "scores": scores, "nodes": nodes,
            "time_ms": round((time.perf_counter() - t0) * 1000, 3)}
