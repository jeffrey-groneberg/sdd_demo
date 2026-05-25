# Copy-Paste Prompts (cheat sheet)

> Second-screen/print cheat sheet. Copy fenced `text` blocks into Copilot Chat; use fenced `powershell` blocks only in the terminal.
>
> ⚡ **All-live:** §2–§5 run live. The agent runs to completion every time, including `/speckit.implement` (5–8 min). No planned cut.
>
> 🧰 **Setup-only:** §6–§7 happen before stage.
>
> 🪂 **Emergency parachute:** branch jumps in §8 only if the agent has no token stream for several minutes, errors without auto-retry, or the demo passes 30 min.

---

## §1 — Plan Mode Prompt (Block 2 — LIVE, run on a freshly created empty folder)

```text
Plan only. Do not edit any files.

This folder is empty. Plan how to bootstrap a tiny FastAPI service:
- a GET /health endpoint returning {"status": "ok"}
- one pytest test that verifies status 200 and the JSON body
- use uv for dependency management

Give me: files to create, exact test cases, and risks.
```

**Terminal preamble (run live, just before the prompt above):**

```powershell
cd $HOME\demos
mkdir plan-mode-demo
cd plan-mode-demo
code .
```

Then open Copilot Chat (Ctrl+Alt+I) → switch mode dropdown to **Plan** → paste the prompt.

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

## §5 — `/speckit.implement` full run (Block 5d — LIVE)

```text
/speckit.implement
```

> **No cut. Do not stop after 30s.** The agent runs to completion (typically 5–8 min). Narrate: point at files as they appear, scroll `tasks.md` for checkmarks, mention dependency order. This live window is the point.
>
> 🪂 **Emergency parachute only if:** no token stream for > 3 min, OR an explicit error appears that doesn't auto-retry, OR you've passed 30 min total demo time. Then: Stop button in chat → `git checkout -f stage-5-complete`.

---

## §6 — `/speckit.constitution` (Project setup — SETUP)

> **Setup-only:** run once before stage. Do not paste during the live demo.
>
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

## §7 — Setup Commands (Project setup — SETUP)

> **Setup-only terminal commands.** Run before demo day, not during the live script.

```powershell
# 1. Install uv (if not already installed) — Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 2. Install SpecKit CLI
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# 3. Prepare demo directory
mkdir $HOME\demos
cd $HOME\demos

# 4. (Block 2 happens LIVE on stage — no demo repo prep needed.
#     The `plan-mode-demo` folder gets created in front of the audience.)

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

## §8 — Emergency Parachute Commands (Block 5/6 — SETUP)

> 🪂 **Terminal only.** `git checkout` lines are the emergency parachute, not planned cuts and not chat prompts. App-start lines are for Block 6.

```powershell
# Only use if the agent is clearly stuck (no tokens for several minutes)
# or has errored out — not for ordinary slowness.

# Block 5a parachute (if /speckit.specify hangs > 3 min with no progress, or errors)
git checkout -f stage-2-after-specify

# Block 5b parachute (if /speckit.plan hangs > 3 min with no progress, or errors)
git checkout -f stage-3-after-plan

# Block 5c parachute (if /speckit.tasks hangs > 2 min with no progress, or errors)
git checkout -f stage-4-after-tasks

# Block 5d parachute (if /speckit.implement hangs > 3 min between tasks, errors, or blows past 30 min demo total)
git checkout -f stage-5-complete

# Start app (Block 6)
uv run uvicorn app.main:app --reload
# Fallback without uv:
python -m uvicorn app.main:app --reload
```

> **`-f` is required** — live SpecKit commands create uncommitted files that block a normal checkout.

---

## §9 — Recovery Mantra (Block 5 emergency — SETUP)

1. **BREATHE** (one deep inhale, slow exhale)
2. **SAY:** "So we don't wait for tokens, we'll use the emergency parachute and continue from the deterministic state."
3. **TYPE:** `git checkout -f stage-N-...`
4. **CONTINUE** in the script as if nothing happened
