# 自定义主题 Custom Themes

用户自带品牌色 / VI 时，不走内置 9 套主题，走这里的三步流程：**extract → 人工确认 → validate**。
机器可读契约：[../themes/theme.schema.json](../themes/theme.schema.json)。

## 主题放哪里（优先级从高到低）

| 位置 | 用途 | 例子 |
|------|------|------|
| `./ppt-themes/*.theme.json` | 项目级，随 deck 仓库走 | 客户 A 的品牌主题 |
| `~/.ppt-design-skill/themes/*.theme.json` | 用户级，跨项目复用 | 你自己的 VI |
| `<skill>/themes/*.theme.json` | 内置 9 套（勿改，升级会覆盖） | ink-classic |

同名时项目级覆盖用户级覆盖内置。`python3 scripts/theme.py list` 的 SOURCE 列显示来源。

## 第 1 步 · extract（从用户 .pptx 提草稿）

```bash
python3 scripts/theme.py extract 客户VI.pptx --name client-a -o ppt-themes/client-a.theme.json
```

- 脚本读 `ppt/theme/theme1.xml` 的 a:clrScheme / a:fontScheme，映射成语义 token 草稿
- 草稿带 `"review": true` 和 notes（每条映射的来源与要复核的点）
- 映射启发式：ink←dk1、paper←lt1、accent←accent1、inkTint←dk2、paperTint←lt2；字体 ea 优先回退 latin，mono 默认 Consolas
- **必须人工复核**：品牌主色常在 accent2-6 而非 accent1；深色封面底该用 dk1 还是 dk2；mono 是否要换

## 第 2 步 · 人工确认

打开草稿，按 notes 逐条核对，改完删掉 `review` 和 `notes` 字段。

## 第 3 步 · validate

```bash
python3 scripts/theme.py validate ppt-themes/client-a.theme.json
```

规则（与 schema 一致）：name kebab-case 且与文件名一致；style ∈ magazine|swiss|custom；
colors 必含 ink/paper/accent，值为 6 位 hex（不带 #）或 "r,g,b" 三元组；accentRgb 与
accent 自动核对；fonts 必含 title/body/mono。

## 用进 deck

```javascript
// 主题 JSON 与 design-system.md 的 JS 预设字段一致
const theme = require("./ppt-themes/client-a.theme.json");
```

SKILL.md 规划步骤：先 `python3 scripts/theme.py list` 看可用主题；发现项目/用户级主题 →
追问用户是否优先使用。

## Token 门禁（写完必跑）

```bash
python3 scripts/qa/token_check.py slides/*.mjs --theme client-a
```

deck 里出现主题 token 之外的硬编码颜色 / 字体即 fail（exit 1）。例外用
`--allow-color` / `--allow-font` 显式声明。字体可用性另跑
`python3 scripts/qa/font_check.py output.pptx`。

## 规则

- 一份 deck 只用一套主题（含自定义），不中途换色
- 颜色一律 6 位 hex 不带 `#`（PptxGenJS 约定）
- 自定义主题也要过 contrast_check / cjk_overflow_check —— 品牌色对比度不够时先调
  paper/ink 而不是加例外
