# Mini FastAPI Skeleton — last-ditch fallback for Block 2

> **Default Block 2 flow does NOT use this folder.** Block 2 normally creates an empty `plan-mode-demo/` live on stage and lets the Plan agent bootstrap from zero — that's the more honest, more pedagogically valuable version.
>
> This skeleton exists **only** as a worst-case fallback: if Copilot is completely down and the Plan agent produces nothing at all, copy these files into a folder, open in VS Code, and *talk through* what the Plan agent *would* have produced — using `plan-agent-output.png` (the screenshot you captured in Phase A4) as visual aid.

## Tiny FastAPI app with one endpoint

A `/hello` endpoint that returns `{"message": "Hello"}`. Nothing else.

## Fallback setup (only if needed during the demo)

```bash
mkdir plan-mode-demo
cd plan-mode-demo
# Copy main.py + requirements.txt from this folder
uv venv
.venv\Scripts\activate    # Windows
uv pip install -r requirements.txt
uv run uvicorn main:app --reload
# → http://localhost:8000/hello
```

## Why so small?

So that even in the worst case, the speaker can show a credibly minimal starting point and the audience still grasps the Plan agent concept in ~60 seconds of narration over the prepared screenshot.

