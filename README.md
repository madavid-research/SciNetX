# SciNetX (Public Landing)

![Docs checks](https://github.com/madavid128/SciNetX-Public/actions/workflows/docs-check.yml/badge.svg)

SciNetX is a bibliometric + network analysis pipeline and UI intended for gated distribution.

This public repository is a landing page only. The source code and release artifacts are shared with licensed users via an institution portal.

## What’s in this repo
- Public overview documentation (`docs/`)
- Access request entry point (`REQUEST_ACCESS.md` + GitHub issue templates)
- Citation metadata (`CITATION.cff`)
- Security and support contact info (`SECURITY.md`, `SUPPORT.md`)
- A tiny fabricated `output/` workspace preview (`docs/sample_output/`)

## What’s not in this repo
- SciNetX implementation source code
- Downloadable binaries/containers
- Registry/portal URLs or credentials

## How it works (60 seconds)
1) Run the pipeline once to produce an `output/` workspace (tables/figures/networks/report).
2) Open the UI (desktop app or Docker) and point it at that `output/` folder (“Data root”).
3) Explore, export, and share results (CSV tables and network exports).

## Public preview (no gated artifacts)
See a tiny, fabricated example workspace layout at [docs/sample_output/](docs/sample_output/).

## Quickstart
### Public (this repo)
1) Read the overview: [docs/index.md](docs/index.md)
2) Review the on-disk outputs: [docs/output_schema.md](docs/output_schema.md)
3) Browse a tiny fabricated workspace preview: [docs/sample_output/](docs/sample_output/)
4) Request access (gated distribution): [REQUEST_ACCESS.md](REQUEST_ACCESS.md)

### After licensing (artifacts distributed via portal)
1) Obtain an artifact (desktop bundle and/or Docker) and onboarding docs from the institution portal.
2) Run the pipeline to produce an `output/` workspace.
3) Open the UI and set “Data root” to the `output/` folder.

## Bug reports (public)
This repo does not include implementation code, but bug reports against distributed artifacts are still useful.

- File a bug: https://github.com/madavid128/SciNetX-Public/issues/new?template=bug_report.yml
- Redaction guidance and support flow: [SUPPORT.md](SUPPORT.md)

## What SciNetX does
- Produces an `output/` workspace (tables/figures/networks/report) from supported inputs (e.g., PubMed/OpenAlex or custom CSV).
- Provides a Streamlit UI (and optional desktop bundle) to explore the resulting outputs.

## Documentation
- Overview: [docs/index.md](docs/index.md)
- Output schema: [docs/output_schema.md](docs/output_schema.md)
- Requirements: [docs/requirements.md](docs/requirements.md)
- Compatibility: [docs/compatibility.md](docs/compatibility.md)
- Glossary: [docs/glossary.md](docs/glossary.md)
- Known issues: [docs/known_issues.md](docs/known_issues.md)
- Licensing (summary): [docs/licensing.md](docs/licensing.md)
- Releases (gated portal): [docs/releases.md](docs/releases.md)
- Sample output (sanitized preview): [docs/sample_output/](docs/sample_output/)
- Screenshots: [docs/screenshots.md](docs/screenshots.md)
- FAQ: [docs/faq.md](docs/faq.md)
- Contributing (docs-only): [CONTRIBUTING.md](CONTRIBUTING.md)

## Licensing at a glance
- Source-available, gated distribution (not open source).
- Academic/nonprofit non-commercial use: permitted under the license provided to licensed users.
- Commercial use: requires a separate agreement.
See [docs/licensing.md](docs/licensing.md), [LICENSE](LICENSE), [LICENSE_COMMERCIAL.md](LICENSE_COMMERCIAL.md), and [REQUEST_ACCESS.md](REQUEST_ACCESS.md).

## How to obtain access (gated distribution)
See [REQUEST_ACCESS.md](REQUEST_ACCESS.md). Portal details/URLs are shared with licensed users during onboarding.

## Citation
See [CITATION.cff](CITATION.cff).

## Security
See [SECURITY.md](SECURITY.md).

## Contact
- michael.david@cuanschutz.edu
- Support details: [SUPPORT.md](SUPPORT.md)

## What this repo is (and isn’t)
- This repo is a public overview and access-request entry point.
- It does not contain the SciNetX implementation code or downloadable binaries/containers.

## FAQ (short)
- Access requests: [REQUEST_ACCESS.md](REQUEST_ACCESS.md)
- Licensing summary: [docs/licensing.md](docs/licensing.md)
- Sample output preview: [docs/sample_output/](docs/sample_output/)
- Known issues: [docs/known_issues.md](docs/known_issues.md)
- Security reporting: [SECURITY.md](SECURITY.md)
