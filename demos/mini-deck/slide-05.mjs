// slide-05.mjs — page 5 · layout: S10 · dark · 「下一步：先跑 30 天」
// summary: 收束 + 3 项行动请求
import { pathToFileURL } from "node:url";

export const meta = { page: 5, layout: "S10" };

export function createSlide(pres, theme) {
  const { ink, paper, accent, accentLight } = theme.colors;
  const { title: fontTitle, body: fontBody } = theme.fonts;
  const slide = pres.addSlide();
  slide.background = { color: theme.backgroundDark.color };

  // 左：收束
  slide.addText("下一步：先跑 30 天", {
    x: 0.6, y: 1.3, w: 4.6, h: 1.6,
    fontSize: 32, bold: true, color: paper, fontFace: fontTitle, align: "left",
  });
  slide.addText("先在财务部试点，跑通再推全公司", {
    x: 0.6, y: 3.0, w: 4.6, h: 0.8,
    fontSize: 15, color: accentLight, fontFace: fontBody, align: "left",
  });

  // 右：行动块（浅底块保证对比度）
  slide.addShape(pres.ShapeType.rect, {
    x: 5.6, y: 1.1, w: 3.8, h: 3.5,
    fill: { color: paper },
    line: { color: paper, width: 0 },
  });
  slide.addShape(pres.ShapeType.rect, {
    x: 5.6, y: 1.1, w: 3.8, h: 0.12,
    fill: { color: accent },
    line: { color: accent, width: 0 },
  });
  const actions = [
    ["第 1 周", "接入近 6 个月历史账单"],
    ["第 2 周", "AI 预审与人工双跑对照"],
    ["第 4 周", "出效率与差错对比报告"],
  ];
  actions.forEach(([w, text], i) => {
    const y = 1.5 + i * 0.95;
    slide.addText(w, {
      x: 5.85, y, w: 1.1, h: 0.7,
      fontSize: 12, bold: true, color: ink, fontFace: fontBody, align: "left",
    });
    slide.addText(text, {
      x: 7.0, y, w: 2.25, h: 0.9,
      fontSize: 12, color: ink, fontFace: fontBody, align: "left", valign: "top",
    });
  });
  return slide;
}

/* 单页预览：node slide-05.mjs */
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const { resolveTheme } = await import("./theme-loader.mjs");
  const pptxgen = (await import("pptxgenjs")).default;
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  createSlide(pres, resolveTheme("swiss-orange"));
  await pres.writeFile({ fileName: "preview-05.pptx" });
  console.log("preview -> preview-05.pptx");
}
