# Shortly — Plan B Reference Implementation

> This app is the **working final result** of the SpecKit workflow from the artifacts in `../speckit-artifacts/`. It serves as a safety net for the demo: if `/speckit.implement` does not complete live, copy the contents of this folder into your demo repo and commit it as `stage-5-complete`.

## Quick Start

```powershell
cd shortly  # or your demo repo after copying
uv venv
.venv\Scripts\activate
uv pip install -e ".[dev]"          # or: uv sync
uv run uvicorn app.main:app --reload
```

Open browser at `http://localhost:8000`.

## Run tests

```powershell
uv run pytest -v
```

Expected output: **5 passed**.

## What the app can do (demo-relevant)

1. `GET /` — form + table of the last 10 URLs
2. `POST /shorten` — creates 6-char code, redirects back to homepage
3. `GET /{code}` — 307 redirect, increments click counter
4. `GET /stats/{code}` — shows original URL, clicks, date

## Mapping to the SpecKit artifacts

| File | Comes from |
|-------|-----------|
| `app/db.py` | `tasks.md` T004 (Phase 2) |
| `app/main.py` | `tasks.md` T005–T009 (Phase 3) |
| `app/templates/*.html` | `tasks.md` T010–T011 (Phase 4) |
| `tests/test_app.py` | `tasks.md` T012–T013 (Phase 5) |
| `pyproject.toml` | `tasks.md` T001 (Phase 1) |

The T numbers refer to `../speckit-artifacts/tasks.md`. The architecture follows `../speckit-artifacts/plan.md` (FastAPI + sqlite3 + Jinja2, no ORMs), which in turn respects the `../speckit-artifacts/constitution.md` principles.

## Demo emergency: copy code into live repo

```powershell
# Assumption: you are in your demo repo ~/demos/shortly
cd ~/demos/shortly
git checkout main
robocopy "<session-files>\04-plan-b\final-app\" "." /E /XD .git
git add .
git commit -m "stage-5-complete: working URL shortener"
git branch stage-5-complete
```

(On macOS/Linux: `cp -R <session-files>/04-plan-b/final-app/* .`)
