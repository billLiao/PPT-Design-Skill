#!/usr/bin/env python3
"""outline_check.py — 规划阶段确定性门禁：校验 deck 规划文件 outline.json。

在写任何幻灯片代码之前运行（SKILL.md Step 1 产出 outline.json → 本脚本全 PASS → Step 2 生成）。

检查项（违规=exit 1；警告默认放行，--strict 升级为违规）：
  结构   theme + slides[] 必填；page 从 1 连续递增不重不漏；title/summary 非空
  主题   theme 必须能解析（内置 9 套 / 项目 ./ppt-themes/ / 用户级，复用 theme.py）
  版式   layout 必须是注册 id（杂志 10 + S01-S22 + 分析模型 5）或 custom:<slug>
  多样性 <7 页 ≥3 种版式；7-9 页 ≥5 种；≥10 页 ≥7 种（对齐 references/checklist.md P1）
  连续   同一版式连续 ≥4 页 = 违规；连续 3 页 = 警告
  明暗   variant 只能 dark/light；连续 ≥3 页同明暗 = 警告；≥8 页无深底正文页 = 警告
  视觉   缺 visual 字段 = 警告（每页至少一个视觉元素）
  标题   话题式标签词（背景/总结/方案…）或 <4 字 = 警告（行动标题规则，design-playbook §2）

用法：
  python3 scripts/qa/outline_check.py outline.json [--strict] [--json]

Exit：0 = PASS / 1 = 有违规 / 2 = 文件缺失或 JSON 解析失败。
纯 stdlib；仅 import 本仓 theme.py（同为 stdlib，不依赖上游拉取件）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from theme import find_theme, load_theme, skill_root  # noqa: E402

MAGAZINE_LAYOUTS = [
    "cover", "section", "big-number", "two-column", "image-grid",
    "pipeline", "question", "quote", "before-after", "mixed",
]
SWISS_LAYOUTS = [f"S{i:02d}" for i in range(1, 23)]
ANALYSIS_LAYOUTS = [
    "swot", "pest", "business-model-canvas", "double-diamond", "competitive-positioning",
]
REGISTRY = set(MAGAZINE_LAYOUTS) | set(SWISS_LAYOUTS) | set(ANALYSIS_LAYOUTS)
CUSTOM_RE = re.compile(r"^custom:[a-z0-9][a-z0-9-]*$")

# (页数上限, 最少版式种类) —— 对齐 checklist.md P1：7-8 页 ≥5 种、10 页以上 ≥7 种
DIVERSITY_TIERS = [(6, 3), (9, 5), (10**9, 7)]

VALID_VISUALS = {"image", "chart", "icon", "shape", "diagram"}

# 话题式标题词（strip 后 exact match、不分大小写）——标题应写结论不写话题（design-playbook §2 行动标题）
TOPIC_TITLES = {
    "目录", "背景", "背景介绍", "简介", "介绍", "概述", "概况", "详情",
    "现状", "问题", "分析", "数据", "数据情况", "方案", "方案介绍", "方案说明",
    "计划", "规划", "目标", "优势", "劣势", "亮点", "成果", "进展", "汇报",
    "总结", "小结", "附录", "其他", "谢谢", "感谢", "q&a", "qa",
}


def _check_action_title(title: str, label: str, warnings: list[str]) -> None:
    if title.lower() in TOPIC_TITLES:
        warnings.append(
            f"{label}: 标题「{title}」是话题式标签——改成行动标题（写结论/判断，"
            f"观众只读标题也能听懂故事线，见 design-playbook §2）"
        )
    elif len(title) < 4:
        warnings.append(f"{label}: 标题「{title}」过短，写不下一个结论")


def builtin_theme_names() -> list[str]:
    d = skill_root() / "themes"
    return sorted(p.name.removesuffix(".theme.json") for p in d.glob("*.theme.json"))


def _runs(values: list[str]) -> list[tuple[str, int, int]]:
    """Run-length encode → [(value, start_index, length)]."""
    out: list[tuple[str, int, int]] = []
    for i, v in enumerate(values):
        if out and out[-1][0] == v:
            _, start, ln = out[-1]
            out[-1] = (v, start, ln + 1)
        else:
            out.append((v, i, 1))
    return out


def check(data) -> tuple[list[str], list[str], dict]:
    errors: list[str] = []
    warnings: list[str] = []
    stats: dict = {}

    if not isinstance(data, dict):
        return ["顶层必须是 JSON 对象（{theme, slides[]}）"], warnings, stats

    # --- theme ---
    theme_name = data.get("theme")
    theme_src = None
    if not isinstance(theme_name, str) or not theme_name.strip():
        errors.append("缺少必填字段 theme（字符串）")
    else:
        path, theme_src = find_theme(theme_name.strip())
        if path is None:
            errors.append(
                f"theme \"{theme_name}\" 无法解析（内置可用：{', '.join(builtin_theme_names())}；"
                f"项目 ./ppt-themes/ 与用户级 ~/.ppt-design-skill/themes/ 也参与查找）"
            )
        else:
            try:
                load_theme(path)
            except Exception as exc:  # noqa: BLE001
                errors.append(f"theme \"{theme_name}\" 的主题文件解析失败：{exc}")

    # --- slides ---
    slides = data.get("slides")
    if not isinstance(slides, list) or not slides:
        errors.append("缺少必填字段 slides（非空数组）")
        return errors, warnings, stats

    n = len(slides)
    pages: list[int] = []
    layouts: list[str] = []
    variants: list[str] = []

    for idx, slide in enumerate(slides, 1):
        label = f"slide #{idx}"
        if not isinstance(slide, dict):
            errors.append(f"{label}: 必须是对象")
            layouts.append("?")
            variants.append("light")
            continue

        page = slide.get("page")
        if isinstance(page, bool) or not isinstance(page, int):
            errors.append(f"{label}: page 必须是整数")
        else:
            pages.append(page)
            label = f"page {page}"

        layout = slide.get("layout")
        if not isinstance(layout, str) or not layout.strip():
            errors.append(f"{label}: 缺少必填字段 layout")
            layouts.append("?")
        else:
            layout = layout.strip()
            layouts.append(layout)
            if layout not in REGISTRY and not CUSTOM_RE.match(layout):
                errors.append(
                    f"{label}: layout \"{layout}\" 未注册（注册 id 见 references/outline-schema.md，"
                    f"自定义版式用 custom:<slug>）"
                )

        for field in ("title", "summary"):
            val = slide.get(field)
            if not isinstance(val, str) or not val.strip():
                errors.append(f"{label}: 缺少必填字段 {field}（非空字符串）")
        title = slide.get("title")
        if isinstance(title, str) and title.strip():
            _check_action_title(title.strip(), label, warnings)

        variant = slide.get("variant", "light")
        if variant not in ("dark", "light"):
            errors.append(f"{label}: variant 只能是 dark / light（缺省 light）")
            variant = "light"
        variants.append(variant)

        visual = slide.get("visual")
        if visual is None:
            warnings.append(
                f"{label}: 未声明 visual（每页至少一个视觉元素：image/chart/icon/shape/diagram）"
            )
        elif not (isinstance(visual, str) and visual.strip().lower() in VALID_VISUALS):
            warnings.append(f"{label}: visual \"{visual}\" 不在 image/chart/icon/shape/diagram 内")

    # page 序列
    if pages:
        dups = sorted({p for p in pages if pages.count(p) > 1})
        if dups:
            errors.append(f"page 重复：{dups}")
        expected = set(range(1, n + 1))
        missing = sorted(expected - set(pages))
        extra = sorted(set(pages) - expected)
        if missing:
            errors.append(f"page 缺号：{missing}（必须从 1 连续递增到 {n}）")
        if extra:
            errors.append(f"page 超出范围：{extra}（共 {n} 页）")

    # 版式多样性
    real = [x for x in layouts if x != "?"]
    distinct = len(set(real))
    min_distinct = next(th for upper, th in DIVERSITY_TIERS if n <= upper)
    if real and distinct < min_distinct:
        errors.append(
            f"版式多样性不足：{n} 页只用了 {distinct} 种（要求 ≥{min_distinct}）；"
            f"同版式变形不算新种类，拆内容换注册版式"
        )

    # 同版式连续重复
    for value, start, ln in _runs(layouts):
        if value == "?" or ln < 3:
            continue
        msg = f"page {start + 1} 起连续 {ln} 页同一版式 \"{value}\""
        if ln >= 4:
            errors.append(msg + "（上限 3 页）")
        else:
            warnings.append(msg + "（建议换版式）")

    # 明暗节奏（警告级，对齐 checklist.md P1）
    for value, start, ln in _runs(variants):
        if ln >= 3:
            warnings.append(f"page {start + 1} 起连续 {ln} 页同明暗（{value}），节奏偏平")
    if n >= 8 and "dark" not in variants[1:-1]:
        warnings.append("≥8 页的 deck 建议至少 1 个深底正文页（variant: dark）")

    stats = {
        "pages": n,
        "distinct_layouts": distinct,
        "min_required_layouts": min_distinct,
        "theme": theme_name if isinstance(theme_name, str) else None,
        "theme_source": theme_src,
    }
    return errors, warnings, stats


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="outline.json 规划门禁（SKILL.md Step 1）")
    ap.add_argument("outline", help="outline.json 路径")
    ap.add_argument("--strict", action="store_true", help="警告也视为失败")
    ap.add_argument("--json", action="store_true", help="JSON 输出（供 CI/脚本消费）")
    args = ap.parse_args(argv)

    path = Path(args.outline)
    if not path.is_file():
        print(f"ERROR: 找不到 {path}", file=sys.stderr)
        return 2
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        print(f"ERROR: {path} 不是合法 JSON：{exc}", file=sys.stderr)
        return 2

    errors, warnings, stats = check(data)
    if args.strict:
        errors.extend(warnings)
        warnings = []

    if args.json:
        print(json.dumps(
            {"result": "PASS" if not errors else "FAIL",
             "errors": errors, "warnings": warnings, "stats": stats},
            ensure_ascii=False, indent=2))
    else:
        src = f", theme source: {stats['theme_source']}" if stats.get("theme_source") else ""
        print(f"outline.json — {stats.get('pages', '?')} pages, "
              f"{stats.get('distinct_layouts', '?')} distinct layouts{src}")
        for e in errors:
            print(f"ERROR  {e}")
        for w in warnings:
            print(f"WARN   {w}")
        if errors:
            print(f"RESULT: FAIL（{len(errors)} 违规 / {len(warnings)} 警告）——先改 outline.json 再进 Step 2")
        elif warnings:
            print(f"RESULT: PASS（0 违规 / {len(warnings)} 警告；--strict 可升级警告为失败）")
        else:
            print("RESULT: PASS")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
