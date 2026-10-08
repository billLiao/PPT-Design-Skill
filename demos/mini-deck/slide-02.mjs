// slide-02.mjs — page 2 · layout: S18 · light · 「为什么是现在」
// summary: 3 个论点 + 行业数据
import { pathToFileURL } from "node:url";

export const meta = { page: 2, layout: "S18" };

export function createSlide(pres, theme) {
  const { ink, paper, accent } = theme.colors;
  const { title: fontTitle, body: fontBody, mono: fontMono } = theme.fonts;
  const slide = pres.addSlide();
  slide.background = { color: paper };

  slide.addText("为什么是现在", {
    x: 0.6, y: 0.45, w: 8.8, h: 0.8,
    fontSize: 28, bold: true, color: ink, fontFace: fontTitle, align: "left",
  });

  const rows = [
    ["3 天", "月结对账从关账到出报表的天数，旺季还要顺延"],
    ["40 工时", "每月人工核对发票、订单、入库单的总投入"],
    ["0.5%", "手工录入差错率，旺季单量翻倍时风险敞口最大"],
  ];
  rows.forEach(([num, text], i) => {
    const y = 1.6 + i * 1.15;
    // accent 只做色块标记（文字用 ink——accent 在浅底上对比度不足 3:1）
    slide.addShape(pres.ShapeType.rect, {
      x: 0.6, y: y + 0.28, w: 0.16, h: 0.16,
      fill: { color: accent }, line: { color: accent, width: 0 },
    });
    slide.addText(num, {
      x: 0.95, y, w: 1.85, h: 0.9,
      fontSize: 26, bold: true, color: ink, fontFace: fontMono, align: "left",
    });
    slide.addText(text, {
      x: 2.8, y: y + 0.08, w: 6.6, h: 0.8,
      fontSize: 14, color: ink, fontFace: fontBody, align: "left", valign: "top",
    });
  });
  return slide;
}

/* 单页预览：node slide-02.mjs */
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const { resolveTheme } = await import("./theme-loader.mjs");
  const pptxgen = (await import("pptxgenjs")).default;
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  createSlide(pres, resolveTheme("swiss-orange"));
  await pres.writeFile({ fileName: "preview-02.pptx" });
  console.log("preview -> preview-02.pptx");
}
