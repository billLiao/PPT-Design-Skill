# 质量检查清单（Checklist · .pptx 专用）

> 按 P0 → P3 顺序检查。P0 全部通过才能交付。
> 本清单针对 **pptxgenjs 生成的 .pptx 文件**。HTML/Web 概念（vw/vh、动效、lucide）不适用于 pptx，不要套用。

## 🔴 P0 · 必须修复，否则不能交付

### 0-1. 文件完整性
- [ ] `python scripts/office/validate.py output.pptx` 通过（schema / relationship / chart 检查）
- [ ] 无 `#` 前缀或 8 位 hex 颜色值（会损坏文件，必须 6 位无 `#`）
- [ ] 阴影 `offset` ≥ 0（向上阴影用 `angle: 270`）
- [ ] 堆叠柱状图 `dataLabelPosition` 只能是 `ctr` / `inEnd` / `inBase`（`outEnd` 损坏文件）
- [ ] combo 图表用了 `secondaryValAxis` 时，`valAxes` + `catAxes` 各两条都已提供

**已知误报**（pptxgenjs 库级怪癖，PowerPoint 正常打开，不要追）：
- `presentation.xml`: `notesMasterIdLst` 元素顺序不符合 XSD
- `chartN.xml`: `axId` 位置不符合 XSD

**无 LibreOffice 时的降级 QA**（python-pptx 边界检查）：

```python
from pptx import Presentation
from pptx.util import Emu
p = Presentation("output.pptx")
W, H = 10.0, 5.625   # LAYOUT_16x9
for i, s in enumerate(p.slides, 1):
    for sh in s.shapes:
        x, y = Emu(sh.left).inches, Emu(sh.top).inches
        w, h = Emu(sh.width).inches, Emu(sh.height).inches
        assert x >= -0.01 and y >= -0.01 and x+w <= W+0.01 and y+h <= H+0.01, f"slide{i} 越界"
```

### 0-2. 文字边界
- [ ] `python3 scripts/qa/cjk_overflow_check.py output.pptx` 通过（自动估宽：垂直溢出 / 不可断行 token / 越界形状）
- [ ] 无文字溢出文本框 / 卡片 / 幻灯片边缘（中文按 字号×1.0 预估宽度）
- [ ] 无元素超出画布（10" × 5.625"），坐标越界不会报错，只会不可见
- [ ] 无元素互相重叠（文字穿过色块、线条压字）
- [ ] 长标题换行后，下方元素没有被压住（装饰元素按单行设计、标题变两行是最常见的翻车）

### 0-3. 内容正确
- [ ] 无占位符残留（`xxxx` / `lorem` / `TODO` / `[insert`）
- [ ] `python -m markitdown output.pptx` 核对：无缺页、无错序、无错别字
- [ ] 数据页的数字与来源材料一致
- [ ] 图表数据标签与正文陈述一致

### 0-4. 主题一致性
- [ ] 全 deck 只用一套主题（颜色未中途切换）
- [ ] 明暗变体只来自主题自身（ink / paper / tint），没有自造 hex
- [ ] 字号达到下限：页面标题 ≥ 26pt，正文 ≥ 14pt，caption ≥ 10pt

## 🟠 P1 · 应该修复

- [ ] 版式多样性：7-8 页 ≥ 5 种版式，10 页以上 ≥ 7 种
- [ ] 无连续 3 页同一版式结构
- [ ] 明暗节奏：无连续 3 页同明暗；8 页以上有 ≥1 个深底正文页
- [ ] 边距 ≥ 0.5"，内容块间距 0.3-0.5" 且全 deck 一致
- [ ] 对比度：无浅底浅字 / 深底深字；深底上的 accent 文字已做提亮（如克莱因蓝在深底上不可读）
- [ ] `python3 scripts/qa/contrast_check.py output.pptx` 通过（WCAG 4.5:1 正文 / 3.0:1 大字）
- [ ] 正文左对齐（只有标题/大数字可居中）
- [ ] 图表有数据标签、主题化配色、单系列隐藏图例
- [ ] 每页正文 ≤ 90 字（中文），超标拆页

## 🟡 P2 · 打磨

- [ ] 无 accent 色条 / 标题下划线（AI 味标志，用留白或底色代替）
- [ ] 卡片样式统一：并列卡片同底色同圆角，突出只突出一张
- [ ] 图标有对比底色（深底上的深色图标加了浅色圆底）
- [ ] 图片比例匹配槽位（无拉伸压扁），多图组统一比例
- [ ] 数字/英文标签用 mono 字体，与中文正文区分
- [ ] 页码 / 页脚位置全 deck 一致

## 🟢 P3 · 锦上添花

- [ ] 文件体积合理（图片多的 deck < 50MB）
- [ ] 灰度打印可读（对比度不只靠色相）
- [ ] 演讲者备注已写（`slide.addNotes()`，不要写在画面文本框里）

---

## 失败模式目录（QA 时按此排查）

> 借鉴 Akxan/ppt-agent-skill 与 humanize-ppt 的失败模式思路。每条写明"观众视角会看到什么"。

| # | 失败模式 | 观众视角 | 修法 |
|---|----------|----------|------|
| 1 | 文字溢出/裁切 | 字被切一半、压到下一元素 | 加宽文本框或删文案（先删文案） |
| 2 | 元素遮挡 | 页码/装饰盖住正文，句子被"吃掉" | 移开装饰或缩小正文区外的元素 |
| 3 | underfill 填不满 | 大片空白，页面像没做完 | 内容太少就换轻量版式或加大字号一档 |
| 4 | 密度超标 | 挤到看不动，观众直接放弃 | 删 30% 文案或拆页 |
| 5 | 装饰替代内容 | 页面好看但什么都没说 | 删装饰，补真实内容（AST 状态转移） |
| 6 | 层级扁平 | 全页一个字号字重，不知道先看哪 | 拉开字号档位，标题加粗 |
| 7 | 低对比 | 浅底浅字/深底深字，投影后消失 | 换 ink/paper 主题色对 |
| 8 | AST 漂移 | 页面内容与规划表的任务对不上 | 回到规划表改内容，不是改样式 |

**修复顺序铁律**：内容 → 结构（拆页/换版式）→ 版式（坐标/对齐）→ 样式（字号/颜色）。
**永远不要从样式开始修**——样式修不好的页面，问题几乎都在内容和结构。

## 视觉 QA 执行方式

1. 转图片（需要 LibreOffice + poppler）：
   ```bash
   python scripts/office/soffice.py --headless --convert-to pdf output.pptx
   pdftoppm -png -r 150 output.pdf slide
   python3 scripts/qa/edge_check.py slide-*.png   # 边缘裁切/空页像素门禁（先跑，PASS 再人工看图）
   ```
2. **用子代理看图**（自己盯代码会只看到预期）。逐页检查 P0-2 / P1 的每一项。
3. 环境没有 LibreOffice 时，降级方案：
   - `python -m markitdown output.pptx` 做内容核对
   - `python scripts/office/validate.py` 做结构校验
   - 用 python-pptx 读回坐标做边界检查（x+w ≤ 10, y+h ≤ 5.625）
   - 明确告知用户"未做视觉渲染核对"
4. 修复后**只重渲染受影响的页**，但必须复检相邻页（一次修复常引入新问题）。
5. **QA 轮次封顶 3 轮**（借鉴 humanize-ppt）：3 轮后仍有 P0 问题，停下来向用户说明剩余问题，不要无限重试。
