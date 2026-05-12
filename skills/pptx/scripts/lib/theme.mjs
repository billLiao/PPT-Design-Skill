import fs from "node:fs/promises";
import path from "node:path";

export async function loadTheme(themeName, skillRoot) {
  const themesPath = path.resolve(skillRoot, "assets", "themes.json");
  const allThemes = JSON.parse(await fs.readFile(themesPath, "utf8"));
  const theme = allThemes[themeName];
  if (!theme) {
    const names = Object.keys(allThemes).sort().join(", ");
    throw new Error(`unknown theme: ${themeName}. available: ${names}`);
  }
  return { name: themeName, ...theme };
}
