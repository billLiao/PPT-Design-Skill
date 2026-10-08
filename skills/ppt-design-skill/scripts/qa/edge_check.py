#!/usr/bin/env python3
"""Deterministic pixel gate for rendered slide images (stdlib only).

Consumes the slide images the visual-QA step already produces
(`soffice.py -> pdf`, `pdftoppm -png -r 150 out.pdf slide`) and checks what
XML-level checks cannot see: content clipped at the slide edge and
near-blank renders.

Checks per image:
  1. edge bleed   -- fraction of pixels in each outer margin strip that
                     differ from the strip's median color; a flat background
                     scores ~0, text/graphics crossing the edge score high
  2. near-blank   -- per-channel std-dev over a subsampled grid; catches
                     empty/underfill renders

PNG is decoded natively (zlib + unfilter). If Pillow is installed it is used
as the fast path and JPEG is also accepted; without Pillow, render with
`pdftoppm -png` (JPEG cannot be decoded by the stdlib).

Usage:
    python3 scripts/qa/edge_check.py slide-*.png
    python3 scripts/qa/edge_check.py slides_dir/ --json

Exit codes: 0 = pass, 1 = findings, 2 = could not read input.

Note: full-bleed photo backgrounds legitimately trip check 1 -- raise
--threshold or exclude those slides; the gate is tuned for flat-background
decks produced by this skill's themes.
"""
from __future__ import annotations

import argparse
import json
import math
import struct
import sys
import zlib
from pathlib import Path

try:
    from PIL import Image  # fast path only; not required
except ImportError:
    Image = None

IMG_EXTS = {".png", ".jpg", ".jpeg"}


def decode_png_stdlib(data: bytes):
    """Minimal PNG decoder: 8-bit, colortype 0/2/4/6, no interlace -> RGB."""
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    pos, idat, w, h, bd, ct, interlace = 8, bytearray(), 0, 0, 8, 6, 0
    while pos + 8 <= len(data):
        length, ctype = struct.unpack(">I4s", data[pos:pos + 8])
        chunk = data[pos + 8:pos + 8 + length]
        if ctype == b"IHDR":
            w, h, bd, ct, _comp, _filt, interlace = struct.unpack(
                ">IIBBBBB", chunk)
        elif ctype == b"IDAT":
            idat += chunk
        elif ctype == b"IEND":
            break
        pos += 12 + length
    if bd != 8 or interlace != 0:
        raise ValueError("unsupported PNG (bitdepth %d interlace %d)"
                         % (bd, interlace))
    channels = {0: 1, 2: 3, 4: 2, 6: 4}.get(ct)
    if channels is None:
        raise ValueError("unsupported PNG colortype %d" % ct)
    raw = zlib.decompress(bytes(idat))
    stride = w * channels
    out = bytearray(stride * h)
    prev = bytearray(stride)
    pos = 0
    for y in range(h):
        ftype = raw[pos]
        pos += 1
        line = bytearray(raw[pos:pos + stride])
        pos += stride
        if ftype == 1:
            for i in range(channels, stride):
                line[i] = (line[i] + line[i - channels]) & 0xFF
        elif ftype == 2:
            for i in range(stride):
                line[i] = (line[i] + prev[i]) & 0xFF
        elif ftype == 3:
            for i in range(stride):
                a = line[i - channels] if i >= channels else 0
                line[i] = (line[i] + ((a + prev[i]) >> 1)) & 0xFF
        elif ftype == 4:
            for i in range(stride):
                a = line[i - channels] if i >= channels else 0
                c = prev[i - channels] if i >= channels else 0
                b = prev[i]
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pr) & 0xFF
        elif ftype != 0:
            raise ValueError("bad PNG filter %d" % ftype)
        out[y * stride:(y + 1) * stride] = line
        prev = line
    # to packed RGB
    rgb = bytearray(w * h * 3)
    if ct == 2:
        return w, h, bytes(out)
    for y in range(h):
        row = out[y * stride:(y + 1) * stride]
        dst = y * w * 3
        if ct == 0:
            for x in range(w):
                v = row[x]
                rgb[dst:dst + 3] = bytes((v, v, v))
        elif ct == 4:
            for x in range(w):
                v = row[x * 2]
                rgb[dst:dst + 3] = bytes((v, v, v))
        elif ct == 6:
            for x in range(w):
                s = x * 4
                rgb[dst:dst + 3] = row[s:s + 3]
    return w, h, bytes(rgb)


def load_image(path: Path, stdlib_only: bool):
    data = path.read_bytes()
    use_pil = Image is not None and not stdlib_only
    if use_pil:
        img = Image.open(path)
        img = img.convert("RGB")
        return img.size[0], img.size[1], img.tobytes()
    if path.suffix.lower() == ".png":
        return decode_png_stdlib(data)
    raise ValueError("JPEG needs Pillow; render with `pdftoppm -png` "
                     "or install Pillow")


def median(values):
    s = sorted(values)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2.0


def analyze(w, h, rgb, margin, delta, threshold, blank_std):
    findings = []

    def px(x, y):
        i = (y * w + x) * 3
        return rgb[i], rgb[i + 1], rgb[i + 2]

    m = margin if margin > 0 else max(4, round(min(w, h) * 0.006))
    strips = {
        "top": [(x, y) for y in range(m) for x in range(w)],
        "bottom": [(x, y) for y in range(h - m, h) for x in range(w)],
        "left": [(x, y) for x in range(m) for y in range(h)],
        "right": [(x, y) for x in range(w - m, w) for y in range(h)],
    }
    for name, coords in strips.items():
        if not coords:
            continue
        rs = [px(x, y)[0] for x, y in coords]
        gs = [px(x, y)[1] for x, y in coords]
        bs = [px(x, y)[2] for x, y in coords]
        mr, mg, mb = median(rs), median(gs), median(bs)
        diff = 0
        for i in range(len(coords)):
            if (max(abs(rs[i] - mr), abs(gs[i] - mg), abs(bs[i] - mb))
                    > delta):
                diff += 1
        frac = diff / len(coords)
        if frac > threshold:
            findings.append({
                "type": "edge-bleed", "edge": name,
                "message": "%.1f%% of %s-edge margin pixels differ from "
                           "background (threshold %.1f%%) -- content "
                           "touches or clips the edge"
                           % (frac * 100, name, threshold * 100),
            })

    step = max(1, min(w, h) // 200)
    xs = range(0, w, step)
    ys = range(0, h, step)
    n = len(xs) * len(ys)
    sums = [0, 0, 0]
    sq = [0.0, 0.0, 0.0]
    for y in ys:
        for x in xs:
            r, g, b = px(x, y)
            for k, v in enumerate((r, g, b)):
                sums[k] += v
                sq[k] += v * v
    worst = 0.0
    for k in range(3):
        mean = sums[k] / n
        worst = max(worst, math.sqrt(max(0.0, sq[k] / n - mean * mean)))
    if worst < blank_std:
        findings.append({
            "type": "near-blank",
            "message": "image is near-uniform (max channel std-dev %.2f < "
                        "%.2f) -- blank or underfill render?" % (worst, blank_std),
        })
    return findings


def check_image(path, args):
    try:
        w, h, rgb = load_image(path, args.stdlib_only)
    except Exception as exc:  # noqa: BLE001 - report and fail the gate
        print("ERROR: %s: %s" % (path, exc), file=sys.stderr)
        return None
    findings = analyze(w, h, rgb, args.margin, args.delta, args.threshold,
                       args.blank_std)
    if args.json:
        return {"file": str(path), "size": [w, h], "findings": findings}
    print("== %s (%dx%d): %s" % (path, w, h,
                                 "%d findings" % len(findings) if findings
                                 else "PASS"))
    for f in findings:
        print("  FAIL [%s] %s" % (f["type"], f["message"]))
    return {"file": str(path), "size": [w, h], "findings": findings}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="+",
                    help="slide image files and/or directories")
    ap.add_argument("--margin", type=int, default=0, metavar="PX",
                    help="edge strip width; 0 = auto (~0.6%% of short side)")
    ap.add_argument("--delta", type=int, default=24, metavar="LEVEL",
                    help="per-channel diff vs strip median that counts as "
                         "content (default 24)")
    ap.add_argument("--threshold", type=float, default=0.02, metavar="FRAC",
                    help="flag edge when content fraction exceeds this "
                         "(default 0.02)")
    ap.add_argument("--blank-std", type=float, default=6.0, metavar="STD",
                    help="max channel std-dev below which the image is "
                         "near-blank (default 6.0)")
    ap.add_argument("--stdlib-only", action="store_true",
                    help="never use Pillow (PNG inputs only)")
    ap.add_argument("--json", action="store_true", help="JSON report")
    args = ap.parse_args(argv)

    files = []
    for p in args.paths:
        path = Path(p)
        if path.is_dir():
            files.extend(sorted(f for f in path.iterdir()
                                if f.suffix.lower() in IMG_EXTS))
        elif path.suffix.lower() in IMG_EXTS:
            files.append(path)
        else:
            print("ERROR: skipping non-image %s" % path, file=sys.stderr)
    if not files:
        print("ERROR: no input images", file=sys.stderr)
        return 2

    reports, had_error, any_findings = [], False, False
    for f in files:
        rep = check_image(f, args)
        if rep is None:
            had_error = True
            continue
        reports.append(rep)
        if rep["findings"]:
            any_findings = True
    if args.json:
        print(json.dumps({"images": reports}, ensure_ascii=False, indent=2))
    if had_error:
        return 2
    return 1 if any_findings else 0


if __name__ == "__main__":
    sys.exit(main())
