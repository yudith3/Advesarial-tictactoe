import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from http.server import BaseHTTPRequestHandler
from core import ALGOS, parse


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            board, me, opts = parse(body)
            code, data = 200, {n: m.get_move(board, me, **opts) for n, m in ALGOS.items()}
        except (ValueError, KeyError, TypeError) as e:
            code, data = 400, {"error": str(e)}
        raw = json.dumps(data).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)