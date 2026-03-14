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

CARD_FIELDS = [
    "title",
    "description",
    "date",
    "cover",
    "cover_alt",
    "gallery",
    "files",
    "status",
    "featured",
    "tags",
    "cad_tool",
    "license",
    "links",
    "credits",
    "subpages",
]


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


def resolve_file(build_dir: Path, bare_name: str) -> str | None:
    """
    Given a bare file name (no extension, no path), find the matching file
    in the build's files/ subdirectory and return its relative path
    (e.g. 'files/01-rocket-cap.stl').
    Returns None and prints a warning if no match is found.
    Multiple files with the same stem are an error — the convention requires
    unique names regardless of extension.
    """
    files_dir = build_dir / "files"
    if not files_dir.is_dir():
        print(f"  [warn] No files/ directory in {build_dir.name} — cannot resolve '{bare_name}'")
        return None
    matches = [f for f in files_dir.iterdir() if f.is_file() and f.stem == bare_name]
    if not matches:
        print(f"  [warn] File not found for bare name '{bare_name}' in {build_dir.name}/files/")
        return None
    if len(matches) > 1:
        names = ", ".join(f.name for f in matches)
        print(f"  [warn] Multiple files match '{bare_name}' in {build_dir.name}/files/: {names} — using first")
    return f"files/{matches[0].name}"


def resolve_image(build_dir: Path, bare_name: str) -> str | None:
    """
    Given a bare image name (no extension, no path), find the matching file
    in the build's images/ subdirectory and return its relative path
    (e.g. 'images/02-model-cap.jpeg').
    Returns None and prints a warning if no match is found.
    Multiple files with the same stem are an error — the convention requires
    unique names regardless of extension.
    """
    images_dir = build_dir / "images"
    if not images_dir.is_dir():
        print(f"  [warn] No images/ directory in {build_dir.name} — cannot resolve '{bare_name}'")
        return None
    matches = [f for f in images_dir.iterdir() if f.is_file() and f.stem == bare_name]
    if not matches:
        print(f"  [warn] Image not found for bare name '{bare_name}' in {build_dir.name}/images/")
        return None
    if len(matches) > 1:
        names = ", ".join(f.name for f in matches)
        print(f"  [warn] Multiple files match '{bare_name}' in {build_dir.name}/images/: {names} — using first")
    return f"images/{matches[0].name}"


def build_card(slug: str, frontmatter: dict, build_dir: Path) -> dict:
    """Build a single card entry from a slug and its parsed frontmatter."""
    card = {"slug": slug}
    for field in CARD_FIELDS:
        if field in frontmatter:
            value = frontmatter[field]
            # Normalise date to ISO string for consistent JSON serialisation
            if field == "date" and hasattr(value, "isoformat"):
                value = value.isoformat()
            elif field == "cover" and isinstance(value, str):
                value = resolve_image(build_dir, value) or value
            elif field == "gallery" and isinstance(value, list):
                resolved = []
                for entry in value:
                    if isinstance(entry, dict):
                        name = entry.get("name", "")
                        resolved.append({
                            "src": resolve_image(build_dir, name) or name,
                            "label": entry.get("label", ""),
                        })
                    else:
                        resolved.append({"src": resolve_image(build_dir, entry) or entry})
                value = resolved
            elif field == "files" and isinstance(value, list):
                resolved = []
                for entry in value:
                    if isinstance(entry, dict):
                        name = entry.get("name", "")
                        resolved.append({
                            "src": resolve_file(build_dir, name) or name,
                            "label": entry.get("label", ""),
                        })
                    else:
                        resolved.append({"src": resolve_file(build_dir, entry) or entry})
                value = resolved
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

        card = build_card(slug, frontmatter, build_dir)
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
