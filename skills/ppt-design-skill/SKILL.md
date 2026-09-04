---
name: ppt-design-skill
description: "Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file; editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Includes 9 built-in design themes (5 magazine + 4 Swiss) and 32 layout templates. Trigger whenever the user mentions 'deck,' 'slides,' 'presentation,' or references a .pptx filename."
license: Proprietary. LICENSE.txt has complete terms
---

# PPT Design Skill

## Quick Reference

| Task | Guide |
|------|-------|
| Read/analyze content | `python -m markitdown presentation.pptx` |
| Edit or create from template | Read [editing.md](editing.md) |
| Create from scratch | **规划 → 生成 → QA**（见下方 Creating from Scratch） |
| Design decisions (叙事/节奏/自适应) | Read [references/design-playbook.md](references/design-playbook.md) |
| Design themes & layouts | Read [design-system.md](design-system.md) |

---

## Reading Content

```bash
# Text extraction
python -m markitdown presentation.pptx

# Visual overview
python scripts/thumbnail.py presentation.pptx

# Raw XML
python scripts/office/unpack.py presentation.pptx unpacked/
```

---

## Editing Workflow

**Read [editing.md](editing.md) for full details.**

1. Analyze template with `thumbnail.py`
2. Unpack → manipulate slides → edit content → clean → pack

---

## Creating from Scratch

**Creation workflow（三段式，顺序固定）：**

### Step 1 · 规划（必做，禁止跳过）

**Read [references/design-playbook.md](references/design-playbook.md)** — 叙事弧、页面规划表、明暗节奏、版式决策树、自适应规则、中文排版、密度控制。

产出页面规划表（页码 → 版式 → 明暗 → 内容形状 → 视觉元素）后再写代码。

### Step 2 · 生成

**Read [pptxgenjs.md](pptxgenjs.md)** for API details and corruption gotchas.

- 主题与配色：[design-system.md](design-system.md)（9 主题，只用安全字体）
- 版式代码：杂志风 [templates/layouts/magazine-layouts.md](templates/layouts/magazine-layouts.md) / 瑞士风 [templates/layouts/swiss-layouts.md](templates/layouts/swiss-layouts.md)
- 组件配方：[templates/components.md](templates/components.md)
- 瑞士风硬约束：[references/swiss-layout-lock.md](references/swiss-layout-lock.md)

### Step 3 · QA

按 [references/checklist.md](references/checklist.md) P0-P3 检查（见下方 QA 节）。

---

## Design Ideas

**Don't create boring slides.** Plain bullets on a white background won't impress anyone. Consider ideas from this list for each slide.

### Before Starting

- **Pick a bold, content-informed color palette**: The palette should feel designed for THIS topic. If swapping your colors into a completely different presentation would still "work," you haven't made specific enough choices.
- **Dominance over equality**: One color should dominate (60-70% visual weight), with 1-2 supporting tones and one sharp accent. Never give all colors equal weight.
- **Dark/light contrast**: Dark backgrounds for title + conclusion slides, light for content ("sandwich" structure). Or commit to dark throughout for a premium feel.
- **Commit to a visual motif**: Pick ONE distinctive element and repeat it — rounded image frames, icons in colored circles, thick single-side borders. Carry it across every slide.

#### Design System Quick Start

For pre-built themes and layout coordinates, see [design-system.md](design-system.md). It provides:
- **9 built-in themes** (5 magazine + 4 Swiss) with ready-to-use PptxGenJS color configs
- **32 layout templates** — 完整代码见 templates/layouts/（杂志 10 + 瑞士 22）
- **Office 安全字体** pairings for both magazine (serif) and Swiss (sans-serif) styles

**规划先行**：写代码前先读 [references/design-playbook.md](references/design-playbook.md)，产出页面规划表。版式坐标是基线不是牢房——按 playbook 第 4 节的自适应规则变形。

**7-Question Clarification** (optional best practice when user has only a vague idea):
1. **Audience & scenario**: Roadshow / internal share / tech launch / portfolio / academic?
2. **Duration & page count**: 10-12 / 15-20 / 25+ slides?
3. **Existing materials**: Documents / links / old PPT / data / images?
4. **Theme choice**: See Color Palettes below — magazine (elegant/humanistic) or Swiss (minimal/rational)?
5. **Style preference**: Serif titles with warm tones, or sans-serif with high-contrast accent colors?
6. **Language**: Chinese / English / bilingual?
7. **Deliverables**: PPTX only / also need cover images / also need web version?

**Theme usage rhythm**:
```
Cover       →  Main theme (consistent across deck)
Section     →  Same theme, variant switch (light/dark)
Data page   →  Same theme, light variant
Highlight   →  Same theme, dark variant
Closing     →  Same theme, dark variant or cover style
```

**Rule**: Never switch to a different theme mid-deck.

### Color Palettes

Choose colors that match your topic — don't default to generic blue. Use these palettes as inspiration, or pick from the **built-in design system themes** below.

#### Built-in Design System Themes

Pre-configured themes with PptxGenJS-ready color values. See [design-system.md](design-system.md) for full config code.

**Magazine Style** (serif titles, warm tones, editorial feel):

| Theme | Ink (text/dark-bg) | Paper (light-bg) | Accent | Best for |
|-------|-------------------|------------------|--------|----------|
| **Ink Classic** | `0a0a0b` | `f1efea` | `d4a574` (warm gold) | General default, business, editorial |
| **Indigo Porcelain** | `0a1f3d` | `f1f3f5` | `4a90a4` (steel blue) | Tech, research, data, AI launch |
| **Forest Ink** | `1a2e1f` | `f5f1e8` | `6b8e5a` (moss) | Nature, culture, non-fiction |
| **Kraft Paper** | `2a1e13` | `eedfc7` | `b87333` (copper) | Humanities, nostalgia, literature |
| **Dune** | `1f1a14` | `f0e6d2` | `c4a265` (sand) | Art, design, creative, gallery |

**Swiss Style** (sans-serif, grid-driven, high-contrast accent):

| Theme | Ink | Paper | Accent | Best for |
|-------|-----|-------|--------|----------|
| **Swiss IKB Blue** | `1a1a1a` | `f5f5f5` | `002FA7` (Klein blue) | Minimal, data-driven, rational |
| **Swiss Lemon Yellow** | `1a1a1a` | `f5f5f5` | `FFD700` (yellow) | Energetic, optimistic, bold |
| **Swiss Lime Green** | `1a1a1a` | `f5f5f5` | `CCFF00` (lime) | Innovation, tech, futuristic |
| **Swiss Safety Orange** | `1a1a1a` | `f5f5f5` | `FF5F00` (orange) | Warning, emphasis, high-impact |

#### General Inspiration Palettes

| Theme | Primary | Secondary | Accent |
|-------|---------|-----------|--------|
| **Midnight Executive** | `1E2761` (navy) | `CADCFC` (ice blue) | `FFFFFF` (white) |
| **Forest & Moss** | `2C5F2D` (forest) | `97BC62` (moss) | `F5F5F5` (cream) |
| **Coral Energy** | `F96167` (coral) | `F9E795` (gold) | `2F3C7E` (navy) |
| **Warm Terracotta** | `B85042` (terracotta) | `E7E8D1` (sand) | `A7BEAE` (sage) |
| **Ocean Gradient** | `065A82` (deep blue) | `1C7293` (teal) | `21295C` (midnight) |
| **Charcoal Minimal** | `36454F` (charcoal) | `F2F2F2` (off-white) | `212121` (black) |
| **Teal Trust** | `028090` (teal) | `00A896` (seafoam) | `02C39A` (mint) |
| **Berry & Cream** | `6D2E46` (berry) | `A26769` (dusty rose) | `ECE2D0` (cream) |
| **Sage Calm** | `84B59F` (sage) | `69A297` (eucalyptus) | `50808E` (slate) |
| **Cherry Bold** | `990011` (cherry) | `FCF6F5` (off-white) | `2F3C7E` (navy) |

### For Each Slide

**Every slide needs a visual element** — image, chart, icon, or shape. Text-only slides are forgettable.

**Layout options:**
- Two-column (text left, illustration on right)
- Icon + text rows (icon in colored circle, bold header, description below)
- 2x2 or 2x3 grid (image on one side, grid of content blocks on other)
- Half-bleed image (full left or right side) with content overlay)

**Built-in layout templates** (see [design-system.md](design-system.md) for coordinates):

*Magazine Style* (10 layouts): `cover`, `section`, `big-number`, `two-column`, `image-grid`, `pipeline`, `question`, `quote`, `before-after`, `mixed`

*Swiss Style* (22 layouts): `S01`-`S22` grid-based layouts with strict 12-column alignment

**Layout diversity rules** (from `references/checklist.md`):
- Avoid using the same layout for every slide — vary columns, cards, and callouts
- Mix at least 4 different layout types per deck
- Never use the same layout type more than 3 times in a row
- Match information density to layout (cover = lowest, appendix = highest)

**Data display:**
- Large stat callouts (big numbers 60-72pt with small labels below)
- Comparison columns (before/after, pros/cons, side-by-side options)
- Timeline or process flow (numbered steps, arrows)

**Visual polish:**
- Icons in small colored circles next to section headers
- Italic accent text for key stats or taglines

### Typography

**Choose an interesting font pairing** — don't default to Arial. Pick a header font with personality and pair it with a clean body font.

#### General Pairings

| Header Font | Body Font |
|-------------|-----------|
| Georgia | Calibri |
| Arial Black | Arial |
| Calibri | Calibri Light |
| Cambria | Calibri |
| Trebuchet MS | Calibri |
| Impact | Arial |
| Palatino | Garamond |
| Consolas | Calibri |

#### Design System Font Pairings

For built-in themes, use these pre-mapped pairings (see [design-system.md](design-system.md)). **只用 Office 安全字体**——用户机器上没有的字体（Inter / Playfair / Noto 系列）会 fallback 到宋体：

**Magazine Style** (serif headers, editorial):

| Role | 中文 deck | 英文 deck |
|------|-----------|-----------|
| Title (serif) | STZhongsong（华文中宋） | Cambria |
| Body (sans) | Microsoft YaHei | Calibri |
| Mono (labels) | Consolas | Consolas |

**Swiss Style** (sans-serif throughout, grid-driven):

| Role | 中文 deck | 英文 deck |
|------|-----------|-----------|
| Title (sans bold) | Microsoft YaHei | Arial |
| Body (sans) | Microsoft YaHei | Arial |
| Mono (labels) | Consolas | Consolas |

| Element | Size |
|---------|------|
| Slide title | 36-44pt bold |
| Section header | 20-24pt bold |
| Body text | 14-16pt |
| Captions | 10-12pt muted |

### Spacing

- 0.5" minimum margins
- 0.3-0.5" between content blocks
- Leave breathing room—don't fill every inch

### Avoid (Common Mistakes)

- **Don't repeat the same layout** — vary columns, cards, and callouts across slides
- **Don't center body text** — left-align paragraphs and lists; center only titles
- **Don't skimp on size contrast** — titles need 36pt+ to stand out from 14-16pt body
- **Don't default to blue** — pick colors that reflect the specific topic
- **Don't mix spacing randomly** — choose 0.3" or 0.5" gaps and use consistently
- **Don't style one slide and leave the rest plain** — commit fully or keep it simple throughout
- **Don't create text-only slides** — add images, icons, charts, or visual elements; avoid plain title + bullets
- **Don't forget text box padding** — when aligning lines or shapes with text edges, set `margin: 0` on the text box or offset the shape to account for padding
- **Don't use low-contrast elements** — icons AND text need strong contrast against the background; avoid light text on light backgrounds or dark text on dark backgrounds
- **NEVER use accent lines under titles** — these are a hallmark of AI-generated slides; use whitespace or background color instead

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

### Visual QA

**⚠️ USE SUBAGENTS** — even for 2-3 slides. You've been staring at the code and will see what you expect, not what's there. Subagents have fresh eyes.

Convert slides to images (see [Converting to Images](#converting-to-images)), then use this prompt:

```
Visually inspect these slides. Assume there are issues — find them.

Look for:
- Overlapping elements (text through shapes, lines through words, stacked elements)
- Text overflow or cut off at edges/box boundaries
- Decorative lines positioned for single-line text but title wrapped to two lines
- Source citations or footers colliding with content above
- Elements too close (< 0.3" gaps) or cards/sections nearly touching
- Uneven gaps (large empty area in one place, cramped in another)
- Insufficient margin from slide edges (< 0.5")
- Columns or similar elements not aligned consistently
- Low-contrast text (e.g., light gray text on cream-colored background)
- Low-contrast icons (e.g., dark icons on dark backgrounds without a contrasting circle)
- Text boxes too narrow causing excessive wrapping
- Leftover placeholder content

For each slide, list issues or areas of concern, even if minor.

Read and analyze these images:
1. /path/to/slide-01.jpg (Expected: [brief description])
2. /path/to/slide-02.jpg (Expected: [brief description])

Report ALL issues found, including minor ones.
```

### Pre-Flight Checklist

Before declaring success, run through `references/checklist.md` (P0-P3 levels):

**P0 — Must fix before delivery:**
- [ ] No placeholder text remaining (`xxxx`, `lorem`, `ipsum`, `this page layout`)
- [ ] No text overflow or cut-off at slide edges
- [ ] No overlapping elements (text through shapes, lines through words)
- [ ] Theme consistent across all slides (no mid-deck color switch)
- [ ] Font sizes meet minimums (title >= 36pt, body >= 14pt)

**P1 — Should fix:**
- [ ] Layout variety >= 4 different types
- [ ] No same layout repeated > 3 times in a row
- [ ] Margins >= 0.5" on all sides
- [ ] Contrast sufficient (no light-on-light or dark-on-dark text)

**P2 — Polish:**
- [ ] No accent lines under titles (whitespace or background color instead)
- [ ] Icons have contrasting circular backgrounds where needed
- [ ] Image proportions match layout slots (no stretched/squashed images)

**P3 — Nice to have:**
- [ ] File size reasonable (< 50MB for image-heavy decks)
- [ ] Cross-device compatible fonts used
- [ ] Print preview readable in grayscale

### Verification Loop

1. Generate slides → Convert to images → Inspect
2. **List issues found** (if none found, look again more critically)
3. Fix issues
4. **Re-verify affected slides** — one fix often creates another problem
5. Repeat until a full pass reveals no new issues

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
| [templates/components.md](templates/components.md) | Component cookbook (stat cards, callouts, icon rows, charts, chrome) |
| [references/checklist.md](references/checklist.md) | P0-P3 quality checklist (.pptx specific) |
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

- `pip install "markitdown[pptx]"` - text extraction
- `pip install Pillow` - thumbnail grids
- `npm install -g pptxgenjs` - creating from scratch
- LibreOffice (`soffice`) - PDF conversion (auto-configured for sandboxed environments via `scripts/office/soffice.py`)
- Poppler (`pdftoppm`) - PDF to images
