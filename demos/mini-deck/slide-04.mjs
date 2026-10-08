// slide-04.mjs — page 4 · layout: S19 · light · 「四个部门怎么用」
// summary: 财务/采购/销售/仓储各一张卡
import { pathToFileURL } from "node:url";

export const meta = { page: 4, layout: "S19" };

export function createSlide(pres, theme) {
  const { ink, paper, accent, accentLight, grid } = theme.colors;
  const { title: fontTitle, body: fontBody } = theme.fonts;
  const slide = pres.addSlide();
  slide.background = { color: paper };

  slide.addText("四个部门怎么用", {
    x: 0.6, y: 0.45, w: 8.8, h: 0.8,
    fontSize: 28, bold: true, color: ink, fontFace: fontTitle, align: "left",
  });

  const cards = [
    ["财务", "AI 预审对账，差异自动标注", true],
    ["采购", "到货与订单自动匹配", false],
    ["销售", "回款账龄实时预警", false],
    ["仓储", "出入库单据自动核销", false],
  ];
  cards.forEach(([dept, text, hot], i) => {
    const x = 0.6 + i * 2.28;
    slide.addShape(pres.ShapeType.rect, {
      x, y: 1.7, w: 2.08, h: 2.9,
      fill: { color: hot ? accentLight : paper },
      line: { color: hot ? accent : grid, width: hot ? 1.5 : 1 },
    });
    slide.addText(dept, {
      x: x + 0.15, y: 1.95, w: 1.78, h: 0.6,
      fontSize: 16, bold: true, color: ink, fontFace: fontTitle, align: "left",
    });
    slide.addText(text, {
      x: x + 0.15, y: 2.7, w: 1.78, h: 1.6,
      fontSize: 11, color: ink, fontFace: fontBody, align: "left", valign: "top",
    });
  });
  return slide;
}

/* 单页预览：node slide-04.mjs */
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const { resolveTheme } = await import("./theme-loader.mjs");
  const pptxgen = (await import("pptxgenjs")).default;
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  createSlide(pres, resolveTheme("swiss-orange"));
  await pres.writeFile({ fileName: "preview-04.pptx" });
  console.log("preview -> preview-04.pptx");
}
