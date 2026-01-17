# Recommended GitHub settings (manual)

These settings are applied in the GitHub repository UI.

## About panel
Set:
- **Description**: “Public landing page and access request entry point for SciNetX (gated distribution).”
- **Website**: optional (leave blank until GitHub Pages is enabled)
- **Topics**: `bibliometrics`, `scientometrics`, `network-analysis`, `pubmed`, `openalex`

## Social preview
Add a social preview image that does not include restricted data (for example, a simple SciNetX wordmark).

Suggested file from this repository:
- `docs/img/SciNetX_logo_wordmark_below_square_1024.png`

## Discussions (optional)
Enable Discussions if separating questions from Issues is preferred.

## Issues
Keep `blank_issues_enabled: false` and use issue forms to route:
- access requests
- bug reports
- general inquiries

## Labels and triage (manual)
Recommended labels:
- `access-request`: access requests and licensing inquiries
- `bug`: bug reports against distributed artifacts
- `question`: general inquiries
- `docs`: documentation-only changes/issues
- `security`: security-related reports (public issues should be avoided; use as an internal marker if needed)

See: [labels.md](labels.md)

Recommended triage:
- **Access requests**: acknowledge and route to onboarding channel; avoid sharing portal/registry URLs publicly.
- **Bug reports**: request build identifier + environment + minimal reproduction; link to `docs/redaction_guide.md` for safe sharing.
- **Questions**: answer if public-safe; otherwise route to email.
