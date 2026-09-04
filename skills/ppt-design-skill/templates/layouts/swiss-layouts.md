# 瑞士风版式库 S01-S22（PptxGenJS 版）

> 22 个登记版式的 pptxgenjs 实现。颜色变量来自 [design-system.md](../design-system.md) 的 `theme`（Swiss 主题）。
> 网格常量与 `span()` 辅助函数见 design-system.md「瑞士风版式」一节。
> 自适应规则见 [design-playbook.md](../references/design-playbook.md) 第 4 节。

**通用约定**：
- 画布 10" × 5.625"，边距 0.5"，12 列网格（col=0.75, gap=0.25）
- `theme.colors` = `{ ink, paper, paperTint, accent }`
- `fonts` = `{ title, body, mono }`（瑞士风：标题/正文微软雅黑或 Arial，mono 用 Consolas）
- 标题一律左上对齐（S03/S09/S10 statement 版式除外）
- accent 色只用于强调和数据，占比 < 10%

```javascript
// 每个文件开头
const pptxgen = require("pptxgenjs");
let pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
const C = theme.colors, F = fonts;
const span = (cols, offset = 0) => ({
  x: 0.5 + offset * 1.0,
  w: cols * 0.75 + (cols - 1) * 0.25,
});
```

---

## S01 · Index Cover（封面）

**内容形状**：左大编号 + 右标题 ≤ 10 字 + 元数据 1 行。

```javascript
let s = pres.addSlide();
s.background = { color: C.ink };
s.addText("01", { x: 0.5, y: 1.6, w: 2.2, h: 1.6,
  fontSize: 88, color: C.accent, fontFace: F.title, bold: true });
s.addText("组织正在被折叠", { x: 3.0, y: 1.75, w: 6.5, h: 1.0,
  fontSize: 44, color: C.paper, fontFace: F.title, bold: true });
s.addText("ANNUAL REPORT · 2026", { x: 3.0, y: 2.9, w: 6.5, h: 0.35,
  fontSize: 12, color: C.paper, fontFace: F.mono, charSpacing: 4 });
```

## S02 · Vertical Timeline + KPI

**内容形状**：3-4 个时间节点（每个 ≤ 12 字）+ 底部 4 个 KPI（数字 ≤ 5 字符 + 标签 ≤ 6 字）。

```javascript
let s = pres.addSlide();
s.background = { color: C.paper };
s.addText("演化路径", { x: 0.5, y: 0.4, w: 9, h: 0.6,
  fontSize: 28, color: C.ink, fontFace: F.title, bold: true });
// 纵向时间线：左轴 + 节点
s.addShape(pres.shapes.RECTANGLE, { x: 1.1, y: 1.3, w: 0.03, h: 2.4, fill: { color: C.ink } });
[
  { y: 1.3, t: "2023 · 工具爆发", d: "单点效率提升" },
  { y: 2.1, t: "2024 · 流程重构", d: "部门级试点" },
  { y: 2.9, t: "2025 · 组织折叠", d: "一人承担一条线" },
].forEach(n => {
  s.addShape(pres.shapes.OVAL, { x: 1.02, y: n.y + 0.05, w: 0.2, h: 0.2, fill: { color: C.accent } });
  s.addText(n.t, { x: 1.45, y: n.y, w: 4.2, h: 0.35, fontSize: 15, color: C.ink, fontFace: F.body, bold: true });
  s.addText(n.d, { x: 1.45, y: n.y + 0.36, w: 4.2, h: 0.3, fontSize: 11, color: C.ink, fontFace: F.body });
});
// 底部 KPI 行
[{ n: "3×", l: "人效" }, { n: "-40%", l: "周期" }, { n: "92%", l: "准确率" }, { n: "5", l: "试点部门" }]
  .forEach((k, i) => {
    const x = 0.5 + i * 2.3;
    s.addText(k.n, { x, y: 4.0, w: 2.0, h: 0.7, fontSize: 34, color: C.accent, fontFace: F.title, bold: true });
    s.addText(k.l, { x, y: 4.7, w: 2.0, h: 0.3, fontSize: 11, color: C.ink, fontFace: F.mono });
  });
```

## S03 · Split Statement（左右分屏）

**内容形状**：左巨字 ≤ 8 字 + 右解释 ≤ 40 字。允许强中心叙事。

```javascript
let s = pres.addSlide();
s.background = { color: C.ink };
s.addShape(pres.shapes.RECTANGLE, { x: 5.0, y: 0, w: 5.0, h: 5.625, fill: { color: C.paperTint } });
s.addText("一人\n公司", { x: 0.5, y: 1.5, w: 4.0, h: 2.6,
  fontSize: 60, color: C.paper, fontFace: F.title, bold: true, lineSpacingMultiple: 1.05 });
s.addText("AI 让个体具备了过去一个团队的生产力。组织形态正在被重新定义。",
  { x: 5.5, y: 2.0, w: 4.0, h: 1.6, fontSize: 16, color: C.ink, fontFace: F.body, lineSpacingMultiple: 1.5 });
```

## S04 · Six Cells（六格概念）

**内容形状**：6 个概念，每个 = 标题 ≤ 6 字 + 说明 ≤ 14 字。

```javascript
let s = pres.addSlide();
s.background = { color: C.paper };
s.addText("六个关键概念", { x: 0.5, y: 0.4, w: 9, h: 0.6,
  fontSize: 28, color: C.ink, fontFace: F.title, bold: true });
const cells = [/* {t:"概念", d:"一句话说明"} × 6 */];
cells.forEach((c, i) => {
  const col = i % 3, row = Math.floor(i / 3);
  const x = 0.5 + col * 3.1, y = 1.3 + row * 2.0;
  s.addShape(pres.shapes.RECTANGLE, { x, y, w: 2.8, h: 1.8, fill: { color: C.paperTint } });
  s.addText(c.t, { x: x + 0.2, y: y + 0.2, w: 2.4, h: 0.4, fontSize: 16, color: C.ink, fontFace: F.body, bold: true });
  s.addText(c.d, { x: x + 0.2, y: y + 0.7, w: 2.4, h: 0.9, fontSize: 11, color: C.ink, fontFace: F.body, lineSpacingMultiple: 1.35 });
});
```

## S05 · Three Layers（三层架构）

**内容形状**：3 个层级块，每块 = 层名 ≤ 6 字 + 要点 ≤ 20 字。

```javascript
let s = pres.addSlide();
s.background = { color: C.paper };
s.addText("三层架构", { x: 0.5, y: 0.4, w: 9, h: 0.6, fontSize: 28, color: C.ink, fontFace: F.title, bold: true });
[
  { t: "应用层", d: "面向业务的场景与工具", c: C.accent, tc: C.paper },
  { t: "模型层", d: "大模型 + 领域微调", c: C.paperTint, tc: C.ink },
  { t: "数据层", d: "知识库 / 工单 / 日志", c: C.paperTint, tc: C.ink },
].forEach((L, i) => {
  const y = 1.3 + i * 1.35;
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y, w: 9, h: 1.15, fill: { color: L.c } });
  s.addText(L.t, { x: 0.8, y: y + 0.2, w: 2.0, h: 0.7, fontSize: 20, color: L.tc, fontFace: F.title, bold: true, valign: "middle" });
  s.addText(L.d, { x: 3.0, y: y + 0.2, w: 6.2, h: 0.7, fontSize: 14, color: L.tc, fontFace: F.body, valign: "middle" });
});
```

## S06 · KPI Tower（不等高数据塔）

**内容形状**：4 个指标，高度按数值比例，数字 ≤ 5 字符。

```javascript
let s = pres.addSlide();
s.background = { color: C.paper };
s.addText("渠道表现对比", { x: 0.5, y: 0.4, w: 4.5, h: 1.0, fontSize: 26, color: C.ink, fontFace: F.title, bold: true });
s.addText("高度 = 转化率", { x: 0.5, y: 1.5, w: 4.5, h: 0.3, fontSize: 12, color: C.ink, fontFace: F.mono });
const towers = [{ n: "92%", h: 3.2, l: "直营" }, { n: "71%", h: 2.5, l: "分销" }, { n: "45%", h: 1.6, l: "电商" }, { n: "28%", h: 1.0, l: "私域" }];
towers.forEach((t, i) => {
  const x = 5.2 + i * 1.15;
  s.addShape(pres.shapes.RECTANGLE, { x, y: 4.9 - t.h, w: 0.95, h: t.h, fill: { color: i === 0 ? C.accent : C.paperTint } });
  s.addText(t.n, { x: x - 0.1, y: 4.9 - t.h - 0.45, w: 1.15, h: 0.4, fontSize: 16, color: C.ink, fontFace: F.title, bold: true, align: "center" });
  s.addText(t.l, { x: x - 0.1, y: 4.95, w: 1.15, h: 0.3, fontSize: 11, color: C.ink, fontFace: F.mono, align: "center" });
});
```

## S07 · H-Bar Chart（排名条形图）

**内容形状**：5-10 项排名。**必须用原生图表**，不要手画矩形。

```javascript
let s = pres.addSlide();
s.background = { color: C.paper };
s.addText("省份猪价排名", { x: 0.5, y: 0.4, w: 9, h: 0.6, fontSize: 28, color: C.ink, fontFace: F.title, bold: true });
s.addChart(pres.charts.BAR, [{
  name: "价格", labels: ["广东", "福建", "浙江", "山东", "河南", "四川"],
  values: [9.8, 9.6, 9.4, 9.1, 8.9, 8.7],
}], {
  x: 0.5, y: 1.2, w: 9, h: 3.9, barDir: "bar",
  chartColors: [C.accent], showLegend: false, showValue: true,
  dataLabelPosition: "outEnd", dataLabelColor: C.ink, dataLabelFontSize: 11,
  dataLabelFormatCode: "0.0",   // 小数数据必须指定，否则渲染成整数
  catAxisLabelColor: C.ink, valAxisHidden: true, valGridLine: { style: "none" },
  catGridLine: { style: "none" }, barGapWidthPct: 60,
});
```

## S08 · Duo Compare（Before/After）

**内容形状**：两侧各 3-4 条 × ≤ 14 字。实现同杂志风 before-after（见 magazine-layouts.md 第 9 节），底色改 `paperTint` / `accent`，文字用 `ink` / `paper`。

## S09 · Dot Matrix Statement（大引述）

**内容形状**：statement ≤ 20 字。点阵用小圆点形状阵列（≤ 60 个，太多会拖慢 PowerPoint）。

```javascript
let s = pres.addSlide();
s.background = { color: C.ink };
for (let r = 0; r < 6; r++) for (let c = 0; c < 16; c++)
  s.addShape(pres.shapes.OVAL, { x: 0.5 + c * 0.58, y: 0.4 + r * 0.28, w: 0.06, h: 0.06, fill: { color: C.paperTint } });
s.addText("先清理数据，再上 AI。", { x: 0.5, y: 2.3, w: 9, h: 1.0,
  fontSize: 40, color: C.paper, fontFace: F.title, bold: true });
```

## S10 · Split Closing（收束页）

**内容形状**：行动号召 ≤ 12 字 + 联系方式/下一步 1 行。结构同 S03，左字右块，右块放二维码或行动要点。

## S11 · Horizontal Timeline（横向流程）

**内容形状**：4-7 步，每步 = 标题 ≤ 6 字 + 说明 ≤ 14 字。实现同杂志风 pipeline（magazine-layouts.md 第 6 节），卡片底色 `paperTint`，编号用 accent。

## S12 · Manifesto + Ink Banner（阶段结论）

**内容形状**：宣言句 ≤ 18 字 + 满宽 accent 横幅内白字要点 ≤ 20 字。

```javascript
let s = pres.addSlide();
s.background = { color: C.paper };
s.addText("AI 进流程，不进工位。", { x: 0.5, y: 1.2, w: 9, h: 1.0,
  fontSize: 36, color: C.ink, fontFace: F.title, bold: true });
s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 3.2, w: 10, h: 1.4, fill: { color: C.accent } });
s.addText("先拆流程 → 找到最贵的一步 → 用 AI 替换 → 度量前后差异",
  { x: 0.5, y: 3.2, w: 9, h: 1.4, fontSize: 18, color: C.paper, fontFace: F.body, valign: "middle" });
```

## S13 · Three Forces（三力对等）

**内容形状**：3 个对等概念，每个 = 名称 ≤ 6 字 + 说明 ≤ 24 字。三列等宽卡（w=2.8），第一张可用 accent 底突出。

## S14 · Loop Form（闭环图）

**内容形状**：4-5 个环节 + 回路。用 4 张卡 + 4 个箭头文本（"→" "↓" "←" "↑"）摆成环形；中心放主题词 ≤ 4 字。

## S15 · Matrix + Hero Stat（矩阵 + 大数）

**内容形状**：8-12 项矩阵（2 行小卡）+ 右侧 1 个大数字。矩阵卡 = 标题 ≤ 6 字；大数字 72pt accent。

```javascript
let s = pres.addSlide();
s.background = { color: C.paper };
s.addText("能力矩阵", { x: 0.5, y: 0.4, w: 6, h: 0.6, fontSize: 28, color: C.ink, fontFace: F.title, bold: true });
// 左侧 2×4 小卡矩阵（每卡 w=1.5, h=1.0）
items.forEach((it, i) => {
  const col = i % 4, row = Math.floor(i / 4);
  const x = 0.5 + col * 1.7, y = 1.3 + row * 1.2;
  s.addShape(pres.shapes.RECTANGLE, { x, y, w: 1.5, h: 1.0, fill: { color: C.paperTint } });
  s.addText(it, { x: x + 0.1, y, w: 1.3, h: 1.0, fontSize: 12, color: C.ink, fontFace: F.body, valign: "middle" });
});
// 右侧 hero 数字
s.addText("92%", { x: 7.6, y: 1.6, w: 2.0, h: 1.2, fontSize: 72, color: C.accent, fontFace: F.title, bold: true });
s.addText("平均采纳率", { x: 7.6, y: 2.9, w: 2.0, h: 0.3, fontSize: 12, color: C.ink, fontFace: F.mono });
```

## S16 · Multi-card Brief（快讯小卡）

**内容形状**：6 张快讯卡（3×2），每张 = 标签 ≤ 4 字 + 一句话 ≤ 18 字。结构同 S04 六格，卡内加 mono 标签行。

## S17 · System Diagram（系统图）

**内容形状**：3 层 + 连线。用 S05 三层块 + 层间细线（`RECTANGLE` 高 0.02）+ 侧注 ≤ 10 字。

## S18 · Why Now（三论点 + 数据）

**内容形状**：3 个论点列，每列 = 论点 ≤ 8 字 + 数据 ≤ 5 字符 + 依据 ≤ 16 字。三列等宽，数据用 accent 大字（28pt）。

## S19 · Four Cards（四卡等权）

**内容形状**：4 个特性，每个 = 标题 ≤ 6 字 + 说明 ≤ 20 字。一行四卡（w=2.1，公式见 playbook 4.1），第一卡 accent 底。

## S20 · Stacked KPI Ledger（纵向账单）

**内容形状**：4-6 行账目，每行 = 名称 ≤ 8 字 + 数值 ≤ 6 字符 + 占比条。

```javascript
let s = pres.addSlide();
s.background = { color: C.paper };
s.addText("成本结构", { x: 0.5, y: 0.4, w: 9, h: 0.6, fontSize: 28, color: C.ink, fontFace: F.title, bold: true });
[
  { l: "人力", v: "58.9%", p: 0.589 },
  { l: "房租", v: "12.0%", p: 0.12 },
  { l: "耗材", v: "9.5%", p: 0.095 },
  { l: "其他", v: "19.6%", p: 0.196 },
].forEach((r, i) => {
  const y = 1.35 + i * 0.85;
  s.addText(r.l, { x: 0.5, y, w: 1.2, h: 0.4, fontSize: 14, color: C.ink, fontFace: F.body, bold: true });
  s.addShape(pres.shapes.RECTANGLE, { x: 1.9, y: y + 0.05, w: 5.5 * r.p, h: 0.3, fill: { color: i === 0 ? C.accent : C.paperTint } });
  s.addText(r.v, { x: 7.6, y, w: 1.9, h: 0.4, fontSize: 14, color: C.ink, fontFace: F.mono, align: "right" });
});
```

## S21 · Tech Spec Sheet（规格表）

**内容形状**：6-10 行键值对，键 ≤ 10 字，值 ≤ 16 字。用行线分隔（`RECTANGLE` 高 0.01，`paperTint`），mono 字体对齐数值列。

## S22 · Image Hero（顶图 + 三列 KPI）

**内容形状**：顶部 21:9 图（w=10, h=3.0，x=0, y=0 满宽出血）+ 标题 ≤ 10 字 + 三列 KPI。

```javascript
let s = pres.addSlide();
s.background = { color: C.paper };
s.addImage({ path: "images/01-hero.jpg", x: 0, y: 0, w: 10, h: 3.0 }); // 21:9 裁切
s.addText("新基地投产", { x: 0.5, y: 3.25, w: 9, h: 0.7, fontSize: 30, color: C.ink, fontFace: F.title, bold: true });
[{ n: "1200 头", l: "设计产能" }, { n: "8 个月", l: "建设周期" }, { n: "-18%", l: "单位成本" }]
  .forEach((k, i) => {
    const x = 0.5 + i * 3.1;
    s.addText(k.n, { x, y: 4.15, w: 2.8, h: 0.6, fontSize: 28, color: C.accent, fontFace: F.title, bold: true });
    s.addText(k.l, { x, y: 4.8, w: 2.8, h: 0.3, fontSize: 11, color: C.ink, fontFace: F.mono });
  });
```

---

## 地图页（原 S08 Map Component 的 pptx 替代）

pptx 无法内嵌交互地图。做法：用静态地图截图/生成图作为 `addImage` 放入 S08 右侧槽位（或 S22 顶图），点位标注用小圆点形状 + mono 文本叠加在图上。坐标按图片实际落位换算。

## 版式多样性硬规则

- 7-8 页 deck ≥ 6 个不同 S 版式；10 页以上 ≥ 8 个
- 不允许连续 3 页同一主体结构
- 开写代码前先列「页码 → S 版式 → 选用理由 → 图片槽位」草稿
