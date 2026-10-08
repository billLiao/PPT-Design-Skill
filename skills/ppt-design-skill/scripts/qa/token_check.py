#!/usr/bin/env python3
"""Deck-level design-token gate: hardcoded colors/fonts outside the theme fail.

Scans PptxGenJS slide sources (.mjs/.js) for color literals and fontFace
values that are not part of the deck's theme tokens. Closes the loop with
scripts/theme.py: a deck either uses theme tokens or this gate fails — no
silent one-off hex values drifting across slides.

Scanned patterns (comment-stripped source, see _jsscan.py):
  color|fill|background|line|outline|glow|shadow : "6hex"|"3hex"
    (property-scoped, so date strings like "202610" elsewhere don't hit)
  fontFace: "Name" / fontFace = "Name"

Usage:
  python3 scripts/qa/token_check.py slides/*.mjs --theme ink-classic
  python3 scripts/qa/token_check.py src/ --theme ./ppt-themes/my.theme.json
  python3 scripts/qa/token_check.py deck.mjs --theme ink-classic \
      --allow-color C0392B --allow-font Arial

Exit codes: 0 = pass, 1 = violations found, 2 = bad input (theme/file not found).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # scripts/ for theme.py
from theme import find_theme, load_theme, validate_theme  # noqa: E402
from _jsscan import COLOR_RE, FONT_RE, expand_hex, strip_comments  # noqa: E402


def collect_files(inputs: list[str]) -> list[Path]:
    files: list[Path] = []
    for item in inputs:
        p = Path(item)
        if p.is_dir():
            for pat in ("*.mjs", "*.js"):
                for f in sorted(p.rglob(pat)):
                    if "node_modules" not in f.parts:
                        files.append(f)
        elif p.is_file():
            files.append(p)
        else:
            print(f"not found: {item}", file=sys.stderr)
            raise SystemExit(2)
    return files


def nearest_color(hexv: str, allowed: set[str]) -> str | None:
    if not allowed:
        return None
    r, g, b = int(hexv[0:2], 16), int(hexv[2:4], 16), int(hexv[4:6], 16)
    best, bestd = None, 1 << 30
    for h in allowed:
        d = ((int(h[0:2], 16) - r) ** 2 + (int(h[2:4], 16) - g) ** 2
             + (int(h[4:6], 16) - b) ** 2)
        if d < bestd:
            best, bestd = h, d
    return best


def scan_file(path: Path, allowed_colors: set[str], allowed_fonts: set[str],
              theme_label: str) -> list[dict]:
    try:
        src = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        print(f"{path}: cannot read ({e})", file=sys.stderr)
        raise SystemExit(2)
    stripped = strip_comments(src)
    violations = []
    for m in COLOR_RE.finditer(stripped):
        line = stripped.count("\n", 0, m.start()) + 1
        value = expand_hex(m.group(1))
        if value not in allowed_colors:
            near = nearest_color(value, allowed_colors)
            hint = f" (nearest token: {near})" if near else ""
            violations.append({
                "file": str(path), "line": line, "kind": "color", "value": value,
                "message": f"{value} not in theme '{theme_label}'{hint}",
            })
    for m in FONT_RE.finditer(stripped):
        line = stripped.count("\n", 0, m.start()) + 1
        value = m.group(1)
        if value.casefold() not in allowed_fonts:
            allowed = ", ".join(sorted(allowed_fonts))
            violations.append({
                "file": str(path), "line": line, "kind": "font", "value": value,
                "message": f"{value!r} not in theme fonts (allowed: {allowed})",
            })
    return violations


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("inputs", nargs="+", help=".mjs/.js files or directories")
    ap.add_argument("--theme", required=True,
                    help="theme name (list: python3 scripts/theme.py list) or path to .theme.json")
    ap.add_argument("--allow-color", action="append", default=[],
                    help="extra allowed hex (repeatable, with or without #)")
    ap.add_argument("--allow-font", action="append", default=[],
                    help="extra allowed font name (repeatable)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    tpath, tsource = find_theme(args.theme)
    if tpath is None:
        print(f"theme not found: {args.theme} "
              "(list available: python3 scripts/theme.py list)", file=sys.stderr)
        return 2
    try:
        theme = load_theme(tpath)
    except (OSError, json.JSONDecodeError) as e:
        print(f"{tpath}: cannot read ({e})", file=sys.stderr)
        return 2
    errors = validate_theme(theme, tpath)
    if errors:
        print(f"theme {tpath} is invalid — fix it before gating decks:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 2

    allowed_colors = {expand_hex(v) for v in theme["colors"].values()
                      if len(v) == 6 and not ("," in v)} \
        | {expand_hex(theme["background"]["color"]),
           expand_hex(theme["backgroundDark"]["color"])} \
        | {expand_hex(c) for c in args.allow_color}
    allowed_fonts = {f.casefold() for f in theme["fonts"].values()} \
        | {f.casefold() for f in args.allow_font}

    try:
        files = collect_files(args.inputs)
    except SystemExit as e:
        return e.code
    if not files:
        print("no .mjs/.js files to scan", file=sys.stderr)
        return 2

    violations: list[dict] = []
    for f in files:
        violations.extend(scan_file(f, allowed_colors, allowed_fonts, theme["name"]))

    if args.json:
        print(json.dumps({
            "theme": theme["name"], "source": tsource, "files": len(files),
            "violations": violations,
        }, ensure_ascii=False, indent=2))
    else:
        for v in violations:
            print(f"{v['file']}:{v['line']}  {v['kind']:<5} {v['message']}")
        label = f"{theme['name']} ({tsource})" if tsource != "file" else str(tpath)
        status = "PASS" if not violations else f"FAIL ({len(violations)} violation(s))"
        print(f"\ntoken_check {status} — theme: {label}, files: {len(files)}")
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())
