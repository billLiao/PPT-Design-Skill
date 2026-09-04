# 组件手册（PptxGenJS 版）

> 可复用组件的 pptxgenjs 配方。变量约定：`C = theme.colors`，`F = fonts`，画布 10" × 5.625"。
> 组件是"积木"，版式是"图纸"——先选版式（layouts/），再用组件填充。

---

## Kicker / Tag（mono 标签）

页面顶部的分类标签，全 deck 统一用这一种样式。

```javascript
s.addText("KICKER · 章节", { x: 0.5, y: 0.45, w: 6, h: 0.3,
  fontSize: 12, color: C.accent, fontFace: F.mono, charSpacing: 3 });
```

## Stat Card（数字卡）

```javascript
s.addShape(pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: C.paperTint } });
s.addText("92%", { x: x+0.2, y: y+0.25, w: w-0.4, h: 0.8,
  fontSize: 40, color: C.accent, fontFace: F.title, bold: true });
s.addText("意图分类准确率", { x: x+0.2, y: y+1.15, w: w-0.4, h: 0.35,
  fontSize: 14, color: C.ink, fontFace: F.body, bold: true });
s.addText("few-shot 后 70% → 92%", { x: x+0.2, y: y+1.55, w: w-0.4, h: 0.6,
  fontSize: 11, color: C.ink, fontFace: F.body, lineSpacingMultiple: 1.3 });
```

**规则**：并列卡片同底色同尺寸；突出只突出一张（换 accent 底 + paper 字）。

## Callout（引用框）

```javascript
s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 3.6, w: 9, h: 1.2, fill: { color: C.paperTint } });
s.addText("问题不在模型，在检索链路。", { x: 0.8, y: 3.6, w: 8.4, h: 1.2,
  fontSize: 16, color: C.ink, fontFace: F.body, italic: true, valign: "middle" });
```

## Icon Row（图标行）

```javascript
s.addShape(pres.shapes.OVAL, { x: 4.7, y, w: 0.42, h: 0.42, fill: { color: C.accent } });
s.addText("①", { x: 4.7, y, w: 0.42, h: 0.42, fontSize: 14,
  color: C.paper, fontFace: F.body, align: "center", valign: "middle" });
s.addText("接入", { x: 5.3, y: y-0.02, w: 4.2, h: 0.35, fontSize: 15, color: C.ink, fontFace: F.body, bold: true });
s.addText("工单系统 API 自动同步", { x: 5.3, y: y+0.33, w: 4.2, h: 0.35, fontSize: 12, color: C.ink, fontFace: F.body });
```

**规则**：深底上的图标必须加浅色圆底；圆内符号用 ①②③ 或单字符，不用 emoji。

## Ghost Number（巨型背景字）

章节页/收束页用，压在内容层后面（先画字再画内容）。

```javascript
s.addText("01", { x: 5.5, y: 3.0, w: 4.5, h: 2.6,
  fontSize: 160, color: C.paperTint, fontFace: F.title, bold: true });
```

## Rowline（表格行）

```javascript
[
  { l: "人力成本", v: "58.9%" }, { l: "会员计划毛利率", v: "95%" },
].forEach((r, i) => {
  const y = 1.4 + i * 0.62;
  s.addText(r.l, { x: 0.5, y, w: 4, h: 0.4, fontSize: 14, color: C.ink, fontFace: F.body });
  s.addText(r.v, { x: 6.5, y, w: 3, h: 0.4, fontSize: 14, color: C.ink, fontFace: F.mono, align: "right", bold: true });
  s.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: y+0.48, w: 9, h: 0.008, fill: { color: C.paperTint } });
});
```

## Figure + Caption（图片框）

```javascript
s.addImage({ path: "images/03-demo.png", x, y, w, h });   // 比例必须匹配槽位
s.addText("图 3 · 上线后工单分布", { x, y: y+h+0.1, w, h: 0.3,
  fontSize: 10, color: C.ink, fontFace: F.mono });
```

**规则**：多图组统一比例统一高度；截图类图片先按 screenshot-framing.md 做画布适配再插入。

## Chart 预设（原生图表）

```javascript
s.addChart(pres.charts.BAR, [{ name: "系列", labels: [...], values: [...] }], {
  x: 0.5, y: 1.2, w: 9, h: 3.9, barDir: "bar",
  chartColors: [C.accent], showLegend: false, showValue: true,
  dataLabelPosition: "outEnd", dataLabelColor: C.ink, dataLabelFontSize: 11,
  dataLabelFormatCode: "0.0",   // 小数数据必须指定，否则渲染成整数
  catAxisLabelColor: C.ink, catAxisLabelFontSize: 11,
  valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" },
});
```

**规则**：能用原生图表就不贴图；单系列隐藏图例；配色只用主题色；数据点超限先合并类目（见 design-playbook.md 第 6 节）。

## 页脚（Chrome）

```javascript
s.addText("一人公司 · 2026", { x: 0.5, y: 5.25, w: 4, h: 0.25,
  fontSize: 9, color: C.ink, fontFace: F.mono });
s.addText("03", { x: 9.0, y: 5.25, w: 0.5, h: 0.25,
  fontSize: 9, color: C.ink, fontFace: F.mono, align: "right" });
```

**规则**：位置全 deck 一致；封面/章节页可省略。

---

## 禁用组件（HTML 遗留，pptx 不适用）

- ❌ Motion 动效 / `data-anim` / recipe —— pptx 无动效系统
- ❌ vw/vh 单位、CSS 类名、`<section>` 骨架 —— pptx 用英寸坐标
- ❌ lucide 图标库、WebGL 背景、MapLibre 交互地图
- ❌ 渐变填充（pptxgenjs 不支持，用纯色或渐变图片代替）
