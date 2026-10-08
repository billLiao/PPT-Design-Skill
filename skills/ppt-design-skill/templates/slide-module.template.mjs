// slide-{{PAGE2}}.mjs — page {{PAGE}} · layout: {{LAYOUT}} · {{VARIANT}} · 「{{TITLE}}」
// summary: {{SUMMARY}}
// 由 scripts/scaffold_deck.py 从 outline.json 生成；只改 createSlide 内部，勿改导出契约。
// 版式代码：templates/layouts/（杂志 magazine-layouts.md / 瑞士 swiss-layouts.md / 分析 analysis-models.md）
// 硬约束：颜色/字体只用 theme token（token_check.py 会查）；正文 ≤90 字；标题 ≤12 字。
import { pathToFileURL } from "node:url";

export const meta = { page: {{PAGE}}, layout: "{{LAYOUT}}" };

export function createSlide(pres, theme) {
  const { ink, paper, paperTint, inkTint, accent, accentRgb } = theme.colors;
  const { title: fontTitle, body: fontBody, mono: fontMono } = theme.fonts;
  const dark = {{VARIANT_JS}}; // variant: {{VARIANT}}
  const bg = dark ? theme.backgroundDark.color : paper;
  const fg = dark ? paper : ink;

  const slide = pres.addSlide();
  slide.background = { color: bg };

  // TODO: 按 {{LAYOUT}} 版式代码填充本页（下方是占位骨架，替换成真实内容）
  slide.addText({{TITLE_JS}}, {
    x: 0.5, y: 0.4, w: 9.0, h: 0.9,
    fontSize: 28, bold: true, color: fg, fontFace: fontTitle, align: "left",
  });
  slide.addText({{SUMMARY_JS}}, {
    x: 0.5, y: 1.5, w: 9.0, h: 3.0,
    fontSize: 14, color: fg, fontFace: fontBody, align: "left", valign: "top",
  });

  return slide;
}

/* 单页预览：node slide-{{PAGE2}}.mjs（--theme 可覆盖，默认 {{THEME}}） */
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const { resolveTheme } = await import("./theme-loader.mjs");
  const pptxgen = (await import("pptxgenjs")).default;
  const i = process.argv.indexOf("--theme");
  const themeArg = i > -1 && process.argv[i + 1] ? process.argv[i + 1] : "{{THEME}}";
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  createSlide(pres, resolveTheme(themeArg));
  await pres.writeFile({ fileName: "preview-{{PAGE2}}.pptx" });
  console.log("preview -> preview-{{PAGE2}}.pptx");
}
