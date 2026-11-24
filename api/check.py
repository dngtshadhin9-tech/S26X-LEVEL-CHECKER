"""S26X LEVEL CHECKER — POST /api/check (Starlette ASGI)"""
import hmac
import json
import os
import sys
from pathlib import Path

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

# Ensure _core.py in the root directory can be imported
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MAX_BODY = 4096
CHECKER_KEY = os.environ.get("CHECKER_KEY", "").strip()


async def check(request: Request) -> JSONResponse:
    # Lazy import to avoid errors during the build phase
    try:
        import _core
    except Exception as e:
        return JSONResponse({"status": "error", "error": f"core import failed: {e}"}, status_code=500)

    if not CHECKER_KEY:
        return JSONResponse({"status": "error", "error": "server not configured (CHECKER_KEY missing)"}, status_code=503)

    # Validate request body size
    try:
        body = await request.body()
    except Exception:
        return JSONResponse({"status": "error", "error": "bad request"}, status_code=400)

    if not body or len(body) > MAX_BODY:
        return JSONResponse({"status": "error", "error": "bad request size"}, status_code=413)

    try:
        data = json.loads(body)
    except Exception:
        return JSONResponse({"status": "error", "error": "invalid JSON"}, status_code=400)

    # Constant-time key comparison
    if not hmac.compare_digest(str(data.get("key", "")), CHECKER_KEY):
        return JSONResponse({"status": "error", "error": "invalid access key"}, status_code=401)

    uid = str(data.get("uid", "")).strip()
    pwd = str(data.get("password", "")).strip()
    if not uid or not pwd:
        return JSONResponse({"status": "error", "uid": uid, "error": "uid/password missing"}, status_code=400)

    # Call core logic
    try:
        info = _core.generate_jwt_with_info(uid, pwd)
    except Exception as e:
        return JSONResponse({"status": "error", "uid": uid, "error": str(e)[:200]})

    # Safely convert numerical values
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

    return JSONResponse({
        "status": "success",
        "uid": uid,
        "account_id": str(info.get("account_id") or "N/A"),
        "nickname": str(info.get("nickname") or "N/A"),
        "level": lvl_int,
        "exp": exp_int,
        "region": str(info.get("region") or "N/A"),
    })


# Key: Export ASGI application named app
app = Starlette(routes=[
    Route("/api/check", check, methods=["POST"]),
])