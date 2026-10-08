#!/usr/bin/env python3
"""Deterministic WCAG contrast gate for .pptx decks (stdlib only).

Reads text colors and effective backgrounds straight from the OOXML -- no
rendering, no third-party deps, no coupling with the upstream validate.py.

For every text run with an explicit color, resolves the effective background:
  1. the shape's own solid fill
  2. the slide background (p:bg solid fill / bgRef scheme color)
  3. the topmost earlier shape whose bbox contains the text shape's center
  4. white fallback
then computes the WCAG 2.x contrast ratio and flags runs below threshold:
  - 4.5:1 normal text
  - 3.0:1 large text (>= 18pt, or >= 14pt bold)

schemeClr is resolved through the theme clrScheme + master clrMap; the common
color transforms (lumMod/lumOff in HSL, tint/shade as RGB mixes) are applied.
Approximations are fine for a gate: borderline cases deserve human eyes.

Usage:
    python3 scripts/qa/contrast_check.py deck.pptx [more.pptx ...]
    python3 scripts/qa/contrast_check.py deck.pptx --json

Exit codes: 0 = pass, 1 = violations found, 2 = could not read input.

Known limits (by design):
  - runs without an explicit color are skipped (inherited style unknown)
  - gradient / picture / pattern backgrounds are skipped (unresolvable)
  - alpha transforms are ignored (opacity treated as opaque)
"""
from __future__ import annotations

import argparse
import colorsys
import json
import sys
import zipfile
import xml.etree.ElementTree as ET

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
DEFAULT_SZ = 1800

THEME_ORDER = ("dk1", "lt1", "dk2", "lt2", "accent1", "accent2", "accent3",
               "accent4", "accent5", "accent6", "hlink", "folHlink")
CLRMAP_DEFAULT = {"bg1": "lt1", "tx1": "dk1", "bg2": "lt2", "tx2": "dk2"}


def q(ns: str, tag: str) -> str:
    return "{%s}%s" % (ns, tag)


def hex_to_rgb(v: str):
    v = v.strip().lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    if len(v) != 6:
        return None
    try:
        return tuple(int(v[i:i + 2], 16) / 255.0 for i in (0, 2, 4))
    except ValueError:
        return None


def rgb_to_hex(rgb) -> str:
    return "%02X%02X%02X" % tuple(max(0, min(255, round(c * 255))) for c in rgb)


def parse_theme(zf):
    """Return {theme color name: (r,g,b)} from the first theme part."""
    names = sorted(n for n in zf.namelist()
                   if n.startswith("ppt/theme/theme") and n.endswith(".xml"))
    if not names:
        return {}
    try:
        root = ET.fromstring(zf.read(names[0]))
    except ET.ParseError:
        return {}
    scheme = root.find(".//" + q(A, "clrScheme"))
    if scheme is None:
        return {}
    colors = {}
    for entry in scheme:
        name = entry.tag.split("}")[1]
        if name not in THEME_ORDER:
            continue
        for child in entry:
            tag = child.tag.split("}")[1]
            if tag == "srgbClr":
                rgb = hex_to_rgb(child.get("val", ""))
            elif tag == "sysClr":
                rgb = hex_to_rgb(child.get("lastClr", "") or "000000")
            else:
                rgb = None
            if rgb:
                colors[name] = rgb
                break
    return colors


def parse_clrmap(zf):
    names = sorted(n for n in zf.namelist()
                   if n.startswith("ppt/slideMasters/slideMaster")
                   and n.endswith(".xml") and "rels" not in n)
    if not names:
        return dict(CLRMAP_DEFAULT)
    try:
        root = ET.fromstring(zf.read(names[0]))
    except ET.ParseError:
        return dict(CLRMAP_DEFAULT)
    cm = root.find(".//" + q(P, "clrMap"))
    mapping = dict(CLRMAP_DEFAULT)
    if cm is not None:
        for k, v in cm.attrib.items():
            if v:
                mapping[k] = v
    return mapping


def apply_transforms(color_elem, rgb):
    """Apply lumMod/lumOff/tint/shade children in document order."""
    r, g, b = rgb
    for t in color_elem:
        tag = t.tag.split("}")[1]
        try:
            val = int(t.get("val", "0")) / 100000.0
        except ValueError:
            continue
        if tag == "alpha":
            continue  # treated as opaque
        if tag in ("lumMod", "lumOff"):
            h, l, s = colorsys.rgb_to_hls(r, g, b)
            if tag == "lumMod":
                l *= val
            else:
                l += val
            l = max(0.0, min(1.0, l))
            r, g, b = colorsys.hls_to_rgb(h, l, s)
        elif tag == "tint":
            r, g, b = (c * val + (1.0 - val) for c in (r, g, b))
        elif tag == "shade":
            r, g, b = (c * val for c in (r, g, b))
    return (r, g, b)


class Resolver:
    def __init__(self, zf):
        self.theme = parse_theme(zf)
        self.clrmap = parse_clrmap(zf)

    def scheme(self, name):
        mapped = self.clrmap.get(name, name)
        return self.theme.get(mapped)

    def from_color_elem(self, elem):
        """Resolve an srgbClr/schemeClr/sysClr element to (r,g,b) or None."""
        tag = elem.tag.split("}")[1]
        rgb = None
        if tag == "srgbClr":
            rgb = hex_to_rgb(elem.get("val", ""))
        elif tag == "sysClr":
            rgb = hex_to_rgb(elem.get("lastClr", "") or "000000")
        elif tag == "schemeClr":
            rgb = self.scheme(elem.get("val", ""))
        elif tag == "prstClr":
            return None
        if rgb is None:
            return None
        return apply_transforms(elem, rgb)

    def from_fill(self, fill_elem):
        """fill_elem: a:solidFill etc. Returns (r,g,b) | 'none' | None."""
        if fill_elem is None:
            return None
        tag = fill_elem.tag.split("}")[1]
        if tag == "noFill":
            return "none"
        if tag != "solidFill":
            return None  # grad/blip/patt/grp: unresolvable
        for child in fill_elem:
            rgb = self.from_color_elem(child)
            if rgb is not None:
                return rgb
        return None


def rel_luminance(rgb):
    def lin(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(c1, c2):
    l1, l2 = sorted((rel_luminance(c1), rel_luminance(c2)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def iter_shapes(parent, depth=0):
    for child in parent:
        if child.tag in (q(P, "sp"), q(P, "cxnSp")):
            yield child, depth
        elif child.tag == q(P, "grpSp"):
            yield from iter_shapes(child, depth + 1)


def get_xfrm(sp):
    spPr = sp.find(q(P, "spPr"))
    if spPr is None:
        return None
    xfrm = spPr.find(q(A, "xfrm"))
    if xfrm is None:
        return None
    off, ext = xfrm.find(q(A, "off")), xfrm.find(q(A, "ext"))
    if off is None or ext is None:
        return None
    try:
        return (int(off.get("x")), int(off.get("y")),
                int(ext.get("cx")), int(ext.get("cy")))
    except (TypeError, ValueError):
        return None


def slide_bg(root, resolver):
    cSld = root.find(q(P, "cSld"))
    if cSld is None:
        return None
    bg = cSld.find(q(P, "bg"))
    if bg is None:
        return None
    bgPr = bg.find(q(P, "bgPr"))
    if bgPr is not None:
        return resolver.from_fill(bgPr.find(q(A, "solidFill")))
    bgRef = bg.find(q(P, "bgRef"))
    if bgRef is not None:
        for child in bgRef:
            rgb = resolver.from_color_elem(child)
            if rgb is not None:
                return rgb
    return None


def contains(bbox, px, py):
    x, y, cx, cy = bbox
    return x <= px <= x + cx and y <= py <= y + cy


def check_pptx(path, min_normal, min_large, as_json):
    try:
        z = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as exc:
        print("ERROR: cannot open %s: %s" % (path, exc), file=sys.stderr)
        return 2
    with z:
        names = z.namelist()
        slide_names = sorted(
            (n for n in names if n.startswith("ppt/slides/slide")
             and n.endswith(".xml") and "rels" not in n),
            key=lambda n: int("".join(c for c in n if c.isdigit()) or 0))
        if not slide_names:
            print("ERROR: no slides found in %s" % path, file=sys.stderr)
            return 2
        resolver = Resolver(z)
        findings, stats = [], {"slides": len(slide_names), "runs": 0,
                               "violations": 0, "skipped": 0}
        for idx, sn in enumerate(slide_names):
            try:
                root = ET.fromstring(z.read(sn))
            except (KeyError, ET.ParseError) as exc:
                print("ERROR: bad %s: %s" % (sn, exc), file=sys.stderr)
                return 2
            no = idx + 1
            cSld = root.find(q(P, "cSld"))
            sp_tree = cSld.find(q(P, "spTree")) if cSld is not None else None
            if sp_tree is None:
                continue
            shapes = list(iter_shapes(sp_tree))
            bg = slide_bg(root, resolver)
            flat = []
            for sp, _depth in shapes:
                bbox = get_xfrm(sp)
                spPr = sp.find(q(P, "spPr"))
                fill = resolver.from_fill(
                    spPr.find(q(A, "solidFill")) if spPr is not None else None)
                flat.append((sp, bbox, fill))

            for sp, bbox, fill in flat:
                tx = sp.find(q(P, "txBody"))
                if tx is None:
                    continue
                # effective background for this shape
                if isinstance(fill, tuple):
                    bg_rgb = fill
                elif fill == "none" or fill is None:
                    # z-order semantics: an opaque shape under the text hides
                    # the slide background, so containment wins over slide bg
                    bg_rgb = None
                    if bbox is not None:
                        cx_, cy_ = bbox[0] + bbox[2] / 2, bbox[1] + bbox[3] / 2
                        for other, obbox, ofill in reversed(flat):
                            if other is sp or not isinstance(ofill, tuple):
                                continue
                            if obbox and contains(obbox, cx_, cy_):
                                bg_rgb = ofill
                                break
                    if bg_rgb is None:
                        bg_rgb = bg
                    if bg_rgb is None:
                        bg_rgb = (1.0, 1.0, 1.0)  # white fallback
                else:
                    stats["skipped"] += 1
                    continue

                body_def = None
                lst = tx.find(q(A, "lstStyle"))
                if lst is not None:
                    lvl1 = lst.find(q(A, "lvl1pPr"))
                    if lvl1 is not None:
                        body_def = lvl1.find(q(A, "defRPr"))

                for para in tx.findall(q(A, "p")):
                    pPr = para.find(q(A, "pPr"))
                    def_fill = None
                    def_sz, def_b = DEFAULT_SZ, False
                    if body_def is not None:
                        def_fill = body_def.find(q(A, "solidFill"))
                        if body_def.get("sz"):
                            def_sz = int(body_def.get("sz"))
                        def_b = body_def.get("b") in ("1", "true")
                    if pPr is not None:
                        d = pPr.find(q(A, "defRPr"))
                        if d is not None:
                            fe = d.find(q(A, "solidFill"))
                            if fe is not None:
                                def_fill = fe
                            if d.get("sz"):
                                def_sz = int(d.get("sz"))
                            def_b = d.get("b") in ("1", "true")
                    for r in para:
                        # a:fld (slide numbers, dates) is chrome -- skip it:
                        # flagging gray page numbers on every deck trains
                        # users to ignore the gate
                        if r.tag != q(A, "r"):
                            continue
                        t = r.find(q(A, "t"))
                        text = (t.text or "").strip() if t is not None else ""
                        if not text:
                            continue
                        rPr = r.find(q(A, "rPr"))
                        fill_elem, sz, bold = def_fill, def_sz, def_b
                        if rPr is not None:
                            fe = rPr.find(q(A, "solidFill"))
                            if fe is not None:
                                fill_elem = fe
                            if rPr.get("sz"):
                                sz = int(rPr.get("sz"))
                            bold = rPr.get("b") in ("1", "true")
                        if fill_elem is None:
                            stats["skipped"] += 1
                            continue
                        fg = resolver.from_fill(fill_elem)
                        if not isinstance(fg, tuple):
                            stats["skipped"] += 1
                            continue
                        stats["runs"] += 1
                        large = sz >= 1800 or (bold and sz >= 1400)
                        required = min_large if large else min_normal
                        ratio = contrast_ratio(fg, bg_rgb)
                        if ratio + 1e-9 < required:
                            findings.append({
                                "slide": no,
                                "text": text[:24],
                                "fg": rgb_to_hex(fg),
                                "bg": rgb_to_hex(bg_rgb),
                                "ratio": round(ratio, 2),
                                "required": required,
                                "message": "contrast %.2f:1 < %.1f:1 "
                                           "(%s, %dpt%s)"
                                           % (ratio, required,
                                              "large" if large else "normal",
                                              sz / 100.0,
                                              ", bold" if bold else ""),
                            })
                            stats["violations"] += 1

    if as_json:
        print(json.dumps({"file": path, **stats, "findings": findings},
                         ensure_ascii=False, indent=2))
    else:
        print("== %s: %d slides, %d runs checked, %d violations, %d skipped"
              % (path, stats["slides"], stats["runs"],
                 stats["violations"], stats["skipped"]))
        for f in findings:
            print("  FAIL slide %d %s on %s/%s: %s"
                  % (f["slide"], f["text"], f["fg"], f["bg"], f["message"]))
        if not findings:
            print("  PASS")
    return 1 if findings else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="+", help=".pptx file(s) to check")
    ap.add_argument("--min-normal", type=float, default=4.5)
    ap.add_argument("--min-large", type=float, default=3.0)
    ap.add_argument("--json", action="store_true", help="JSON report")
    args = ap.parse_args(argv)

    worst = 0
    for path in args.files:
        rc = check_pptx(path, args.min_normal, args.min_large, args.json)
        worst = max(worst, rc)
    return worst


if __name__ == "__main__":
    sys.exit(main())
