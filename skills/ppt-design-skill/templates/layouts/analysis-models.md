# 分析模型版式库（PptxGenJS 版）

> 商业分析常用框架的现成版式。来源：dashi-ppt-skill 的分析模型版式思路，适配 pptxgenjs。
> 变量约定同其他版式库：`C = theme.colors`，`F = fonts`，画布 10" × 5.625"。
> 这些版式**必须填真实分析结论**，不要拿文案硬凑框架。

---

## SWOT（2×2 四象限）

**内容形状**：4 象限，每象限 = 标签 ≤ 4 字 + 2-3 条 × ≤ 12 字。

```javascript
let s = pres.addSlide();
s.background = { color: C.paper };
s.addText("SWOT 分析", { x: 0.5, y: 0.4, w: 9, h: 0.6, fontSize: 28, color: C.ink, fontFace: F.title, bold: true });
const quads = [
  { t: "S 优势", items: ["自研意图分类模型", "3 天交付能力"], c: C.accent, tc: C.paper },
  { t: "W 劣势", items: ["数据积累不足", "无行业案例背书"], c: C.paperTint, tc: C.ink },
  { t: "O 机会", items: ["中小企业 AI 预算上升", "竞品聚焦大客户"], c: C.paperTint, tc: C.ink },
  { t: "T 威胁", items: ["大厂下沉", "开源方案成熟"], c: C.inkTint, tc: C.paper },
];
quads.forEach((q, i) => {
  const x = 0.5 + (i % 2) * 4.65, y = 1.2 + Math.floor(i / 2) * 2.05;
  s.addShape(pres.shapes.RECTANGLE, { x, y, w: 4.35, h: 1.85, fill: { color: q.c } });
  s.addText(q.t, { x: x + 0.25, y: y + 0.15, w: 3.8, h: 0.4, fontSize: 16, color: q.tc, fontFace: F.body, bold: true });
  s.addText(q.items.map((t, j) => ({ text: t, options: { breakLine: j < q.items.length - 1 } })),
    { x: x + 0.25, y: y + 0.6, w: 3.8, h: 1.1, fontSize: 12, color: q.tc, fontFace: F.body, lineSpacingMultiple: 1.5 });
});
```

**变体**：只突出一个象限时，仅该象限用 accent 底，其余统一 paperTint。

## PEST / PESTEL（四行外部环境）

**内容形状**：4 行，每行 = 维度 ≤ 6 字 + 因素 ≤ 20 字 + 影响（↑/↓/→）。

```javascript
let s = pres.addSlide();
s.background = { color: C.paper };
s.addText("外部环境扫描", { x: 0.5, y: 0.4, w: 9, h: 0.6, fontSize: 28, color: C.ink, fontFace: F.title, bold: true });
[
  { d: "政治 Policy", f: "数据合规监管趋严", i: "→" },
  { d: "经济 Economy", f: "企业降本增效预算向 AI 倾斜", i: "↑" },
  { d: "社会 Society", f: "一线员工对 AI 接受度提高", i: "↑" },
  { d: "技术 Technology", f: "小模型推理成本一年降 90%", i: "↑" },
].forEach((r, i) => {
  const y = 1.3 + i * 0.95;
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y, w: 2.2, h: 0.75, fill: { color: C.paperTint } });
  s.addText(r.d, { x: 0.7, y, w: 1.9, h: 0.75, fontSize: 13, color: C.ink, fontFace: F.body, bold: true, valign: "middle" });
  s.addText(r.f, { x: 3.0, y, w: 5.2, h: 0.75, fontSize: 14, color: C.ink, fontFace: F.body, valign: "middle" });
  s.addText(r.i, { x: 8.5, y, w: 1.0, h: 0.75, fontSize: 20, color: C.accent, fontFace: F.body, bold: true, align: "center", valign: "middle" });
});
```

## 商业模式画布（9 宫格）

**内容形状**：9 块，每块 = 标签 ≤ 5 字 + 2-3 条 × ≤ 10 字。标准布局：左 2 块（1:1）、中 3 块（KP/KA/VP 竖排规则见下）、右 2 块、底部 2 满宽。

```javascript
let s = pres.addSlide();
s.background = { color: C.paper };
s.addText("商业模式画布", { x: 0.5, y: 0.35, w: 9, h: 0.5, fontSize: 24, color: C.ink, fontFace: F.title, bold: true });
// 上区 5 列：KP | KA | VP | CR | CS（VP 列跨两行）
const top = [
  { t: "关键合作", x: 0.5 }, { t: "关键活动", x: 2.3 }, { t: "价值主张", x: 4.1 },
  { t: "客户关系", x: 5.9 }, { t: "客户细分", x: 7.7 },
];
top.forEach(b => {
  s.addShape(pres.shapes.RECTANGLE, { x: b.x, y: 1.0, w: 1.7, h: 1.7, fill: { color: C.paperTint } });
  s.addText(b.t, { x: b.x + 0.12, y: 1.1, w: 1.45, h: 0.35, fontSize: 12, color: C.ink, fontFace: F.body, bold: true });
});
s.addShape(pres.shapes.RECTANGLE, { x: 4.1, y: 2.8, w: 1.7, h: 1.0, fill: { color: C.accent } });
s.addText("成本结构", { x: 4.22, y: 2.9, w: 1.45, h: 0.35, fontSize: 12, color: C.paper, fontFace: F.body, bold: true });
s.addShape(pres.shapes.RECTANGLE, { x: 5.9, y: 2.8, w: 3.5, h: 1.0, fill: { color: C.paperTint } });
s.addText("收入来源", { x: 6.02, y: 2.9, w: 1.45, h: 0.35, fontSize: 12, color: C.ink, fontFace: F.body, bold: true });
s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 2.8, w: 3.5, h: 1.0, fill: { color: C.paperTint } });
s.addText("核心资源", { x: 0.62, y: 2.9, w: 1.45, h: 0.35, fontSize: 12, color: C.ink, fontFace: F.body, bold: true });
```

**注意**：9 块内容每块 ≤ 3 条；塞不下说明业务没想清楚，先删后画。

## 双钻模型（收敛-发散-收敛-发散）

**内容形状**：4 阶段，每阶段 = 阶段名 ≤ 6 字 + 动作 ≤ 14 字。两个菱形用旋转矩形近似（pptxgenjs 支持 `rotate`），或简化为 4 个 chevron 块。

```javascript
let s = pres.addSlide();
s.background = { color: C.paper };
s.addText("问题解决路径", { x: 0.5, y: 0.4, w: 9, h: 0.6, fontSize: 28, color: C.ink, fontFace: F.title, bold: true });
const phases = [
  { t: "探索问题", d: "访谈 + 数据定位真问题", c: C.paperTint },
  { t: "定义问题", d: "收敛为一句问题陈述", c: C.accent },
  { t: "发散方案", d: "多方案并行小成本验证", c: C.paperTint },
  { t: "交付方案", d: "选定方案落地度量", c: C.accent },
];
phases.forEach((p, i) => {
  const x = 0.5 + i * 2.3;
  s.addShape(pres.shapes.RECTANGLE, { x, y: 2.2, w: 2.1, h: 1.9, fill: { color: p.c } });  // 垂直居中：内容区 1.2-5.1
  s.addText(`0${i + 1}`, { x: x + 0.15, y: 2.35, w: 1.8, h: 0.5, fontSize: 22, color: p.c === C.accent ? C.paper : C.accent, fontFace: F.title, bold: true });
  s.addText(p.t, { x: x + 0.15, y: 2.9, w: 1.8, h: 0.4, fontSize: 15, color: p.c === C.accent ? C.paper : C.ink, fontFace: F.body, bold: true });
  s.addText(p.d, { x: x + 0.15, y: 3.3, w: 1.8, h: 0.7, fontSize: 11, color: p.c === C.accent ? C.paper : C.ink, fontFace: F.body, lineSpacingMultiple: 1.3 });
});
```

## 竞争格局（2×2 定位图）

**内容形状**：两轴各 ≤ 8 字 + 3-6 个竞品点（名称 ≤ 6 字）+ 我方位置（accent 大点）。

```javascript
let s = pres.addSlide();
s.background = { color: C.paper };
s.addText("竞争定位", { x: 0.5, y: 0.4, w: 9, h: 0.6, fontSize: 28, color: C.ink, fontFace: F.title, bold: true });
// 坐标区
const px = 1.6, py = 1.3, pw = 6.8, ph = 3.6;
s.addShape(pres.shapes.RECTANGLE, { x: px, y: py, w: pw, h: ph, fill: { color: C.paperTint } });
s.addShape(pres.shapes.RECTANGLE, { x: px + pw / 2 - 0.005, y: py, w: 0.01, h: ph, fill: { color: C.ink } });
s.addShape(pres.shapes.RECTANGLE, { x: px, y: py + ph / 2 - 0.005, w: pw, h: 0.01, fill: { color: C.ink } });
s.addText("自动化程度 ↑", { x: px, y: py + ph + 0.08, w: pw, h: 0.3, fontSize: 11, color: C.ink, fontFace: F.mono, align: "center" });
s.addText("服务深度 ↑", { x: 0.4, y: py, w: 1.1, h: ph, fontSize: 11, color: C.ink, fontFace: F.mono, valign: "middle" });
// 竞品点（x/y 为 0-1 相对位置）
[
  { n: "传统外包", x: 0.2, y: 0.75 }, { n: "SaaS 工具", x: 0.75, y: 0.25 }, { n: "咨询公司", x: 0.3, y: 0.3 },
].forEach(p => {
  s.addShape(pres.shapes.OVAL, { x: px + p.x * pw - 0.07, y: py + (1 - p.y) * ph - 0.07, w: 0.14, h: 0.14, fill: { color: C.ink } });
  s.addText(p.n, { x: px + p.x * pw - 0.6, y: py + (1 - p.y) * ph + 0.1, w: 1.2, h: 0.3, fontSize: 10, color: C.ink, fontFace: F.body, align: "center" });
});
// 我方位置
s.addShape(pres.shapes.OVAL, { x: px + 0.68 * pw - 0.11, y: py + (1 - 0.72) * ph - 0.11, w: 0.22, h: 0.22, fill: { color: C.accent } });
s.addText("我们", { x: px + 0.68 * pw - 0.6, y: py + (1 - 0.72) * ph + 0.14, w: 1.2, h: 0.3, fontSize: 11, color: C.accent, fontFace: F.body, bold: true, align: "center" });
```

---

## 使用规则

- 分析模型页在页面规划表里算独立版式类型，计入版式多样性
- 一份 deck 最多 1-2 个分析模型页——模型是论证工具，不是装饰
- 框架里的每一条都必须有材料支撑；填不出内容的格子直接删，不要凑对称
