const SLIDE_W = 10;
const SLIDE_H = 5.625;

function isDark(variant) {
  return variant === "dark";
}

function slideColors(theme, variant) {
  const dark = isDark(variant);
  return {
    bg: dark ? theme.ink : theme.paper,
    fg: dark ? theme.paper : theme.ink,
    muted: dark ? theme.paperTint : theme.inkTint,
    card: dark ? theme.inkTint : theme.paperTint
  };
}

function safeText(v) {
  if (v === null || v === undefined) return "";
  return String(v);
}

function addChrome(slide, theme, colors, content) {
  const left = safeText(content?.left);
  const right = safeText(content?.right);
  if (!left && !right) return;

  const fontFace = theme.fonts.mono || theme.fonts.body;
  const y = 0.2;
  const h = 0.25;
  if (left) {
    slide.addText(left, {
      x: 0.65,
      y,
      w: 6.6,
      h,
      fontFace,
      fontSize: 10,
      color: colors.muted
    });
  }
  if (right) {
    slide.addText(right, {
      x: 7.25,
      y,
      w: 2.1,
      h,
      fontFace,
      fontSize: 10,
      color: colors.muted,
      align: "right"
    });
  }
}

function addFoot(slide, theme, colors, content) {
  const left = safeText(content?.left);
  const right = safeText(content?.right);
  if (!left && !right) return;

  const fontFace = theme.fonts.mono || theme.fonts.body;
  const y = SLIDE_H - 0.42;
  const h = 0.25;
  if (left) {
    slide.addText(left, {
      x: 0.65,
      y,
      w: 6.6,
      h,
      fontFace,
      fontSize: 10,
      color: colors.muted
    });
  }
  if (right) {
    slide.addText(right, {
      x: 7.25,
      y,
      w: 2.1,
      h,
      fontFace,
      fontSize: 10,
      color: colors.muted,
      align: "right"
    });
  }
}

function addKicker(slide, theme, colors, text, y) {
  const t = safeText(text);
  if (!t) return y;
  slide.addText(t, {
    x: 0.65,
    y,
    w: 8.7,
    h: 0.3,
    fontFace: theme.fonts.mono || theme.fonts.body,
    fontSize: 12,
    color: colors.muted
  });
  return y + 0.35;
}

function addTitle(slide, theme, colors, text, y, fontSize = 48) {
  const t = safeText(text);
  if (!t) return y;
  slide.addText(t, {
    x: 0.65,
    y,
    w: 8.7,
    h: 0.9,
    fontFace: theme.fonts.head,
    fontSize,
    color: colors.fg
  });
  return y + 0.75;
}

function addSubtitle(slide, theme, colors, text, y) {
  const t = safeText(text);
  if (!t) return y;
  slide.addText(t, {
    x: 0.65,
    y,
    w: 8.7,
    h: 0.5,
    fontFace: theme.fonts.body,
    fontSize: 20,
    color: colors.fg
  });
  return y + 0.5;
}

function addLead(slide, theme, colors, text, y, maxW = 7.2) {
  const t = safeText(text);
  if (!t) return y;
  slide.addText(t, {
    x: 0.65,
    y,
    w: maxW,
    h: 1.1,
    fontFace: theme.fonts.body,
    fontSize: 16,
    color: colors.fg,
    valign: "top"
  });
  return y + 0.95;
}

function renderCover(slide, deck, theme, ST, slideSpec, idx, total) {
  const colors = slideColors(theme, slideSpec.variant || "dark");
  slide.background = { color: colors.bg };

  addChrome(slide, theme, colors, {
    left: slideSpec?.chrome?.[0] || deck?.meta?.date || "",
    right: slideSpec?.chrome?.[1] || slideSpec?.kicker || ""
  });

  let y = 1.35;
  y = addKicker(slide, theme, colors, slideSpec.kicker, y);
  y = addTitle(slide, theme, colors, slideSpec.title, y, 54);
  y = addSubtitle(slide, theme, colors, slideSpec.subtitle, y);
  y = addLead(slide, theme, colors, slideSpec.lead, y, 7.8);

  const meta = Array.isArray(slideSpec.meta) ? slideSpec.meta.map(safeText).filter(Boolean) : [];
  if (meta.length) {
    slide.addText(meta.join(" · "), {
      x: 0.65,
      y: y + 0.1,
      w: 8.7,
      h: 0.35,
      fontFace: theme.fonts.mono || theme.fonts.body,
      fontSize: 12,
      color: colors.muted
    });
  }

  const foot = Array.isArray(slideSpec.foot) ? slideSpec.foot : [];
  addFoot(slide, theme, colors, { left: safeText(foot[0]), right: safeText(foot[1]) });
}

function renderSection(slide, deck, theme, ST, slideSpec, idx, total) {
  const variant = slideSpec.variant || "light";
  const colors = slideColors(theme, variant);
  slide.background = { color: colors.bg };

  addChrome(slide, theme, colors, {
    left: slideSpec?.chrome?.[0] || "",
    right: slideSpec?.chrome?.[1] || `${idx + 1} / ${total}`
  });

  let y = 1.6;
  y = addKicker(slide, theme, colors, slideSpec.kicker, y);
  y = addTitle(slide, theme, colors, slideSpec.title, y, 64);
  y = addSubtitle(slide, theme, colors, slideSpec.subtitle, y);
  addFoot(slide, theme, colors, {
    left: safeText(slideSpec?.foot?.[0] || ""),
    right: safeText(slideSpec?.foot?.[1] || "")
  });
}

function renderBigNumber(slide, deck, theme, ST, slideSpec, idx, total) {
  const variant = slideSpec.variant || "light";
  const colors = slideColors(theme, variant);
  slide.background = { color: colors.bg };

  addChrome(slide, theme, colors, {
    left: slideSpec?.chrome?.[0] || "",
    right: slideSpec?.chrome?.[1] || `${idx + 1} / ${total}`
  });

  let y = 0.75;
  y = addKicker(slide, theme, colors, slideSpec.kicker, y);
  y = addTitle(slide, theme, colors, slideSpec.title, y, 44);

  const items = Array.isArray(slideSpec.items) ? slideSpec.items : [];
  const cols = 3;
  const rows = 2;
  const cardW = (SLIDE_W - 0.65 * 2 - 0.35 * (cols - 1)) / cols;
  const cardH = 1.45;
  const startX = 0.65;
  const startY = y + 0.25;

  for (let i = 0; i < Math.min(items.length, cols * rows); i += 1) {
    const c = i % cols;
    const r = Math.floor(i / cols);
    const x = startX + c * (cardW + 0.35);
    const yy = startY + r * (cardH + 0.35);
    const it = items[i] || {};

    slide.addShape(ST.rect, {
      x,
      y: yy,
      w: cardW,
      h: cardH,
      fill: { color: colors.card }
    });

    slide.addText(safeText(it.label), {
      x: x + 0.2,
      y: yy + 0.15,
      w: cardW - 0.4,
      h: 0.3,
      fontFace: theme.fonts.mono || theme.fonts.body,
      fontSize: 11,
      color: colors.muted
    });

    const value = safeText(it.value);
    const unit = safeText(it.unit);
    slide.addText(unit ? `${value} ${unit}` : value, {
      x: x + 0.2,
      y: yy + 0.42,
      w: cardW - 0.4,
      h: 0.6,
      fontFace: theme.fonts.head,
      fontSize: 34,
      color: colors.fg
    });

    slide.addText(safeText(it.note), {
      x: x + 0.2,
      y: yy + 1.1,
      w: cardW - 0.4,
      h: 0.3,
      fontFace: theme.fonts.body,
      fontSize: 12,
      color: colors.muted
    });
  }

  const foot = Array.isArray(slideSpec.foot) ? slideSpec.foot : [];
  addFoot(slide, theme, colors, { left: safeText(foot[0]), right: safeText(foot[1]) });
}

function renderTwoColumn(slide, deck, theme, ST, slideSpec, idx, total) {
  const variant = slideSpec.variant || "light";
  const colors = slideColors(theme, variant);
  slide.background = { color: colors.bg };

  addChrome(slide, theme, colors, {
    left: slideSpec?.chrome?.[0] || "",
    right: slideSpec?.chrome?.[1] || `${idx + 1} / ${total}`
  });

  let y = 0.75;
  y = addKicker(slide, theme, colors, slideSpec.kicker, y);
  y = addTitle(slide, theme, colors, slideSpec.title, y, 44);

  const leftX = 0.65;
  const leftW = 5.85;
  const rightX = leftX + leftW + 0.45;
  const rightW = 2.4;
  const contentY = y + 0.2;

  const left = slideSpec.left || {};
  const right = slideSpec.right || {};

  addLead(slide, theme, colors, left.lead, contentY, leftW);

  if (slideSpec.callout?.text) {
    const boxY = SLIDE_H - 1.65;
    slide.addShape(ST.roundRect, {
      x: leftX,
      y: boxY,
      w: leftW,
      h: 1.1,
      fill: { color: colors.card }
    });
    slide.addText(safeText(slideSpec.callout.text), {
      x: leftX + 0.25,
      y: boxY + 0.18,
      w: leftW - 0.5,
      h: 0.55,
      fontFace: theme.fonts.body,
      fontSize: 14,
      color: colors.fg
    });
    if (slideSpec.callout.source) {
      slide.addText("— " + safeText(slideSpec.callout.source), {
        x: leftX + 0.25,
        y: boxY + 0.75,
        w: leftW - 0.5,
        h: 0.3,
        fontFace: theme.fonts.mono || theme.fonts.body,
        fontSize: 11,
        color: colors.muted
      });
    }
  }

  if (slideSpec.image) {
    slide.addImage({
      path: slideSpec.image,
      x: rightX,
      y: contentY,
      w: rightW,
      h: 3.25,
      sizing: { type: "cover", w: rightW, h: 3.25 }
    });
  } else {
    slide.addShape(ST.rect, {
      x: rightX,
      y: contentY,
      w: rightW,
      h: 3.25,
      fill: { color: colors.card }
    });
    slide.addText(safeText(right.caption || ""), {
      x: rightX + 0.2,
      y: contentY + 0.2,
      w: rightW - 0.4,
      h: 3.0,
      fontFace: theme.fonts.body,
      fontSize: 12,
      color: colors.muted,
      valign: "top"
    });
  }

  const foot = Array.isArray(slideSpec.foot) ? slideSpec.foot : [];
  addFoot(slide, theme, colors, { left: safeText(foot[0]), right: safeText(foot[1]) });
}

function renderImageGrid(slide, deck, theme, ST, slideSpec, idx, total) {
  const variant = slideSpec.variant || "light";
  const colors = slideColors(theme, variant);
  slide.background = { color: colors.bg };

  addChrome(slide, theme, colors, {
    left: slideSpec?.chrome?.[0] || "",
    right: slideSpec?.chrome?.[1] || `${idx + 1} / ${total}`
  });

  let y = 0.75;
  y = addKicker(slide, theme, colors, slideSpec.kicker, y);
  y = addTitle(slide, theme, colors, slideSpec.title, y, 40);

  const images = Array.isArray(slideSpec.images) ? slideSpec.images : [];
  const cols = 3;
  const rows = 2;
  const gap = 0.25;
  const gridW = SLIDE_W - 0.65 * 2;
  const cellW = (gridW - gap * (cols - 1)) / cols;
  const cellH = 1.35;
  const startX = 0.65;
  const startY = y + 0.15;

  for (let i = 0; i < cols * rows; i += 1) {
    const c = i % cols;
    const r = Math.floor(i / cols);
    const x = startX + c * (cellW + gap);
    const yy = startY + r * (cellH + gap);
    const img = images[i];
    if (img?.path) {
      slide.addImage({
        path: img.path,
        x,
        y: yy,
        w: cellW,
        h: cellH,
        sizing: { type: "cover", w: cellW, h: cellH }
      });
    } else {
      slide.addShape(ST.rect, { x, y: yy, w: cellW, h: cellH, fill: { color: colors.card } });
      slide.addText(safeText(img?.caption || ""), {
        x: x + 0.15,
        y: yy + 0.15,
        w: cellW - 0.3,
        h: cellH - 0.3,
        fontFace: theme.fonts.body,
        fontSize: 11,
        color: colors.muted,
        valign: "top"
      });
    }
  }
}

function renderPipeline(slide, deck, theme, ST, slideSpec, idx, total) {
  const variant = slideSpec.variant || "light";
  const colors = slideColors(theme, variant);
  slide.background = { color: colors.bg };

  addChrome(slide, theme, colors, {
    left: slideSpec?.chrome?.[0] || "",
    right: slideSpec?.chrome?.[1] || `${idx + 1} / ${total}`
  });

  let y = 0.75;
  y = addKicker(slide, theme, colors, slideSpec.kicker, y);
  y = addTitle(slide, theme, colors, slideSpec.title, y, 42);

  const lanes = Array.isArray(slideSpec.lanes) ? slideSpec.lanes : [];
  const laneW = (SLIDE_W - 0.65 * 2 - 0.35) / 2;
  const laneH = 3.55;
  const startX = 0.65;
  const startY = y + 0.15;

  for (let i = 0; i < Math.min(lanes.length, 2); i += 1) {
    const lane = lanes[i] || {};
    const x = startX + i * (laneW + 0.35);
    slide.addShape(ST.roundRect, { x, y: startY, w: laneW, h: laneH, fill: { color: colors.card } });
    slide.addText(safeText(lane.label), {
      x: x + 0.25,
      y: startY + 0.18,
      w: laneW - 0.5,
      h: 0.3,
      fontFace: theme.fonts.mono || theme.fonts.body,
      fontSize: 11,
      color: colors.muted
    });

    const steps = Array.isArray(lane.steps) ? lane.steps : [];
    let sy = startY + 0.55;
    for (let s = 0; s < Math.min(steps.length, 4); s += 1) {
      const st = steps[s] || {};
      slide.addShape(ST.roundRect, {
        x: x + 0.2,
        y: sy,
        w: laneW - 0.4,
        h: 0.7,
        fill: { color: colors.bg },
        line: { color: colors.bg }
      });
      slide.addText(String(s + 1).padStart(2, "0"), {
        x: x + 0.35,
        y: sy + 0.12,
        w: 0.55,
        h: 0.3,
        fontFace: theme.fonts.mono || theme.fonts.body,
        fontSize: 12,
        color: colors.muted,
        align: "center"
      });
      slide.addText(safeText(st.title), {
        x: x + 0.95,
        y: sy + 0.1,
        w: laneW - 1.2,
        h: 0.3,
        fontFace: theme.fonts.body,
        fontSize: 13,
        color: colors.fg,
        bold: true
      });
      slide.addText(safeText(st.desc), {
        x: x + 0.95,
        y: sy + 0.38,
        w: laneW - 1.2,
        h: 0.28,
        fontFace: theme.fonts.body,
        fontSize: 11,
        color: colors.muted
      });
      sy += 0.8;
    }
  }
}

function renderQuestion(slide, deck, theme, ST, slideSpec, idx, total) {
  const colors = slideColors(theme, slideSpec.variant || "dark");
  slide.background = { color: colors.bg };

  addChrome(slide, theme, colors, {
    left: slideSpec?.chrome?.[0] || "",
    right: slideSpec?.chrome?.[1] || `${idx + 1} / ${total}`
  });

  let y = 1.7;
  y = addKicker(slide, theme, colors, slideSpec.kicker, y);
  slide.addText(safeText(slideSpec.question), {
    x: 0.65,
    y,
    w: 8.7,
    h: 2.2,
    fontFace: theme.fonts.head,
    fontSize: 46,
    color: colors.fg,
    valign: "top"
  });
}

function renderQuote(slide, deck, theme, ST, slideSpec, idx, total) {
  const colors = slideColors(theme, slideSpec.variant || "dark");
  slide.background = { color: colors.bg };

  addChrome(slide, theme, colors, {
    left: slideSpec?.chrome?.[0] || "",
    right: slideSpec?.chrome?.[1] || `${idx + 1} / ${total}`
  });

  slide.addText("“" + safeText(slideSpec.quote) + "”", {
    x: 0.9,
    y: 1.6,
    w: 8.2,
    h: 1.8,
    fontFace: theme.fonts.head,
    fontSize: 40,
    color: colors.fg,
    align: "center",
    valign: "middle"
  });

  if (slideSpec.source) {
    slide.addText("— " + safeText(slideSpec.source), {
      x: 0.9,
      y: 3.6,
      w: 8.2,
      h: 0.4,
      fontFace: theme.fonts.mono || theme.fonts.body,
      fontSize: 12,
      color: colors.muted,
      align: "center"
    });
  }
}

function renderBeforeAfter(slide, deck, theme, ST, slideSpec, idx, total) {
  const variant = slideSpec.variant || "light";
  const colors = slideColors(theme, variant);
  slide.background = { color: colors.bg };

  addChrome(slide, theme, colors, {
    left: slideSpec?.chrome?.[0] || "",
    right: slideSpec?.chrome?.[1] || `${idx + 1} / ${total}`
  });

  let y = 0.75;
  y = addTitle(slide, theme, colors, slideSpec.title, y, 40);

  const colW = (SLIDE_W - 0.65 * 2 - 0.35) / 2;
  const leftX = 0.65;
  const rightX = leftX + colW + 0.35;
  const boxY = y + 0.25;

  const before = Array.isArray(slideSpec.before) ? slideSpec.before : [];
  const after = Array.isArray(slideSpec.after) ? slideSpec.after : [];

  for (const [x, label, items] of [
    [leftX, "BEFORE", before],
    [rightX, "AFTER", after]
  ]) {
    slide.addShape(ST.roundRect, { x, y: boxY, w: colW, h: 3.25, fill: { color: colors.card } });
    slide.addText(label, {
      x: x + 0.25,
      y: boxY + 0.18,
      w: colW - 0.5,
      h: 0.3,
      fontFace: theme.fonts.mono || theme.fonts.body,
      fontSize: 11,
      color: colors.muted
    });

    let ty = boxY + 0.55;
    for (let i = 0; i < Math.min(items.length, 6); i += 1) {
      slide.addText("• " + safeText(items[i]), {
        x: x + 0.3,
        y: ty,
        w: colW - 0.6,
        h: 0.35,
        fontFace: theme.fonts.body,
        fontSize: 14,
        color: colors.fg
      });
      ty += 0.45;
    }
  }
}

function renderMixed(slide, deck, theme, ST, slideSpec, idx, total) {
  const variant = slideSpec.variant || "light";
  const colors = slideColors(theme, variant);
  slide.background = { color: colors.bg };

  addChrome(slide, theme, colors, {
    left: slideSpec?.chrome?.[0] || "",
    right: slideSpec?.chrome?.[1] || `${idx + 1} / ${total}`
  });

  let y = 0.75;
  y = addKicker(slide, theme, colors, slideSpec.kicker, y);
  y = addTitle(slide, theme, colors, slideSpec.title, y, 40);

  const imgX = 0.65;
  const imgY = y + 0.15;
  const imgW = 5.1;
  const imgH = 3.2;
  const textX = imgX + imgW + 0.45;
  const textW = SLIDE_W - 0.65 - textX;

  if (slideSpec.image) {
    slide.addImage({ path: slideSpec.image, x: imgX, y: imgY, w: imgW, h: imgH, sizing: { type: "cover", w: imgW, h: imgH } });
  } else {
    slide.addShape(ST.rect, { x: imgX, y: imgY, w: imgW, h: imgH, fill: { color: colors.card } });
  }

  const bullets = Array.isArray(slideSpec.bullets) ? slideSpec.bullets : [];
  const lines = bullets.map((b) => "• " + safeText(b)).join("\n");
  slide.addText(lines, {
    x: textX,
    y: imgY,
    w: textW,
    h: imgH,
    fontFace: theme.fonts.body,
    fontSize: 14,
    color: colors.fg,
    valign: "top"
  });

  if (slideSpec.caption) {
    slide.addText(safeText(slideSpec.caption), {
      x: imgX,
      y: imgY + imgH + 0.12,
      w: imgW,
      h: 0.3,
      fontFace: theme.fonts.mono || theme.fonts.body,
      fontSize: 11,
      color: colors.muted
    });
  }
}

function ensureSlides(deck) {
  const slides = Array.isArray(deck?.slides) ? deck.slides : [];
  if (!slides.length) throw new Error("deck.json has no slides");
  return slides;
}

export async function renderDeck(pptx, deck, theme) {
  const slides = ensureSlides(deck);
  const total = slides.length;
  const ST = pptx.ShapeType;
  for (let i = 0; i < slides.length; i += 1) {
    const slideSpec = slides[i] || {};
    const type = slideSpec.type;
    const slide = pptx.addSlide();

    if (type === "cover") renderCover(slide, deck, theme, ST, slideSpec, i, total);
    else if (type === "section") renderSection(slide, deck, theme, ST, slideSpec, i, total);
    else if (type === "big-number") renderBigNumber(slide, deck, theme, ST, slideSpec, i, total);
    else if (type === "two-column") renderTwoColumn(slide, deck, theme, ST, slideSpec, i, total);
    else if (type === "image-grid") renderImageGrid(slide, deck, theme, ST, slideSpec, i, total);
    else if (type === "pipeline") renderPipeline(slide, deck, theme, ST, slideSpec, i, total);
    else if (type === "question") renderQuestion(slide, deck, theme, ST, slideSpec, i, total);
    else if (type === "quote") renderQuote(slide, deck, theme, ST, slideSpec, i, total);
    else if (type === "before-after") renderBeforeAfter(slide, deck, theme, ST, slideSpec, i, total);
    else if (type === "mixed") renderMixed(slide, deck, theme, ST, slideSpec, i, total);
    else {
      const colors = slideColors(theme, slideSpec.variant || deck?.defaults?.variant || "light");
      slide.background = { color: colors.bg };
      slide.addText(`Unknown slide type: ${safeText(type)}`, {
        x: 0.65,
        y: 1.8,
        w: 8.7,
        h: 1.0,
        fontFace: theme.fonts.body,
        fontSize: 20,
        color: colors.fg
      });
    }
  }
}
