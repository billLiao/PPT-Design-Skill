# PPT Design System

本设计系统整合了「电子杂志 × 电子墨水」与「瑞士国际主义」两套视觉体系，为 PptxGenJS 提供即拿即用的主题、版式和字体配置。

---

## 目录

- [主题色 Themes](#主题色-themes)
  - [杂志风 Magazine (5套)](#杂志风-magazine)
  - [瑞士风 Swiss (4套)](#瑞士风-swiss)
- [字体体系 Typography](#字体体系-typography)
- [版式布局 Layouts](#版式布局-layouts)
  - [杂志风版式 (10种)](#杂志风版式)
  - [瑞士风版式 (22种)](#瑞士风版式)
- [快速开始 Quick Start](#快速开始-quick-start)

---

## 主题色 Themes

### 使用原则

- **一份 deck 只用一套主题**，不要中途换色
- **不允许用户自定义 hex 值**——色彩搭配错了画面瞬间变丑，从以下预设中挑选
- 所有颜色在 PptxGenJS 中使用 **6位 hex，不带 `#` 前缀**

### 杂志风 Magazine

适合：人文分享、行业观察、商业发布、需要"杂志感"的演讲

#### 1. 墨水经典 Ink Classic（默认）
通用 / 商业发布 / 不知道选啥时的默认选择。像 Monocle 杂志贴上了代码。

```javascript
const themeInkClassic = {
  name: "ink-classic",
  style: "magazine",
  colors: {
    ink: "0a0a0b",          // 主文字 / dark背景
    paper: "f1efea",        // 主背景 / light底色
    paperTint: "e8e5de",    // 卡片/区块底色
    inkTint: "18181a",      // 深色变体
    accent: "d4a574",       // 暖金强调色
    accentRgb: "212,165,116"
  },
  background: { color: "f1efea" },
  backgroundDark: { color: "0a0a0b" }
};
```

#### 2. 靛蓝瓷 Indigo Porcelain
科技 / 研究 / AI / 技术发布会。冷静、理性、有深度，像学术期刊或蓝印花瓷器。

```javascript
const themeIndigoPorcelain = {
  name: "indigo-porcelain",
  style: "magazine",
  colors: {
    ink: "0a1f3d",
    paper: "f1f3f5",
    paperTint: "e4e8ec",
    inkTint: "152a4a",
    accent: "4a90a4",
    accentRgb: "74,144,164"
  },
  background: { color: "f1f3f5" },
  backgroundDark: { color: "0a1f3d" }
};
```

#### 3. 森林墨 Forest Ink
自然 / 可持续 / 文化 / 非虚构。沉稳、有呼吸感，像旧版《国家地理》。

```javascript
const themeForestInk = {
  name: "forest-ink",
  style: "magazine",
  colors: {
    ink: "1a2e1f",
    paper: "f5f1e8",
    paperTint: "ece7da",
    inkTint: "253d2c",
    accent: "6b8e5a",
    accentRgb: "107,142,90"
  },
  background: { color: "f5f1e8" },
  backgroundDark: { color: "1a2e1f" }
};
```

#### 4. 牛皮纸 Kraft Paper
怀旧 / 人文 / 文学 / 独立杂志。像牛皮信封或老笔记本，温暖、有年代感。

```javascript
const themeKraftPaper = {
  name: "kraft-paper",
  style: "magazine",
  colors: {
    ink: "2a1e13",
    paper: "eedfc7",
    paperTint: "e0d0b6",
    inkTint: "3a2a1d",
    accent: "b87333",
    accentRgb: "184,115,51"
  },
  background: { color: "eedfc7" },
  backgroundDark: { color: "2a1e13" }
};
```

#### 5. 沙丘 Dune
艺术 / 设计 / 创意 / 画廊。克制、高级、中性，像沙漠黄昏或建筑设计图册。

```javascript
const themeDune = {
  name: "dune",
  style: "magazine",
  colors: {
    ink: "1f1a14",
    paper: "f0e6d2",
    paperTint: "e3d7bf",
    inkTint: "2d2620",
    accent: "c4a265",
    accentRgb: "196,162,101"
  },
  background: { color: "f0e6d2" },
  backgroundDark: { color: "1f1a14" }
};
```

### 瑞士风 Swiss

适合：科技产品、数据汇报、设计/工程领域分享、年度总结。极简、理性、信息驱动。

#### 6. IKB 克莱因蓝 Klein Blue
极简、冲击力强。克莱因蓝作为高反差功能色。

```javascript
const themeSwissBlue = {
  name: "swiss-blue",
  style: "swiss",
  colors: {
    ink: "1a1a1a",
    paper: "f5f5f5",
    accent: "002FA7",       // IKB 克莱因蓝
    accentLight: "e6ebf7",
    grid: "d0d0d0"
  },
  background: { color: "f5f5f5" },
  backgroundDark: { color: "1a1a1a" }
};
```

#### 7. 柠檬黄 Lemon Yellow
活力、乐观。深色底 + 高饱和黄。

```javascript
const themeSwissYellow = {
  name: "swiss-yellow",
  style: "swiss",
  colors: {
    ink: "1a1a1a",
    paper: "f5f5f5",
    accent: "FFD700",
    accentLight: "fff8d6",
    grid: "d0d0d0"
  },
  background: { color: "f5f5f5" },
  backgroundDark: { color: "1a1a1a" }
};
```

#### 8. 柠檬绿 Lime Green
创新、科技。深色底 + 荧光绿。

```javascript
const themeSwissGreen = {
  name: "swiss-green",
  style: "swiss",
  colors: {
    ink: "1a1a1a",
    paper: "f5f5f5",
    accent: "CCFF00",
    accentLight: "f5ffd6",
    grid: "d0d0d0"
  },
  background: { color: "f5f5f5" },
  backgroundDark: { color: "1a1a1a" }
};
```

#### 9. 安全橙 Safety Orange
警示、强调。深色底 + 亮橙。

```javascript
const themeSwissOrange = {
  name: "swiss-orange",
  style: "swiss",
  colors: {
    ink: "1a1a1a",
    paper: "f5f5f5",
    accent: "FF5F00",
    accentLight: "ffe8d6",
    grid: "d0d0d0"
  },
  background: { color: "f5f5f5" },
  backgroundDark: { color: "1a1a1a" }
};
```

---

## 字体体系 Typography

### 杂志风字体

| 角色 | 字体 | 用途 |
|------|------|------|
| 标题（衬线） | Playfair Display / Noto Serif SC | 大标题、封面、引用 |
| 正文（无衬线） | Noto Sans SC / Calibri | 段落、列表、说明 |
| 标注（等宽） | IBM Plex Mono / Consolas | 数据标签、页码、元数据 |

```javascript
const fontsMagazine = {
  title: "Playfair Display",
  titleFallback: "Noto Serif SC",
  body: "Noto Sans SC",
  bodyFallback: "Calibri",
  mono: "IBM Plex Mono",
  monoFallback: "Consolas"
};
```

### 瑞士风字体

| 角色 | 字体 | 用途 |
|------|------|------|
| 标题（无衬线） | Inter / Helvetica / Noto Sans SC Bold | 所有标题，极致字号对比 |
| 正文（无衬线） | Inter / Noto Sans SC | 段落、列表 |
| 标注（等宽） | IBM Plex Mono | 数据、标签、网格坐标 |

```javascript
const fontsSwiss = {
  title: "Inter",
  titleFallback: "Helvetica",
  body: "Inter",
  bodyFallback: "Noto Sans SC",
  mono: "IBM Plex Mono",
  monoFallback: "Consolas"
};
```

### 字号规范

| 元素 | 杂志风 | 瑞士风 |
|------|--------|--------|
| 封面大标题 | 44-54pt | 48-60pt |
| 章节标题 | 36-44pt | 40-48pt |
| 页面标题 | 28-36pt | 32-40pt |
| 正文 | 14-18pt | 14-16pt |
| 数据大字 | 60-72pt | 60-80pt |
| 标注/页脚 | 10-12pt | 10-12pt |

---

## 版式布局 Layouts

### 杂志风版式

详细骨架和 HTML/CSS 参考见 `templates/layouts/magazine-layouts.md`。以下为 PptxGenJS 坐标映射。

#### cover — 开场封面
暗底，大字号衬线标题居中，副标题和元数据上下分布。

```javascript
// 封面版式坐标 (10" x 5.625" 16:9)
const layoutCover = {
  background: { color: theme.colors.ink },
  objects: [
    { text: "KICKER", x: 0.5, y: 1.8, w: 9, h: 0.4, fontSize: 14, color: theme.colors.accent, fontFace: fonts.mono },
    { text: "主标题", x: 0.5, y: 2.3, w: 9, h: 1.2, fontSize: 48, color: theme.colors.paper, fontFace: fonts.title, bold: true },
    { text: "副标题", x: 0.5, y: 3.6, w: 9, h: 0.6, fontSize: 24, color: theme.colors.paper, fontFace: fonts.body },
    { text: "元数据 · 日期", x: 0.5, y: 4.8, w: 9, h: 0.3, fontSize: 12, color: theme.colors.paper, fontFace: fonts.mono }
  ]
};
```

#### section — 章节幕封
极简，kicker + 大标题 + 一行引语。

```javascript
const layoutSection = {
  background: { color: theme.colors.paper },
  objects: [
    { text: "ACT I", x: 0.5, y: 1.8, w: 9, h: 0.4, fontSize: 14, color: theme.colors.accent, fontFace: fonts.mono },
    { text: "章节标题", x: 0.5, y: 2.3, w: 9, h: 1.0, fontSize: 44, color: theme.colors.ink, fontFace: fonts.title, bold: true },
    { text: "章节引语", x: 0.5, y: 3.5, w: 7, h: 0.5, fontSize: 18, color: theme.colors.ink, fontFace: fonts.body }
  ]
};
```

#### big-number — 数据大字报
3×2 或 4×2 网格数字卡片。

```javascript
const layoutBigNumber = {
  background: { color: theme.colors.paper },
  // 6个数据卡片网格: 3列 x 2行
  // 列宽 2.8", 行高 1.6", 间距 0.3"
  objects: [
    // 标题区
    { text: "数据标题", x: 0.5, y: 0.4, w: 9, h: 0.6, fontSize: 32, color: theme.colors.ink, fontFace: fonts.title, bold: true },
    // 卡片1 (row1, col1)
    { shape: pres.shapes.RECTANGLE, x: 0.5, y: 1.2, w: 2.8, h: 1.6, fill: { color: theme.colors.paperTint } },
    { text: "Label", x: 0.7, y: 1.3, w: 2.4, h: 0.3, fontSize: 12, color: theme.colors.ink, fontFace: fonts.mono },
    { text: "128", x: 0.7, y: 1.6, w: 2.4, h: 0.6, fontSize: 48, color: theme.colors.ink, fontFace: fonts.title, bold: true },
    // ... 重复6个卡片
  ]
};
```

#### two-column — 左文右图
7:5 比例，左列文字，右列图片。

```javascript
const layoutTwoColumn = {
  background: { color: theme.colors.paper },
  objects: [
    // 左列文字 (7份 ≈ 5.8")
    { text: "KICKER", x: 0.5, y: 0.8, w: 5.3, h: 0.3, fontSize: 12, color: theme.colors.accent, fontFace: fonts.mono },
    { text: "标题", x: 0.5, y: 1.2, w: 5.3, h: 0.8, fontSize: 36, color: theme.colors.ink, fontFace: fonts.title, bold: true },
    { text: "正文内容...", x: 0.5, y: 2.2, w: 5.3, h: 2.5, fontSize: 16, color: theme.colors.ink, fontFace: fonts.body },
    // 右列图片 (5份 ≈ 4.2")
    { image: { path: "image.png", x: 6.0, y: 1.0, w: 3.5, h: 3.5, sizing: { type: "cover", w: 3.5, h: 3.5 } } }
  ]
};
```

#### image-grid — 图片网格
3×2 图片网格，统一高度。

```javascript
const layoutImageGrid = {
  background: { color: theme.colors.paper },
  // 3列 x 2行, 每格 w=2.9, h=2.0, gap=0.3
  objects: [
    { image: { path: "img1.png", x: 0.5, y: 1.0, w: 2.9, h: 2.0 } },
    { image: { path: "img2.png", x: 3.4, y: 1.0, w: 2.9, h: 2.0 } },
    { image: { path: "img3.png", x: 6.3, y: 1.0, w: 2.9, h: 2.0 } },
    { image: { path: "img4.png", x: 0.5, y: 3.3, w: 2.9, h: 2.0 } },
    { image: { path: "img5.png", x: 3.4, y: 3.3, w: 2.9, h: 2.0 } },
    { image: { path: "img6.png", x: 6.3, y: 3.3, w: 2.9, h: 2.0 } }
  ]
};
```

#### pipeline — 流程步骤
水平排列的步骤卡片。

```javascript
const layoutPipeline = {
  background: { color: theme.colors.paper },
  // 4步骤, 每步 w=2.1, h=2.8, gap=0.3
  objects: [
    { shape: pres.shapes.RECTANGLE, x: 0.5, y: 1.5, w: 2.1, h: 2.8, fill: { color: theme.colors.paperTint } },
    { text: "01", x: 0.7, y: 1.7, w: 1.7, h: 0.5, fontSize: 36, color: theme.colors.accent, fontFace: fonts.title },
    { text: "步骤标题", x: 0.7, y: 2.3, w: 1.7, h: 0.4, fontSize: 16, color: theme.colors.ink, fontFace: fonts.body, bold: true },
    // ... 重复4步
  ]
};
```

#### question — 悬念问题页
暗底居中，大问题。

```javascript
const layoutQuestion = {
  background: { color: theme.colors.ink },
  objects: [
    { text: "如果...?", x: 0.5, y: 2.0, w: 9, h: 1.5, fontSize: 48, color: theme.colors.paper, fontFace: fonts.title, bold: true, align: "center" },
    { text: "引导思考的一句话", x: 1.5, y: 3.8, w: 7, h: 0.5, fontSize: 18, color: theme.colors.paper, fontFace: fonts.body, align: "center" }
  ]
};
```

#### quote — 大引用页
衬线斜体金句。

```javascript
const layoutQuote = {
  background: { color: theme.colors.inkTint },
  objects: [
    { text: "\"金句内容\"", x: 1.0, y: 1.8, w: 8, h: 1.5, fontSize: 36, color: theme.colors.paper, fontFace: fonts.title, italic: true },
    { text: "— 出处", x: 1.0, y: 3.5, w: 8, h: 0.3, fontSize: 14, color: theme.colors.accent, fontFace: fonts.mono }
  ]
};
```

#### before-after — 左右对比
5:5 比例，左右对照。

```javascript
const layoutBeforeAfter = {
  background: { color: theme.colors.paper },
  objects: [
    // 左侧 Before
    { shape: pres.shapes.RECTANGLE, x: 0.5, y: 0.8, w: 4.4, h: 4.0, fill: { color: theme.colors.paperTint } },
    { text: "BEFORE", x: 0.7, y: 1.0, w: 4.0, h: 0.3, fontSize: 12, color: theme.colors.accent, fontFace: fonts.mono },
    { text: "旧模式描述", x: 0.7, y: 1.5, w: 4.0, h: 2.5, fontSize: 16, color: theme.colors.ink, fontFace: fonts.body },
    // 右侧 After
    { shape: pres.shapes.RECTANGLE, x: 5.1, y: 0.8, w: 4.4, h: 4.0, fill: { color: theme.colors.accentLight || theme.colors.paperTint } },
    { text: "AFTER", x: 5.3, y: 1.0, w: 4.0, h: 0.3, fontSize: 12, color: theme.colors.accent, fontFace: fonts.mono },
    { text: "新模式描述", x: 5.3, y: 1.5, w: 4.0, h: 2.5, fontSize: 16, color: theme.colors.ink, fontFace: fonts.body }
  ]
};
```

#### mixed — 图文混排
灵活网格，信息密集。

```javascript
const layoutMixed = {
  background: { color: theme.colors.paper },
  // 2列: 左5 右5, 上标题 下内容
  objects: [
    { text: "标题", x: 0.5, y: 0.5, w: 9, h: 0.6, fontSize: 32, color: theme.colors.ink, fontFace: fonts.title, bold: true },
    // 左列: 文字 + 小图
    { text: "正文...", x: 0.5, y: 1.3, w: 4.5, h: 2.0, fontSize: 14, color: theme.colors.ink, fontFace: fonts.body },
    { image: { path: "small.png", x: 0.5, y: 3.5, w: 4.5, h: 1.5 } },
    // 右列: 大图
    { image: { path: "large.png", x: 5.5, y: 1.3, w: 4.0, h: 3.7 } }
  ]
};
```

### 瑞士风版式

瑞士风使用 12列网格系统，强调极致的字号对比和无衬线字体层级。
详细版式定义见 `templates/layouts/swiss-layouts.md`。

核心原则：
- 所有元素对齐到 12列网格
- 标题使用超大字号（48-60pt），正文保持克制（14-16pt）
- 高反差功能色仅用于强调和数据
- 留白是设计的一部分

```javascript
// 瑞士风网格常量 (10" 宽)
const SWISS_GRID = {
  col: 0.75,      // 每列宽 0.75"
  gap: 0.25,      // 间距 0.25"
  margin: 0.5     // 边距 0.5"
};

// 12列定位辅助函数
function span(cols, offset = 0) {
  const x = SWISS_GRID.margin + offset * (SWISS_GRID.col + SWISS_GRID.gap);
  const w = cols * SWISS_GRID.col + (cols - 1) * SWISS_GRID.gap;
  return { x, w };
}
```

---

## 快速开始 Quick Start

### 1. 选择主题

```javascript
const pptxgen = require("pptxgenjs");
let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";

// 选择主题
const theme = themeInkClassic;  // 或 themeSwissBlue 等
const fonts = fontsMagazine;    // 或 fontsSwiss
```

### 2. 应用背景

```javascript
let slide = pres.addSlide();
slide.background = theme.background;
```

### 3. 添加内容（使用版式坐标）

```javascript
// 封面示例
slide.addText("私享会 · 2026", { x: 0.5, y: 1.8, w: 9, h: 0.4, fontSize: 14, color: theme.colors.accent, fontFace: fonts.mono });
slide.addText("一人公司", { x: 0.5, y: 2.3, w: 9, h: 1.2, fontSize: 48, color: theme.colors.paper, fontFace: fonts.title, bold: true });
slide.addText("被 AI 折叠的组织", { x: 0.5, y: 3.6, w: 9, h: 0.6, fontSize: 24, color: theme.colors.paper, fontFace: fonts.body });
```

### 4. 写入文件

```javascript
pres.writeFile({ fileName: "output.pptx" });
```

---

## 参考文档

- 杂志风主题详情: `templates/themes/magazine-themes.md`
- 瑞士风主题详情: `templates/themes/swiss-themes.md`
- 杂志风版式骨架: `templates/layouts/magazine-layouts.md`
- 瑞士风版式骨架: `templates/layouts/swiss-layouts.md`
- 组件手册: `templates/components.md`
- 质量检查清单: `references/checklist.md`
- PptxGenJS API 参考: `pptxgenjs.md`
