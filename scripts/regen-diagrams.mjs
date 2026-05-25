// Regenerate excalidraw PNGs from the mermaid blocks inside the markdown docs.
//
// Reads mermaid code-fence blocks (including those nested inside `> ` quoted
// blockquotes and `<details>` blocks) from the markdown files listed in
// DIAGRAMS, converts each one to an excalidraw scene via
// @excalidraw/mermaid-to-excalidraw, then exports a PNG via @excalidraw/excalidraw.
//
// Output: docs/diagrams/<slug>.png + <slug>.excalidraw
//
// Prerequisites:
//   - Node.js 20+
//   - Microsoft Edge OR Google Chrome installed (used as the headless browser)
//   - `npm install puppeteer-core` (see scripts/package.json)
//
// Run:
//   pwsh -File scripts/regen-diagrams.ps1     (Windows)
//   node scripts/regen-diagrams.mjs            (any OS, after npm install)

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import puppeteer from "puppeteer-core";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, "..");
const DOCS = REPO_ROOT;
const OUT = path.join(DOCS, "diagrams");
fs.mkdirSync(OUT, { recursive: true });

// Mapping: (markdown file relative to repo root) -> ordered list of [slug, label]
// for each mermaid block in that file. The order must match the order the
// mermaid blocks appear in the source. Update this if you add/remove blocks.
const DIAGRAMS = {
  "01-demo-script.md": [
    ["01-timeline", "25-min demo timeline"],
    ["02-sdd-pipeline", "SDD pipeline"],
    ["03-live-decision-flow", "Live decision flow"],
  ],
  "03-setup-checklist.md": [
    ["04-branch-chain", "Branch chain stage-1..stage-5"],
  ],
  "05-recovery.md": [["05-recovery-tree", "Emergency decision tree"]],
};

function findBrowser() {
  if (process.env.PUPPETEER_EXECUTABLE_PATH) {
    return process.env.PUPPETEER_EXECUTABLE_PATH;
  }
  const candidates =
    os.platform() === "win32"
      ? [
          "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
          "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
          "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
          "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        ]
      : os.platform() === "darwin"
        ? [
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
          ]
        : ["/usr/bin/microsoft-edge", "/usr/bin/google-chrome", "/usr/bin/chromium"];
  for (const c of candidates) if (fs.existsSync(c)) return c;
  throw new Error(
    "No Chromium-based browser found. Install Edge or Chrome, or set PUPPETEER_EXECUTABLE_PATH.",
  );
}

function extractMermaidBlocks(mdPath) {
  const content = fs.readFileSync(mdPath, "utf-8");
  const lines = content.split(/\r?\n/);
  const blocks = [];
  let inBlock = false;
  let buf = [];
  let isQuoted = false;
  for (const line of lines) {
    if (!inBlock) {
      const m = line.match(/^(\s*>?\s*)```mermaid\s*$/);
      if (m) {
        inBlock = true;
        buf = [];
        isQuoted = /^\s*>/.test(line);
      }
    } else {
      if (/^\s*>?\s*```\s*$/.test(line)) {
        inBlock = false;
        const cleaned = isQuoted ? buf.map((l) => l.replace(/^\s*>\s?/, "")) : buf;
        blocks.push(cleaned.join("\n"));
      } else {
        buf.push(line);
      }
    }
  }
  return blocks;
}

const browserExe = findBrowser();
console.log("Using browser:", browserExe);
const PAGE_URL =
  "file:///" + path.join(__dirname, "regen-diagrams-page.html").replace(/\\/g, "/");

const browser = await puppeteer.launch({
  executablePath: browserExe,
  headless: "new",
  args: ["--no-sandbox", "--disable-web-security"],
});

const page = await browser.newPage();
page.on("console", (m) => console.log("[page]", m.type(), m.text()));
page.on("pageerror", (e) => console.log("[page error]", e.message));

await page.goto(PAGE_URL, { waitUntil: "networkidle2", timeout: 60000 });
await page.waitForFunction("window.__convertReady === true", { timeout: 60000 });
console.log("Page ready.");

const results = [];

for (const [mdName, slots] of Object.entries(DIAGRAMS)) {
  const mdPath = path.join(DOCS, mdName);
  if (!fs.existsSync(mdPath)) {
    console.error(`! ${mdName}: file missing at ${mdPath}`);
    continue;
  }
  const blocks = extractMermaidBlocks(mdPath);
  if (blocks.length !== slots.length) {
    console.error(
      `! ${mdName}: expected ${slots.length} mermaid blocks, found ${blocks.length}`,
    );
    continue;
  }
  for (let i = 0; i < blocks.length; i++) {
    const [slug, label] = slots[i];
    const mermaid = blocks[i];
    process.stdout.write(`Converting ${slug} ... `);
    try {
      const r = await page.evaluate(
        async (text, opts) => await window.convertOne(text, opts),
        mermaid,
        { scale: 2, padding: 28, bg: "#ffffff" },
      );
      if (!r || !r.ok) throw new Error("convertOne returned no ok");
      const pngPath = path.join(OUT, `${slug}.png`);
      const excPath = path.join(OUT, `${slug}.excalidraw`);
      fs.writeFileSync(pngPath, Buffer.from(r.base64png, "base64"));
      fs.writeFileSync(excPath, JSON.stringify(r.excalidraw, null, 2));
      const sz = fs.statSync(pngPath).size;
      console.log(`OK (${sz} bytes)`);
      results.push({ slug, label, mdName, blockIndex: i, ok: true, size: sz });
    } catch (e) {
      console.log(`FAIL: ${e.message}`);
      results.push({
        slug,
        label,
        mdName,
        blockIndex: i,
        ok: false,
        error: e.message,
      });
    }
  }
}

await browser.close();

console.log("\n=== Summary ===");
for (const r of results) {
  console.log(
    `${r.ok ? "OK  " : "FAIL"}  ${r.slug.padEnd(28)}  ${r.mdName}  ${r.ok ? r.size + "B" : r.error}`,
  );
}
process.exit(results.every((r) => r.ok) ? 0 : 1);
