# Contributing

Thanks for helping improve SciNetX documentation and onboarding.

This repository supports the public SciNetX materials at [scinetx.com](https://scinetx.com). Licensed application access is handled through [scinetx.com](https://scinetx.com).

## What contributions are welcome here
- Documentation improvements (typos, clarity, structure).
- Public onboarding content (FAQ improvements, diagrams, screenshots).
- Issue reports that help the maintainer reproduce problems in distributed artifacts.

## What is not accepted here
- Code contributions to the full SciNetX application.
- Requests to publish non-public application source or release artifacts here.

## How to contribute
1) Open an Issue if you’re not sure (or if the change is substantial).
2) For small doc changes:
   - Fork this repository
   - Edit files under `docs/` or `README.md`
   - Open a pull request
3) For screenshots:
   - Add images under `docs/img/` (create the folder if needed)
   - Ensure screenshots contain no restricted/sensitive data

## Documentation conventions
- Prefer clickable Markdown links over bare paths (for example, `[docs/index.md](docs/index.md)`).
- Keep links compatible with GitHub (avoid references that rely on local filesystem structure).
- Keep the public materials free of restricted data (datasets, internal URLs, registry endpoints, credentials).
- Run the link check before submitting: `python scripts/check_markdown_links.py`.

## Docs style (lightweight)
- Use a single top-level `#` heading per file.
- Use sentence case for headings where possible.
- Keep paragraphs short and scannable (prefer bullets for checklists).
- Avoid adding screenshots unless fully sanitized and approved for public release.
- Avoid internal URLs and non-public application/registry details.

## Support and access
- Access requests: use `REQUEST_ACCESS.md`.
- Security issues: do not post publicly; see `SECURITY.md`.
