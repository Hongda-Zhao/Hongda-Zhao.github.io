# Hongda Zhao — personal website

This repository contains the source for [hongda-zhao.github.io](https://hongda-zhao.github.io), built with [Quarto](https://quarto.org/). The structure supports academic work, technical projects, activities, and personal writing without mixing everything into one long CV page.

## Where to add content

The site is intentionally a visual skeleton. Search the `.qmd` files for `EDIT:`, `PHOTO:`, `PDF:`, and square-bracket placeholders such as `[Role · Institution]`.

- Homepage and featured evidence: `index.qmd`
- Profile, education, experience, and personal interests: `about.qmd`
- Research themes: `research.qmd`
- Selected projects: `projects.qmd`
- Publications and preprints: `publications.qmd`
- Conferences, talks, teaching, service, and life photographs: `activities.qmd`
- Life, technology, research, and activity writing: `notes.qmd`
- Web CV and printable résumé: `cv.qmd`
- New-note template: `posts/template/index.qmd`
- Image replacement instructions: `assets/README.md`
- Colors, typography, and layout: `styles.scss`
- Navigation and site-wide settings: `_quarto.yml`

Keep the homepage short. Put detail on the corresponding inner page and link to evidence such as a paper, repository, poster, dataset, talk, or activity photograph.

## Recommended filling order

1. Replace the homepage statement, current role, and opportunity preference.
2. Complete the Profile and CV pages.
3. Add two strong projects and two or three research themes.
4. Add one academic activity, one community activity, and three personal photographs.
5. Add publications and external evidence links.
6. Publish the first note only after replacing its metadata and changing `draft: true` to `draft: false`.

## Preview the site

```bash
./scripts/preview.sh
```

Build the complete site before publishing:

```bash
./scripts/render.sh
```

## Add a note

Copy the template folder, rename it, and update the YAML header:

```bash
cp -R posts/template posts/my-note
```

The new note appears automatically on the Writing page after rendering. Use `Life`, `Technology`, `Research`, or `Activities` as its first category.

## Publishing

The workflow in `.github/workflows/publish.yml` renders and publishes the site to the `gh-pages` branch whenever `main` is updated. The repository's GitHub Pages source must be set to the `gh-pages` branch once during initial setup.
