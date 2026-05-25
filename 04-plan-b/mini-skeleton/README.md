# Mini FastAPI Skeleton — for Plan Mode demo (Block 2)

Tiny FastAPI project that **intentionally has only one endpoint**. Plan Mode should plan adding `/health` + test against this.

## Setup

```bash
cd plan-mode-demo
uv venv
.venv\Scripts\activate    # Windows
uv pip install -r requirements.txt
uv run uvicorn main:app --reload
# → http://localhost:8000/hello
```

## Usage in the demo

1. VS Code opens the project (`$HOME\demos\plan-mode-demo`)
2. Copilot Chat → choose **Plan** mode in the dropdown
3. Paste prompt from `02-prompts.md` §1 (in the session files folder)
4. Plan comes back, **no** code is written (that is exactly the point)

## Why so small?

So Plan Mode delivers a complete plan in 60–90 sec and the audience can **fully grasp** the plan. Larger tasks here would be risky for the 25-minute demo.
