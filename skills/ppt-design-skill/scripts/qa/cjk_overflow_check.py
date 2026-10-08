#!/usr/bin/env python3
"""Deterministic text-overflow gate for .pptx decks (stdlib only).

Estimates rendered text extents straight from the OOXML -- no rendering, no
third-party deps, no coupling with the upstream validate.py (which is fetched
at install time and may change). Width model: CJK/fullwidth glyph = 1.0em,
everything else = 0.5em.

Checks per slide:
  1. vertical overflow   -- estimated wrapped-text height vs text-box height
  2. horizontal overflow -- an unbreakable token (URL, long number) wider
                            than the box's usable width
  3. off-canvas shapes   -- top-level shapes extending past the slide edge

Usage:
    python3 scripts/qa/cjk_overflow_check.py deck.pptx [more.pptx ...]
    python3 scripts/qa/cjk_overflow_check.py deck.pptx --json

Exit codes: 0 = pass, 1 = violations found, 2 = could not read input.

Known limits (by design, keep the gate deterministic):
  - shapes without an explicit xfrm (placeholder inheritance) are skipped
  - table cells and chart labels are not checked
  - group children are measured in the group's child coordinate space
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import zipfile
import xml.etree.ElementTree as ET

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
EMU_PER_PT = 12700.0
DEFAULT_LINS = 91440    # 0.1" left/right inset
DEFAULT_TINS = 45720    # 0.05" top/bottom inset
DEFAULT_SZ = 1800       # hundredths of a point (18pt)
CANVAS_TOL = 9144       # 0.01" grace for off-canvas check

# Ranges rendered full-width in CJK fonts (1.0em). Everything else 0.5em.
WIDE_RANGES = (
    (0x1100, 0x11FF), (0x2E80, 0x303F), (0x3040, 0x318F), (0x3200, 0x32FF),
    (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xA000, 0xA4CF), (0xAC00, 0xD7AF),
    (0xF900, 0xFAFF), (0xFE30, 0xFE4F), (0xFF01, 0xFF60),
    (0x20000, 0x2FFFD), (0x30000, 0x3FFFD),
)
# Ambiguous-width punctuation that renders full-width in CJK decks.
WIDE_SINGLES = {0x2014, 0x2026, 0x2018, 0x2019, 0x201C, 0x201D}


def is_wide(ch: str) -> bool:
    cp = ord(ch)
    if cp in WIDE_SINGLES:
        return True
    return any(lo <= cp <= hi for lo, hi in WIDE_RANGES)


def q(ns: str, tag: str) -> str:
    return "{%s}%s" % (ns, tag)


def text_width_pt(text: str, sz_hundredths: float) -> float:
    em = sz_hundredths / 100.0
    return sum(em * (1.0 if is_wide(c) else 0.5) for c in text)


def slide_no(name: str) -> int:
    digits = "".join(c for c in name if c.isdigit())
    return int(digits) if digits else 0


def iter_shapes(parent, depth: int = 0):
    """Yield (element, depth) for sp/cxnSp, recursing into groups."""
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


def shape_name(sp) -> str:
    nv = sp.find(q(P, "nvSpPr"))
    if nv is None:
        nv = sp.find(q(P, "nvCxnSpPr"))
    if nv is not None:
        c = nv.find(q(P, "cNvPr"))
        if c is not None:
            return c.get("name") or "shape"
    return "shape"


def para_runs(para, default_sz: int):
    """Return (segments, max_sz, marL_emu, lnSpc, spc_bef_pt, spc_aft_pt).

    segments: list of run lists, split at <a:br>; each run is (text, sz, bold).
    """
    pPr = para.find(q(A, "pPr"))
    marL = 0
    ln_pct, ln_pts = None, None
    spc_bef, spc_aft = 0.0, 0.0
    def_sz = default_sz
    if pPr is not None:
        marL = int(pPr.get("marL", "0") or 0)
        d = pPr.find(q(A, "defRPr"))
        if d is not None and d.get("sz"):
            def_sz = int(d.get("sz"))
        ln = pPr.find(q(A, "lnSpc"))
        if ln is not None:
            pct = ln.find(q(A, "spcPct"))
            pts = ln.find(q(A, "spcPts"))
            if pct is not None and pct.get("val"):
                ln_pct = int(pct.get("val")) / 100000.0
            elif pts is not None and pts.get("val"):
                ln_pts = int(pts.get("val")) / 100.0
        for tag, store in ((q(A, "spcBef"), "bef"), (q(A, "spcAft"), "aft")):
            node = pPr.find(tag)
            if node is None:
                continue
            pts = node.find(q(A, "spcPts"))
            pct = node.find(q(A, "spcPct"))
            if pts is not None and pts.get("val"):
                val = int(pts.get("val")) / 100.0
            elif pct is not None and pct.get("val"):
                val = 1.2 * def_sz / 100.0 * int(pct.get("val")) / 100000.0
            else:
                val = 0.0
            if store == "bef":
                spc_bef = val
            else:
                spc_aft = val

    segments, seg, max_sz = [], [], 0
    for child in para:
        if child.tag == q(A, "r") or child.tag == q(A, "fld"):
            t = child.find(q(A, "t"))
            text = t.text or "" if t is not None else ""
            rPr = child.find(q(A, "rPr"))
            sz, bold = def_sz, False
            if rPr is not None:
                if rPr.get("sz"):
                    sz = int(rPr.get("sz"))
                bold = rPr.get("b") in ("1", "true")
            seg.append((text, sz, bold))
            max_sz = max(max_sz, sz)
        elif child.tag == q(A, "br"):
            segments.append(seg)
            seg = []
    segments.append(seg)
    return segments, max_sz or def_sz, marL, ln_pct, ln_pts, spc_bef, spc_aft


def check_shape(sp, depth, slide_w, slide_h, grace_pt, findings, stats):
    xfrm = get_xfrm(sp)
    if xfrm is None:
        stats["skipped"] += 1
        return
    x, y, cx, cy = xfrm
    name = shape_name(sp)

    if depth == 0:  # group children live in child-space; only check top level
        if (x < -CANVAS_TOL or y < -CANVAS_TOL
                or x + cx > slide_w + CANVAS_TOL
                or y + cy > slide_h + CANVAS_TOL):
            findings.append({
                "shape": name, "type": "off-canvas",
                "message": "shape extends beyond slide bounds "
                           "(x=%.2f y=%.2f w=%.2f h=%.2f pt)"
                           % (x / EMU_PER_PT, y / EMU_PER_PT,
                              cx / EMU_PER_PT, cy / EMU_PER_PT),
            })
            stats["violations"] += 1

    tx = sp.find(q(P, "txBody"))
    if tx is None:
        return
    # default font size: txBody lstStyle lvl1pPr defRPr (pptxgenjs writes
    # slide-number/footer sizes here), overridable per paragraph and per run
    body_default_sz = DEFAULT_SZ
    lst = tx.find(q(A, "lstStyle"))
    if lst is not None:
        lvl1 = lst.find(q(A, "lvl1pPr"))
        if lvl1 is not None:
            d = lvl1.find(q(A, "defRPr"))
            if d is not None and d.get("sz"):
                body_default_sz = int(d.get("sz"))
    bodyPr = tx.find(q(A, "bodyPr"))
    l_ins = int(bodyPr.get("lIns", DEFAULT_LINS)) if bodyPr is not None else DEFAULT_LINS
    r_ins = int(bodyPr.get("rIns", DEFAULT_LINS)) if bodyPr is not None else DEFAULT_LINS
    t_ins = int(bodyPr.get("tIns", DEFAULT_TINS)) if bodyPr is not None else DEFAULT_TINS
    b_ins = int(bodyPr.get("bIns", DEFAULT_TINS)) if bodyPr is not None else DEFAULT_TINS
    wrap_none = bodyPr is not None and bodyPr.get("wrap") == "none"
    autofit = None
    if bodyPr is not None:
        if bodyPr.find(q(A, "normAutofit")) is not None:
            autofit = "norm"
        elif bodyPr.find(q(A, "spAutoFit")) is not None:
            autofit = "sp"
    font_scale = 1.0
    if autofit == "norm" and bodyPr is not None:
        na = bodyPr.find(q(A, "normAutofit"))
        if na.get("fontScale"):
            font_scale = int(na.get("fontScale")) / 100000.0

    usable_w = cx / EMU_PER_PT - (l_ins + r_ins) / EMU_PER_PT
    usable_h = cy / EMU_PER_PT - (t_ins + b_ins) / EMU_PER_PT
    if usable_w <= 1 or usable_h <= 1:
        return

    est_h, max_token = 0.0, 0.0
    has_text = False
    for para in tx.findall(q(A, "p")):
        segments, para_sz, marL, ln_pct, ln_pts, sb, sa = para_runs(
            para, body_default_sz)
        para_sz *= font_scale
        para_usable_w = usable_w - marL / EMU_PER_PT
        if para_usable_w <= 1:
            continue
        lines = 0
        for seg in segments:
            seg_text = "".join(t for t, _, _ in seg)
            if seg_text:
                has_text = True
            w = sum(text_width_pt(t, s * font_scale) for t, s, _ in seg)
            if wrap_none:
                lines += 1 if seg_text else 0
                if w > para_usable_w + 1:
                    max_token = max(max_token, w)
            else:
                lines += max(1, math.ceil(w / para_usable_w - 1e-9))
            # unbreakable token = maximal run of narrow, non-space chars
            cur = 0.0
            for t, s, _ in seg:
                for ch in t:
                    if is_wide(ch) or ch.isspace():
                        max_token = max(max_token, cur)
                        cur = 0.0
                    else:
                        cur += s * font_scale / 100.0 * 0.5
            max_token = max(max_token, cur)
        if lines == 0:
            continue
        if ln_pts is not None:
            line_h = ln_pts
        else:
            line_h = 1.2 * para_sz / 100.0 * (ln_pct if ln_pct else 1.0)
        est_h += lines * line_h + sb + sa

    if not has_text:
        return

    if wrap_none and max_token > usable_w + 1:
        findings.append({
            "shape": name, "type": "horizontal-overflow",
            "message": "no-wrap text %.1fpt wider than box %.1fpt"
                       % (max_token, usable_w),
        })
        stats["violations"] += 1
    elif not wrap_none and max_token > usable_w + 1:
        findings.append({
            "shape": name, "type": "horizontal-overflow",
            "message": "unbreakable token ~%.1fpt > usable width %.1fpt "
                       "(will clip or force overflow)" % (max_token, usable_w),
        })
        stats["violations"] += 1

    if autofit == "sp":
        return  # box grows with text; vertical overflow not applicable
    if est_h > usable_h + grace_pt:
        findings.append({
            "shape": name, "type": "vertical-overflow",
            "message": "estimated text height %.1fpt > box %.1fpt "
                       "(ratio %.2f%s)"
                       % (est_h, usable_h, est_h / usable_h,
                          ", normAutofit may shrink" if autofit == "norm" else ""),
        })
        stats["violations"] += 1


def check_pptx(path, grace_pt, as_json):
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
            key=slide_no)
        if not slide_names:
            print("ERROR: no slides found in %s" % path, file=sys.stderr)
            return 2
        try:
            pres = ET.fromstring(z.read("ppt/presentation.xml"))
        except (KeyError, ET.ParseError) as exc:
            print("ERROR: bad presentation.xml in %s: %s" % (path, exc),
                  file=sys.stderr)
            return 2
        sldSz = pres.find(q(P, "sldSz"))
        if sldSz is None:
            slide_w, slide_h = 9144000, 6858000  # 4:3 fallback
        else:
            slide_w = int(sldSz.get("cx", 9144000))
            slide_h = int(sldSz.get("cy", 6858000))

        all_findings = []
        stats = {"slides": len(slide_names), "shapes": 0,
                 "violations": 0, "skipped": 0}
        for sn in slide_names:
            try:
                root = ET.fromstring(z.read(sn))
            except (KeyError, ET.ParseError) as exc:
                print("ERROR: bad %s in %s: %s" % (sn, path, exc),
                      file=sys.stderr)
                return 2
            tree = root.find(q(P, "cSld"))
            sp_tree = tree.find(q(P, "spTree")) if tree is not None else None
            if sp_tree is None:
                continue
            no = slide_no(sn)
            for sp, depth in iter_shapes(sp_tree):
                stats["shapes"] += 1
                before = len(all_findings)
                check_shape(sp, depth, slide_w, slide_h, grace_pt,
                            all_findings, stats)
                for f in all_findings[before:]:
                    f["slide"] = no

    if as_json:
        print(json.dumps({"file": path, **stats, "findings": all_findings},
                         ensure_ascii=False, indent=2))
    else:
        print("== %s: %d slides, %d shapes, %d violations, %d skipped"
              % (path, stats["slides"], stats["shapes"],
                 stats["violations"], stats["skipped"]))
        for f in all_findings:
            print("  FAIL slide %s [%s] %s: %s"
                  % (f["slide"], f["type"], f["shape"], f["message"]))
        if not all_findings:
            print("  PASS")
    return 1 if all_findings else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="+", help=".pptx file(s) to check")
    ap.add_argument("--grace", type=float, default=2.0, metavar="PT",
                    help="vertical grace in points (default 2.0)")
    ap.add_argument("--json", action="store_true", help="JSON report")
    args = ap.parse_args(argv)

    worst = 0
    for path in args.files:
        rc = check_pptx(path, args.grace, args.json)
        worst = max(worst, rc)
    return worst


if __name__ == "__main__":
    sys.exit(main())
