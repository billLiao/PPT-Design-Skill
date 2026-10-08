// slide-03.mjs — page 3 · layout: S07 · dark · 「对账效率对比」
// summary: 上线前后 5 项指标排名条形图
import { pathToFileURL } from "node:url";

export const meta = { page: 3, layout: "S07" };

export function createSlide(pres, theme) {
  const { ink, paper, accent, grid } = theme.colors;
  const { title: fontTitle, body: fontBody } = theme.fonts;
  const dark = true; // variant: dark —— 数据页深底（design-playbook 明暗节奏）
  const bg = dark ? theme.backgroundDark.color : paper;
  const fg = dark ? paper : ink;

  const slide = pres.addSlide();
  slide.background = { color: bg };

  slide.addText("对账效率对比", {
    x: 0.6, y: 0.45, w: 8.8, h: 0.8,
    fontSize: 28, bold: true, color: fg, fontFace: fontTitle, align: "left",
  });

  slide.addChart(
    pres.ChartType.bar,
    [
      {
        name: "人工耗时（分钟）",
        labels: ["归档", "出报告", "核发票", "对订单", "找差异"],
        values: [20, 30, 40, 55, 65],
      },
    ],
    {
      x: 0.6, y: 1.45, w: 8.8, h: 3.4,
      barDir: "bar",
      chartColors: [accent],
      barGapWidthPct: 60,
      showValue: true,
      dataLabelColor: fg,
      dataLabelFontSize: 10,
      dataLabelFontFace: fontBody,
      catAxisLabelColor: fg,
      catAxisLabelFontSize: 11,
      catAxisLabelFontFace: fontBody,
      valAxisHidden: true,
      valGridLine: { style: "none" },
      showLegend: false,
      showTitle: false,
    },
  );

  slide.addText("上线 AI 预审前各环节平均耗时（分钟，示例数据）", {
    x: 0.6, y: 5.0, w: 8.8, h: 0.4,
    fontSize: 10, color: grid, fontFace: fontBody, align: "left",
  });
  return slide;
}

/* 单页预览：node slide-03.mjs */
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const { resolveTheme } = await import("./theme-loader.mjs");
  const pptxgen = (await import("pptxgenjs")).default;
  const pres = new pptxgen();
  pres.layout = "LAYOUT_16x9";
  createSlide(pres, resolveTheme("swiss-orange"));
  await pres.writeFile({ fileName: "preview-03.pptx" });
  console.log("preview -> preview-03.pptx");
}
