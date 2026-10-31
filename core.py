from algorithms import minimax, alphabeta, expectimax, dls, mcts

ALGOS = {"minimax": minimax, "alphabeta": alphabeta, "expectimax": expectimax, "dls": dls, "mcts": mcts}


def parse(body):
    board = [[str(c or "").strip().upper() for c in row] for row in body["board"]]
    if len(board) != 3 or any(len(r) != 3 for r in board) or any(c not in ("", "X", "O") for r in board for c in r):
        raise ValueError("Papan harus matriks 3x3 berisi 'X', 'O', atau ''.")
    me = str(body.get("player", "O")).upper()
    if me not in ("X", "O"):
        raise ValueError("player harus 'X' atau 'O'.")
    return board, me, {"limit": int(body.get("limit", 3)), "sims": int(body.get("sims", 1000))}