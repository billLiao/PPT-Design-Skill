# Changelog

## v2.1 (2026-10-09)

### Added

- **Deterministic QA gates** (stdlib-only, exit 0/1/2, CI-ready): CJK overflow estimation (`cjk_overflow_check`), WCAG contrast (`contrast_check`), render edge-bleed (`edge_check`), deck-level theme-token gate (`token_check`), Office-safe font check (`font_check`)
- **Theme token system**: 9 built-in themes as JSON + `theme.schema.json`; `theme.py list/validate/extract`; resolution order project `./ppt-themes/` > user `~/.ppt-design-skill/themes/` > built-in
- **outline.json planning gate** (`outline_check.py` + schema doc): structure, theme resolution, registered layout ids (magazine 10 + S01–S22 + analysis 5, or `custom:<slug>`), diversity tiers (<7p ≥3 / 7–9p ≥5 / ≥10p ≥7), consecutive-repeat cap, dark/light rhythm, action-title checks
- **Action-title rules** in the design playbook (write conclusions, not topic labels) with topic-label detection in the outline gate
- **Modular pipeline for large decks (≥15 pages)**: `scaffold_deck.py` turns a validated outline into `slide-NN.mjs` modules + `compile.mjs`; locked `createSlide(pres, theme)` contract, `meta.page` ordering, single-page preview via `require.main`; ≤5-pages-per-subagent parallel fill; 5-slide demo deck (`demos/mini-deck/`) doubles as the CI fixture
- **GitHub Actions CI**: Node 20/22 matrix — upstream fetch → theme validate → outline gate (`--strict`) → compile demo → token gate → OOXML validate → overflow/contrast/font → LibreOffice render + edge check → artifact

### Changed

- SKILL.md slimmed 345 → ~260 lines; theme/font tables and checklists moved to their authoritative docs (`design-system.md`, `checklist.md`)
- `contrast_check`: containment fallback now wins over slide background — an opaque shape under text hides the slide bg (previously only active on bg-less slides, contradicting the docstring)
- `font_check`: theme fontScheme per-script fallback fonts (Office boilerplate, ~40 false violations) are no longer scanned — only major/minor latin/ea/cs slots; `Calibri Light` added to the safe list

## v2.0 (2026-10-08)

- **License compliance**: the pptx tooling runtime is no longer vendored — `scripts/setup_upstream.py` fetches it from [anthropics/skills](https://github.com/anthropics/skills) at install time (pinned commit, codeload + mirror fallback, manifest + `--check`); original content re-licensed MIT
- **Skill v2 design system**: design playbook (narrative arcs, page planning, theme rhythm, adaptive rules), pptx-native layouts, Office-safe fonts, Chinese typography tiers
