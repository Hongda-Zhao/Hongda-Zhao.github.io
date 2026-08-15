# Asset policy

## Images

- Shared site artwork lives directly in `assets/` (`avatar-cat.jpg`, `og.png`).
- Gallery photographs live in `assets/gallery/` as metadata-stripped WebP files named `YYYY-MM-DD-place-slug.webp`.
- Highlight images live beside their corresponding `highlights/<slug>/index.qmd` so each record remains self-contained.
- `profile.jpg` is currently unreferenced; do not expose or reuse it unless the user explicitly asks.

Always record the image's real `width` and `height`, write a factual English alt, and add a Chinese alt through `data-i18n-alt` when the page supports language switching. Do not commit desktop originals or absolute local paths.

## Privacy and provenance

- Remove EXIF, GPS, XMP, device, and author metadata before publishing personal photographs.
- Confirm consent before publishing identifiable group photographs.
- Inspect workplace photographs for screens, papers, badges, contact details, and unpublished information.
- Do not guess species, people, or locations in alt text; describe only what is visible and verified.
- Prefer official publication, conference, university, and brand sources for third-party material.

## Sidebar icons

The profile links use local copies so they remain visible without third-party icon requests:

- Google Scholar: [Simple Icons](https://simpleicons.org/)
- GitHub: official [Primer Octicons](https://primer.style/octicons/)
- LinkedIn: approved blue `[in]` mark from the official [LinkedIn brand site](https://brand.linkedin.com/in-logo)
- Email: [Bootstrap Icons](https://icons.getbootstrap.com/)
- iNaturalist: official [iNaturalist press asset](https://www.inaturalist.org/pages/press)

Platform names and logos remain trademarks of their respective owners. They are used only to identify and link to Hongda Zhao's profiles on those services.
