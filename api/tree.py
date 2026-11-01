import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from http.server import BaseHTTPRequestHandler
from core import parse, ALGOS
from algorithms.visualize import build_tree


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            board, me, opts = parse(body)
            name = body.get("algorithm", "alphabeta")
            if name not in ALGOS:
                raise ValueError("Algoritma tidak dikenal.")
            max_nodes = max(30, min(500, int(body.get("max_nodes", 260))))
            code, data = 200, build_tree(board, me, body.get("turn", me), name, opts["limit"], max_nodes)
        except (ValueError, KeyError, TypeError) as e:
            code, data = 400, {"error": str(e)}
        raw = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)
