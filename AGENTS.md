# Repository workflow

## Required context

- Before changing this website, read `.github/MAINTENANCE.md`. It is the canonical site design and content-update guide.
- For Gallery map data or boundaries, also read `assets/map/README.md`.
- Treat the current source as authoritative. If an architectural or design rule changes, update `.github/MAINTENANCE.md` in the same PR.

## Site contract

- Preserve the restrained bilingual personal-notebook design: English by default, optional Chinese, white editorial layout, green accent, global left sidebar, short factual homepage entries, standalone Highlights, and the location-based Gallery.
- Do not reintroduce a top navigation, Blog/Research/Activities/About categories, CV, long biography, commercial card shadows/rounded panels, or verbose placeholder commentary unless the user explicitly requests a new direction. Preserve the existing functional circles used by the avatar and map markers.
- Keep external links, language controls, images, keyboard focus, ARIA labels, and mobile layouts accessible.
- Do not place HTML inside translation values in `head.html`; its i18n code writes with `textContent`. Keep semantic markup in QMD/HTML and split translated sentences when needed.
- Ordinary Gallery updates must synchronize the WebP asset, `gallery.qmd`, `assets/map/gallery-places.js`, and the place/alt translations in `head.html`. Do not edit `assets/js/gallery-map.js` for routine additions.

## Automatic Draft PRs

- For any task that changes this website's tracked source files, finish the implementation and relevant validation, then automatically publish the completed work as a GitHub Draft PR without asking for a separate confirmation.
- If the current branch is the default branch, create a focused branch named `codex/<short-description>`. If the current task branch already has an open PR, update that PR instead of creating a duplicate.
- Before publishing, inspect the full diff, run `git diff --check`, and run `./scripts/render.sh`. Do not publish when a relevant check fails.
- Stage only files that belong to the requested change. Never include unrelated user changes or generated `_site/` output unless the user explicitly requests it.
- Use a concise commit message and a Draft PR description that states what changed, why, user impact, and validation performed.
- Push only the task branch. Never push directly to the default branch, force-push, mark a PR ready for review, merge a PR, or enable auto-merge unless the user explicitly asks in that turn.
- If authentication, conflicts, failing checks, or mixed unrelated changes prevent a safe Draft PR, stop and report the blocker rather than bypassing it.
- Read-only requests such as explanations, reviews, investigations, or status checks do not create commits or PRs.

## Site validation

- Treat `_quarto.yml`, Quarto source pages, shared HTML, JavaScript, and SCSS as source of truth; do not hand-edit generated files under `_site/`.
- For visual changes, verify the rendered site at desktop and mobile widths and check at least one nested page when shared navigation or layout changes.
- Preserve the site's English-default bilingual behavior and ensure the language control remains keyboard accessible.
- For Gallery changes, verify that cards, image files, map photo IDs, administrative codes, translation keys, counts, marker scrolling, and lightbox order remain synchronized.
