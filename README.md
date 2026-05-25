# 📦 SpecKit Demo Package — Overview

> **Everything you need for Tuesday's 25-minute demo.**
> Reading order follows the numbering.

> 💡 **Tip:** All Mermaid diagrams in the docs render in VS Code with **Ctrl+Shift+V** (Markdown preview).

## 🎯 Strategy (Live First with safety net)

- **Live**: `/speckit.specify`, `/speckit.plan`, `/speckit.tasks` run completely live in chat — the audience sees the slash-command flow in action.
- **Live start + cut**: `/speckit.implement` starts live, then after 30 seconds cut to `stage-5-complete` (full implementation takes 5–8 min).
- **Safety net**: Branches `stage-1` through `stage-5` are pre-staged and ready. For timeouts > 90 sec (Block 5a/b) or > 60 sec (Block 5c): `git checkout -f stage-N-...` in < 10 sec.
- **Pre-stage assumption**: Demo starts on `stage-1-after-init` (= `specify init` + `/speckit.constitution` already done). Saves 90 seconds of one-time setup fiddling on stage.

## 📋 Contents

| File / Folder | Purpose | When to read? |
|----------------|-------|-------------|
| `01-demo-script.md` | **Word-for-word speaker script** with block cues, time checkpoints, and fallback lines | Read immediately, then talk through it once |
| `02-prompts.md` | All prompts ready to copy and paste (Plan Mode + 4× SpecKit + setup) | Print it or put it on a second display |
| `03-setup-checklist.md` | 2-phase checklist: Monday evening + 30 min before demo | **Complete by Monday evening at the latest** |
| `04-plan-b/` | Prepared artifacts as a safety net — see below | Use during setup |
| `05-recovery.md` | "What to do if …" — emergency playbook | Skim beforehand, keep handy during the demo |

## 📁 04-plan-b/ — safety net in detail

```
04-plan-b/
├── mini-skeleton/              ← Block 2 (Plan Mode): tiny FastAPI with /hello
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

## ⚡ Quick-start order (for you)

1. **Now** read `01-demo-script.md` → the story lands
2. **Now** skim `05-recovery.md` → the fallbacks are familiar
3. **Monday evening** complete `03-setup-checklist.md` Phase A (approx. 120 min)
   – use `02-prompts.md` as the source for the slash commands
4. **Tuesday, 30 min before demo** `03-setup-checklist.md` Phase B (approx. 30 min)
5. **Demo** — cheat sheet = `02-prompts.md` + block cues from `01-demo-script.md`

## ⭐ Core message (takeaway)

> **"The spec is the executable artifact. Code is the result."**
>
> Plan Mode helps me think in the **moment**, before coding.
> SpecKit makes sure that intent persists **over time**.

Know this sentence cold — it is the throughline of the demo.

## ⏱ Time checkpoints

The authoritative pacing table is at the end of `01-demo-script.md`. Rule of thumb:

> **If you are > 60 sec behind** → use the bailout branch directly for the next slash command instead of waiting for the stream.

## 🔗 Links for Wrap-up

- SpecKit: https://github.com/github/spec-kit
- VS Code Chat Modes: https://code.visualstudio.com/docs/copilot/chat/chat-modes
- Spec-Driven Methodology: https://github.com/github/spec-kit/blob/main/spec-driven.md

---

**Good luck Tuesday! 🍀**
