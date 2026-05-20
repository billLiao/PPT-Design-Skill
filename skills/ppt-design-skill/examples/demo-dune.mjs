import pptxgen from "pptxgenjs";

// ========================
// 沙丘主题示例 - Dune Theme
// ========================
// 调性: 炭灰 + 沙色，克制、高级、中性
// 适合: 艺术/设计/创意/时尚分享、画廊手册、审美优先的私享会

const theme = {
  colors: {
    ink: "1f1a14",        // 炭灰 - 主文字 / dark背景
    paper: "f0e6d2",      // 沙色 - 主背景 / light底色
    paperTint: "e3d7bf",  // 沙色暗调 - 卡片/区块底色
    inkTint: "2d2620",    // 炭灰亮调 - 深色变体
    accent: "c4a265",     // 暖沙金 - 强调色
    accentRgb: "196,162,101"
  }
};

const fonts = {
  title: "Georgia",
  body: "Calibri",
  mono: "Consolas"
};

let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "Dune Theme Demo";
pres.author = "PPT Design Skill";

// --- Slide 1: Cover ---
let slide1 = pres.addSlide();
slide1.background = { color: theme.colors.ink };
slide1.addText("DESIGN GALLERY · 2026", {
  x: 0.5, y: 1.6, w: 9, h: 0.3,
  fontSize: 11, color: theme.colors.accent, fontFace: fonts.mono, charSpacing: 3
});
slide1.addText("沙丘", {
  x: 0.5, y: 2.0, w: 9, h: 1.0,
  fontSize: 56, color: theme.colors.paper, fontFace: fonts.title, bold: true
});
slide1.addText("一场关于空间、光影与材质的对话", {
  x: 0.5, y: 3.1, w: 9, h: 0.4,
  fontSize: 18, color: theme.colors.paper, fontFace: fonts.body
});
slide1.addText("Vol.03 · 夏", {
  x: 0.5, y: 4.3, w: 9, h: 0.25,
  fontSize: 11, color: theme.colors.accent, fontFace: fonts.mono
});

// --- Slide 2: Section Divider ---
let slide2 = pres.addSlide();
slide2.background = { color: theme.colors.paper };
slide2.addText("CHAPTER I", {
  x: 0.5, y: 1.8, w: 9, h: 0.25,
  fontSize: 10, color: theme.colors.accent, fontFace: fonts.mono, charSpacing: 4
});
slide2.addText("空间叙事", {
  x: 0.5, y: 2.15, w: 9, h: 0.8,
  fontSize: 44, color: theme.colors.ink, fontFace: fonts.title, bold: true
});
slide2.addText("建筑是凝固的音乐，空间是流动的诗。", {
  x: 0.5, y: 3.1, w: 7, h: 0.4,
  fontSize: 16, color: theme.colors.ink, fontFace: fonts.body, italic: true
});

// --- Slide 3: Big Numbers ---
let slide3 = pres.addSlide();
slide3.background = { color: theme.colors.paper };
slide3.addText("展览数据", {
  x: 0.5, y: 0.4, w: 9, h: 0.5,
  fontSize: 32, color: theme.colors.ink, fontFace: fonts.title, bold: true
});

const stats = [
  { label: "参展艺术家", value: "47", note: "来自 12 个国家", x: 0.5 },
  { label: "作品数量", value: "186", note: "跨越 3 个世纪", x: 3.4 },
  { label: "展厅面积", value: "2,400", unit: "m²", note: "主馆 + 副馆", x: 6.3 }
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
  slide3.addText(s.value + (s.unit ? " " + s.unit : ""), {
    x: s.x + 0.15, y: 1.6, w: 2.5, h: 0.5,
    fontSize: 36, color: theme.colors.ink, fontFace: fonts.title, bold: true
  });
  slide3.addText(s.note, {
    x: s.x + 0.15, y: 2.15, w: 2.5, h: 0.3,
    fontSize: 10, color: theme.colors.ink, fontFace: fonts.body
  });
});

const stats2 = [
  { label: "观展人次", value: "12.8K", note: "开幕首周", x: 0.5 },
  { label: "媒体曝光", value: "86", unit: "篇", note: "国际艺术媒体", x: 3.4 },
  { label: "收藏意向", value: "34", unit: "件", note: "画廊洽谈中", x: 6.3 }
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
  slide3.addText(s.value + (s.unit ? " " + s.unit : ""), {
    x: s.x + 0.15, y: 3.4, w: 2.5, h: 0.5,
    fontSize: 36, color: theme.colors.ink, fontFace: fonts.title, bold: true
  });
  slide3.addText(s.note, {
    x: s.x + 0.15, y: 3.95, w: 2.5, h: 0.3,
    fontSize: 10, color: theme.colors.ink, fontFace: fonts.body
  });
});

// --- Slide 4: Two Column (Text + Image Placeholder) ---
let slide4 = pres.addSlide();
slide4.background = { color: theme.colors.paper };
slide4.addText("MATERIAL", {
  x: 0.5, y: 0.7, w: 5.3, h: 0.2,
  fontSize: 10, color: theme.colors.accent, fontFace: fonts.mono, charSpacing: 3
});
slide4.addText("材质即语言", {
  x: 0.5, y: 1.0, w: 5.3, h: 0.7,
  fontSize: 32, color: theme.colors.ink, fontFace: fonts.title, bold: true
});
slide4.addText("混凝土的粗粝、原木的温度、金属的冷峻——每一种材质都在诉说一种态度。我们不追求完美的表面，而是让材料本身成为表达的主体。", {
  x: 0.5, y: 1.8, w: 5.3, h: 1.5,
  fontSize: 14, color: theme.colors.ink, fontFace: fonts.body
});
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 3.4, w: 5.3, h: 1.3,
  fill: { color: theme.colors.paperTint }
});
slide4.addText("\"好的设计不是让材料服从于形式，而是让形式服从于材料。\"", {
  x: 0.7, y: 3.55, w: 4.9, h: 0.7,
  fontSize: 13, color: theme.colors.ink, fontFace: fonts.body, italic: true
});
slide4.addText("— 安藤忠雄", {
  x: 0.7, y: 4.25, w: 4.9, h: 0.2,
  fontSize: 10, color: theme.colors.accent, fontFace: fonts.mono
});

// Right image placeholder
slide4.addShape(pres.shapes.RECTANGLE, {
  x: 6.0, y: 1.0, w: 3.5, h: 3.5,
  fill: { color: theme.colors.inkTint }
});
slide4.addText("[材质摄影]", {
  x: 6.0, y: 2.5, w: 3.5, h: 0.4,
  fontSize: 12, color: theme.colors.paper, fontFace: fonts.body, align: "center"
});

// --- Slide 5: Quote ---
let slide5 = pres.addSlide();
slide5.background = { color: theme.colors.inkTint };
slide5.addText("\"光，是空间的灵魂。\"", {
  x: 1.0, y: 1.8, w: 8, h: 1.0,
  fontSize: 36, color: theme.colors.paper, fontFace: fonts.title, italic: true
});
slide5.addText("— 路易斯·康", {
  x: 1.0, y: 2.9, w: 8, h: 0.25,
  fontSize: 11, color: theme.colors.accent, fontFace: fonts.mono
});

// --- Slide 6: Image Grid ---
let slide6 = pres.addSlide();
slide6.background = { color: theme.colors.paper };
slide6.addText("GALLERY", {
  x: 0.5, y: 0.4, w: 9, h: 0.2,
  fontSize: 10, color: theme.colors.accent, fontFace: fonts.mono, charSpacing: 4
});
slide6.addText("展厅掠影", {
  x: 0.5, y: 0.65, w: 9, h: 0.4,
  fontSize: 28, color: theme.colors.ink, fontFace: fonts.title, bold: true
});

// 3x2 image grid placeholders
const gridItems = [
  { x: 0.5, y: 1.2, label: "入口大厅" },
  { x: 3.4, y: 1.2, label: "主展厅" },
  { x: 6.3, y: 1.2, label: "装置区" },
  { x: 0.5, y: 3.3, label: "光影走廊" },
  { x: 3.4, y: 3.3, label: "冥想空间" },
  { x: 6.3, y: 3.3, label: "天台花园" }
];

gridItems.forEach(g => {
  slide6.addShape(pres.shapes.RECTANGLE, {
    x: g.x, y: g.y, w: 2.8, h: 1.8,
    fill: { color: theme.colors.inkTint }
  });
  slide6.addText(g.label, {
    x: g.x, y: g.y + 0.7, w: 2.8, h: 0.4,
    fontSize: 12, color: theme.colors.paper, fontFace: fonts.body, align: "center"
  });
});

// --- Slide 7: Before/After ---
let slide7 = pres.addSlide();
slide7.background = { color: theme.colors.paper };
slide7.addText("BEFORE", {
  x: 0.7, y: 0.5, w: 4.0, h: 0.2,
  fontSize: 10, color: theme.colors.accent, fontFace: fonts.mono, charSpacing: 3
});
slide7.addShape(pres.shapes.RECTANGLE, {
  x: 0.5, y: 0.8, w: 4.4, h: 4.0,
  fill: { color: theme.colors.paperTint }
});
slide7.addText("旧仓库\n\n• 废弃工业空间\n• 光线昏暗\n• 结构老化\n• 毫无生气", {
  x: 0.7, y: 1.0, w: 4.0, h: 3.0,
  fontSize: 14, color: theme.colors.ink, fontFace: fonts.body
});

slide7.addText("AFTER", {
  x: 5.3, y: 0.5, w: 4.0, h: 0.2,
  fontSize: 10, color: theme.colors.accent, fontFace: fonts.mono, charSpacing: 3
});
slide7.addShape(pres.shapes.RECTANGLE, {
  x: 5.1, y: 0.8, w: 4.4, h: 4.0,
  fill: { color: "d8c9a8" }
});
slide7.addText("沙丘美术馆\n\n• 天窗引入自然光\n• 保留原始结构\n• 沙色墙面\n• 冥想氛围", {
  x: 5.3, y: 1.0, w: 4.0, h: 3.0,
  fontSize: 14, color: theme.colors.ink, fontFace: fonts.body
});

// --- Slide 8: Closing ---
let slide8 = pres.addSlide();
slide8.background = { color: theme.colors.ink };
slide8.addText("感谢观展", {
  x: 0.5, y: 2.0, w: 9, h: 1.0,
  fontSize: 48, color: theme.colors.paper, fontFace: fonts.title, bold: true, align: "center"
});
slide8.addText("Dune Gallery · dune.gallery", {
  x: 0.5, y: 3.2, w: 9, h: 0.25,
  fontSize: 11, color: theme.colors.accent, fontFace: fonts.mono, align: "center"
});

pres.writeFile({ fileName: "demo-dune.pptx" });
console.log("Generated: demo-dune.pptx");
