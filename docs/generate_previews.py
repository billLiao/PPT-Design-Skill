#!/usr/bin/env python3
"""Generate theme preview cards for PPT-Design-Skill README.

Reproduces each theme's cover-slide design (colors + layout structure from
design-system.md and examples/demo-*.mjs) as a 1200x675 PNG, then composes
a 3x3 grid. Typography approximated with locally available fonts:
  - CJK: WenQuanYi Zen Hei (decks use Georgia/Songti on user machines)
  - Latin/mono: DejaVu Serif / DejaVu Sans / DejaVu Sans Mono
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "previews"
OUT.mkdir(exist_ok=True)

W, H = 1200, 675  # 16:9, 120px per inch (matches LAYOUT_16x9 coords x120)
MX = 60           # 0.5" left margin

F_CJK = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"
F_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
F_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def hexc(h):
    return "#" + h


def blend(c1, c2, t):
    """Blend hex c1 toward c2 by t (0..1)."""
    a = tuple(int(c1[i:i + 2], 16) for i in (0, 2, 4))
    b = tuple(int(c2[i:i + 2], 16) for i in (0, 2, 4))
    m = tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))
    return "#%02x%02x%02x" % m


def lum(h):
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255


def on_dark(h):
    """Accent color readable on dark ink bg: brighten dark accents."""
    return blend(h, "ffffff", 0.6) if lum(h) < 0.35 else hexc(h)


def spaced(draw, xy, text, fnt, fill, spacing):
    """Draw text with letter-spacing (charSpacing approximation)."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + spacing
    return x


MAGAZINE = [
    ("ink-classic", "墨水经典", "INK CLASSIC · VOL.01", "商业发布与人文观察的通用默认选择",
     dict(ink="0a0a0b", paper="f1efea", accent="d4a574")),
    ("indigo-porcelain", "靛蓝瓷", "INDIGO PORCELAIN · TECH", "科技、研究与 AI 发布的冷静理性",
     dict(ink="0a1f3d", paper="f1f3f5", accent="4a90a4")),
    ("forest-ink", "森林墨", "FOREST INK · NATURE", "自然、文化与非虚构叙事的呼吸感",
     dict(ink="1a2e1f", paper="f5f1e8", accent="6b8e5a")),
    ("kraft-paper", "牛皮纸", "KRAFT PAPER · LIT", "怀旧、人文与独立杂志的年代感",
     dict(ink="2a1e13", paper="eedfc7", accent="b87333")),
    ("dune", "沙丘", "DESIGN GALLERY · 2026", "一场关于空间、光影与材质的对话",
     dict(ink="1f1a14", paper="f0e6d2", accent="c4a265")),
]

SWISS = [
    ("klein-blue", "克莱因蓝", "IKB KLEIN BLUE · SYSTEM", "科技发布会与数据陈述的高对比理性",
     dict(ink="1a1a1a", paper="f5f5f5", accent="002FA7")),
    ("lemon-yellow", "柠檬黄", "LEMON YELLOW · BOLD", "创意提案与年轻化品牌的高亮表达",
     dict(ink="1a1a1a", paper="f5f5f5", accent="FFD700")),
    ("lime-green", "柠檬绿", "LIME GREEN · ENERGY", "增长、活力与新技术主题的锐利强调",
     dict(ink="1a1a1a", paper="f5f5f5", accent="CCFF00")),
    ("safety-orange", "安全橙", "SAFETY ORANGE · ALERT", "行动号召与关键信息的高可见度",
     dict(ink="1a1a1a", paper="f5f5f5", accent="FF5F00")),
]


def draw_magazine(name, cjk, kicker, sub, c, idx):
    img = Image.new("RGB", (W, H), hexc(c["ink"]))
    d = ImageDraw.Draw(img)
    dim = blend(c["paper"], c["ink"], 0.35)

    # top-right style tag
    tag = f"MAGAZINE {idx:02d}/05"
    f_tag = font(F_MONO, 16)
    tw = d.textlength(tag, font=f_tag)
    d.text((W - MX - tw, 40), tag, font=f_tag, fill=dim)

    # kicker (mono, accent, charSpacing)
    spaced(d, (MX, 192), kicker, font(F_MONO, 18), hexc(c["accent"]), 5)

    # big title (CJK, serif-weight)
    d.text((MX, 238), cjk, font=font(F_CJK, 92), fill=hexc(c["paper"]),
           stroke_width=2, stroke_fill=hexc(c["paper"]))

    # subtitle
    d.text((MX, 372), sub, font=font(F_CJK, 30), fill=hexc(c["paper"]))

    # bottom hex line
    hexline = f"ink {c['ink']}  ·  paper {c['paper']}  ·  accent {c['accent']}"
    d.text((MX, 516), hexline, font=font(F_MONO, 18), fill=hexc(c["accent"]))
    return img


def draw_swiss(name, cjk, kicker, sub, c, idx):
    img = Image.new("RGB", (W, H), hexc(c["ink"]))
    d = ImageDraw.Draw(img)
    dim = blend("cccccc", c["ink"], 0.1)

    tag = f"SWISS {idx:02d}/04"
    f_tag = font(F_MONO, 16)
    tw = d.textlength(tag, font=f_tag)
    d.text((W - MX - tw, 40), tag, font=f_tag, fill=dim)

    # kicker (mono, accent, charSpacing 4)
    spaced(d, (MX, 180), kicker, font(F_MONO, 18), on_dark(c["accent"]), 5)

    # huge title (sans black weight)
    d.text((MX, 228), cjk, font=font(F_CJK, 90), fill="#ffffff",
           stroke_width=3, stroke_fill="#ffffff")

    # best-for line (mono gray, like demo bottom line)
    d.text((MX, 420), sub, font=font(F_CJK, 24), fill="#cccccc")

    # accent square motif (Swiss geometry)
    d.rectangle((W - MX - 48, 420, W - MX, 468), fill=hexc(c["accent"]))

    hexline = f"ink {c['ink']}  ·  paper {c['paper']}  ·  accent {c['accent']}"
    d.text((MX, 516), hexline, font=font(F_MONO, 18), fill=on_dark(c["accent"]))
    return img


def main():
    cards = []
    for i, (name, cjk, kicker, sub, c) in enumerate(MAGAZINE, 1):
        img = draw_magazine(name, cjk, kicker, sub, c, i)
        img.save(OUT / f"theme-{name}.png", optimize=True)
        cards.append(img)
    for i, (name, cjk, kicker, sub, c) in enumerate(SWISS, 1):
        img = draw_swiss(name, cjk, kicker, sub, c, i)
        img.save(OUT / f"theme-{name}.png", optimize=True)
        cards.append(img)

    # 3x3 grid
    gap = 24
    gw, gh = 3 * W + 4 * gap, 3 * H + 4 * gap
    grid = Image.new("RGB", (gw, gh), "#ffffff")
    for i, img in enumerate(cards):
        r, col = divmod(i, 3)
        grid.paste(img, (gap + col * (W + gap), gap + r * (H + gap)))
    grid = grid.resize((1600, round(gh * 1600 / gw)), Image.LANCZOS)
    grid.save(OUT / "themes-grid.png", optimize=True)
    print("generated:", sorted(p.name for p in OUT.glob("*.png")))


if __name__ == "__main__":
    main()
