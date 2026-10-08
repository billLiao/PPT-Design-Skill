#!/usr/bin/env python3
"""scaffold_deck.py — 从 outline.json 生成分模块 deck 工程（≥15 页推荐，契约见 references/modular-decks.md）。

用法：
  python3 scripts/scaffold_deck.py outline.json --out-dir deck --theme swiss-orange [--force]

行为：
  1. 先跑 outline_check.check()，规划门禁不过拒绝生成（先改 outline.json）
  2. 写 <out-dir>/compile.mjs + theme-loader.mjs（从 templates/ 复制）
  3. 把解析到的主题 JSON 复制到 <out-dir>/ppt-themes/（compile/token_check 从 deck 目录即可解析）
  4. 按 templates/slide-module.template.mjs 生成 slide-NN.mjs 桩（含页码/版式/明暗/标题/摘要头注释）
  5. 已存在的文件不覆盖（--force 才覆盖），保护已填内容
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "qa"))
from outline_check import check  # noqa: E402
from theme import find_theme  # noqa: E402

SKILL = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL / "templates"


def js_str(val: str) -> str:
    return json.dumps(val, ensure_ascii=False)


def fill_template(tpl: str, slide: dict, theme: str) -> str:
    page = slide["page"]
    variant = slide.get("variant", "light")
    out = tpl
    for key, val in {
        "{{PAGE2}}": f"{page:02d}",
        "{{PAGE}}": str(page),
        "{{LAYOUT}}": slide["layout"],
        "{{VARIANT}}": variant,
        "{{VARIANT_JS}}": "true" if variant == "dark" else "false",
        "{{TITLE}}": slide["title"],
        "{{SUMMARY}}": slide["summary"],
        "{{TITLE_JS}}": js_str(slide["title"]),
        "{{SUMMARY_JS}}": js_str(slide["summary"]),
        "{{THEME}}": theme,
    }.items():
        out = out.replace(key, val)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="从 outline.json 生成分模块 deck 工程")
    ap.add_argument("outline", help="outline.json 路径")
    ap.add_argument("--out-dir", default="deck", help="输出目录（默认 ./deck）")
    ap.add_argument("--theme", required=True, help="主题名或主题 JSON 路径")
    ap.add_argument("--force", action="store_true", help="覆盖已存在的文件")
    args = ap.parse_args(argv)

    src = Path(args.outline)
    if not src.is_file():
        print(f"ERROR: 找不到 {src}", file=sys.stderr)
        return 2
    try:
        data = json.loads(src.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR: {src} 不是合法 JSON：{exc}", file=sys.stderr)
        return 2

    errors, warnings, stats = check(data)
    for e in errors:
        print(f"ERROR  {e}")
    if errors:
        print("RESULT: 规划门禁未过，拒绝生成——先改 outline.json（python3 scripts/qa/outline_check.py）")
        return 1

    theme_path, theme_src = find_theme(args.theme)
    if theme_path is None:
        print(f"ERROR: 主题 \"{args.theme}\" 无法解析", file=sys.stderr)
        return 1
    theme_name = json.loads(theme_path.read_text(encoding="utf-8")).get("name", args.theme)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    written, skipped = [], []

    def put(rel: str, content: str) -> None:
        dest = out / rel
        if dest.exists() and not args.force:
            skipped.append(rel)
            return
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
        written.append(rel)

    for name in ("compile.mjs", "theme-loader.mjs"):
        put(name, (TEMPLATES / name).read_text(encoding="utf-8"))
    put(f"ppt-themes/{theme_name}.theme.json", theme_path.read_text(encoding="utf-8"))
    put("outline.json", json.dumps(data, ensure_ascii=False, indent=2) + "\n")

    tpl = (TEMPLATES / "slide-module.template.mjs").read_text(encoding="utf-8")
    for slide in data["slides"]:
        put(f"slide-{slide['page']:02d}.mjs", fill_template(tpl, slide, theme_name))

    for rel in written:
        print(f"WROTE  {out / rel}")
    for rel in skipped:
        print(f"SKIP   {out / rel}（已存在，--force 覆盖）")
    print(
        f"\n下一步：\n"
        f"  cd {out} && npm install pptxgenjs\n"
        f"  # 填充各 slide-NN.mjs（版式代码见 templates/layouts/），单页预览：node slide-NN.mjs\n"
        f"  node compile.mjs --theme {theme_name}\n"
        f"  # QA：python3 <skill>/scripts/qa/cjk_overflow_check.py output.pptx 等（见 SKILL.md Step 3）"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
