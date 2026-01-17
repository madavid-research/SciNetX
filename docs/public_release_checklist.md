---
title: Public Release Checklist
---

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

