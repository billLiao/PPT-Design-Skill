#!/usr/bin/env python3
"""Shared JS source scanner for QA gates (stdlib only).

strip_comments(): blank out // and /* */ comments while preserving character
offsets (comments become spaces, newlines kept), so regex matches over the
stripped source still carry valid line numbers. String literals are tracked
so "https://..." inside quotes is not treated as a comment.

Known approximations (fine for a gate):
  - regex literals containing // are misread as comments (rare in slide code)
  - template-literal ${} nesting is not tracked
"""
from __future__ import annotations

import re

# Property-scoped color literal: color/fill/background/line/outline/glow/shadow
# followed by a quoted 3- or 6-hex value. Property scoping avoids false
# positives on unrelated quoted numbers (dates like "202610").
COLOR_RE = re.compile(
    r"\b(?:color|fill|background|line|outline|glow|shadow)\s*[:=]\s*"
    r"[\"']#?([0-9A-Fa-f]{3}|[0-9A-Fa-f]{6})[\"']")

FONT_RE = re.compile(r"\bfontFace\s*[:=]\s*[\"']([^\"']+)[\"']")


def strip_comments(src: str) -> str:
    out = list(src)
    i, n = 0, len(src)
    quote = None
    while i < n:
        c = src[i]
        if quote:
            if c == "\\":
                i += 2
                continue
            if c == quote:
                quote = None
            i += 1
            continue
        if c in "\"'`":
            quote = c
            i += 1
            continue
        if c == "/" and i + 1 < n:
            nxt = src[i + 1]
            if nxt == "/":
                j = i
                while j < n and src[j] != "\n":
                    out[j] = " "
                    j += 1
                i = j
                continue
            if nxt == "*":
                j = i + 2
                while j + 1 < n and not (src[j] == "*" and src[j + 1] == "/"):
                    if src[j] != "\n":
                        out[j] = " "
                    j += 1
                if j + 1 < n:
                    out[j] = " "
                    out[j + 1] = " "
                    j += 2
                i = j
                continue
        i += 1
    return "".join(out)


def expand_hex(v: str) -> str:
    """3-hex -> 6-hex; returns upper-case 6-hex."""
    v = v.strip().lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    return v.upper()
