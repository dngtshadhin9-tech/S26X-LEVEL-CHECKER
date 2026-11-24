"""S26X LEVEL CHECKER — POST /api/check
Body : {"key": "<access key>", "uid": "...", "password": "..."}
Reply: {"status": "success", "uid", "account_id", "nickname", "level", "exp", "region"}
       {"status": "error", "uid", "error"}
"""
import hmac
import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

# Root e _core.py ache — path add koro (Vercel build er jonno safe)
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MAX_BODY = 4096
CHECKER_KEY = os.environ.get("CHECKER_KEY", "").strip()


class handler(BaseHTTPRequestHandler):
    def _send(self, code: int, obj: dict):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._send(405, {"status": "error", "error": "POST only"})

    def do_POST(self):
        # Lazy import — Vercel static parse fail korbe na
        try:
            import _core
        except Exception as e:
            return self._send(500, {"status": "error", "error": f"core import failed: {e}"})

        if not CHECKER_KEY:
            return self._send(503, {"status": "error", "error": "server not configured (CHECKER_KEY missing)"})

        try:
            length = int(self.headers.get("content-length", "0") or 0)
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_BODY:
            return self._send(413, {"status": "error", "error": "bad request size"})

        try:
            data = json.loads(self.rfile.read(length) or b"{}")
        except Exception:
            return self._send(400, {"status": "error", "error": "invalid JSON"})

        if not hmac.compare_digest(str(data.get("key", "")), CHECKER_KEY):
            return self._send(401, {"status": "error", "error": "invalid access key"})

        uid = str(data.get("uid", "")).strip()
        pwd = str(data.get("password", "")).strip()
        if not uid or not pwd:
            return self._send(400, {"status": "error", "uid": uid, "error": "uid/password missing"})

        try:
            info = _core.generate_jwt_with_info(uid, pwd)
        except Exception as e:
            return self._send(200, {"status": "error", "uid": uid, "error": str(e)[:200]})

        lvl = info.get("level")
        exp = info.get("exp")
        try:
            lvl_int = int(lvl) if lvl not in (None, "N/A") else 0
        except (TypeError, ValueError):
            lvl_int = 0
        try:
            exp_int = int(exp) if exp not in (None, "N/A") else 0
        except (TypeError, ValueError):
            exp_int = 0

        return self._send(200, {
            "status": "success",
            "uid": uid,
            "account_id": str(info.get("account_id") or "N/A"),
            "nickname": str(info.get("nickname") or "N/A"),
            "level": lvl_int,
            "exp": exp_int,
            "region": str(info.get("region") or "N/A"),
        })