# Public release checklist

Use this checklist before making the repository public.

## Content and data hygiene
- Confirm `docs/img/` contains no sensitive data (PII, organization identifiers, internal hostnames, registry URLs).
- Confirm email/contact details are correct and consistent across `README.md`, `SUPPORT.md`, `SECURITY.md`, and issue templates.

## Landing page readiness
- Confirm `README.md` accurately describes the gated distribution model and does not imply binaries/source are present here.
- Confirm `docs/what_you_get.md` reflects the current licensed user experience.
- Confirm docs navigation links work: run `python scripts/check_markdown_links.py`.

## GitHub settings (manual)
- Set repository **About** text and topics to match [github_settings.md](github_settings.md).
- Configure default branch protections as desired.
- No separate website build is required for the public record repository.

## Go-live settings (manual)
Apply these settings in the GitHub repository UI after the repository is public.

- Set **Social preview** image (Settings → Social preview) to `docs/img/SciNetX_logo_wordmark_below_square_1024.png`.
- Confirm **About** panel:
  - Description: “Bibliometric and network analysis platform with access, citation, and publication information for SciNetX.”
  - Topics: `bibliometrics`, `scientometrics`, `network-analysis`, `research-analytics`, `publication-analysis`, `citation-analysis`, `science-of-science`, `openalex`, `pubmed`
- Create standard **labels** used by issue templates and triage (see [docs/labels.md](labels.md)).
- Decide whether to enable **Discussions** (Settings → General → Features → Discussions).
- Create a public **Git tag and GitHub Release** for the current software version:
  - Create a tag like `v1.0.0`.
  - Use [../RELEASE_NOTES_v1.0.0.md](../RELEASE_NOTES_v1.0.0.md) as the public release-note body.
  - Keep the GitHub Release limited to public software, citation, and publication information.
  - Suggested local commands:
    - `git add -A`
    - `git commit -m "Prepare public release v1.0.0"`
    - `git tag -a v1.0.0 -m "SciNetX v1.0.0"`
    - `git push origin main`
    - `git push origin v1.0.0`
  - Suggested GitHub CLI command:
    - `gh release create v1.0.0 --title "SciNetX v1.0.0" --notes-file RELEASE_NOTES_v1.0.0.md`

## Citation metadata (manual)
When the manuscript is published, update [CITATION.cff](../CITATION.cff) with:
- `doi` (if available) and `date-released`
- preferred citation text for the paper (if the journal requires a specific format)
