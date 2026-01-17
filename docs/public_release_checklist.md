# Public release checklist

Use this checklist before making the repository public.

## Content and data hygiene
- Confirm `docs/sample_output/` is fabricated/sanitized and does not contain restricted data.
- Confirm `docs/img/` contains no sensitive data (PII, institution identifiers, internal hostnames, registry URLs).
- Confirm email/contact details are correct and consistent across `README.md`, `SUPPORT.md`, `SECURITY.md`, and issue templates.

## Landing page readiness
- Confirm `README.md` accurately describes the gated distribution model and does not imply binaries/source are present here.
- Confirm docs navigation links work: run `python scripts/check_markdown_links.py`.

## GitHub settings (manual)
- Set repository **About** text and topics (bibliometrics/scientometrics/network-analysis).
- Configure default branch protections as desired.
- Optionally enable GitHub Pages (recommended after public): Settings → Pages → `main` /docs.

## Go-live settings (manual)
Apply these settings in the GitHub repository UI after the repository is public.

- Set **Social preview** image (Settings → Social preview) to `docs/img/SciNetX_logo_wordmark_below_square_1024.png`.
- Confirm **About** panel:
  - Description: “Public landing page and access request entry point for SciNetX (gated distribution).”
  - Topics: `bibliometrics`, `scientometrics`, `network-analysis`, `pubmed`, `openalex`
- Create standard **labels** used by issue templates and triage (see [docs/labels.md](labels.md)).
- Decide whether to enable **Discussions** (Settings → General → Features → Discussions).
- Create a lightweight **docs snapshot tag/release** in this repo (optional, for stable citations of the landing docs):
  - Create a tag like `landing-v0.1` (or similar) and a GitHub Release with a short note.
  - Avoid implying this is a SciNetX implementation release (gated artifacts are separate).

## Citation metadata (manual)
When the manuscript is published, update [CITATION.cff](../CITATION.cff) with:
- `doi` (if available) and `date-released`
- preferred citation text for the paper (if the journal requires a specific format)
