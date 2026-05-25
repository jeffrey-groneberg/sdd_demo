"""Shortly — minimal URL shortener.

Generated from .specify/specs/001-url-shortener/{spec,plan,tasks}.md
"""
from __future__ import annotations

import secrets
import string
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app import db

ALPHABET = string.ascii_letters + string.digits
CODE_LEN = 6
MAX_COLLISION_RETRIES = 5


@asynccontextmanager
async def lifespan(_app: FastAPI):
    db.init_db()
    yield


app = FastAPI(title="Shortly", description="URL shortener with click stats", lifespan=lifespan)
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


# --- DB lifecycle -------------------------------------------------------------

def db_conn():
    """FastAPI dependency yielding a sqlite connection per request."""
    with db.get_conn() as conn:
        yield conn


# --- helpers ------------------------------------------------------------------

def _generate_code() -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(CODE_LEN))


def _is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    return parsed.scheme in ("http", "https") and bool(parsed.netloc)


# --- routes -------------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def index(request: Request, conn=Depends(db_conn)):
    recent = db.list_recent(conn, limit=10)
    return templates.TemplateResponse(
        request,
        "index.html",
        {"recent": recent, "error": None, "created": None},
    )


@app.post("/shorten", response_class=HTMLResponse)
def shorten(request: Request, url: str = Form(...), conn=Depends(db_conn)):
    url = url.strip()
    if not _is_valid_url(url):
        recent = db.list_recent(conn, limit=10)
        return templates.TemplateResponse(
            request,
            "index.html",
            {"recent": recent, "error": "URL must start with http:// or https://", "created": None},
            status_code=400,
        )

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for _ in range(MAX_COLLISION_RETRIES):
        code = _generate_code()
        if db.insert_url(conn, code, url, now):
            recent = db.list_recent(conn, limit=10)
            return templates.TemplateResponse(
                request,
                "index.html",
                {"recent": recent, "error": None, "created": code},
            )
    raise HTTPException(status_code=500, detail="Could not allocate unique code")


@app.get("/stats/{code}", response_class=HTMLResponse)
def stats(request: Request, code: str, conn=Depends(db_conn)):
    row = db.get_url(conn, code)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Unknown code: {code}")
    return templates.TemplateResponse(request, "stats.html", {"row": row})


@app.get("/{code}")
def redirect(code: str, conn=Depends(db_conn)):
    row = db.get_url(conn, code)
    if row is None:
        raise HTTPException(status_code=404, detail=f"Unknown code: {code}")
    db.increment_clicks(conn, code)
    return RedirectResponse(url=row["url"], status_code=307)
