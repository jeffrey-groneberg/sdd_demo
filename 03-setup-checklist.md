# Setup Checklist

> **Use in order:** Phase A on Monday evening, Phase B 30 min before demo. Nothing waits until the last minute.

---

## 🅐 Day before the demo (Monday)

### A1 — Verify tools (10 min)

- [ ] Open `Help → About`; confirm VS Code is at least **v1.105** (Plan agent went stable in 1.105). Current Stable as of May 2026 is **1.121** — updating to the latest is recommended.
- [ ] Confirm the GitHub Copilot extension is active, signed in, and **Plan** appears in the **agents dropdown** of the Chat view (alongside Agent and Ask)
  - If Plan is missing: your VS Code is too old → update to current Stable. There is no separate feature toggle to enable; the Plan agent is built-in to current Stable.
- [ ] Run `copilot --version` for the one-sentence Copilot CLI note in the Wrap-up
- [ ] Run `python --version`; confirm Python 3.12
- [ ] Run `uv --version`; confirm uv is installed
- [ ] Run `specify --version`; confirm SpecKit CLI is installed
  ```powershell
  uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
  ```

### A2 — Prepare demo repos (45 min)

> Run this section from `$HOME\demos\`; it is the parent folder for the `shortly/` parachute repo and the `shortly-stage-5` backup worktree. **No `plan-mode-demo/` and no `shortly-live/` are prepared** — Block 2 creates `plan-mode-demo/` live on stage; Block 4 creates `shortly-live/` live on stage. The prepared `shortly/` exists only as the emergency parachute, opened in window B and never demoed unless something stalls.

**Repo 2: `shortly/` (parachute for Blocks 4–6)**

> 🎯 **Purpose of the branches:** They are an **emergency parachute** for live demos. On demo day the agent runs to completion for every SpecKit command, including `/speckit.implement` (5–8 min). Use a branch only when the agent has no token stream for > 3 min, returns an error it does not self-recover from, or pushes the demo past 30 min.
>
> 🏷 **Naming note:** `stage-1-after-init` contains both `specify init` **and** `/speckit.constitution`. That branch is the shared starting point; later stage branches are emergency parachute checkpoints, not planned cuts.

### 🌿 Branch chain overview

```mermaid
flowchart TB
    Init["specify init<br/>--integration copilot"] --> Const["/speckit.constitution<br/>(§6 Prompt)"]
    Const ==> Tag1["🏷 stage-1-after-init<br/>📌 Demo starting point"]
    Tag1 --> Spec["/speckit.specify<br/>(§2 Prompt)"]
    Spec --> Tag2["🏷 stage-2-after-specify<br/>+ spec.md"]
    Tag2 --> Plan["/speckit.plan<br/>(§3 Prompt)"]
    Plan --> Tag3["🏷 stage-3-after-plan<br/>+ plan.md"]
    Tag3 --> Tasks["/speckit.tasks<br/>(§4)"]
    Tasks --> Tag4["🏷 stage-4-after-tasks<br/>+ tasks.md"]
    Tag4 --> Impl["/speckit.implement<br/>(5-8 min, ☕)"]
    Impl ==> Tag5["🏷 stage-5-complete<br/>+ app/ + tests/"]

    style Tag1 fill:#e1f5ff,stroke:#0288d1,stroke-width:3px
    style Tag2 fill:#fff4e1,stroke:#f57c00
    style Tag3 fill:#fff4e1,stroke:#f57c00
    style Tag4 fill:#fff4e1,stroke:#f57c00
    style Tag5 fill:#e1f5d3,stroke:#388e3c,stroke-width:3px
```

Create each setup branch immediately after its slash command: `git add . && git commit -m "stage-N-..."`, then `git branch stage-N-...`.

- [ ] `specify init shortly --integration copilot`
- [ ] `cd shortly`
- [ ] Open `shortly\` in VS Code and open Copilot Chat
- [ ] Run `/speckit.constitution` with prompt from `02-prompts.md` §6
- [ ] Commit: `git add . && git commit -m "stage-1-after-init: init + constitution"`
- [ ] Set branch: `git branch stage-1-after-init`
- [ ] Run `/speckit.specify` with prompt from §2
- [ ] Open generated `.specify\specs\...\spec.md`; confirm 3 user stories and clear acceptance criteria
- [ ] Commit and branch: `git add .; git commit -m "stage-2-after-specify"; git branch stage-2-after-specify`
- [ ] Run `/speckit.plan` with prompt from §3
- [ ] Open generated `.specify\specs\...\plan.md`; confirm FastAPI + sqlite3 + Jinja2 and no ORMs
- [ ] Commit and branch: `git add .; git commit -m "stage-3-after-plan"; git branch stage-3-after-plan`
- [ ] Run `/speckit.tasks`
- [ ] Open generated `.specify\specs\...\tasks.md`; confirm setup, routes, templates, tests, and run order are covered
- [ ] Commit and branch: `git add .; git commit -m "stage-4-after-tasks"; git branch stage-4-after-tasks`
- [ ] Run `/speckit.implement`; let the agent run to completion (**5–8 min**)
- [ ] Test app: `uv run uvicorn app.main:app --reload`
  - Create a short URL
  - Open the short URL and confirm redirect
  - Refresh stats and confirm the click counter increments
  - Open the stats page and confirm correct numbers
- [ ] Produce a working stage-5 tree: use the generated implementation when the four app checks pass; otherwise copy in code from `04-plan-b/final-app/` (see `04-plan-b/final-app/README.md` → section "Demo emergency: copy code into live repo" for the exact `robocopy` commands) and rerun the checks
- [ ] Commit and branch: `git add .; git commit -m "stage-5-complete"; git branch stage-5-complete`
- [ ] **Check list of all branches:** `git branch` shows stage-1 through stage-5
- [ ] Create the separate backup app worktree for Browser tab 1: `cd $HOME\demos\shortly; git worktree add --detach ..\shortly-stage-5 stage-5-complete`

### A2b — Slash-command rehearsal (35 min) — **IMPORTANT**

> Practice only the **live slash commands** on a **second** throw-away repo so you know timing and outputs from your own experience. **Run `/speckit.implement` to completion** — the agent runs to completion on demo day, and the branch chain stays an emergency parachute. (The full ~28-minute dress rehearsal comes in A5.)

- [ ] `cd $HOME\demos && specify init shortly-rehearsal --integration copilot`
- [ ] `cd shortly-rehearsal`, open in VS Code, open Copilot Chat
- [ ] `/speckit.constitution` with §6 prompt — **start stopwatch**
- [ ] `/speckit.specify` with §2 prompt — **note seconds** (expected: 30–90s)
- [ ] `/speckit.plan` with §3 prompt — note seconds
- [ ] `/speckit.tasks` — note seconds
- [ ] `/speckit.implement` — **let it run to completion**, note total minutes (expected: 5–8 min). Record any silent hang or self-recovered error so demo day has no surprises.
- [ ] Enter values in table:

  | Command | Time | Output quality ok? |
  |---------|----------|---------------------|
  | /speckit.constitution | _____ sec | ☐ yes ☐ no |
  | /speckit.specify | _____ sec | ☐ yes ☐ no |
  | /speckit.plan | _____ sec | ☐ yes ☐ no |
  | /speckit.tasks | _____ sec | ☐ yes ☐ no |
  | /speckit.implement | _____ min | ☐ yes ☐ no |

- [ ] Confirm total time for all 5 commands is ≤ 11 min (≈ first 4 commands ≤ 3 min + /implement ≤ 8 min). When total time exceeds 13 min, switch model (VS Code Chat → model dropdown at the bottom of the chat input) to the currently fastest available model with the same quality.
- [ ] Record any command that consistently has no token stream for > 3 min; map it to the matching emergency parachute command `git checkout -f stage-N-...`.
- [ ] **Practice the parachute pattern (in case demo day goes badly):**
  ```powershell
  git checkout -f stage-2-after-specify   # -f discards uncommitted changes
  ```
  Run this checkout 3× until it is muscle memory
- [ ] **Cleanup after rehearsal:** `cd $HOME\demos && Remove-Item -Recurse -Force shortly-rehearsal` (otherwise you may confuse the repos on demo day)

### A3 — Rehearse branch jumps (15 min)

- [ ] Run through this emergency parachute chain 3× without looking: `git checkout -f stage-2-after-specify`, `git checkout -f stage-3-after-plan`, `git checkout -f stage-4-after-tasks`, `git checkout -f stage-5-complete`
- [ ] Use the `-f` flag on every checkout; live commands leave uncommitted files that block normal checkout
- [ ] After each checkout, confirm the expected files appear: `spec.md`, then `plan.md`, then `tasks.md`, then `app\` + `tests\`
- [ ] On `stage-5-complete`, run `uv run uvicorn app.main:app --reload`, confirm it starts cleanly, then stop it with Ctrl+C

### A4 — Backup materials (10 min)

> 📁 **Storage location:** Put all backups in a folder `$HOME\demos\backup\` — easy to find on demo day.

- [ ] Save screenshot of successful Plan agent output to `$HOME\demos\backup\plan-agent-output.png`
- [ ] Save screenshots of successful `spec.md`, `plan.md`, `tasks.md` to `$HOME\demos\backup\{spec,plan,tasks}.png`
- [ ] Record 2 min of the working app to `$HOME\demos\backup\shortly-demo.mp4`
- [ ] Put `02-prompts.md` on the second screen and print one paper copy
- [ ] Copy the `backup\` folder to a USB stick

### A5 — Full dress rehearsal of the entire demo (35 min)

> Complete a ~28-minute run-through on the real `shortly/` repo (not the rehearsal repo from A2b). Here you practice the **flow + timing**, not the slash commands themselves anymore. Plan for ~28 min total because `/speckit.implement` runs full live.

- [ ] Reset `shortly\` to the demo starting point: `git checkout -f stage-1-after-init`
- [ ] Talk through the complete demo once alone with a stopwatch
- [ ] Mark every overflow spot and the sentence you will cut there
- [ ] Practice narrating during the `/speckit.implement` window — that 5–8 min stretch is the hardest. Use the narration arc in `01-demo-script.md` Block 5d as a scaffold. Comfortable silence is fine for 10s; longer than that and you lose the room.
- [ ] Set the 30-min cut plan: shorten Block 4 by 1 min first, then drop Block 7a (60 sec) and point to `06-team-workflow.md` in the wrap-up instead
- [ ] Run the emergency parachute (`git checkout -f stage-5-complete`) once so the muscle memory sticks

---

## 🅑 30 minutes before the demo (Tuesday)

### B1 — Hardware (5 min)

- [ ] Plug in laptop
- [ ] Connect external screen / projector and set resolution
- [ ] Set VS Code zoom to **+3** (Ctrl+= three times); check terminal font size
- [ ] Set browser zoom to **125%**
- [ ] Confirm the mic is unmuted 🙂

### B2 — Open apps ahead of time, in order (10 min)

1. **Terminal tab 1:** `cd $HOME\demos` (Block 2 creates `plan-mode-demo\` live from here)
2. **VS Code window A:** closed or on the welcome screen — you open it live in Block 2 step (a)
3. **Terminal tab 2:** `cd $HOME\demos\shortly`, then `git checkout -f stage-1-after-init` (this terminal stays attached to the **parachute** repo for Blocks 4–6)
4. **VS Code window B (parachute):** `shortly\` on branch `stage-1-after-init` opened in a separate window, Explorer collapsed. **This window is only opened during emergencies** — in Block 4 you create `shortly-live/` live and open a different window for it. Having window B pre-loaded means an emergency switch is one Alt+Tab away.
5. **Terminal tab 3:** `cd $HOME\demos\shortly-stage-5`, confirm `git status` is clean, then run the backup app on port 8001 (`uv run uvicorn app.main:app --port 8001 --reload`) — this is the emergency parachute app
   - Keep this on port 8001 so Browser tab 1 and `05-recovery.md` match.
6. **Browser tab 1:** `http://localhost:8001` (shows the running backup app index page)
7. **Browser tab 2:** `http://localhost:8000` (for the "real" app in Block 6 — you start it live; currently "connection refused" — that is expected)
8. **Browser tab 3:** `https://github.com/github/spec-kit` (for Wrap-up link reference)
9. **Cheat sheet:** `02-prompts.md` on second screen and printed copy beside laptop
10. **Stopwatch/timer** visible on second screen (phone or `timer.onlineclock.net`) — for the 30/60/90-sec marks in Block 5

### B3 — Smoke test (5 min)

- [ ] `$HOME\demos\plan-mode-demo` does **not** exist yet (you will create it live in Block 2; if a previous rehearsal left one, delete it now)
- [ ] `$HOME\demos\shortly-live` does **not** exist yet (you will create it live in Block 4; if a previous rehearsal left one, delete it now)
- [ ] `git status` in `shortly\` = clean (this is the parachute repo)
- [ ] Terminal tab 3 shows the port-8001 backup app running without errors
- [ ] `git branch` in `shortly\` shows all stage-1 through stage-5
- [ ] Copilot Chat responds in the **shortly\** parachute VS Code window (type a short test question, e.g. "hi"). Window A for Block 2 / Block 4 starts empty by design.
- [ ] Browser tab 1 (`http://localhost:8001`) loads the URL shortener index page
- [ ] Turn off notifications, Slack, mail, and updates (Focus Assist / Do Not Disturb)
- [ ] Disable screen saver for the next hour

### B4 — Mental preparation (10 min)

- [ ] Skim demo script block cues one more time
- [ ] Do **box breathing** 3× (inhale 4 sec – hold 4 sec – exhale 6 sec – hold 2 sec)
- [ ] Say the core bridge sentence out loud:
  > "The Plan agent helps me think in the moment, before coding. SpecKit makes sure that intent persists over time."
- [ ] Put water within reach
- [ ] Say out loud: "You are prepared. Even if EVERYTHING live breaks, you have emergency parachute branches + screenshots + video."

---

## ✅ Last-Minute Sanity Check (1 min before start)

| Check | Target value |
|-------|----------|
| Laptop battery | > 60 % (preferably plugged in) |
| Internet | Stable (Ethernet > Wi-Fi) |
| VS Code Copilot status | green icon |
| Terminal tabs | 3 open, in the right directory |
| Browser tabs | 3 open: 8001 loaded, 8000 connection refused, SpecKit loaded |
| Screen shared? | Yes, correct screen |
| Mic | not muted |
| Cheat sheet | within reach |

**Let's go. 🎬**
