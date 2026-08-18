# Hongda Zhao — personal website

Source for [hongda-zhao.github.io](https://hongda-zhao.github.io), built with [Quarto](https://quarto.org/).

The public site is a restrained bilingual personal notebook: a chronological homepage for life, technology, research, and academic records; a small set of evidence-based Highlight pages; and a location-based photo Gallery.

## Start here

- Human and AI maintenance guide: [`.github/MAINTENANCE.md`](.github/MAINTENANCE.md)
- Repository and Draft PR rules: [`AGENTS.md`](AGENTS.md)
- Gallery map internals and data sources: [`assets/map/README.md`](assets/map/README.md)
- Image processing, privacy, and icon sources: [`assets/README.md`](assets/README.md)

## Common commands

```bash
./scripts/preview.sh   # live local preview
./scripts/render.sh    # complete static build
git diff --check       # patch/whitespace check
```

The generated `_site/` directory is ignored. Never hand-edit it, and do not commit it during normal source changes.

Only the pages listed under `project.render` in `_quarto.yml` are public inputs. Working drafts, source data, QA notes, and build scripts must stay outside that allowlist.

## Publishing

Changes are reviewed through Draft PRs. After a PR is merged into `main`, [`.github/workflows/publish.yml`](.github/workflows/publish.yml) renders the site and publishes it to the `gh-pages` branch.
