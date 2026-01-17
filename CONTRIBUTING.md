# Contributing (Public Landing Repo)

Thanks for helping improve SciNetX documentation and onboarding.

This public repository is a landing page only. The SciNetX implementation source code and release artifacts are distributed through a gated institution portal.

## What contributions are welcome here
- Documentation improvements (typos, clarity, structure).
- Public-facing onboarding content (FAQ improvements, diagrams, screenshots).
- Issue reports that help the maintainer reproduce problems in distributed artifacts.

## What is not accepted here
- Code contributions to the SciNetX implementation (the code is not in this public repo).
- Requests to publish the gated implementation source code publicly.

## How to contribute
1) Open an Issue if you’re not sure (or if the change is substantial).
2) For small doc changes:
   - Fork this public repo
   - Edit files under `docs/` or `README.md`
   - Open a pull request
3) For screenshots:
   - Add images under `docs/img/` (create the folder if needed)
   - Ensure screenshots contain no restricted/sensitive data

## Documentation conventions
- Prefer clickable Markdown links over bare paths (for example, `[docs/index.md](docs/index.md)`).
- Keep links compatible with GitHub and GitHub Pages (avoid references that rely on local filesystem structure).
- Keep the public repo free of restricted data (datasets, internal URLs, registry endpoints, credentials).
- Run the link check before submitting: `python scripts/check_markdown_links.py`.

## Support and access
- Access requests: use the “Access request” issue template or `REQUEST_ACCESS.md`.
- Security issues: do not post publicly; see `SECURITY.md`.
