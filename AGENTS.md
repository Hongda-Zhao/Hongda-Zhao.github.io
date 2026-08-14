# Repository workflow

## Automatic Draft PRs

- For any task that changes this website's tracked source files, finish the implementation and relevant validation, then automatically publish the completed work as a GitHub Draft PR without asking for a separate confirmation.
- If the current branch is the default branch, create a focused branch named `codex/<short-description>`. If the current task branch already has an open PR, update that PR instead of creating a duplicate.
- Before publishing, inspect the full diff, run `git diff --check`, and run `quarto render` when Quarto is available. Do not publish when a relevant check fails.
- Stage only files that belong to the requested change. Never include unrelated user changes or generated `_site/` output unless the user explicitly requests it.
- Use a concise commit message and a Draft PR description that states what changed, why, user impact, and validation performed.
- Push only the task branch. Never push directly to the default branch, force-push, mark a PR ready for review, merge a PR, or enable auto-merge unless the user explicitly asks in that turn.
- If authentication, conflicts, failing checks, or mixed unrelated changes prevent a safe Draft PR, stop and report the blocker rather than bypassing it.
- Read-only requests such as explanations, reviews, investigations, or status checks do not create commits or PRs.

## Site validation

- Treat `_quarto.yml`, Quarto source pages, shared HTML, JavaScript, and SCSS as source of truth; do not hand-edit generated files under `_site/`.
- For visual changes, verify the rendered site at desktop and mobile widths and check at least one nested page when shared navigation or layout changes.
- Preserve the site's English-default bilingual behavior and ensure the language control remains keyboard accessible.
