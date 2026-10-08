// slide-01.mjs — page 1 · layout: S01 · dark · 「供应链 AI 落地复盘」
// summary: 开场：一句话定位 + 汇报人
import { pathToFileURL } from "node:url";

export const meta = { page: 1, layout: "S01" };

export function createSlide(pres, theme) {
  const { paper, accent, accentLight, grid } = theme.colors;
  const { title: fontTitle, mono: fontMono } = theme.fonts;
  const slide = pres.addSlide();
  slide.background = { color: theme.backgroundDark.color };

  // 左：大编号
  slide.addText("01", {
    x: 0.6, y: 1.1, w: 2.4, h: 2.4,
    fontSize: 110, bold: true, color: accent, fontFace: fontMono, align: "left",
  });
  // 右：标题 + 副题
  slide.addText("供应链 AI 落地复盘", {
    x: 3.4, y: 1.7, w: 6.0, h: 1.1,
    fontSize: 40, bold: true, color: paper, fontFace: fontTitle, align: "left",
  });
  slide.addText("从财务部试点到全公司推广的 90 天", {
    x: 3.4, y: 2.9, w: 6.0, h: 0.6,
    fontSize: 16, color: accentLight, fontFace: fontTitle, align: "left",
  });
  // 底部 kicker
  slide.addText("2026 · 内部复盘 · 示例数据", {
    x: 3.4, y: 4.9, w: 6.0, h: 0.4,
    fontSize: 11, color: grid, fontFace: fontTitle, align: "left",
  });
  return slide;
}

/* 单页预览：node slide-01.mjs */
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const { resolveTheme } = await import("./theme-loader.mjs");
  const pptxgen = (await import("pptxgenjs")).default;
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  createSlide(pres, resolveTheme("swiss-orange"));
  await pres.writeFile({ fileName: "preview-01.pptx" });
  console.log("preview -> preview-01.pptx");
}
