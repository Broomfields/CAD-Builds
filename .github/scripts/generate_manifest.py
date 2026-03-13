"""
generate_manifest.py

Walks the builds/ directory, reads the frontmatter from each build's
Markdown file, and writes a manifest.json at the repo root.

Each build folder is expected to contain a Markdown file with the same
name as the folder (e.g. builds/rocket-booster-bracket/rocket-booster-bracket.md).
Folders without a matching Markdown file are skipped with a warning.

The manifest is sorted by date descending (newest build first).
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
BUILDS_DIR = REPO_ROOT / "builds"
OUTPUT_FILE = REPO_ROOT / "manifest.json"

# Frontmatter fields to include in each card entry.
# 'files' is intentionally excluded — it belongs to the full build page, not the card.
CARD_FIELDS = ["title", "description", "date", "cover", "tags", "cad_tool", "status", "subpages"]


def parse_frontmatter(md_path: Path) -> dict | None:
    """
    Extract YAML frontmatter from a Markdown file.
    Returns a dict, or None if frontmatter is absent or malformed.
    """
    text = md_path.read_text(encoding="utf-8")

    if not text.startswith("---"):
        print(f"  [skip] No frontmatter found in {md_path.relative_to(REPO_ROOT)}")
        return None

    # Find the closing '---'
    end = text.find("\n---", 3)
    if end == -1:
        print(f"  [skip] Unclosed frontmatter in {md_path.relative_to(REPO_ROOT)}")
        return None

    raw_yaml = text[3:end].strip()

    try:
        return yaml.safe_load(raw_yaml)
    except yaml.YAMLError as exc:
        print(f"  [skip] YAML parse error in {md_path.relative_to(REPO_ROOT)}: {exc}")
        return None


def build_card(slug: str, frontmatter: dict) -> dict:
    """Build a single card entry from a slug and its parsed frontmatter."""
    card = {"slug": slug}
    for field in CARD_FIELDS:
        if field in frontmatter:
            value = frontmatter[field]
            # Normalise date to ISO string for consistent JSON serialisation
            if field == "date" and hasattr(value, "isoformat"):
                value = value.isoformat()
            card[field] = value
    return card


def main():
    if not BUILDS_DIR.is_dir():
        print(f"Error: builds directory not found at {BUILDS_DIR}", file=sys.stderr)
        sys.exit(1)

    builds = []

    for build_dir in sorted(BUILDS_DIR.iterdir()):
        if not build_dir.is_dir():
            continue
        if build_dir.name.startswith("."):
            continue

        slug = build_dir.name
        md_path = build_dir / f"{slug}.md"

        if not md_path.exists():
            print(f"  [skip] No markdown file for build: {slug}")
            continue

        print(f"  [read] {md_path.relative_to(REPO_ROOT)}")
        frontmatter = parse_frontmatter(md_path)
        if frontmatter is None:
            continue

        card = build_card(slug, frontmatter)
        builds.append(card)

    # Sort newest first; fall back gracefully if 'date' is missing
    builds.sort(key=lambda b: b.get("date", ""), reverse=True)

    manifest = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(builds),
        "builds": builds,
    }

    OUTPUT_FILE.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nManifest written to {OUTPUT_FILE.relative_to(REPO_ROOT)} ({len(builds)} build(s))")


if __name__ == "__main__":
    main()
