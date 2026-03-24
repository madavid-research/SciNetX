# Documentation style guide

This guide applies to the public record documentation.

## Tone
- Prefer clear, friendly, reader-directed language for onboarding and issue templates.
- Prefer neutral, policy-style language for licensing/security/policies.

## Structure
- Use a single top-level `#` heading per file.
- Use short sections with descriptive headings.
- Prefer bullets for checklists and scannable instructions.

## Links
- Prefer clickable Markdown links instead of bare paths.
- Avoid internal URLs and non-public portal/registry details.
- Keep links compatible with GitHub.

## Data hygiene
- Do not include restricted/sensitive data (PHI/PII, internal hostnames, credentials, proprietary datasets).
- Prefer high-level public descriptions or approved screenshots over bundled example workspaces.

## Checks
- Run the link checker before submitting: `python scripts/check_markdown_links.py`.
