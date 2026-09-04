# 杂志风版式库（PptxGenJS 版）

> 10 种杂志风版式的**完整可运行代码**。颜色/字体变量来自 [design-system.md](../design-system.md) 的 `theme` / `fonts` 对象。
> 本文件是版式行为的权威来源；design-system.md 只保留坐标速查。
> 自适应规则（条目增减、文字超长）见 [references/design-playbook.md](../references/design-playbook.md) 第 4 节。

**通用约定**：
- 画布 `LAYOUT_16x9` = 10" × 5.625"，边距 0.5"
- `theme.colors` = `{ ink, paper, paperTint, inkTint, accent }`
- `fonts` = `{ title, body, mono }`（安全字体表见 design-system.md 字体体系）
- 中文文本框宽度按 `字数 × 字号(pt) / 72` 英寸预估，留 10% 余量

---

## 1. cover — 开场封面

**用途**：第 1 页。**内容形状**：kicker ≤ 20 字符 + 主标题 ≤ 8 字（两行则每行 ≤ 8）+ 副题 ≤ 16 字 + 元数据 1 行。

```javascript
let s = pres.addSlide();
s.background = { color: theme.colors.ink };
s.addText("PRODUCT LAUNCH · 2026", { x: 0.5, y: 1.55, w: 9, h: 0.35,
  fontSize: 13, color: theme.colors.accent, fontFace: fonts.mono, charSpacing: 4 });
s.addText("一人公司", { x: 0.5, y: 2.0, w: 9, h: 1.1,
  fontSize: 54, color: theme.colors.paper, fontFace: fonts.title, bold: true });
s.addText("被 AI 折叠的组织", { x: 0.5, y: 3.25, w: 9, h: 0.5,
  fontSize: 22, color: theme.colors.paper, fontFace: fonts.body });
s.addText("私享会 · 2026", { x: 0.5, y: 4.7, w: 9, h: 0.3,
  fontSize: 12, color: theme.colors.accent, fontFace: fonts.mono });
```

**变体**：
- 两行标题：`h: 1.9`，`lineSpacingMultiple: 1.05`，y 上移 0.25，副题相应下移
- 标题 ≤ 4 字时可加 `fontSize: 60`
- **不要**在标题下加 accent 线

---

## 2. section — 章节幕封

**用途**：章节开场，每 3-4 页出现一次。**内容形状**：编号 + 章节标题 ≤ 10 字 + 引语 ≤ 20 字。

```javascript
let s = pres.addSlide();
s.background = { color: theme.colors.paper };
s.addText("01", { x: 0.5, y: 1.35, w: 2, h: 1.0,
  fontSize: 72, color: theme.colors.paperTint, fontFace: fonts.title, bold: true });
s.addText("ACT I · 现象", { x: 0.5, y: 2.45, w: 9, h: 0.35,
  fontSize: 13, color: theme.colors.accent, fontFace: fonts.mono, charSpacing: 4 });
s.addText("组织正在被折叠", { x: 0.5, y: 2.85, w: 9, h: 0.9,
  fontSize: 40, color: theme.colors.ink, fontFace: fonts.title, bold: true });
s.addText("一个人正在获得过去一个团队的产能。", { x: 0.5, y: 3.9, w: 7, h: 0.4,
  fontSize: 16, color: theme.colors.ink, fontFace: fonts.body });
```

**变体**：深底版把 `paper`/`ink` 互换（背景 `inkTint`，文字 `paper`）。

---

## 3. big-number — 数据大字报

**用途**：抛硬数据。**内容形状**：2-6 个指标，每个 = 数字（≤ 6 字符）+ 标签（≤ 8 字）+ 说明（≤ 14 字）。

```javascript
let s = pres.addSlide();
s.background = { color: theme.colors.paper };
s.addText("关键指标", { x: 0.5, y: 0.45, w: 9, h: 0.6,
  fontSize: 30, color: theme.colors.ink, fontFace: fonts.title, bold: true });

const stats = [
  { n: "92%", label: "意图分类准确率", note: "few-shot 后 70% → 92%" },
  { n: "3 天", label: "交付周期", note: "含数据清理与试运行" },
  { n: "<0.7", label: "置信度转人工", note: "兜底策略保证体验" },
];
const N = stats.length, gap = 0.3;
const w = (9 - (N - 1) * gap) / N;          // 自适应卡宽，见 playbook 4.1
stats.forEach((it, i) => {
  const x = 0.5 + i * (w + gap);
  s.addShape(pres.shapes.RECTANGLE, { x, y: 1.5, w, h: 2.9,
    fill: { color: theme.colors.paperTint } });
  s.addText(it.n, { x: x + 0.2, y: 1.8, w: w - 0.4, h: 0.9,
    fontSize: 40, color: theme.colors.accent, fontFace: fonts.title, bold: true });
  s.addText(it.label, { x: x + 0.2, y: 2.8, w: w - 0.4, h: 0.4,
    fontSize: 15, color: theme.colors.ink, fontFace: fonts.body, bold: true });
  s.addText(it.note, { x: x + 0.2, y: 3.3, w: w - 0.4, h: 0.8,
    fontSize: 11, color: theme.colors.ink, fontFace: fonts.body, lineSpacingMultiple: 1.3 });
});
```

**变体**：单指标 → 一张全宽卡（w=9），数字 72pt；6 项 → 3×2 网格（卡 w=2.8，两行 y=1.4 / 3.35，卡高 1.8，说明删掉只留数字+标签）。

---

## 4. two-column — 左文右图

**用途**：观点 + 证据图。**内容形状**：左列标题 ≤ 12 字 + 2-3 段 × ≤ 45 字；右图 16:10 或 4:3。

```javascript
let s = pres.addSlide();
s.background = { color: theme.colors.paper };
s.addText("KICKER · 背景", { x: 0.5, y: 0.55, w: 4.6, h: 0.3,
  fontSize: 12, color: theme.colors.accent, fontFace: fonts.mono, charSpacing: 3 });
s.addText("工具链成熟改变了成本结构", { x: 0.5, y: 0.95, w: 4.6, h: 1.0,
  fontSize: 26, color: theme.colors.ink, fontFace: fonts.title, bold: true,
  lineSpacingMultiple: 1.15 });
s.addText("AI 工具链的成熟让个体创作者具备了传统十人团队的生产力。这不是替代，而是能力的重新分配。",
  { x: 0.5, y: 2.15, w: 4.6, h: 1.6, fontSize: 14, color: theme.colors.ink,
    fontFace: fonts.body, lineSpacingMultiple: 1.45 });
s.addImage({ path: "images/02-workspace.jpg", x: 5.5, y: 0.55, w: 4.0, h: 2.5 }); // 16:10
s.addText("图：2026 年个体创作者工具链", { x: 5.5, y: 3.12, w: 4.0, h: 0.3,
  fontSize: 10, color: theme.colors.ink, fontFace: fonts.mono });
```

**变体**：无图时右列放 callout 卡（paperTint 底 + 引语）；文字多时左列加宽到 5.2（图缩到 3.4）。

---

## 5. image-grid — 图片网格

**用途**：2-6 张图对比/实证。**内容形状**：同组图片**统一比例**，每图 caption ≤ 12 字。

```javascript
let s = pres.addSlide();
s.background = { color: theme.colors.paper };
s.addText("案例实证", { x: 0.5, y: 0.45, w: 9, h: 0.6,
  fontSize: 30, color: theme.colors.ink, fontFace: fonts.title, bold: true });

const imgs = ["images/03-a.jpg", "images/03-b.jpg", "images/03-c.jpg"];
const caps = ["工单分类后台", "置信度分布", "人工复核队列"];
const N = imgs.length, gap = 0.3;
const w = (9 - (N - 1) * gap) / N;
imgs.forEach((p, i) => {
  const x = 0.5 + i * (w + gap);
  s.addImage({ path: p, x, y: 1.4, w, h: w * 0.6 });   // 统一 5:3
  s.addText(caps[i], { x, y: 1.4 + w * 0.6 + 0.12, w, h: 0.3,
    fontSize: 11, color: theme.colors.ink, fontFace: fonts.mono });
});
```

**规则**：同组必须同比例同高度；2 张用 16:10，3-4 张用 5:3 或 4:3；6 张改 3×2。

---

## 6. pipeline — 流程步骤

**用途**：3-7 步流程。**内容形状**：每步 = 编号 + 标题 ≤ 6 字 + 说明 ≤ 16 字。

```javascript
let s = pres.addSlide();
s.background = { color: theme.colors.paper };
s.addText("落地四步", { x: 0.5, y: 0.45, w: 9, h: 0.6,
  fontSize: 30, color: theme.colors.ink, fontFace: fonts.title, bold: true });

const steps = [
  { t: "建风险库", d: "沉淀历史工单与判例" },
  { t: "数据清理", d: "统一字段与格式" },
  { t: "AI 初审", d: "意图分类 + 置信度" },
  { t: "人工复核", d: "低置信度兜底" },
];
const N = steps.length, gap = 0.35;
const w = (9 - (N - 1) * gap) / N;
steps.forEach((st, i) => {
  const x = 0.5 + i * (w + gap);
  s.addShape(pres.shapes.RECTANGLE, { x, y: 1.6, w, h: 2.6,
    fill: { color: theme.colors.paperTint } });
  s.addText(String(i + 1).padStart(2, "0"), { x: x + 0.18, y: 1.8, w: w - 0.36, h: 0.6,
    fontSize: 30, color: theme.colors.accent, fontFace: fonts.title, bold: true });
  s.addText(st.t, { x: x + 0.18, y: 2.5, w: w - 0.36, h: 0.4,
    fontSize: 16, color: theme.colors.ink, fontFace: fonts.body, bold: true });
  s.addText(st.d, { x: x + 0.18, y: 2.95, w: w - 0.36, h: 1.0,
    fontSize: 11, color: theme.colors.ink, fontFace: fonts.body, lineSpacingMultiple: 1.35 });
  if (i < N - 1) s.addText("→", { x: x + w - 0.02, y: 2.6, w: gap + 0.06, h: 0.4,
    fontSize: 16, color: theme.colors.accent, fontFace: fonts.body, align: "center" });
});
```

**变体**：>5 步去掉箭头改步骤间细线；横向放不下改纵向时间线（每行一步）。

---

## 7. question — 悬念问题页

**用途**：幕末/转折。**内容形状**：一个问题 ≤ 16 字，可加一行提示 ≤ 20 字。

```javascript
let s = pres.addSlide();
s.background = { color: theme.colors.inkTint };
s.addText("?", { x: 0.5, y: 1.0, w: 9, h: 1.6,
  fontSize: 96, color: theme.colors.paperTint, fontFace: fonts.title, bold: true });
s.addText("如果 AI 能做 70%，剩下 30% 的人做什么？", {
  x: 0.5, y: 2.7, w: 9, h: 1.0, fontSize: 32, color: theme.colors.paper,
  fontFace: fonts.title, bold: true, lineSpacingMultiple: 1.2 });
s.addText("答案在下一节", { x: 0.5, y: 4.0, w: 9, h: 0.35,
  fontSize: 13, color: theme.colors.accent, fontFace: fonts.mono, charSpacing: 3 });
```

---

## 8. quote — 大引用页

**用途**：金句/takeaway。**内容形状**：引文 ≤ 24 字 + 出处 ≤ 12 字。

```javascript
let s = pres.addSlide();
s.background = { color: theme.colors.inkTint };
s.addText("“", { x: 0.6, y: 0.7, w: 1.5, h: 1.2,
  fontSize: 110, color: theme.colors.accent, fontFace: fonts.title, bold: true });
s.addText("问题不在模型，在检索链路。", { x: 1.0, y: 2.1, w: 8, h: 1.2,
  fontSize: 36, color: theme.colors.paper, fontFace: fonts.title, bold: true });
s.addText("— 某企业知识库项目复盘", { x: 1.0, y: 3.6, w: 8, h: 0.35,
  fontSize: 13, color: theme.colors.accent, fontFace: fonts.mono });
```

**变体**：引文 > 16 字降到 30pt；两句以内引文用 `breakLine` 分行。

---

## 9. before-after — 左右对比

**用途**：旧 vs 新。**内容形状**：两侧各 3-4 条 × ≤ 14 字，左灰右 accent。

```javascript
let s = pres.addSlide();
s.background = { color: theme.colors.paper };
s.addText("模式对比", { x: 0.5, y: 0.45, w: 9, h: 0.6,
  fontSize: 30, color: theme.colors.ink, fontFace: fonts.title, bold: true });

s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 1.4, w: 4.35, h: 3.4,
  fill: { color: theme.colors.paperTint } });
s.addText("BEFORE", { x: 0.75, y: 1.65, w: 3.8, h: 0.3,
  fontSize: 12, color: theme.colors.ink, fontFace: fonts.mono, charSpacing: 3 });
s.addText([
  { text: "十人团队各管一段", options: { breakLine: true } },
  { text: "需求排期以周计", options: { breakLine: true } },
  { text: "改版靠外包", options: {} },
], { x: 0.75, y: 2.15, w: 3.8, h: 2.3, fontSize: 15, color: theme.colors.ink,
  fontFace: fonts.body, lineSpacingMultiple: 1.9 });

s.addShape(pres.shapes.RECTANGLE, { x: 5.15, y: 1.4, w: 4.35, h: 3.4,
  fill: { color: theme.colors.accent } });
s.addText("AFTER", { x: 5.4, y: 1.65, w: 3.8, h: 0.3,
  fontSize: 12, color: theme.colors.paper, fontFace: fonts.mono, charSpacing: 3 });
s.addText([
  { text: "一人 + AI 工具链", options: { breakLine: true } },
  { text: "需求当天闭环", options: { breakLine: true } },
  { text: "迭代以小时计", options: {} },
], { x: 5.4, y: 2.15, w: 3.8, h: 2.3, fontSize: 15, color: theme.colors.paper,
  fontFace: fonts.body, lineSpacingMultiple: 1.9 });
```

**注意**：accent 底上的文字用 `paper` 色；accent 是深色（克莱因蓝）时文字必须白色。

---

## 10. mixed — 图文混排

**用途**：信息密集页。**内容形状**：左图 40% + 右侧标题 + 3 组 icon 要点（每组 ≤ 20 字）。

```javascript
let s = pres.addSlide();
s.background = { color: theme.colors.paper };
s.addImage({ path: "images/05-system.png", x: 0.5, y: 0.9, w: 3.8, h: 3.8 }); // 1:1
s.addText("系统如何运转", { x: 4.7, y: 0.9, w: 4.8, h: 0.7,
  fontSize: 26, color: theme.colors.ink, fontFace: fonts.title, bold: true });
[
  { icon: "①", t: "接入", d: "工单系统 API 自动同步" },
  { icon: "②", t: "分类", d: "大模型意图识别 + 置信度" },
  { icon: "③", t: "分发", d: "高置信度直派，低置信度转人工" },
].forEach((r, i) => {
  const y = 1.85 + i * 0.95;
  s.addShape(pres.shapes.OVAL, { x: 4.7, y, w: 0.42, h: 0.42,
    fill: { color: theme.colors.accent } });
  s.addText(r.icon, { x: 4.7, y, w: 0.42, h: 0.42, fontSize: 14,
    color: theme.colors.paper, fontFace: fonts.body, align: "center", valign: "middle" });
  s.addText(r.t, { x: 5.3, y: y - 0.02, w: 4.2, h: 0.35,
    fontSize: 15, color: theme.colors.ink, fontFace: fonts.body, bold: true });
  s.addText(r.d, { x: 5.3, y: y + 0.33, w: 4.2, h: 0.35,
    fontSize: 12, color: theme.colors.ink, fontFace: fonts.body });
});
```

---

## 版式组合建议

一份 10 页杂志风 deck 的典型节奏：

```
1 cover(深) → 2 two-column(浅) → 3 big-number(浅) → 4 section(深)
→ 5 pipeline(浅) → 6 chart(浅) → 7 quote(深) → 8 two-column(浅)
→ 9 before-after(浅) → 10 cover 变体收束(深)
```

检查：无连续 3 页同明暗 ✓；版式 7 种 ✓；hero 间隔 ≤ 4 页 ✓。
