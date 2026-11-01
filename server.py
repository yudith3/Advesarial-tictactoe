"""Server web tanpa dependensi tambahan. Jalankan: python server.py [port]"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from algorithms import minimax, alphabeta, expectimax, dls, mcts
from algorithms.visualize import build_tree

ALGOS = {"minimax": minimax, "alphabeta": alphabeta, "expectimax": expectimax, "dls": dls, "mcts": mcts}
ROOT = os.path.dirname(os.path.abspath(__file__))


def parse(body):
    board = [[str(c or "").strip().upper() for c in row] for row in body["board"]]
    if len(board) != 3 or any(len(r) != 3 for r in board) or any(c not in ("", "X", "O") for r in board for c in r):
        raise ValueError("Papan harus matriks 3x3 berisi 'X', 'O', atau ''.")
    me = str(body.get("player", "O")).upper()
    if me not in ("X", "O"):
        raise ValueError("player harus 'X' atau 'O'.")
    limit, sims = int(body.get("limit", 3)), int(body.get("sims", 1000))
    if not 1 <= limit <= 9:
        raise ValueError("limit harus berada pada rentang 1-9.")
    if not 10 <= sims <= 50000:
        raise ValueError("sims harus berada pada rentang 10-50000.")
    return board, me, {"limit": limit, "sims": sims}


class Handler(BaseHTTPRequestHandler):
    def send(self, code, data, ctype="application/json"):
        raw = data if isinstance(data, bytes) else json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            with open(os.path.join(ROOT, "public", "index.html"), "rb") as f:
                self.send(200, f.read(), "text/html; charset=utf-8")
        else:
            self.send(404, {"error": "Not found"})

    def do_POST(self):
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            board, me, opts = parse(body)
            if self.path == "/api/move":
                name = body.get("algorithm")
                if name not in ALGOS:
                    raise ValueError("Algoritma tidak dikenal.")
                self.send(200, ALGOS[name].get_move(board, me, **opts))
            elif self.path == "/api/compare":
                self.send(200, {n: m.get_move(board, me, **opts) for n, m in ALGOS.items()})
            elif self.path == "/api/tree":
                name = body.get("algorithm", "alphabeta")
                if name not in ALGOS:
                    raise ValueError("Algoritma tidak dikenal.")
                self.send(200, build_tree(board, me, body.get("turn", me), name, opts["limit"], int(body.get("max_nodes", 260))))
            else:
                self.send(404, {"error": "Not found"})
        except (ValueError, KeyError, TypeError) as e:
            self.send(400, {"error": str(e)})

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    print(f"Buka http://localhost:{port}")
    ThreadingHTTPServer(("", port), Handler).serve_forever()
