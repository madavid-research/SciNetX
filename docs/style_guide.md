# Documentation style guide

This guide applies to the public landing repository documentation.

## Tone
- Prefer clear, friendly, reader-directed language for onboarding and issue templates.
- Prefer neutral, policy-style language for licensing/security/policies.

## Structure
- Use a single top-level `#` heading per file.
- Use short sections with descriptive headings.
- Prefer bullets for checklists and scannable instructions.

## Links
- Prefer clickable Markdown links instead of bare paths.
- Avoid internal URLs and institution-specific portal/registry details.
- Keep links compatible with GitHub and (optionally) GitHub Pages.

## Data hygiene
- Do not include restricted/sensitive data (PHI/PII, internal hostnames, credentials, proprietary datasets).
- Prefer fabricated or sanitized examples for any sample outputs.

## Checks
- Run the link checker before submitting: `python scripts/check_markdown_links.py`.

