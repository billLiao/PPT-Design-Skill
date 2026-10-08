#!/usr/bin/env python3
"""Fetch the pptx tooling runtime from anthropics/skills at install time.

This repository does not vendor Anthropic PBC's pptx skill code -- its
license forbids redistribution. Instead, the runtime files this skill calls
at execution time (scripts/office/*, add_slide.py, clean.py, thumbnail.py)
are downloaded from the upstream repository into this skill directory on
first use, together with the upstream LICENSE.txt that governs them and the
upstream SKILL.md used as a design-ideas reference.

The upstream commit is pinned for reproducibility; override with --ref.

Usage:
    python3 scripts/setup_upstream.py             # install when missing
    python3 scripts/setup_upstream.py --check     # exit 0 iff installed
    python3 scripts/setup_upstream.py --force     # re-download
    python3 scripts/setup_upstream.py --ref main  # track a moving ref
"""

from __future__ import annotations

import argparse
import io
import json
import sys
import tarfile
import time
import urllib.request
from pathlib import Path

UPSTREAM_REPO = "anthropics/skills"
UPSTREAM_SUBDIR = "skills/pptx"
PINNED_REF = "683bc88e56f3e09ba94f7055977f3d3aa499f202"

# Tarball sources, tried in order. The ghfast.top mirror serves regions
# where codeload.github.com is unreachable.
TARBALL_URLS = (
    "https://codeload.github.com/{repo}/tar.gz/{ref}",
    "https://ghfast.top/https://github.com/{repo}/archive/{ref}.tar.gz",
)

# Relative to the skill root; must all exist after a successful install.
REQUIRED_FILES = (
    "LICENSE.txt",
    "upstream/SKILL.md",
    "scripts/add_slide.py",
    "scripts/clean.py",
    "scripts/thumbnail.py",
    "scripts/office/validate.py",
    "scripts/office/soffice.py",
)

MANIFEST_REL = Path("upstream") / ".upstream.json"


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def is_installed(root: Path) -> bool:
    return all((root / rel).is_file() for rel in REQUIRED_FILES)


def fetch_tarball(ref: str) -> bytes:
    errors = []
    for template in TARBALL_URLS:
        url = template.format(repo=UPSTREAM_REPO, ref=ref)
        try:
            print(f"downloading {url}")
            req = urllib.request.Request(
                url, headers={"User-Agent": "ppt-design-skill-setup"}
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                return resp.read()
        except Exception as exc:  # report every mirror failure, then fall through
            errors.append(f"{url}: {exc}")
    raise SystemExit("all mirrors failed:\n  " + "\n  ".join(errors))


def split_member(name: str) -> str | None:
    """Return the path relative to skills/pptx/ for a tarball member.

    Handles both a bare checkout (skills/pptx/...) and a GitHub tarball
    with an archive root dir (skills-<sha>/skills/pptx/...).
    """
    prefix = UPSTREAM_SUBDIR.rstrip("/") + "/"
    if name.startswith(prefix):
        return name[len(prefix):]
    pos = name.find("/" + prefix)
    if pos != -1:
        return name[pos + 1 + len(prefix):]
    return None


def upstream_members(tf: tarfile.TarFile) -> list[tuple[tarfile.TarInfo, str]]:
    """(member, relpath-under-skills/pptx) pairs; files only, no traversal."""
    out = []
    for m in tf.getmembers():
        name = m.name
        while name.startswith("./"):
            name = name[2:]
        if not m.isfile():
            continue
        rel = split_member(name)
        if rel is None or not rel or ".." in Path(rel).parts:
            continue
        out.append((m, rel))
    return out


def map_member(rel: str) -> str:
    """<rel under skills/pptx> -> destination relative to the skill root.

    LICENSE.txt lands at the skill root (it licenses the fetched code),
    SKILL.md goes to upstream/ so it never overwrites this repo's own
    SKILL.md, scripts/** keep their canonical paths, anything else a
    future upstream adds is mirrored under upstream/.
    """
    if rel == "LICENSE.txt":
        return rel
    if rel == "SKILL.md":
        return "upstream/SKILL.md"
    if rel.startswith("scripts/"):
        return rel
    return "upstream/" + rel


def install(root: Path, ref: str) -> None:
    blob = fetch_tarball(ref)
    written = []
    with tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz") as tf:
        for m, rel in upstream_members(tf):
            dest_rel = map_member(rel)
            dest = root / dest_rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            src = tf.extractfile(m)
            if src is None:
                continue
            dest.write_bytes(src.read())
            written.append(dest_rel)
    missing = [rel for rel in REQUIRED_FILES if not (root / rel).is_file()]
    if missing:
        raise SystemExit("install incomplete, missing: " + ", ".join(missing))
    manifest = {
        "repo": UPSTREAM_REPO,
        "ref": ref,
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "files": len(written),
    }
    (root / MANIFEST_REL).write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(f"installed {len(written)} files from {UPSTREAM_REPO}@{ref}")
    print("next: pip install defusedxml lxml Pillow 'markitdown[pptx]'")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ref", default=PINNED_REF, help="upstream ref to fetch")
    ap.add_argument("--check", action="store_true", help="only verify presence")
    ap.add_argument("--force", action="store_true", help="re-download even if present")
    args = ap.parse_args()

    root = skill_root()
    if args.check:
        ok = is_installed(root)
        print("installed" if ok else "not installed")
        return 0 if ok else 1
    if is_installed(root) and not args.force:
        print("already installed; use --force to re-download")
        return 0
    install(root, args.ref)
    return 0


if __name__ == "__main__":
    sys.exit(main())
