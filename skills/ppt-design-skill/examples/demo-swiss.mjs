import pptxgen from "pptxgenjs";

// ========================
// 瑞士风示例 - IKB 克莱因蓝主题
// ========================

const theme = {
  colors: {
    ink: "1a1a1a",
    paper: "f5f5f5",
    accent: "002FA7",
    accentLight: "e6ebf7",
    grid: "d0d0d0"
  }
};

const fonts = {
  title: "Arial Black",
  body: "Arial",
  mono: "Consolas"
};

let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "Swiss Style Demo";
pres.author = "PPT Design Skill";

// --- Slide 1: S01 Hero Cover ---
let slide1 = pres.addSlide();
slide1.background = { color: theme.colors.ink };
slide1.addText("SYSTEM DESIGN", {
  x: 0.5, y: 1.5, w: 9, h: 0.3,
  fontSize: 11, color: theme.colors.accent, fontFace: fonts.mono, charSpacing: 4
});
slide1.addText("Architecture\nOverview", {
  x: 0.5, y: 2.0, w: 9, h: 1.2,
  fontSize: 54, color: "FFFFFF", fontFace: fonts.title, bold: true
});
slide1.addText("2026 · Q2 Roadmap", {
  x: 0.5, y: 3.5, w: 9, h: 0.25,
  fontSize: 12, color: "CCCCCC", fontFace: fonts.mono
});

// --- Slide 2: S03 Split Statement ---
let slide2 = pres.addSlide();
slide2.background = { color: theme.colors.paper };
slide2.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 5, h: 5.625,
  fill: { color: theme.colors.accent }
});
slide2.addText("核心\n论点", {
  x: 0.5, y: 1.8, w: 4, h: 1.0,
  fontSize: 42, color: "FFFFFF", fontFace: fonts.title, bold: true
});
slide2.addText("ONE PERSON\n= ONE TEAM", {
  x: 5.5, y: 1.5, w: 4, h: 1.0,
  fontSize: 32, color: theme.colors.ink, fontFace: fonts.title, bold: true
});
slide2.addText("AI 工具链的成熟让个体创作者具备了传统十人团队的生产力。这不是替代，而是能力的重新分配。", {
  x: 5.5, y: 2.7, w: 4, h: 1.5,
  fontSize: 14, color: theme.colors.ink, fontFace: fonts.body
});

// --- Slide 3: S06 KPI Tower ---
let slide3 = pres.addSlide();
slide3.background = { color: theme.colors.paper };
slide3.addText("关键指标", {
  x: 0.5, y: 0.4, w: 9, h: 0.4,
  fontSize: 28, color: theme.colors.ink, fontFace: fonts.title, bold: true
});

const kpis = [
  { label: "代码行数", value: "110K+", h: 3.2, x: 0.5, color: theme.colors.accent },
  { label: "GitHub Stars", value: "5.2K", h: 2.4, x: 2.6, color: "1a1a1a" },
  { label: "下载量", value: "41K+", h: 2.8, x: 4.7, color: theme.colors.accent },
  { label: "AI 平台", value: "19", h: 1.8, x: 6.8, color: "1a1a1a" }
];

kpis.forEach(k => {
  slide3.addShape(pres.shapes.RECTANGLE, {
    x: k.x, y: 5.625 - k.h - 0.8, w: 1.8, h: k.h,
    fill: { color: k.color }
  });
  slide3.addText(k.value, {
    x: k.x, y: 5.625 - k.h - 0.5, w: 1.8, h: 0.5,
    fontSize: 28, color: "FFFFFF", fontFace: fonts.title, bold: true, align: "center"
  });
  slide3.addText(k.label, {
    x: k.x, y: 5.625 - 0.6, w: 1.8, h: 0.3,
    fontSize: 10, color: theme.colors.ink, fontFace: fonts.mono, align: "center"
  });
});

// --- Slide 4: S07 H-Bar Chart ---
let slide4 = pres.addSlide();
slide4.background = { color: theme.colors.paper };
slide4.addText("平台分布", {
  x: 0.5, y: 0.4, w: 9, h: 0.4,
  fontSize: 28, color: theme.colors.ink, fontFace: fonts.title, bold: true
});

const bars = [
  { label: "VS Code", val: 95, x: 0.5 },
  { label: "Cursor", val: 78, x: 0.5 },
  { label: "Windsurf", val: 62, x: 0.5 },
  { label: "Trae", val: 45, x: 0.5 },
  { label: "Zed", val: 30, x: 0.5 }
];

bars.forEach((b, i) => {
  const y = 1.2 + i * 0.85;
  slide4.addText(b.label, {
    x: 0.5, y: y, w: 2.0, h: 0.3,
    fontSize: 12, color: theme.colors.ink, fontFace: fonts.body
  });
  slide4.addShape(pres.shapes.RECTANGLE, {
    x: 2.5, y: y + 0.05, w: b.val * 0.065, h: 0.2,
    fill: { color: theme.colors.accent }
  });
  slide4.addText(b.val + "%", {
    x: 2.5 + b.val * 0.065 + 0.1, y: y, w: 1.0, h: 0.3,
    fontSize: 11, color: theme.colors.ink, fontFace: fonts.mono
  });
});

// --- Slide 5: S08 Duo Compare ---
let slide5 = pres.addSlide();
slide5.background = { color: theme.colors.paper };
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 0, y: 0, w: 5, h: 5.625,
  fill: { color: theme.colors.paper }
});
slide5.addShape(pres.shapes.RECTANGLE, {
  x: 5, y: 0, w: 5, h: 5.625,
  fill: { color: theme.colors.ink }
});
slide5.addText("TRADITIONAL", {
  x: 0.5, y: 0.5, w: 4, h: 0.3,
  fontSize: 11, color: theme.colors.accent, fontFace: fonts.mono, charSpacing: 3
});
slide5.addText("10人\n团队", {
  x: 0.5, y: 1.0, w: 4, h: 0.8,
  fontSize: 36, color: theme.colors.ink, fontFace: fonts.title, bold: true
});
slide5.addText("6个月交付\n多轮评审\n高沟通成本\n协调 overhead", {
  x: 0.5, y: 2.0, w: 4, h: 2.0,
  fontSize: 14, color: theme.colors.ink, fontFace: fonts.body
});
slide5.addText("AI NATIVE", {
  x: 5.5, y: 0.5, w: 4, h: 0.3,
  fontSize: 11, color: theme.colors.accent, fontFace: fonts.mono, charSpacing: 3
});
slide5.addText("1人\n独立", {
  x: 5.5, y: 1.0, w: 4, h: 0.8,
  fontSize: 36, color: "FFFFFF", fontFace: fonts.title, bold: true
});
slide5.addText("2个月交付\n实时迭代\n零会议成本\n全栈掌控", {
  x: 5.5, y: 2.0, w: 4, h: 2.0,
  fontSize: 14, color: "FFFFFF", fontFace: fonts.body
});

// --- Slide 6: S11 Horizontal Timeline ---
let slide6 = pres.addSlide();
slide6.background = { color: theme.colors.paper };
slide6.addText("演进路线", {
  x: 0.5, y: 0.4, w: 9, h: 0.4,
  fontSize: 28, color: theme.colors.ink, fontFace: fonts.title, bold: true
});

const timeline = [
  { step: "2024", title: "起步", desc: "单工具实验", x: 0.5 },
  { step: "2025", title: "整合", desc: "多平台接入", x: 2.6 },
  { step: "2026 Q1", title: "产品化", desc: "开源发布", x: 4.7 },
  { step: "2026 Q2", title: "规模化", desc: "社区增长", x: 6.8 },
  { step: "2026 Q3", title: "生态", desc: "插件市场", x: 8.9 }
];

// Timeline axis
slide6.addShape(pres.shapes.LINE, {
  x: 0.5, y: 3.0, w: 9, h: 0,
  line: { color: theme.colors.grid, width: 2 }
});

timeline.forEach(t => {
  slide6.addShape(pres.shapes.OVAL, {
    x: t.x + 0.6, y: 2.85, w: 0.3, h: 0.3,
    fill: { color: theme.colors.accent }
  });
  slide6.addText(t.step, {
    x: t.x, y: 1.5, w: 1.5, h: 0.25,
    fontSize: 11, color: theme.colors.accent, fontFace: fonts.mono, align: "center"
  });
  slide6.addText(t.title, {
    x: t.x, y: 1.8, w: 1.5, h: 0.3,
    fontSize: 14, color: theme.colors.ink, fontFace: fonts.body, bold: true, align: "center"
  });
  slide6.addText(t.desc, {
    x: t.x, y: 3.4, w: 1.5, h: 0.4,
    fontSize: 10, color: theme.colors.ink, fontFace: fonts.body, align: "center"
  });
});

// --- Slide 7: S15 Matrix + Hero Stat ---
let slide7 = pres.addSlide();
slide7.background = { color: theme.colors.paper };
slide7.addText("能力矩阵", {
  x: 0.5, y: 0.4, w: 9, h: 0.4,
  fontSize: 28, color: theme.colors.ink, fontFace: fonts.title, bold: true
});

// Matrix grid
const matrixItems = [
  { text: "代码生成", x: 0.5, y: 1.2 },
  { text: "UI 设计", x: 2.6, y: 1.2 },
  { text: "文档写作", x: 4.7, y: 1.2 },
  { text: "数据分析", x: 6.8, y: 1.2 },
  { text: "测试覆盖", x: 0.5, y: 2.4 },
  { text: "部署运维", x: 2.6, y: 2.4 },
  { text: "用户研究", x: 4.7, y: 2.4 },
  { text: "产品规划", x: 6.8, y: 2.4 }
];

matrixItems.forEach(m => {
  slide7.addShape(pres.shapes.RECTANGLE, {
    x: m.x, y: m.y, w: 1.8, h: 0.9,
    fill: { color: theme.colors.accentLight }
  });
  slide7.addText(m.text, {
    x: m.x, y: m.y + 0.25, w: 1.8, h: 0.4,
    fontSize: 12, color: theme.colors.ink, fontFace: fonts.body, align: "center"
  });
});

// Hero stat
slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.6, w: 9, h: 1.5,
  fill: { color: theme.colors.accent }
});
slide7.addText("8 项核心能力 · 1 人全栈覆盖", {
  x: 0.5, y: 4.0, w: 9, h: 0.5,
  fontSize: 24, color: "FFFFFF", fontFace: fonts.title, bold: true, align: "center"
});

// --- Slide 8: S21 Closing ---
let slide8 = pres.addSlide();
slide8.background = { color: theme.colors.ink };
slide8.addText("THANK YOU", {
  x: 0.5, y: 1.8, w: 9, h: 1.0,
  fontSize: 56, color: "FFFFFF", fontFace: fonts.title, bold: true, align: "center"
});
slide8.addText("PPT Design Skill · 2026", {
  x: 0.5, y: 3.0, w: 9, h: 0.25,
  fontSize: 12, color: theme.colors.accent, fontFace: fonts.mono, align: "center"
});

pres.writeFile({ fileName: "demo-swiss.pptx" });
console.log("Generated: demo-swiss.pptx");
