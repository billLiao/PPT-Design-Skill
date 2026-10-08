#!/usr/bin/env python3
"""Font preflight: Office-safe whitelist + local availability (fc-list).

Two checks per font found:
  1. Office-safe — in the safe-font whitelist (design-system.md § 字体体系)?
     Unsafe fonts fall back to 宋体 on user machines and wreck the design.
  2. Installed locally — fc-list lookup. Missing fonts make local preview
     renders (soffice/pdftoppm) lie: screenshots show fallback metrics.
     Warnings only; --strict promotes them to violations.

Inputs: .pptx (typeface= attributes in slide/master/layout/theme XML parts)
and/or .mjs/.js sources (fontFace literals). Mixed inputs allowed.

Usage:
  python3 scripts/qa/font_check.py deck.pptx
  python3 scripts/qa/font_check.py slides/ --strict
  python3 scripts/qa/font_check.py deck.pptx slides/*.mjs --json

Exit codes: 0 = pass (warnings allowed), 1 = violations, 2 = bad input.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # scripts/ for qa/_jsscan
from _jsscan import FONT_RE, strip_comments  # noqa: E402

SAFE_FONTS = {
    # 中文 Office 安全字体（design-system.md § 字体体系）
    "microsoft yahei", "微软雅黑", "stzhongsong", "华文中宋", "simsun", "宋体",
    "simhei", "黑体", "kaiti", "楷体", "fangsong", "仿宋", "dengxian", "等线",
    "stxihei", "华文细黑", "stkaiti", "华文楷体", "stfangsong", "华文仿宋",
    "stliti", "华文隶书", "lisu", "隶书", "youyuan", "幼圆",
    # 西文 Office 安全字体
    "arial", "arial black", "calibri", "calibri light", "cambria", "candara", "consolas",
    "constantia", "corbel", "courier new", "georgia", "impact",
    "palatino linotype", "tahoma", "times new roman", "trebuchet ms",
    "verdana", "segoe ui", "lucida console", "lucida sans unicode",
}

TYPEFACE_RE = re.compile(r'typeface="([^"]+)"')


def fc_families() -> set[str] | None:
    """Installed font families (casefolded), or None if fc-list unavailable."""
    exe = shutil.which("fc-list")
    if not exe:
        return None
    try:
        out = subprocess.run([exe, ":", "family"], capture_output=True,
                             text=True, timeout=15).stdout
    except (OSError, subprocess.TimeoutExpired):
        return None
    fams: set[str] = set()
    for line in out.splitlines():
        for fam in line.split(","):
            fam = fam.strip()
            if fam:
                fams.add(fam.casefold())
    return fams


def _theme_fonts(xml: str) -> set[str]:
    """Theme fontScheme: only majorFont/minorFont latin/ea/cs slots are author
    choices; the per-script <a:font> fallback list is Office boilerplate present
    in every pptxgenjs file — scanning it would flag ~40 false violations."""
    import xml.etree.ElementTree as ET

    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    out: set[str] = set()
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return set()
    for scheme in root.iter():
        if scheme.tag.endswith("}majorFont") or scheme.tag.endswith("}minorFont"):
            for child in scheme:
                tag = child.tag.rsplit("}", 1)[-1]
                if tag in ("latin", "ea", "cs") and child.get("typeface"):
                    out.add(child.get("typeface"))
    return out


def fonts_from_pptx(path: Path) -> set[str]:
    fonts: set[str] = set()
    with zipfile.ZipFile(path) as zf:
        for name in zf.namelist():
            if not (name.startswith(("ppt/slides/", "ppt/slideMasters/",
                                     "ppt/slideLayouts/", "ppt/theme/"))
                    and name.endswith(".xml")):
                continue
            xml = zf.read(name).decode("utf-8", "replace")
            if name.startswith("ppt/theme/"):
                fonts |= _theme_fonts(xml)
                continue
            for t in TYPEFACE_RE.findall(xml):
                if not t.startswith("+"):  # skip theme refs like +mj-lt
                    fonts.add(t)
    return fonts


def fonts_from_source(path: Path) -> set[str]:
    stripped = strip_comments(path.read_text(encoding="utf-8", errors="replace"))
    return set(FONT_RE.findall(stripped))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("inputs", nargs="+", help=".pptx files and/or .mjs/.js files or dirs")
    ap.add_argument("--strict", action="store_true",
                    help="treat not-installed-locally warnings as violations")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    files: list[Path] = []
    for item in args.inputs:
        p = Path(item)
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            for pat in ("*.mjs", "*.js"):
                files.extend(f for f in sorted(p.rglob(pat))
                             if "node_modules" not in f.parts)
        else:
            print(f"not found: {item}", file=sys.stderr)
            return 2
    if not files:
        print("no input files", file=sys.stderr)
        return 2

    local = fc_families()
    fonts: set[str] = set()
    for f in files:
        try:
            if f.suffix == ".pptx":
                fonts |= fonts_from_pptx(f)
            elif f.suffix in (".mjs", ".js"):
                fonts |= fonts_from_source(f)
            else:
                print(f"unsupported input (want .pptx/.mjs/.js): {f}", file=sys.stderr)
                return 2
        except (OSError, zipfile.BadZipFile) as e:
            print(f"{f}: cannot read ({e})", file=sys.stderr)
            return 2

    violations, warnings = [], []
    for font in sorted(fonts):
        if font.casefold() not in SAFE_FONTS:
            violations.append(
                f"{font}: not Office-safe — user machines fall back to 宋体")
        elif local is not None and font.casefold() not in local:
            warnings.append(
                f"{font}: not installed locally — preview renders use fallback "
                "metrics (deck itself is fine on Office)")

    if args.json:
        print(json.dumps({
            "files": [str(f) for f in files],
            "fonts": sorted(fonts),
            "fc_list": local is not None,
            "violations": violations,
            "warnings": warnings,
        }, ensure_ascii=False, indent=2))
    else:
        for v in violations:
            print(f"VIOLATION  {v}")
        for w in warnings:
            print(f"warning    {w}")
        if local is None:
            print("note       fc-list unavailable — local-availability check skipped")
        status = "PASS" if not violations else f"FAIL ({len(violations)} violation(s))"
        extra = f", {len(warnings)} warning(s)" if warnings else ""
        print(f"\nfont_check {status} — {len(fonts)} font(s) scanned{extra}")
    if violations:
        return 1
    return 1 if (args.strict and warnings) else 0


if __name__ == "__main__":
    sys.exit(main())
