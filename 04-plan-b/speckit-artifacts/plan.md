# Implementation Plan: URL Shortener

**Branch:** `001-url-shortener` | **Spec:** `spec.md`

## Technical Context

| Aspect | Choice | Justification |
|--------|--------|---------------|
| **Language** | Python 3.12 | Constitution: minimal deps; Python stdlib is rich |
| **Web framework** | FastAPI | Stated requirement; sync routes are sufficient |
| **Server** | Uvicorn | Standard ASGI server for FastAPI |
| **Persistence** | `sqlite3` (stdlib) | Constitution II: stdlib first; single-user volume |
| **Templates** | Jinja2 | Server-rendered HTML per Constitution IV |
| **CSS** | Pico.css via CDN | Zero build step, classless |
| **Testing** | `pytest` + FastAPI `TestClient` + `httpx` | Constitution III |
| **Dependency mgmt** | `uv` + `pyproject.toml` | Modern, fast, simple lock |

## Constitution Check (PASS)

| Principle | Status | Notes |
|-----------|--------|-------|
| I — Minimal deps | ✅ | 4 runtime deps total |
| II — Stdlib first | ✅ | sqlite3 over SQLAlchemy |
| III — Testability | ✅ | TestClient covers all routes |
| IV — Server-rendered HTML | ✅ | Jinja2, no SPA |
| V — Offline | ✅ | Pico.css from CDN is opt-in; can be vendored if needed |
| VI — Single-file modules | ✅ | `app/main.py` holds routes; `app/db.py` holds persistence |
| VII — Explicit over implicit | ✅ | Manual SQL, no ORM |

## Project Structure

```
shortly/
├── pyproject.toml
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app + routes
│   ├── db.py            # sqlite3 helpers, schema bootstrap
│   └── templates/
│       ├── index.html   # form + recent table
│       └── stats.html   # single-code stats
├── tests/
│   ├── __init__.py
│   └── test_app.py      # 4 acceptance scenarios + edge cases
└── shortly.db           # created on first run (gitignored)
```

## Data Model

Single SQLite table:

```sql
CREATE TABLE IF NOT EXISTS urls (
    code        TEXT PRIMARY KEY,
    url         TEXT NOT NULL,
    clicks      INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_urls_created ON urls (created_at DESC);
```

## Routes

| Method | Path | Handler | Returns |
|--------|------|---------|---------|
| GET | `/` | `index` | HTML (form + recent table) |
| POST | `/shorten` | `shorten` | HTML (redirect-back to `/`) |
| GET | `/{code}` | `redirect` | 307 redirect or 404 |
| GET | `/stats/{code}` | `stats` | HTML or 404 |

## Code Generation Strategy

- Use `secrets.choice` over a 62-char alphabet for the code
- Wrap insert in `INSERT OR IGNORE` + retry loop (max 5) for collision safety
- Use `sqlite3` connection per request via FastAPI dependency
- Validation: simple `urlparse` check for scheme in `("http", "https")`

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Concurrent click updates lose increments | Wrap UPDATE in transaction; SQLite serializes by default for single-file DB |
| SQLite file locked on Windows | Use `check_same_thread=False` and short-lived connections |
| User submits javascript: URL | Scheme validation rejects anything not http/https |
