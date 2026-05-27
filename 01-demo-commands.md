# Demo Cheat Sheet — Commands Only

A stripped-down version of `01-demo-script.md` with only the commands and a one-line note per step.

---

## Block 2 — Plan agent live (~3.5 min)

Create an empty folder and open VS Code so the Plan agent has nothing to lean on:

```powershell
mkdir plan-mode-demo
cd plan-mode-demo
code .
```

Then in VS Code: Chat view (`Ctrl+Alt+I`) → agents dropdown → **Plan**.

Prompt to paste (planning only, no edits):

```
Plan only. Do not edit any files.

This folder is empty. Plan how to bootstrap a tiny FastAPI service:
- a GET /health endpoint returning {"status": "ok"}
- one pytest test that verifies status 200 and the JSON body
- use uv for dependency management

Give me: files to create, exact test cases, and risks.
```

---

## Block 4 — SpecKit install + init (~4 min)

Step out of the previous folder:

```powershell
cd ..
```

One-time install (already done — show, do not run live):

```powershell
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

Init a fresh project and open it (the `--integration copilot` flag writes prompts where VS Code looks for them):

```powershell
specify init shortly-live --integration copilot
cd shortly-live
code .
```

In Copilot Chat of the new window, set the project's DNA:

```
/speckit.constitution Create project principles focused on:
1. Minimal dependencies — only what is essential
2. Standard library first — prefer Python stdlib over third-party
3. Testability — every endpoint needs at least one test
4. Server-rendered HTML — no SPA, no build step
5. No external services — must run fully offline
6. Single-file modules where reasonable
7. Explicit over implicit — no magic frameworks
```

---

## Block 5a — `/speckit.specify` (what & why, no tech)

```
/speckit.specify Build a URL shortener web service.
Users can submit a long URL via a form and receive a short code.
Visiting the short URL redirects to the original and increments
a click counter. A stats page shows the original URL, click count
and creation date for any code. Recent shortened URLs are listed
on the home page. Single-user, no auth, no expiry.
```

Output: `.specify/specs/001-url-shortener/spec.md`

Parachute if stuck >3 min:

```bash
git checkout -f stage-2-after-specify
```

---

## Block 5b — `/speckit.plan` (the tech stack)

```
/speckit.plan Use Python 3.12 with FastAPI as the only web framework.
Use the sqlite3 standard library for persistence (no SQLAlchemy, no
Alembic). Use Jinja2 templates for minimal server-rendered HTML with
Pico.css from CDN. Tests with pytest using FastAPI's TestClient.
Single file app/main.py is preferred. Do NOT introduce: Docker,
Redis, background workers, auth, frontend build tools, or external
services.
```

Output: `.specify/specs/001-url-shortener/plan.md`

Parachute:

```bash
git checkout -f stage-3-after-plan
```

---

## Block 5c — `/speckit.tasks` (decompose into steps)

```
/speckit.tasks
```

Output: `.specify/specs/001-url-shortener/tasks.md` (T001…T014, `[P]` = parallelizable)

Parachute (>2 min):

```bash
git checkout -f stage-4-after-tasks
```

---

## Block 5d — `/speckit.implement` (~5–8 min live)

```
/speckit.implement
```

Agent generates code in dependency order: db → routes → templates → tests, and runs `pytest` itself.

Helpful side commands while it runs:

```bash
git status
git log --oneline
```

Parachute (only after >3 min no tokens or hard error):

```bash
git checkout -f stage-5-complete
```

---

## Block 6 — Run the app (~2 min)

```bash
uv run uvicorn app.main:app --reload
```

Fallback if `uv` not available:

```bash
python -m uvicorn app.main:app --reload
```

Then browser → `http://localhost:8000` → shorten a URL, click the short code, open stats, refresh to see the counter tick up.

---

## Quick reference — all slash commands in order

```
/speckit.constitution   # project principles (Block 4)
/speckit.specify        # what & why         (Block 5a)
/speckit.plan           # how / tech stack   (Block 5b)
/speckit.tasks          # decomposed steps   (Block 5c)
/speckit.implement      # generate code      (Block 5d)
```

Bonus (team workflow, mentioned in Block 7a):

```
/speckit.taskstoissues  # turn tasks.md into GitHub issues
```

---

## Pace checkpoints

| Clock  | Block                              |
|--------|------------------------------------|
| 1:30   | Plan agent live                    |
| 5:00   | Bridge                             |
| 7:00   | SDD concept + install              |
| 11:00  | `/speckit.specify`                 |
| 13:30  | `/speckit.plan`                    |
| 16:00  | `/speckit.tasks`                   |
| 18:00  | `/speckit.implement` (5–8 min)     |
| ~24:00 | Test app in browser                |
| ~26:00 | Team workflow (60 sec)             |
| ~28:30 | Wrap-up                            |
