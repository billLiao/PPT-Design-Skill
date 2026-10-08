// theme-loader.mjs — resolve + normalize a theme JSON for slide modules & compile.mjs
// Search order: explicit path → $PPT_THEMES → ./ppt-themes/ → ~/.ppt-design-skill/themes/ → ./themes/
// Contract doc: references/modular-decks.md
import { existsSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
import { isAbsolute, join, resolve } from "node:path";

const DEFAULTS = {
  colors: {
    ink: "1a1a1a", paper: "f5f5f5", paperTint: "ececec", inkTint: "242424",
    accent: "0966ff", accentRgb: "9,102,255",
  },
  fonts: { title: "Arial", body: "Arial", mono: "Consolas" },
  background: { color: "f5f5f5" },
  backgroundDark: { color: "1a1a1a" },
};

export function normalizeTheme(raw) {
  const t = { ...raw };
  t.colors = { ...DEFAULTS.colors, ...(raw.colors ?? {}) };
  t.fonts = { ...DEFAULTS.fonts, ...(raw.fonts ?? {}) };
  t.background = { ...DEFAULTS.background, ...(raw.background ?? {}) };
  t.backgroundDark = { ...DEFAULTS.backgroundDark, ...(raw.backgroundDark ?? {}) };
  t.label = raw.label ?? raw.name ?? "theme";
  return t;
}

export function resolveTheme(nameOrPath) {
  const candidates = [];
  if (isAbsolute(nameOrPath) || nameOrPath.endsWith(".json")) {
    candidates.push(resolve(nameOrPath));
  } else {
    const dirs = [];
    if (process.env.PPT_THEMES) dirs.push(process.env.PPT_THEMES);
    dirs.push(
      join(process.cwd(), "ppt-themes"),
      join(homedir(), ".ppt-design-skill", "themes"),
      join(process.cwd(), "themes"),
    );
    for (const d of dirs) candidates.push(join(d, `${nameOrPath}.theme.json`));
  }
  const hit = candidates.find((p) => existsSync(p));
  if (!hit) {
    throw new Error(
      `theme "${nameOrPath}" not found — searched:\n  ${candidates.join("\n  ")}` +
        `\nhint: pass a full path to <skill>/themes/<name>.theme.json`,
    );
  }
  return normalizeTheme(JSON.parse(readFileSync(hit, "utf8")));
}
