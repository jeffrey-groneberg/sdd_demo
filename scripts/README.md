# Scripts

Build-time helpers. Currently just one tool: regenerating the PNG diagrams
embedded in the markdown docs from their mermaid source.

## `regen-diagrams.ps1` / `regen-diagrams.mjs`

When you edit a mermaid block in any of the demo docs (e.g.
`01-demo-script.md`), rerun this script to refresh the PNG that ships
alongside it.

### One-time setup

You need Node.js 20+ and either Microsoft Edge or Google Chrome installed
(the script uses them as the headless rendering engine — no extra Chromium
download required).

### Run it

```powershell
pwsh -File scripts/regen-diagrams.ps1
```

Or directly:

```bash
cd scripts
npm install     # first run only
npm run regen-diagrams
```

Output goes to `diagrams/*.png` and `diagrams/*.excalidraw`. The
`.excalidraw` files are editable at <https://excalidraw.com> if you want
finer control than mermaid gives you.

### Adding a new diagram

1. Add a `` ```mermaid ... ``` `` block to one of the docs
2. Append a new `[slug, label]` entry to `DIAGRAMS` in `regen-diagrams.mjs`
3. Rerun the script
4. Embed `![alt](diagrams/<slug>.png)` in the doc where you want it to appear
