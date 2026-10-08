---
name: ppt-design-skill
description: "Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file; editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Includes 9 built-in design themes (5 magazine + 4 Swiss) and 32 layout templates. Trigger whenever the user mentions 'deck,' 'slides,' 'presentation,' or references a .pptx filename."
license: MIT
---

# PPT Design Skill

## Setup (first run)

The pptx tooling this skill calls — `scripts/office/*`, `add_slide.py`, `clean.py`, `thumbnail.py` — is **not vendored in this repo** (its license forbids redistribution). Fetch it from the upstream repository once, before first use:

```bash
python3 scripts/setup_upstream.py           # no-op when already installed
python3 scripts/setup_upstream.py --check   # verify installed
```

The script pins an upstream commit for reproducibility (`--ref` to override) and also fetches `upstream/SKILL.md` (design-ideas reference) plus the upstream `LICENSE.txt` that governs the fetched files. Python deps for the fetched tooling: `pip install defusedxml lxml Pillow "markitdown[pptx]"`.

## Quick Reference

| Task | Guide |
|------|-------|
| Read/analyze content | `python -m markitdown presentation.pptx` |
| Edit or create from template | Read [editing.md](editing.md) |
| Create from scratch | **规划 → 生成 → QA**（见下方 Creating from Scratch） |
| Design decisions (叙事/节奏/自适应) | Read [references/design-playbook.md](references/design-playbook.md) |
| Design themes & layouts | Read [design-system.md](design-system.md) |
| Theme tokens (list/validate/extract) | `python3 scripts/theme.py list` + [references/custom-themes.md](references/custom-themes.md) |
| Deterministic QA gate | `scripts/qa/`（溢出 / 对比度 / 边缘 / token / 字体，stdlib 独立） |
| Outline gate (规划门禁) | `python3 scripts/qa/outline_check.py outline.json` + [references/outline-schema.md](references/outline-schema.md) |
| Modular decks (≥15 页) | `python3 scripts/scaffold_deck.py outline.json --out-dir deck --theme <name>` + [references/modular-decks.md](references/modular-decks.md) |

---

## Reading Content

```bash
# Text extraction
python -m markitdown presentation.pptx

# Visual overview
python scripts/thumbnail.py presentation.pptx

# Raw XML
python3 -c "import sys,zipfile; zipfile.ZipFile(sys.argv[1]).extractall('unpacked')" presentation.pptx
```

---

## Editing Workflow

**Read [editing.md](editing.md) for full details.**

1. Analyze template with `thumbnail.py`
2. Extract → structural changes (`add_slide.py` / `<p:sldIdLst>` / `clean.py`) → edit content → zip → `validate.py --original`

---

## Creating from Scratch

**Creation workflow（三段式，顺序固定）：**

### Step 1 · 规划（必做，禁止跳过）

**Read [references/design-playbook.md](references/design-playbook.md)** — 叙事弧、页面规划表、明暗节奏、版式决策树、自适应规则、中文排版、密度控制。

**选主题**：`python3 scripts/theme.py list`（内置 9 套 + 项目 `./ppt-themes/` + 用户级）。发现项目/用户级主题 → 追问用户是否优先使用；用户自带品牌色 → [references/custom-themes.md](references/custom-themes.md) 的 extract 流程。

产出页面规划表（页码 → 版式 → 明暗 → 内容形状 → 视觉元素），落成 **outline.json** 并过规划门禁后再写代码：

```bash
python3 scripts/qa/outline_check.py outline.json   # exit 0=PASS；主题名/版式 id/多样性/连续重复全查
```

Schema 与注册版式 id 见 [references/outline-schema.md](references/outline-schema.md)。门禁不过先改 outline.json——规划阶段改一行，代码阶段返工一页。

### Step 2 · 生成

**Read [pptxgenjs.md](pptxgenjs.md)** for API details and corruption gotchas.

- 主题与配色：[design-system.md](design-system.md)（9 主题，只用安全字体）
- 版式代码：杂志风 [templates/layouts/magazine-layouts.md](templates/layouts/magazine-layouts.md) / 瑞士风 [templates/layouts/swiss-layouts.md](templates/layouts/swiss-layouts.md) / 分析模型 [templates/layouts/analysis-models.md](templates/layouts/analysis-models.md)（SWOT/PEST/画布/双钻/竞争定位）
- 组件配方：[templates/components.md](templates/components.md)
- 瑞士风硬约束：[references/swiss-layout-lock.md](references/swiss-layout-lock.md)
- **≥15 页走分模块管线**：`python3 scripts/scaffold_deck.py outline.json --out-dir deck --theme <name>` 生成 slide-NN.mjs + compile.mjs，契约与子代理并行填充见 [references/modular-decks.md](references/modular-decks.md)

### Step 3 · QA

**确定性门禁（先跑，全 PASS 再进视觉检查；exit 0=PASS / 1=有违规，可入 CI）：**

```bash
python3 scripts/qa/cjk_overflow_check.py output.pptx   # 文字溢出/越界（CJK 1em·半角 0.5em 估宽）
python3 scripts/qa/contrast_check.py output.pptx       # WCAG 对比度（4.5:1 正文 / 3:1 大字）
python3 scripts/qa/token_check.py slides/*.mjs --theme ink-classic  # 主题 token 门禁（硬编码色/字体即 fail）
python3 scripts/qa/font_check.py output.pptx                        # Office 安全字体 + 本地可用性（fc-list）
pdftoppm -png -r 150 output.pdf slide \
  && python3 scripts/qa/edge_check.py slide-*.png      # 渲染后边缘裁切/空页（纯 stdlib，PNG）
```

五个脚本纯 stdlib、独立解析（不依赖上游拉取件）。再按 [references/checklist.md](references/checklist.md) P0-P3 检查（见下方 QA 节）。

---

## Design Ideas

**Full design-ideas checklist** — inspiration palettes, typography rules, spacing, and the common-mistakes list — lives in the upstream reference fetched at setup: **read `upstream/SKILL.md` (§ Design Ideas)** after running `scripts/setup_upstream.py`. The sections below are this repo's own design system layered on top.

**Core principles (short form):**

- One dominant color carries the deck; accents stay sharp and rare
- Dark backgrounds for title + closing slides, light for content — or dark throughout for a premium feel
- Pick ONE visual motif and repeat it on every slide
- Every slide gets at least one visual element (image, chart, icon, shape) — no text-only slides
- Vary layouts across the deck; never repeat one layout more than 3 slides in a row

### Design System Quick Start

For pre-built themes and layout coordinates, see [design-system.md](design-system.md). It provides:
- **9 built-in themes** (5 magazine + 4 Swiss) with ready-to-use PptxGenJS color configs
- **32 layout templates** — 完整代码见 templates/layouts/（杂志 10 + 瑞士 22）
- **Office 安全字体** pairings for both magazine (serif) and Swiss (sans-serif) styles

**规划先行**：写代码前先读 [references/design-playbook.md](references/design-playbook.md)，产出页面规划表。版式坐标是基线不是牢房——按 playbook 第 4 节的自适应规则变形。

**7-Question Clarification** (optional best practice when user has only a vague idea):
1. **Audience & scenario**: Roadshow / internal share / tech launch / portfolio / academic?
2. **Duration & page count**: 10-12 / 15-20 / 25+ slides?
3. **Existing materials**: Documents / links / old PPT / data / images?
4. **Theme choice**: See Built-in themes below — magazine (elegant/humanistic) or Swiss (minimal/rational)?
5. **Style preference**: Serif titles with warm tones, or sans-serif with high-contrast accent colors?
6. **Language**: Chinese / English / bilingual?
7. **Deliverables**: PPTX only / also need cover images / also need web version?

**风格画廊技巧**（借鉴 humanize-ppt）：用户对主题犹豫时，不要盲选——用 2-4 套候选主题各渲染一张封面给用户挑，选定后再出全 deck。

**Theme usage rhythm**:
```
Cover       →  Main theme (consistent across deck)
Section     →  Same theme, variant switch (light/dark)
Data page   →  Same theme, light variant
Highlight   →  Same theme, dark variant
Closing     →  Same theme, dark variant or cover style
```

**Rule**: Never switch to a different theme mid-deck.

### Built-in Design System Themes

9 套内置主题（5 magazine + 4 Swiss）的完整色值与适用场景见 [design-system.md](design-system.md)。主题名即 token：`ink-classic` / `indigo-porcelain` / `forest-ink` / `kraft-paper` / `dune` / `swiss-blue` / `swiss-yellow` / `swiss-green` / `swiss-orange`（项目/用户级主题用 `python3 scripts/theme.py list` 查看）。

### Built-in Layout Templates

Coordinates in [design-system.md](design-system.md); complete code in `templates/layouts/` — 杂志 10 版式 + 瑞士 S01-S22 + 分析模型 5（SWOT/PEST/画布/双钻/竞争定位）。outline.json 引用这些注册 id（全表见 [references/outline-schema.md](references/outline-schema.md)）；版式多样性与连续重复上限由 `outline_check.py` 在规划阶段强制。

### 中文安全字体（内置主题已锁定）

**只用 Office 安全字体**——用户机器上没有的字体（Inter / Playfair / Noto 系列）会 fallback 到宋体。内置主题的中英文字体配对（magazine serif / Swiss sans）已锁定在 [design-system.md](design-system.md)，直接用主题 token，不要自造字体组合（`font_check.py` 会查）。

---

## QA (Required)

**Assume there are problems. Your job is to find them.**

Your first render is almost never correct. Approach QA as a bug hunt, not a confirmation step. If you found zero issues on first inspection, you weren't looking hard enough.

### Content QA

```bash
python -m markitdown output.pptx
```

Check for missing content, typos, wrong order.

**When using templates, check for leftover placeholder text:**

```bash
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```

If grep returns results, fix them before declaring success.

### File QA

```bash
python scripts/office/validate.py output.pptx                      # built from scratch
python scripts/office/validate.py output.pptx --original src.pptx  # built from a template
```

**If the deck came from a template, always pass `--original`** — it baselines schema/slide checks against the template so the template's own defects don't read as yours.

### Visual QA

**⚠️ USE SUBAGENTS** — even for 2-3 slides. You've been staring at the code and will see what you expect, not what's there. Subagents have fresh eyes.

Convert slides to images (see [Converting to Images](#converting-to-images)), then send the ready-to-use inspection prompt in [references/checklist.md](references/checklist.md) §「子代理看图提示词」to a subagent — it checks overlaps, overflow, collisions, gaps, contrast, and leftover placeholders per slide, and reports ALL issues including minor ones.

### Pre-Flight Checklist

Before declaring success, run through [references/checklist.md](references/checklist.md) (P0-P3 levels). **P0 must all pass before delivery**: no placeholder text, no overflow/cut-off, no overlapping elements, theme consistent, minimum font sizes.

**Verification Loop**

1. Generate slides → Convert to images → Inspect
2. **List issues found** (if none found, look again more critically)
3. Fix issues — **按失败模式目录的修复顺序：内容 → 结构 → 版式 → 样式，不要从样式开始修**
4. **Re-verify affected slides** — one fix often creates another problem
5. Repeat until a full pass reveals no new issues. **最多 3 轮**；3 轮后仍有 P0 问题，向用户说明剩余问题，不要无限重试。

**Do not declare success until you've completed at least one fix-and-verify cycle.**

---

## Design System Reference

| Document | Content |
|----------|---------|
| [design-system.md](design-system.md) | 9 built-in themes (5 magazine + 4 Swiss), layout coordinate quick-reference, safe font pairings |
| [references/design-playbook.md](references/design-playbook.md) | **设计决策手册：叙事弧、页面规划表、明暗节奏、版式决策树、自适应规则、中文排版、密度控制（写代码前必读）** |
| [templates/themes/magazine-themes.md](templates/themes/magazine-themes.md) | 5 magazine theme color details |
| [templates/themes/swiss-themes.md](templates/themes/swiss-themes.md) | 4 Swiss theme color details |
| [templates/layouts/magazine-layouts.md](templates/layouts/magazine-layouts.md) | 10 magazine layouts — complete PptxGenJS code + variants (authoritative) |
| [templates/layouts/swiss-layouts.md](templates/layouts/swiss-layouts.md) | 22 Swiss layouts S01-S22 — complete PptxGenJS code (authoritative) |
| [templates/layouts/analysis-models.md](templates/layouts/analysis-models.md) | Business analysis layouts: SWOT / PEST / business model canvas / double diamond / competitive positioning |
| [templates/components.md](templates/components.md) | Component cookbook (stat cards, callouts, icon rows, charts, chrome) |
| [references/checklist.md](references/checklist.md) | P0-P3 quality checklist (.pptx specific) |
| [references/outline-schema.md](references/outline-schema.md) | outline.json 规划门禁：schema、注册版式 id、检查规则 |
| [references/image-prompts.md](references/image-prompts.md) | Image generation prompt guide |
| [references/screenshot-framing.md](references/screenshot-framing.md) | Screenshot adaptation specs |
| [references/swiss-layout-lock.md](references/swiss-layout-lock.md) | 22 registered Swiss layouts, hard constraints |

---

## Converting to Images

Convert presentations to individual slide images for visual inspection:

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

This creates `slide-01.jpg`, `slide-02.jpg`, etc.

To re-render specific slides after fixes:

```bash
pdftoppm -jpeg -r 150 -f N -l N output.pdf slide-fixed
```

---

## Dependencies

- First run: `python3 scripts/setup_upstream.py` — fetches the tooling runtime (see Setup)
- `pip install "markitdown[pptx]"` - text extraction
- `pip install Pillow defusedxml lxml` - thumbnail grids / validate
- `npm install -g pptxgenjs` - creating from scratch
- LibreOffice (`soffice`) - PDF conversion (auto-configured for sandboxed environments via `scripts/office/soffice.py`)
- Poppler (`pdftoppm`) - PDF to images
