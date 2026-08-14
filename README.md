# Hongda Zhao — personal website

This repository contains the source for [hongda-zhao.github.io](https://hongda-zhao.github.io), built with [Quarto](https://quarto.org/). The public site is intentionally simple: one chronological notebook homepage, a small set of standalone detail pages, and external profile links in the sidebar.

## Where to add content

Search the `.qmd` files for `EDIT:`, `PHOTO:`, `PDF:`, and square-bracket placeholders when replacing unfinished content.

- Homepage notebook and its chronological entries: `index.qmd`
- Standalone records linked from the homepage: `highlights/*/index.qmd`
- Photo gallery, dates, places, and bilingual descriptions: `gallery.qmd`
- Optimized gallery images: `assets/gallery/`
- Optional project and publication pages: `projects.qmd` and `publications.qmd`
- Image replacement instructions: `assets/README.md`
- Colors, typography, and layout: `styles.scss`
- Sidebar links and site-wide settings: `_quarto.yml`
- English and Chinese interface copy: `head.html`

Keep each homepage entry short. Put longer personal notes, photographs, and evidence on a standalone page under `highlights/`.

## Recommended filling order

1. Replace the pending images and personal notes on the three existing highlight pages.
2. Add future life, technology, research, and activity entries to the homepage in date order.
3. Create a standalone detail page only when an entry needs more context or evidence.
4. Keep external profile links current in `_quarto.yml`.

## Preview the site

```bash
./scripts/preview.sh
```

Build the complete site before publishing:

```bash
./scripts/render.sh
```

## Add a standalone entry

Copy an existing highlight folder, rename it, and update its content and translation keys:

```bash
cp -R highlights/current-biology-acceptance highlights/my-new-entry
```

Then add a corresponding row to `index.qmd`. Standalone pages are not added to the homepage automatically.

## Publishing

The workflow in `.github/workflows/publish.yml` renders and publishes the site to the `gh-pages` branch whenever `main` is updated. The repository's GitHub Pages source must be set to the `gh-pages` branch once during initial setup.
