import pptxgen from "pptxgenjs";

// ========================
// 杂志风示例 - 墨水经典主题
// ========================

const theme = {
  colors: {
    ink: "0a0a0b",
    paper: "f1efea",
    paperTint: "e8e5de",
    inkTint: "18181a",
    accent: "d4a574"
  }
};

const fonts = {
  title: "Georgia",
  body: "Calibri",
  mono: "Consolas"
};

let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "Magazine Style Demo";
pres.author = "PPT Design Skill";

// --- Slide 1: Cover ---
let slide1 = pres.addSlide();
slide1.background = { color: theme.colors.ink };
slide1.addText("A Talk · 2026.05", {
  x: 0.5, y: 1.8, w: 9, h: 0.3,
  fontSize: 12, color: theme.colors.accent, fontFace: fonts.mono
});
slide1.addText("一人公司", {
  x: 0.5, y: 2.2, w: 9, h: 1.0,
  fontSize: 48, color: theme.colors.paper, fontFace: fonts.title, bold: true
});
slide1.addText("被 AI 折叠的组织", {
  x: 0.5, y: 3.3, w: 9, h: 0.5,
  fontSize: 22, color: theme.colors.paper, fontFace: fonts.body
});
slide1.addText("歸藏 · 独立创作者", {
  x: 0.5, y: 4.5, w: 9, h: 0.3,
  fontSize: 12, color: theme.colors.paper, fontFace: fonts.mono
});

// --- Slide 2: Section Divider ---
let slide2 = pres.addSlide();
slide2.background = { color: theme.colors.paper };
slide2.addText("ACT I", {
  x: 0.5, y: 1.8, w: 9, h: 0.3,
  fontSize: 12, color: theme.colors.accent, fontFace: fonts.mono
});
slide2.addText("硬数据", {
  x: 0.5, y: 2.2, w: 9, h: 0.9,
  fontSize: 44, color: theme.colors.ink, fontFace: fonts.title, bold: true
});
slide2.addText("先看数字，再谈方法。", {
  x: 0.5, y: 3.2, w: 7, h: 0.4,
  fontSize: 16, color: theme.colors.ink, fontFace: fonts.body
});

// --- Slide 3: Big Numbers ---
let slide3 = pres.addSlide();
slide3.background = { color: theme.colors.paper };
slide3.addText("过去 64 天", {
  x: 0.5, y: 0.4, w: 9, h: 0.5,
  fontSize: 32, color: theme.colors.ink, fontFace: fonts.title, bold: true
});

const stats = [
  { label: "Duration", value: "64", unit: "天", note: "从 0 到现在", x: 0.5 },
  { label: "Lines of Code", value: "110K+", unit: "", note: "一行行写到 11 万+", x: 3.4 },
  { label: "GitHub Stars", value: "5,166", unit: "", note: "一个开源仓库", x: 6.3 }
];

stats.forEach(s => {
  slide3.addShape(pres.shapes.RECTANGLE, {
    x: s.x, y: 1.2, w: 2.8, h: 1.6,
    fill: { color: theme.colors.paperTint }
  });
  slide3.addText(s.label, {
    x: s.x + 0.15, y: 1.3, w: 2.5, h: 0.25,
    fontSize: 10, color: theme.colors.ink, fontFace: fonts.mono
  });
  slide3.addText(s.value, {
    x: s.x + 0.15, y: 1.6, w: 2.5, h: 0.5,
    fontSize: 36, color: theme.colors.ink, fontFace: fonts.title, bold: true
  });
  slide3.addText(s.note, {
    x: s.x + 0.15, y: 2.15, w: 2.5, h: 0.3,
    fontSize: 10, color: theme.colors.ink, fontFace: fonts.body
  });
});

// Row 2
const stats2 = [
  { label: "Downloads", value: "41K+", note: "装到了几万台电脑里", x: 0.5 },
  { label: "AI Providers", value: "19", note: "跨平台接入", x: 3.4 },
  { label: "Commits", value: "608+", note: "没有协作者", x: 6.3 }
];

stats2.forEach(s => {
  slide3.addShape(pres.shapes.RECTANGLE, {
    x: s.x, y: 3.0, w: 2.8, h: 1.6,
    fill: { color: theme.colors.paperTint }
  });
  slide3.addText(s.label, {
    x: s.x + 0.15, y: 3.1, w: 2.5, h: 0.25,
    fontSize: 10, color: theme.colors.ink, fontFace: fonts.mono
  });
  slide3.addText(s.value, {
    x: s.x + 0.15, y: 3.4, w: 2.5, h: 0.5,
    fontSize: 36, color: theme.colors.ink, fontFace: fonts.title, bold: true
  });
  slide3.addText(s.note, {
    x: s.x + 0.15, y: 3.95, w: 2.5, h: 0.3,
    fontSize: 10, color: theme.colors.ink, fontFace: fonts.body
  });
});

// --- Slide 4: Two Column ---
let slide4 = pres.addSlide();
slide4.background = { color: theme.colors.paper };
slide4.addText("BUT", {
  x: 0.5, y: 0.8, w: 5.3, h: 0.25,
  fontSize: 11, color: theme.colors.accent, fontFace: fonts.mono
});
slide4.addText("我不是程序员。", {
  x: 0.5, y: 1.1, w: 5.3, h: 0.7,
  fontSize: 32, color: theme.colors.ink, fontFace: fonts.title, bold: true
});
slide4.addText("大学毕业之后再也没写过一行代码。过去十年做的是 UI 设计和 AI 特效。", {
  x: 0.5, y: 1.9, w: 5.3, h: 1.2,
  fontSize: 14, color: theme.colors.ink, fontFace: fonts.body
});
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.2, w: 5.3, h: 1.5,
  fill: { color: theme.colors.paperTint }
});
slide4.addText("\"这东西在三年前，需要一个十人团队做一年。\"", {
  x: 0.7, y: 3.35, w: 4.9, h: 0.8,
  fontSize: 14, color: theme.colors.ink, fontFace: fonts.body, italic: true
});
slide4.addText("— 一个观察者的判断", {
  x: 0.7, y: 4.2, w: 4.9, h: 0.25,
  fontSize: 10, color: theme.colors.accent, fontFace: fonts.mono
});

// Right column placeholder
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 6.0, y: 1.0, w: 3.5, h: 3.5,
  fill: { color: theme.colors.inkTint }
});
slide4.addText("[图片占位]", {
  x: 6.0, y: 2.5, w: 3.5, h: 0.5,
  fontSize: 14, color: theme.colors.paper, fontFace: fonts.body, align: "center"
});

// --- Slide 5: Quote ---
let slide5 = pres.addSlide();
slide5.background = { color: theme.colors.inkTint };
slide5.addText("\"AI 不会取代你，但会用 AI 的人会。\"", {
  x: 1.0, y: 1.8, w: 8, h: 1.2,
  fontSize: 32, color: theme.colors.paper, fontFace: fonts.title, italic: true
});
slide5.addText("— 歸藏", {
  x: 1.0, y: 3.2, w: 8, h: 0.25,
  fontSize: 12, color: theme.colors.accent, fontFace: fonts.mono
});

// --- Slide 6: Pipeline ---
let slide6 = pres.addSlide();
slide6.background = { color: theme.colors.paper };
slide6.addText("Pipeline · 流水线", {
  x: 0.5, y: 0.4, w: 9, h: 0.3,
  fontSize: 11, color: theme.colors.accent, fontFace: fonts.mono
});
slide6.addText("两条流水线", {
  x: 0.5, y: 0.7, w: 9, h: 0.5,
  fontSize: 28, color: theme.colors.ink, fontFace: fonts.title, bold: true
});

const steps = [
  { nb: "01", title: "需求澄清", desc: "7问对齐", x: 0.5 },
  { nb: "02", title: "内容生产", desc: "AI 辅助写作", x: 2.9 },
  { nb: "03", title: "视觉设计", desc: "模板套用", x: 5.3 },
  { nb: "04", title: "交付迭代", desc: "反馈修正", x: 7.7 }
];

steps.forEach(s => {
  slide6.addShape(pres.shapes.RECTANGLE, {
    x: s.x, y: 1.5, w: 2.1, h: 2.8,
    fill: { color: theme.colors.paperTint }
  });
  slide6.addText(s.nb, {
    x: s.x + 0.15, y: 1.65, w: 1.8, h: 0.45,
    fontSize: 32, color: theme.colors.accent, fontFace: fonts.title
  });
  slide6.addText(s.title, {
    x: s.x + 0.15, y: 2.2, w: 1.8, h: 0.3,
    fontSize: 14, color: theme.colors.ink, fontFace: fonts.body, bold: true
  });
  slide6.addText(s.desc, {
    x: s.x + 0.15, y: 2.55, w: 1.8, h: 0.4,
    fontSize: 11, color: theme.colors.ink, fontFace: fonts.body
  });
});

// --- Slide 7: Before/After ---
let slide7 = pres.addSlide();
slide7.background = { color: theme.colors.paper };
slide7.addText("BEFORE", {
  x: 0.7, y: 0.6, w: 4.0, h: 0.25,
  fontSize: 10, color: theme.colors.accent, fontFace: fonts.mono
});
slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 0.9, w: 4.4, h: 3.8,
  fill: { color: theme.colors.paperTint }
});
slide7.addText("传统工作流\n\n• 10人团队\n• 6个月周期\n• 多轮评审\n• 高沟通成本", {
  x: 0.7, y: 1.1, w: 4.0, h: 3.0,
  fontSize: 14, color: theme.colors.ink, fontFace: fonts.body
});

slide7.addText("AFTER", {
  x: 5.3, y: 0.6, w: 4.0, h: 0.25,
  fontSize: 10, color: theme.colors.accent, fontFace: fonts.mono
});
slide7.addShape(pres.shapes.RECTANGLE, {
  x: 5.1, y: 0.9, w: 4.4, h: 3.8,
  fill: { color: "e8dfd0" }
});
slide7.addText("AI 工作流\n\n• 1人独立完成\n• 2个月交付\n• 实时迭代\n• 零会议成本", {
  x: 5.3, y: 1.1, w: 4.0, h: 3.0,
  fontSize: 14, color: theme.colors.ink, fontFace: fonts.body
});

// --- Slide 8: Closing ---
let slide8 = pres.addSlide();
slide8.background = { color: theme.colors.ink };
slide8.addText("谢谢", {
  x: 0.5, y: 2.0, w: 9, h: 1.0,
  fontSize: 48, color: theme.colors.paper, fontFace: fonts.title, bold: true, align: "center"
});
slide8.addText("歸藏 · guizang.dev", {
  x: 0.5, y: 3.2, w: 9, h: 0.3,
  fontSize: 12, color: theme.colors.accent, fontFace: fonts.mono, align: "center"
});

pres.writeFile({ fileName: "demo-magazine.pptx" });
console.log("Generated: demo-magazine.pptx");
