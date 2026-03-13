# PS-CMS-Builds

This repo manages documentation and media for CAD design builds. Each build is a folder under `builds/` containing a Markdown file whose frontmatter is compiled into a release manifest, allowing the site to dynamically render project cards and build pages.

---

## Usage

### Adding a new build

1. Create a folder under `builds/` named with a kebab-case slug (e.g. `my-new-widget`).
2. Add a Markdown file inside it with the **same name as the folder** (e.g. `builds/my-new-widget/my-new-widget.md`). This is the main page.
3. Populate the frontmatter (see field reference below).
4. Push to `main`. The [generate-manifest](.github/workflows/generate-manifest.yml) workflow runs automatically and publishes an updated `manifest.json` to the `builds-manifest` release tag.

The stable manifest URL is always:

```
https://github.com/Broomfields/CAD-Builds/releases/download/builds-manifest/manifest.json
```

Raw assets (images, STL files, etc.) are served directly from the repo:

```
https://raw.githubusercontent.com/Broomfields/CAD-Builds/main/builds/{slug}/{filename}
```

### Running the manifest generator locally

```bash
pip install pyyaml
python .github/scripts/generate_manifest.py
```

---

## Frontmatter field reference

All fields are written in the YAML frontmatter block at the top of the main page Markdown file.

| Field | Type | Required | Description |
|---|---|---|---|
| `title` | string | yes | Display name of the build. |
| `description` | string | yes | One-sentence summary shown on the project card. |
| `date` | `YYYY-MM-DD` | yes | Completion or publish date. Used to sort the manifest (newest first). |
| `cover` | string | yes | Relative path to the cover image (e.g. `images/01-cover.png`). |
| `tags` | list of strings | no | Freeform tags for filtering (e.g. `["openscad", "3d-printing"]`). |
| `cad_tool` | string | no | Primary CAD application used (e.g. `"OpenSCAD"`, `"Fusion 360"`). |
| `status` | string | no | Build status: `"complete"`, `"wip"`, or `"archived"`. |
| `subpages` | list of strings | no | Bare filename stems of sub-page Markdown files in the same folder (see below). |
| `files` | list of objects | no | Downloadable assets. Each entry has `name` (filename) and `label` (display text). Not included in the manifest — only used on the full build page. |

### `files` entry shape

```yaml
files:
  - name: "part.stl"
    label: "Part — STL"
  - name: "part.scad"
    label: "Part — OpenSCAD Source"
```

---

## Sub-pages

A build can have one or more sub-pages for supplementary content (print settings, design notes, etc.).

**Convention:**

- Sub-pages live in the **same folder** as the main page.
- The main page is always the `.md` file that matches the folder name. Every other `.md` file in that folder is a sub-page.
- Declare sub-pages in the main page's frontmatter as bare filename stems — no `.md` extension, no path:

```yaml
subpages:
  - "print-settings"
  - "design-notes"
```

- Sub-pages carry their own minimal frontmatter with a `title` and a `parent` field pointing back to the build slug:

```yaml
---
title: "Print Settings — My Build"
parent: "my-build"
---
```

**Internal links** to sub-pages in body Markdown use bare slugs with no extension:

```markdown
See [Print Settings](print-settings) for the layer config.
```

The site consumer intercepts relative links (no protocol, no leading slash) and routes them to sub-page components rather than rendering a plain `<a>` tag.
