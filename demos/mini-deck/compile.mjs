#!/usr/bin/env node
// compile.mjs — assemble slide-NN.mjs modules into one .pptx
// Contract: each module exports createSlide(pres, theme) (sync) + optional meta {page, layout}.
// Usage: node compile.mjs --theme <name-or-path> [--out output.pptx] [--outline outline.json]
// Doc: references/modular-decks.md
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { resolve } from "node:path";
import pptxgen from "pptxgenjs";
import { resolveTheme } from "./theme-loader.mjs";

function arg(name, fallback = null) {
  const i = process.argv.indexOf(`--${name}`);
  return i > -1 && process.argv[i + 1] && !process.argv[i + 1].startsWith("--")
    ? process.argv[i + 1]
    : fallback;
}

const themeArg = arg("theme");
if (!themeArg) {
  console.error(
    "usage: node compile.mjs --theme <name-or-path> [--out output.pptx] [--outline outline.json]",
  );
  process.exit(2);
}
const out = arg("out", "output.pptx");
const outlinePath = arg("outline", existsSync("outline.json") ? "outline.json" : null);

const modules = readdirSync(".").filter((f) => /^slide-\d{2,}\.mjs$/.test(f)).sort();
if (modules.length === 0) {
  console.error("ERROR: no slide-NN.mjs modules found in cwd");
  process.exit(2);
}

if (outlinePath) {
  const outline = JSON.parse(readFileSync(outlinePath, "utf8"));
  const pages = (outline.slides ?? []).length;
  if (pages !== modules.length) {
    console.error(
      `ERROR: outline.json has ${pages} slides but ${modules.length} slide modules found — ` +
        "re-run scaffold_deck.py or fix the files",
    );
    process.exit(1);
  }
}

const theme = resolveTheme(themeArg);
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";

const t0 = Date.now();
for (const [i, file] of modules.entries()) {
  const mod = await import(pathToFileURL(resolve(file)).href);
  if (typeof mod.createSlide !== "function") {
    console.error(`ERROR: ${file} must export createSlide(pres, theme)`);
    process.exit(1);
  }
  mod.createSlide(pres, theme);
  const page = mod.meta?.page;
  if (page != null && page !== i + 1) {
    console.error(`ERROR: ${file} meta.page=${page} but its position is ${i + 1} — rename or fix meta`);
    process.exit(1);
  }
}
await pres.writeFile({ fileName: out });
console.log(`OK ${modules.length} slides -> ${out} (${theme.label}, ${Date.now() - t0}ms)`);
