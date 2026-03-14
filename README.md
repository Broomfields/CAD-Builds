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
https://github.com/Broomfields/PS-CMS-Builds/releases/download/builds-manifest/manifest.json
```

Raw assets are served directly from the repo:

```
# Images
https://raw.githubusercontent.com/Broomfields/PS-CMS-Builds/main/builds/{slug}/images/{filename}

# Downloadable files (STL, SCAD, etc.)
https://raw.githubusercontent.com/Broomfields/PS-CMS-Builds/main/builds/{slug}/files/{filename}
```

### Running the manifest generator locally

```bash
pip install pyyaml
python .github/scripts/generate_manifest.py
```

---

## Image convention

All images for a build live in an `images/` subdirectory inside the build folder:

```
builds/my-new-widget/
├── images/
│   ├── 01-overview.png
│   ├── 02-detail.jpeg
│   └── 03-printed.jpeg
└── my-new-widget.md
```

**Rules:**

- Every image must have a **unique stem** (filename without extension) regardless of extension.
- Use a **two-digit numeric prefix** to control display order: `01-`, `02-`, `03-`, etc.
- Rename screenshots and exports when adding them — don't keep CAD tool or OS-generated filenames.
- In frontmatter, `cover` and `gallery` use **bare names only** — no path, no extension:

```yaml
cover: "02-detail"
cover_alt: "Descriptive alt text for the cover image"
gallery:
  - name: "01-overview"
    label: "Overview of the assembled part"
  - name: "02-detail"
    label: "Close-up of the mounting geometry"
  - name: "03-printed"
    label: "Finished print on the bench"
```

The manifest generator resolves bare names to full relative paths (e.g. `images/02-detail.jpeg`) at build time by scanning the `images/` subdirectory. A warning is printed if a name cannot be resolved.

---

## Files convention

All downloadable assets (STL, SCAD, etc.) for a build live in a `files/` subdirectory inside the build folder:

```
builds/my-new-widget/
├── files/
│   ├── 01-part.stl
│   ├── 02-part-lid.stl
│   └── 03-part.scad
└── my-new-widget.md
```

**Rules:**

- Every file must have a **unique stem** (filename without extension) regardless of extension.
- Use a **two-digit numeric prefix** to control display order: `01-`, `02-`, `03-`, etc.
- In frontmatter, `files` uses **bare names only** — no path, no extension:

```yaml
files:
  - name: "01-part"
    label: "Part — STL"
  - name: "02-part-lid"
    label: "Part Lid — STL"
  - name: "03-part"
    label: "Part — OpenSCAD Source"
```

The manifest generator resolves bare names to full relative paths (e.g. `files/01-part.stl`) at build time by scanning the `files/` subdirectory. A warning is printed if a name cannot be resolved.

---

## Frontmatter field reference

All fields are written in the YAML frontmatter block at the top of the main page Markdown file.

| Field | Type | Required | Description |
|---|---|---|---|
| `title` | string | yes | Display name of the build. |
| `description` | string | yes | One-sentence summary shown on the project card. |
| `date` | `YYYY-MM-DD` | yes | Completion or publish date. Used to sort the manifest (newest first). |
| `cover` | bare image name | yes | Cover image shown on the project card. Use bare name — the generator resolves the extension (e.g. `"02-model-cap"`). |
| `cover_alt` | string | yes | Descriptive alt text for the cover image, used by screen readers and as a fallback. Should describe what is shown, not repeat the build title. |
| `gallery` | list of `{name, label}` | no | Ordered screenshots/renders for a gallery. Each entry is a bare name (resolved to a full path in the manifest) with a descriptive label for use as alt text or a caption. |
| `status` | string | no | Build status: `"complete"`, `"wip"`, or `"archived"`. |
| `featured` | boolean | no | Pin this build as featured (`true` / `false`). |
| `tags` | list of strings | no | Freeform tags for filtering (e.g. `["openscad", "3d-printing"]`). |
| `cad_tool` | string | no | Primary CAD application used (e.g. `"OpenSCAD"`, `"Fusion 360"`). |
| `license` | string | no | SPDX or Creative Commons identifier for the design (e.g. `"CC BY-SA 4.0"`, `"CC0"`). |
| `links` | list of `{label, url}` | no | External appearances — Thingiverse, Printables, MakerWorld, etc. |
| `credits` | list of `{label, author, url, license}` | no | Third-party assets or designs used. `license` key is optional within each entry. |
| `subpages` | list of strings | no | Bare filename stems of sub-page Markdown files in the same folder (see below). |
| `files` | list of `{name, label}` | no | Downloadable assets. Each entry is a bare name (resolved to a full path in the manifest) with a descriptive label. Files live in the `files/` subdirectory and use the same two-digit prefix convention as images. |

### `gallery` entry shape

```yaml
gallery:
  - name: "01-overview"
    label: "Overview of the assembled part"
  - name: "02-detail"
    label: "Close-up of the mounting geometry"
  - name: "03-printed"
    label: "Finished print on the bench"
```

In the manifest, each entry is resolved to `{ "src": "images/01-overview.png", "label": "..." }`.

### `links` entry shape

```yaml
links:
  - label: "Printables"
    url: "https://www.printables.com/model/example"
  - label: "Thingiverse"
    url: "https://www.thingiverse.com/thing:example"
```

### `credits` entry shape

```yaml
credits:
  - label: "Original bracket design"
    author: "Someone"
    url: "https://www.printables.com/model/original"
    license: "CC BY 4.0"
```

### `files` entry shape

```yaml
files:
  - name: "01-part"
    label: "Part — STL"
  - name: "02-part"
    label: "Part — OpenSCAD Source"
```

In the manifest, each entry is resolved to `{ "src": "files/01-part.stl", "label": "..." }`.

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
