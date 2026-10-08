# outline.json 规划门禁（Step 1 产出物）

> 规划阶段把页面规划表落成 `outline.json`，先过 `scripts/qa/outline_check.py` 再写代码。
> 规划阶段改一行，代码阶段返工一页——门禁不过不要进 Step 2。

## 用法

```bash
python3 scripts/qa/outline_check.py outline.json           # exit 0=PASS / 1=违规 / 2=文件或 JSON 坏
python3 scripts/qa/outline_check.py outline.json --strict  # 警告也视为失败
python3 scripts/qa/outline_check.py outline.json --json    # CI/脚本消费
```

## Schema

```json
{
  "theme": "ink-classic",
  "language": "zh",
  "slides": [
    {
      "page": 1,
      "layout": "cover",
      "variant": "dark",
      "title": "2026 年度经营复盘",
      "summary": "一句话说清这页讲什么、观众看完记住什么",
      "visual": "chart"
    }
  ]
}
```

| 字段 | 级别 | 说明 |
|------|------|------|
| `theme` | 必填 | 主题名，`theme.py` 可解析：内置 9 套 / 项目 `./ppt-themes/` / 用户级 `~/.ppt-design-skill/themes/` |
| `language` | 可选 | `zh` / `en` / `bilingual` |
| `slides[].page` | 必填 | 整数，从 1 连续递增，不重不漏 |
| `slides[].layout` | 必填 | 注册版式 id（见下表）或 `custom:<slug>` |
| `slides[].variant` | 可选 | `dark` / `light`（缺省 light） |
| `slides[].title` | 必填 | 非空；写行动标题（结论/判断，见 design-playbook §2），不写话题标签 |
| `slides[].summary` | 必填 | 非空；一句话内容摘要（AST 状态转移的锚点，QA 时对照） |
| `slides[].visual` | 可选 | `image` / `chart` / `icon` / `shape` / `diagram`；缺省 = 警告（每页至少一个视觉元素） |

## 注册版式 id

| 家族 | id |
|------|-----|
| 杂志（10） | `cover` `section` `big-number` `two-column` `image-grid` `pipeline` `question` `quote` `before-after` `mixed` |
| 瑞士（22） | `S01`-`S22`（速查表见 [swiss-layout-lock.md](swiss-layout-lock.md)） |
| 分析模型（5） | `swot` `pest` `business-model-canvas` `double-diamond` `competitive-positioning` |
| 自定义 | `custom:<小写slug>`（如 `custom:timeline`）——注册版式变形确实不够用时才用 |

## 门禁规则（与 [checklist.md](checklist.md) P1 对齐）

| 类别 | 规则 | 级别 |
|------|------|------|
| 结构 | `theme`/`slides` 必填；`page` 1..N 连续；`title`/`summary` 非空 | 违规 |
| 主题 | `theme` 必须能被 theme.py 解析 | 违规 |
| 版式 | `layout` 必须注册或 `custom:` 前缀 | 违规 |
| 多样性 | <7 页 ≥3 种；7-9 页 ≥5 种；≥10 页 ≥7 种 | 违规 |
| 连续 | 同版式连续 ≥4 页 | 违规（连续 3 页 = 警告） |
| 明暗 | `variant` ∈ {dark, light}；连续 ≥3 页同明暗；≥8 页无深底正文页 | 警告 |
| 视觉 | 每页应声明 visual 元素 | 警告 |
| 标题 | 话题式标签词（背景/总结/方案…）或 <4 字 | 警告 |

## 示例（10 页 deck 片段）

```json
{
  "theme": "swiss-orange",
  "language": "zh",
  "slides": [
    { "page": 1, "layout": "S01", "variant": "dark", "title": "供应链 AI 落地复盘", "summary": "开场：一句话定位 + 汇报人", "visual": "shape" },
    { "page": 2, "layout": "S18", "title": "为什么是现在", "summary": "3 个论点 + 行业数据", "visual": "chart" },
    { "page": 3, "layout": "S13", "title": "三大痛点", "summary": "对账慢/催收难/报表迟，各配一个真实场景", "visual": "icon" },
    { "page": 4, "layout": "S02", "title": "落地路线图", "summary": "4 阶段时间线 + 每阶段 KPI", "visual": "diagram" },
    { "page": 5, "layout": "S07", "title": "对账效率对比", "summary": "上线前后 5 项指标排名条形图", "variant": "dark", "visual": "chart" },
    { "page": 6, "layout": "S19", "title": "四个部门怎么用", "summary": "财务/采购/销售/仓储各一张卡", "visual": "icon" },
    { "page": 7, "layout": "S20", "title": "投入产出账", "summary": "成本 4 行 + 回收周期占比条", "visual": "chart" },
    { "page": 8, "layout": "S08", "title": "上线前后", "summary": "Before/After 各 4 条工作方式对比", "visual": "shape" },
    { "page": 9, "layout": "S17", "title": "系统架构", "summary": "AI 网关与现有系统的接线图", "visual": "diagram" },
    { "page": 10, "layout": "S10", "variant": "dark", "title": "下一步", "summary": "收束 + 3 项行动请求", "visual": "shape" }
  ]
}
```

> 版式坐标是基线不是牢房：注册 id 锁定的是「内容形状」，坐标按 design-playbook 自适应规则变形，不需要 `custom:`。
