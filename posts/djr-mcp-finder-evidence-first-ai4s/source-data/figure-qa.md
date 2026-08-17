# Figure QA notes

- Target: responsive web article with an 820 px body column, not a journal submission.
- Core conclusion: a reliable AI4S result depends on auditable evidence boundaries, not the largest development score alone.
- Archetypes: evidence-flow cover; label matrix plus selection funnel; conceptual split schematic plus quantitative audit; model-selection lollipop plus decision cards; end-to-end provenance workflow.
- Backend: Python/Matplotlib only for drawing, previewing, and export.
- Source data: `figure-data.json`; the row-split expectation is an explicitly labelled derivation from the frozen component-size histogram.
- Exclusions: none performed by the plotting script. The script reads all values in the compact source record that are used by the figures.
- Exports: SVG is the primary web asset, PDF preserves editable text, and 320 dpi PNG is the visual-review/fallback asset. TIFF is intentionally omitted because the deliverable is a web article and every panel is vector line art rather than microscopy or photography.
- Width warning: the 12–12.5 inch design canvas targets responsive browser scaling and is intentionally wider than common 89/183 mm journal defaults.
- Color: labels and direct text accompany color; red/green is never the only carrier of meaning.
- Statistics: the figures report frozen Train-only five-fold selection values and a deterministic split-risk expectation. They do not display a Test result, confidence interval, causal HardNeg effect, or external-generalization claim.
- Visual review: inspect SVG/PNG at full size and at the rendered article width; verify text remains readable and no label is clipped or overlapped.
