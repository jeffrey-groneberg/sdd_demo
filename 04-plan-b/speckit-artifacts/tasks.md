# Tasks: URL Shortener

**Input:** `plan.md`, `spec.md`
**Total tasks:** 14

> **Convention:** `[P]` = can run in parallel (different files). Sequential within a numbered group.

## Phase 1: Project Scaffold

- [ ] **T001** Create `pyproject.toml` with deps `fastapi`, `uvicorn[standard]`, `jinja2`, `pytest`, `httpx`
- [ ] **T002** Create `app/__init__.py` (empty) and `tests/__init__.py` (empty) [P]
- [ ] **T003** Add `shortly.db`, `.venv`, `__pycache__/` to `.gitignore` [P]

## Phase 2: Persistence Layer

- [ ] **T004** Implement `app/db.py` with:
  - `get_conn()` factory (sqlite3, `check_same_thread=False`)
  - `init_db()` creating `urls` table + index
  - `insert_url(code, url, created_at)` returning bool (False on collision)
  - `get_url(code)` returning row or None
  - `increment_clicks(code)` (transactional)
  - `list_recent(limit=10)` returning list of dicts

## Phase 3: Routes

- [ ] **T005** Implement `app/main.py` skeleton: FastAPI app, `Jinja2Templates`, startup hook calling `init_db()`
- [ ] **T006** Implement `GET /` returning rendered `index.html` with recent list
- [ ] **T007** Implement `POST /shorten`:
  - validate scheme (http/https) → return 400 on invalid
  - generate 6-char code via `secrets.choice` on `string.ascii_letters + string.digits`
  - retry on collision up to 5×
  - redirect to `/` on success
- [ ] **T008** Implement `GET /{code}`:
  - lookup, 404 if missing
  - `increment_clicks(code)`
  - return `RedirectResponse(url, status_code=307)`
- [ ] **T009** Implement `GET /stats/{code}` rendering `stats.html` or 404

## Phase 4: Templates

- [ ] **T010** Create `app/templates/index.html`: Pico.css CDN, header, shorten form, "Recent URLs" table (code, url truncated, clicks, stats link) [P]
- [ ] **T011** Create `app/templates/stats.html`: shows original url, code, clicks, created_at, back link [P]

## Phase 5: Tests

- [ ] **T012** `tests/test_app.py`: fixture for fresh in-memory DB via dependency override
- [ ] **T013** Test cases:
  - `test_shorten_creates_code()`
  - `test_redirect_increments_clicks()`
  - `test_stats_shows_count()`
  - `test_unknown_code_returns_404()`
  - `test_invalid_url_returns_400()`

## Phase 6: Manual Verification

- [ ] **T014** Run `uv run uvicorn app.main:app --reload`; manually:
  - shorten `https://github.com/github/spec-kit`
  - click the short URL twice
  - stats shows clicks=2
  - home page lists the URL

## Dependency Graph

```
T001 → T002, T003 (parallel)
T004 → T005 → T006, T007, T008, T009 (sequential — same file)
T010, T011 (parallel, depend on T005 contract)
T012 → T013 (sequential — same file)
T014 (after all above)
```

## Estimated Effort

| Phase | Time (with `/speckit.implement`) | Manual fallback time |
|-------|----------------------------------|-----------------------|
| 1 | 30 s | 5 min |
| 2 | 60 s | 15 min |
| 3 | 90 s | 30 min |
| 4 | 60 s | 15 min |
| 5 | 60 s | 20 min |
| 6 | manual | manual |
| **Total** | **~5 min** | **~90 min** |
