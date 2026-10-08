#!/usr/bin/env python3
"""Theme token manager for PPT Design Skill (stdlib only).

Subcommands:
  list      show available themes (built-in + project + user)
  validate  check a .theme.json against themes/theme.schema.json rules
  extract   draft a theme from a user's .pptx (theme1.xml) for review

Theme resolution order (first hit wins, by name):
  1. ./ppt-themes/<name>.theme.json                 (project)
  2. ~/.ppt-design-skill/themes/<name>.theme.json   (user)
  3. <skill>/themes/<name>.theme.json               (built-in, shipped)

Usage:
  python3 scripts/theme.py list [--json] [--style magazine|swiss|custom]
  python3 scripts/theme.py validate FILE.theme.json [--json]
  python3 scripts/theme.py extract deck.pptx [-o out.theme.json] [--name my-brand] [--json]

Exit codes: 0 = ok, 1 = validation violations, 2 = bad input / not found.

Known limits (by design):
  - extract maps OOXML clrScheme heuristically (ink<-dk1, paper<-lt1,
    accent<-accent1); the draft is marked "review": true and must be
    confirmed by a human before use
  - OOXML has no mono font slot; extract defaults mono to Consolas
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
HEX6_RE = re.compile(r"^[0-9A-Fa-f]{6}$")
TRIPLET_RE = re.compile(r"^(\d{1,3}),(\d{1,3}),(\d{1,3})$")
USER_DIR = Path.home() / ".ppt-design-skill" / "themes"
PROJECT_DIR = Path.cwd() / "ppt-themes"

A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
SYSCLR_MAP = {"windowText": "000000", "window": "FFFFFF"}


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def search_dirs():
    """Ordered (source, dir) pairs: project > user > built-in."""
    return [
        ("project", PROJECT_DIR),
        ("user", USER_DIR),
        ("built-in", skill_root() / "themes"),
    ]


def find_theme(name_or_path: str):
    """Resolve a --theme argument to (path, source). Path form used as-is."""
    p = Path(name_or_path)
    if p.suffix == ".json" or p.exists():
        if p.is_file():
            return p.resolve(), "file"
        return None, None
    for source, d in search_dirs():
        cand = d / f"{name_or_path}.theme.json"
        if cand.is_file():
            return cand, source
    return None, None


def load_theme(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _triplet_ok(val: str) -> bool:
    m = TRIPLET_RE.match(val)
    return bool(m) and all(int(x) <= 255 for x in m.groups())


def validate_theme(data, path: Path | None = None) -> list[str]:
    """Return violation strings (empty = valid). Mirrors theme.schema.json."""
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["top level must be an object"]
    for key in ("name", "style", "colors", "fonts", "background", "backgroundDark"):
        if key not in data:
            errors.append(f"missing required key: {key}")
    if errors:
        return errors

    name = data["name"]
    if not isinstance(name, str) or not NAME_RE.match(name):
        errors.append(f"name must be kebab-case (got {name!r})")
    if data["style"] not in ("magazine", "swiss", "custom"):
        errors.append(f"style must be magazine|swiss|custom (got {data['style']!r})")

    colors = data["colors"]
    if not isinstance(colors, dict) or not colors:
        errors.append("colors must be a non-empty object")
    else:
        for req in ("ink", "paper", "accent"):
            if req not in colors:
                errors.append(f"colors missing required token: {req}")
        for key, val in colors.items():
            if not isinstance(val, str) or not (HEX6_RE.match(val) or _triplet_ok(val)):
                errors.append(
                    f"colors.{key}: must be 6-hex (no #) or 'r,g,b' triplet (got {val!r})")
        if isinstance(colors.get("accentRgb"), str) and isinstance(colors.get("accent"), str) \
                and HEX6_RE.match(colors["accent"]):
            m = TRIPLET_RE.match(colors["accentRgb"])
            if m:
                rgb = tuple(int(x) for x in m.groups())
                hexv = colors["accent"]
                expected = tuple(int(hexv[i:i + 2], 16) for i in (0, 2, 4))
                if rgb != expected:
                    errors.append(
                        f"colors.accentRgb {colors['accentRgb']} does not match "
                        f"colors.accent #{hexv.upper()}")

    for key in ("background", "backgroundDark"):
        surf = data[key]
        if (not isinstance(surf, dict) or not isinstance(surf.get("color"), str)
                or not HEX6_RE.match(surf["color"])):
            errors.append(f"{key}.color must be 6-hex (no #)")

    fonts = data["fonts"]
    if not isinstance(fonts, dict):
        errors.append("fonts must be an object")
    else:
        for req in ("title", "body", "mono"):
            v = fonts.get(req)
            if not isinstance(v, str) or not v.strip():
                errors.append(f"fonts.{req} must be a non-empty string")

    if path is not None and isinstance(name, str) and NAME_RE.match(name):
        if path.name != f"{name}.theme.json":
            errors.append(
                f"filename must be '{name}.theme.json' (got {path.name}) — "
                "the resolver looks themes up by filename")
    if "review" in data and not isinstance(data["review"], bool):
        errors.append("review must be a boolean")
    if "notes" in data and not (
            isinstance(data["notes"], list) and all(isinstance(n, str) for n in data["notes"])):
        errors.append("notes must be an array of strings")
    return errors


def collect_themes(style_filter: str | None = None) -> tuple[dict, list]:
    """name -> {path, source, data}; first hit wins (project > user > built-in)."""
    found: dict[str, dict] = {}
    order: list[str] = []
    for source, d in search_dirs():
        if not d.is_dir():
            continue
        for f in sorted(d.glob("*.theme.json")):
            if f.name == "theme.schema.json":
                continue
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if not isinstance(data, dict) or not isinstance(data.get("name"), str):
                continue
            if style_filter and data.get("style") != style_filter:
                continue
            if data["name"] in found:
                continue
            found[data["name"]] = {"path": f, "source": source, "data": data}
            order.append(data["name"])
    return found, order


def cmd_list(args) -> int:
    themes, order = collect_themes(args.style)
    if args.json:
        payload = [
            {
                "name": n,
                "label": themes[n]["data"].get("label", ""),
                "style": themes[n]["data"].get("style", ""),
                "source": themes[n]["source"],
                "path": str(themes[n]["path"]),
                "colors": themes[n]["data"].get("colors", {}),
                "fonts": themes[n]["data"].get("fonts", {}),
                "review": bool(themes[n]["data"].get("review")),
            }
            for n in order
        ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0
    if not themes:
        print("no themes found", file=sys.stderr)
        return 2
    print(f"{'NAME':<20} {'STYLE':<10} {'SOURCE':<9} {'INK':<8} {'PAPER':<8} "
          f"{'ACCENT':<8} FONTS (title / body / mono)")
    for n in order:
        t = themes[n]
        c = t["data"].get("colors", {})
        f = t["data"].get("fonts", {})
        fonts = f"{f.get('title', '?')} / {f.get('body', '?')} / {f.get('mono', '?')}"
        print(f"{n:<20} {t['data'].get('style', '?'):<10} {t['source']:<9} "
              f"{c.get('ink', '?'):<8} {c.get('paper', '?'):<8} {c.get('accent', '?'):<8} {fonts}")
    print("\nresolution: project ./ppt-themes/ > user ~/.ppt-design-skill/themes/ > built-in")
    return 0


def cmd_validate(args) -> int:
    path = Path(args.file)
    if not path.is_file():
        print(f"not a file: {path}", file=sys.stderr)
        return 2
    try:
        data = load_theme(path)
    except (OSError, json.JSONDecodeError) as e:
        print(f"{path}: cannot read ({e})", file=sys.stderr)
        return 2
    errors = validate_theme(data, path)
    if args.json:
        print(json.dumps({"file": str(path), "valid": not errors, "errors": errors},
                         ensure_ascii=False, indent=2))
    elif errors:
        for e in errors:
            print(f"ERROR {path}: {e}", file=sys.stderr)
    else:
        label = data.get("label", data["name"])
        print(f"OK {path} — {label} ({data['style']})")
    return 1 if errors else 0


def _color_of(elem: ET.Element) -> str | None:
    """srgbClr val, or sysClr lastClr / window mapping -> hex (upper)."""
    srgb = elem.find(f"{{{A_NS}}}srgbClr")
    if srgb is not None:
        v = srgb.get("val", "")
        if len(v) == 3:
            v = "".join(c * 2 for c in v)
        return v.upper() if HEX6_RE.match(v) else None
    sysc = elem.find(f"{{{A_NS}}}sysClr")
    if sysc is not None:
        last = sysc.get("lastClr")
        if last and HEX6_RE.match(last):
            return last.upper()
        return SYSCLR_MAP.get(sysc.get("val", ""), "000000")
    return None


def _font_scheme(root: ET.Element) -> dict[str, str]:
    out: dict[str, str] = {}
    fs = root.find(f".//{{{A_NS}}}fontScheme")
    if fs is None:
        return out
    for role, key in (("majorFont", "major"), ("minorFont", "minor")):
        el = fs.find(f"{{{A_NS}}}{role}")
        if el is None:
            continue
        for slot, tag in (("latin", "latin"), ("ea", "ea")):
            f = el.find(f"{{{A_NS}}}{tag}")
            out[f"{key}_{slot}"] = (f.get("typeface") if f is not None else "") or ""
    return out


def build_draft(raw: dict[str, str], fonts_raw: dict[str, str], name: str, src_label: str) -> dict:
    dk1 = raw.get("dk1", "000000")
    lt1 = raw.get("lt1", "FFFFFF")
    dk2 = raw.get("dk2", dk1)
    lt2 = raw.get("lt2", lt1)
    accent1 = raw.get("accent1", "4A90A4")
    accent_rgb = ",".join(str(int(accent1[i:i + 2], 16)) for i in (0, 2, 4))
    title_font = fonts_raw.get("major_ea") or fonts_raw.get("major_latin") or "Microsoft YaHei"
    body_font = fonts_raw.get("minor_ea") or fonts_raw.get("minor_latin") or "Microsoft YaHei"
    notes = [
        f"草稿来源：{src_label} 的 a:clrScheme / a:fontScheme，映射为语义 token，需人工确认后再用",
        f"ink={dk1}（取 dk1）、paper={lt1}（取 lt1）、accent={accent1}（取 accent1）"
        "——品牌主色常在 accent2-6，不对就手动改",
        f"inkTint={dk2}（dk2）、paperTint={lt2}（lt2）——深浅变体仅为猜测，按视觉调整",
        f"字体取 fontScheme：title={title_font}、body={body_font}（ea 优先，缺省回退 latin）；"
        "OOXML 无 mono 槽位，默认 Consolas",
        "确认后：删掉 review / notes 字段，跑 python3 scripts/theme.py validate <file> 通过即可用",
        "deck 写完后跑 python3 scripts/qa/token_check.py <slides> --theme <name> 做 token 门禁",
    ]
    return {
        "name": name,
        "label": f"Extracted from {src_label}",
        "style": "custom",
        "description": "从用户 .pptx 主题提取的草稿，映射需人工复核",
        "review": True,
        "notes": notes,
        "colors": {
            "ink": dk1,
            "paper": lt1,
            "paperTint": lt2,
            "inkTint": dk2,
            "accent": accent1,
            "accentRgb": accent_rgb,
        },
        "background": {"color": lt1},
        "backgroundDark": {"color": dk1},
        "fonts": {"title": title_font, "body": body_font, "mono": "Consolas"},
    }


def cmd_extract(args) -> int:
    pptx = Path(args.pptx)
    if not pptx.is_file():
        print(f"not a file: {pptx}", file=sys.stderr)
        return 2
    try:
        with zipfile.ZipFile(pptx) as zf:
            theme_parts = sorted(n for n in zf.namelist()
                                 if n.startswith("ppt/theme/theme") and n.endswith(".xml"))
            if not theme_parts:
                print(f"{pptx}: no ppt/theme/themeN.xml part found", file=sys.stderr)
                return 2
            root = ET.fromstring(zf.read(theme_parts[0]))
    except (zipfile.BadZipFile, ET.ParseError) as e:
        print(f"{pptx}: cannot parse ({e})", file=sys.stderr)
        return 2

    clr = root.find(f".//{{{A_NS}}}clrScheme")
    if clr is None:
        print(f"{pptx}: theme part has no a:clrScheme", file=sys.stderr)
        return 2
    raw: dict[str, str] = {}
    for child in clr:
        tag = child.tag.split("}")[1]
        val = _color_of(child)
        if val:
            raw[tag] = val

    name = args.name or re.sub(r"[^a-z0-9]+", "-", pptx.stem.lower()).strip("-") or "extracted"
    if not NAME_RE.match(name):
        print(f"--name must be kebab-case (got {name!r})", file=sys.stderr)
        return 2
    draft = build_draft(raw, _font_scheme(root), name, pptx.name)

    if args.json:
        print(json.dumps(draft, ensure_ascii=False, indent=2))
        return 0
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(draft, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"draft written: {out}")
    else:
        print(json.dumps(draft, ensure_ascii=False, indent=2))
        print(f"\n(save as ppt-themes/{name}.theme.json to pass the filename check)",
              file=sys.stderr)
    for n in draft["notes"]:
        print(f"note: {n}", file=sys.stderr)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_list = sub.add_parser("list", help="list available themes")
    p_list.add_argument("--json", action="store_true")
    p_list.add_argument("--style", choices=("magazine", "swiss", "custom"))
    p_list.set_defaults(func=cmd_list)

    p_val = sub.add_parser("validate", help="validate a .theme.json")
    p_val.add_argument("file")
    p_val.add_argument("--json", action="store_true")
    p_val.set_defaults(func=cmd_validate)

    p_ext = sub.add_parser("extract", help="draft a theme from a user .pptx")
    p_ext.add_argument("pptx")
    p_ext.add_argument("-o", "--out", help="write draft to this path instead of stdout")
    p_ext.add_argument("--name", help="theme name (kebab-case; default derived from filename)")
    p_ext.add_argument("--json", action="store_true")
    p_ext.set_defaults(func=cmd_extract)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
