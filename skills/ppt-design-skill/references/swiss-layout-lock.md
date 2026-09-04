# Swiss Layout Lock（pptx 版）

> 瑞士主题的硬约束。目的不是增加灵感，而是防止生成"看起来像 Swiss，但结构散架"的页面。
> 22 个版式的完整实现见 [../templates/layouts/swiss-layouts.md](../templates/layouts/swiss-layouts.md)。

## 硬规则

1. 正文页只能使用登记的 22 个版式 S01-S22；封面/收束用 S01/S10。
2. 不允许临时发明 S23/S24 或"自由组合"的正文结构。需要单张大图用 S22；多图用 S15/S16 网格改造。
3. 顶部中文标题默认**左上对齐**，贴近左上内容轴。只有 S03/S09/S10（statement/split 版式）允许强中心叙事。
4. 形状只画几何（块、线、圆、点阵）；文字一律用 `addText` 放在网格/卡片/caption 里，不要试图用形状拼文字。
5. 图片槽位和图片比例必须绑定：先定版式和槽位，再准备图片（21:9 顶图 / 16:10 主图 / 1:1 方图）。
6. accent 色占比 < 10%，只用于强调和数据；大面积底色只用 ink / paper / paperTint。

## 登记版式速查

| ID | 名称 | 内容形状 |
|---|---|---|
| S01 | Index Cover | 左大编号 + 右标题 |
| S02 | Vertical Timeline + KPI | 3-4 节点 + 4 KPI |
| S03 | Split Statement | 左巨字 + 右解释 |
| S04 | Six Cells | 6 概念卡（3×2） |
| S05 | Three Layers | 3 层架构块 |
| S06 | KPI Tower | 4 项不等高数据塔 |
| S07 | H-Bar Chart | 5-10 项排名（原生图表） |
| S08 | Duo Compare | Before/After 两侧 3-4 条 |
| S09 | Dot Matrix Statement | 点阵 + statement |
| S10 | Split Closing | 收束 + 行动块 |
| S11 | Horizontal Timeline | 4-7 步流程 |
| S12 | Manifesto + Ink Banner | 宣言 + 满宽横幅 |
| S13 | Three Forces | 3 个对等概念 |
| S14 | Loop Form | 4-5 环节闭环 |
| S15 | Matrix + Hero Stat | 8-12 项矩阵 + 大数字 |
| S16 | Multi-card Brief | 6 张快讯卡 |
| S17 | System Diagram | 系统图 + 连线 |
| S18 | Why Now | 3 论点 + 数据 |
| S19 | Four Cards | 4 卡等权 |
| S20 | Stacked KPI Ledger | 4-6 行账目 + 占比条 |
| S21 | Tech Spec Sheet | 6-10 行键值对 |
| S22 | Image Hero | 21:9 顶图 + 标题 + 3 KPI |

## 生成前检查

- [ ] 页面规划表已列「页码 → S 版式 → 选用理由 → 图片槽位」
- [ ] 7-8 页 ≥ 6 个不同版式；10 页以上 ≥ 8 个
- [ ] 无连续 3 页同一主体结构
- [ ] 数据页用原生图表（S07）或数据组件（S06/S20），没有文案硬填
