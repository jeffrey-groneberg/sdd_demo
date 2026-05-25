# Copy-Paste Prompts (cheat sheet)

> Print this page or put it on a second display. All prompts are **tested** against the included Plan B artifacts.
>
> ⚡ **Live-first strategy:** §2, §3, §4 are run **live** during the demo. §5 is **started** live and stopped after 30s. §6 is run once ahead of time during setup. Branches are only a safety net for timeouts > 90s.

---

## §1 — Plan Mode Prompt (Block 2 — LIVE)

```text
Plan only. Do not edit any files.

We have a FastAPI URL shortener (currently just /hello).
Plan how to add:
- a GET /health endpoint returning {"status": "ok"}
- one pytest test that verifies status 200 and the JSON body

Give me: files to touch, exact test cases, and risks.
```

---

## §2 — `/speckit.specify` (Block 5a — LIVE)

```text
/speckit.specify Build a URL shortener web service.
Users can submit a long URL via a form and receive a short code.
Visiting the short URL redirects to the original and increments
a click counter. A stats page shows the original URL, click count
and creation date for any code. Recent shortened URLs are listed
on the home page. Single-user, no auth, no expiry.
```

---

## §3 — `/speckit.plan` (Block 5b — LIVE)

```text
/speckit.plan Use Python 3.12 with FastAPI as the only web framework.
Use the sqlite3 standard library for persistence (no SQLAlchemy, no
Alembic). Use Jinja2 templates for minimal server-rendered HTML with
Pico.css from CDN. Tests with pytest using FastAPI's TestClient.
Single file app/main.py is preferred. Do NOT introduce: Docker,
Redis, background workers, auth, frontend build tools, or external
services.
```

---

## §4 — `/speckit.tasks` (Block 5c — LIVE)

```text
/speckit.tasks
```

---

## §5 — `/speckit.implement` (Block 5d — LIVE START, cut after 30s)

```text
/speckit.implement
```

> **Cut routine:** After 30s, click the Stop button in chat (red square at the top right of the chat input), then `git checkout -f stage-5-complete`.

---

## §6 — `/speckit.constitution` (run once ahead of time during project setup!)

> 💡 **In VS Code Copilot Chat: `Shift+Enter` for a line break inside a prompt.**

```text
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

## §7 — Setup Commands (day before the demo, NOT during the demo!)

```powershell
# 1. Install uv (if not already installed) — Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Install SpecKit CLI
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# 3. Prepare demo directory
mkdir $HOME\demos
cd $HOME\demos

# 4. Plan Mode demo repo from skeleton
mkdir plan-mode-demo
cd plan-mode-demo
# Copy contents of files\04-plan-b\mini-skeleton\ here
git init
git add .
git commit -m "FastAPI skeleton with /hello"
cd ..

# 5. Initialize SpecKit demo repo — then open VS Code
specify init shortly --integration copilot
cd shortly
code .
# In VS Code Chat: run /speckit.constitution with the §6 prompt
git add .
git commit -m "stage-1-after-init: init + constitution"
git branch stage-1-after-init

# (Continue with /speckit.specify, /plan, /tasks, /implement —
#  one branch after each step. See 03-setup-checklist.md.)
```

---

## §8 — Branch Jump Commands (safety net during demo, `-f` required!)

```powershell
# Block 5a bailout (if /speckit.specify hangs > 90s)
git checkout -f stage-2-after-specify

# Block 5b bailout (if /speckit.plan > 90s)
git checkout -f stage-3-after-plan

# Block 5c bailout (if /speckit.tasks > 60s)
git checkout -f stage-4-after-tasks

# Block 5d — planned cut after 30s live start
git checkout -f stage-5-complete

# Start app (Block 6)
uv run uvicorn app.main:app --reload
# Fallback without uv:
python -m uvicorn app.main:app --reload
```

> **`-f` is required** — live SpecKit commands create uncommitted files that would block a normal checkout.

---

## §9 — Recovery Mantra (stick it on the cheat sheet)

1. **BREATHE** (one deep inhale, slow exhale)
2. **SAY:** "So we don't wait for tokens, let's jump to the deterministic state."
3. **TYPE:** `git checkout -f stage-N-...`
4. **CONTINUE** in the script as if nothing happened
