# 📦 SpecKit Demo Package — Overview

> **Everything you need for Tuesday's ~28-minute (25–30 min) live demo of GitHub Copilot's Plan agent + SpecKit/Spec-Driven Development.**
> Start with the strategy, then use the contents table to choose: run the demo, review prep, or inspect the working app.

> 🎤 **Live slides for participants:** <https://jeffrey-groneberg.github.io/sdd_demo/> · use these to follow along; slide 1 has the QR for this repo.

> 💡 **Tip:** All Mermaid diagrams in the docs render natively on GitHub. In VS Code, use **Ctrl+Shift+V** to preview the markdown with rendered diagrams.

## 🎯 Strategy (Agent runs to completion; branches are the emergency parachute)

- **Agent runs to completion by default.** All four SpecKit commands run live: `/speckit.specify`, `/speckit.plan`, `/speckit.tasks`, **and** `/speckit.implement`. The audience sees the chat flow, streamed reasoning, and real work. **There is no planned cut.**
- **`/speckit.implement` typically takes 5–8 minutes.** Use that window to narrate the spec → plan → tasks → code connection while the agent works through tasks in dependency order. Total demo wall-clock is ~28 min (range 25–30 depending on agent speed).
- **Branches are an emergency parachute, not the plan.** Pre-staged branches `stage-1` through `stage-5` only get pulled when something is clearly broken: the agent hangs for several minutes with no token stream, hits an explicit error after retries, the network drops, or quota is exhausted. **Default behaviour: wait, narrate, finish.**
- **Pre-stage assumption:** Demo creates everything **live** — `plan-mode-demo/` in Block 2 and `shortly-live/` (with `specify init` + `/speckit.constitution`) in Block 4. The pre-staged `shortly/` repo with `stage-1` through `stage-5` branches sits in a **second VS Code window as the emergency parachute** — only opened if a live step stalls or errors.

## 📋 Contents

| File / Folder | Purpose | When to read? |
|----------------|-------|-------------|
| `01-demo-script.md` | **Word-for-word speaker script** with block cues, time checkpoints, and emergency parachute lines | Start here if you're running or studying the demo |
| `02-prompts.md` | Copy/paste prompts for the Plan agent, 4× SpecKit commands, and setup | Keep on a second display during the demo |
| `03-setup-checklist.md` | 2-phase checklist: Monday evening + 30 min before demo | **Complete by Monday evening at the latest** |
| `04-plan-b/` | Emergency parachute artifacts, including a verified `final-app/` URL shortener | Inspect `final-app/` to explore the app; use branches only in emergencies |
| `05-recovery.md` | "What to do if …" — emergency playbook | Skim beforehand, keep handy during the demo |
| `06-team-workflow.md` | **How SDD scales to multiple features and developers** — hand-offs, parallel features, AI agents as teammates | Read after the demo to plan rollout in your team |
| `07-speckit-anatomy.md` | **Deep-dive reference:** what exactly happens inside each `/speckit.*` command — mechanics, prompt files, helper scripts, real artifact excerpts | Read after the demo when you want to understand the internals |

## 📁 04-plan-b/ — emergency parachute in detail

```
04-plan-b/
├── mini-skeleton/              ← Last-ditch fallback only (if Copilot is fully down in Block 2). Block 2 normally creates an empty folder live and lets the Plan agent bootstrap from zero.
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
├── speckit-artifacts/          ← The 4 Markdown artifacts (Plan B contents for branches stage-1..4)
│   ├── constitution.md
│   ├── spec.md
│   ├── plan.md
│   └── tasks.md
└── final-app/                  ← Working URL shortener implementation (Plan B for stage-5)
    ├── app/main.py
    ├── app/db.py
    ├── app/templates/{index,stats}.html
    ├── tests/test_app.py
    ├── pyproject.toml
    └── README.md
```

**`final-app/` is verified:**
- ✅ `pytest` — 5/5 tests passed
- ✅ `uvicorn app.main:app` — starts cleanly
- ✅ End-to-end HTTP test: shorten → 307 redirect → click counter +1 → stats shows 2

## ⚡ Quick-start order (for presenters)

1. **Now** read `01-demo-script.md` → understand the narrative and timing
2. **Now** skim `05-recovery.md` → know when the emergency parachute applies
3. **Monday evening** complete `03-setup-checklist.md` Phase A (approx. 120 min)
   – use `02-prompts.md` as the source for the slash commands
4. **Tuesday, 30 min before demo** complete `03-setup-checklist.md` Phase B (approx. 30 min)
5. **Demo** — cheat sheet = `02-prompts.md` + block cues from `01-demo-script.md`

## ⭐ Core message (takeaway)

> **"The spec is the executable artifact. Code is the result."**
>
> The Plan agent helps me think in the **moment**, before coding. SpecKit makes sure that intent persists **over time**.

Use this as the throughline: intent captured before coding, then carried through implementation.

## ⏱ Time checkpoints

The authoritative pacing table is at the end of `01-demo-script.md`. The demo runs ~28 min total because the agent runs to completion on `/speckit.implement` (5–8 min for the URL-shortener).

> **Emergency parachute rule (rare):** only pull a branch if the agent has clearly hung (no token stream for several minutes), hits an explicit error after retries, the network drops, or quota is exhausted. Slowness alone is not a reason to switch; while it runs, you narrate.

## 🔗 Links for Wrap-up

- SpecKit: https://github.com/github/spec-kit
- VS Code Plan agent: https://code.visualstudio.com/docs/copilot/agents/planning
- VS Code custom prompt files: https://code.visualstudio.com/docs/copilot/customization/prompt-files
- VS Code custom instructions (AGENTS.md / copilot-instructions.md): https://code.visualstudio.com/docs/copilot/customization/custom-instructions
- Spec-Driven Methodology: https://github.com/github/spec-kit/blob/main/spec-driven.md

## 👥 How this scales to a team

The 25-min demo shows the **single-developer** loop. The same five commands also map naturally to a **multi-feature, multi-developer** workflow — see [`06-team-workflow.md`](06-team-workflow.md) for the full guide. The 30-second version:

```mermaid
flowchart LR
    PM[👤 Product] -->|spec.md| TL[👩‍💻 Tech Lead]
    TL -->|plan.md| Devs[👥 Devs + 🤖 AI]
    Devs -->|tasks → issues → code| PR[💻 Code PR]
    PR --> Main([main])

    style PM fill:#e1f5ff,stroke:#0288d1
    style TL fill:#fff4e1,stroke:#f57c00
    style Devs fill:#f5e1ff,stroke:#7b1fa2
    style PR fill:#e1f5d3,stroke:#388e3c
```

- **One constitution, many feature folders** — each feature lives in `.specify/specs/NNN-name/`, so parallel work has no merge conflicts.
- **Review three times on cheap artifacts**, not once on a 500-line PR. Spec → Plan → Tasks → Code, each a small markdown PR.
- **AI as an async teammate** — `/speckit.taskstoissues` creates GitHub Issues; label one `ai-implement` and Copilot's cloud agent runs `/speckit.implement` on it.

## ⭐ Why each command exists

Quick reference — what you lose if you skip a step:

| Command | Why it exists | What you lose if you skip it |
|---------|---------------|------------------------------|
| `/speckit.constitution` | Persistent team standards across every prompt | Every feature picks its own stack and conventions |
| `/speckit.specify` | Product thinking before architecture | Tech bias creeps in before user needs are clear |
| `/speckit.plan` | Tech decisions reviewed before any code exists | Architectural debate happens *after* 500 lines are written |
| `/speckit.tasks` | Decomposes work into reviewable, parallelizable units | One mega-PR, hand-offs impossible, AI can't claim a slice |
| `/speckit.implement` | Code deterministically derived from approved artifacts | Implementation drifts from intent; no audit trail |

---

**Good luck Tuesday! 🍀**
