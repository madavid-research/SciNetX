# SciNetX (Public Landing)

SciNetX is a bibliometric + network analysis pipeline and UI intended for gated distribution.

This public repository is a landing page only. The source code and release artifacts are shared with licensed users via an institution portal.

## How it works (60 seconds)
1) Run the pipeline once to produce an `output/` workspace (tables/figures/networks/report).
2) Open the UI (desktop app or Docker) and point it at that `output/` folder (“Data root”).
3) Explore, export, and share results (CSV tables and network exports).

## What SciNetX does
- Produces an `output/` workspace (tables/figures/networks/report) from supported inputs (e.g., PubMed/OpenAlex or custom CSV).
- Provides a Streamlit UI (and optional desktop bundle) to explore the resulting outputs.

## Documentation
- Overview: `docs/index.md`
- Output schema: `docs/output_schema.md`
- Requirements: `docs/requirements.md`
- Licensing (summary): `docs/licensing.md`
- Releases (portal): `docs/releases.md`
- Screenshots (placeholders): `docs/screenshots.md`
- FAQ: `docs/faq.md`
- Contributing (docs-only): `CONTRIBUTING.md`

## Licensing at a glance
- Source-available, gated distribution (not open source).
- Academic/nonprofit non-commercial use: permitted under the license provided to licensed users.
- Commercial use: requires a separate agreement.
See `docs/licensing.md` and `REQUEST_ACCESS.md`.

## How to obtain access (gated distribution)
See `REQUEST_ACCESS.md`.

## Citation
See `CITATION.cff`.

## Security
See `SECURITY.md`.

## Contact
- michael.david@cuanschutz.edu

## What this repo is (and isn’t)
- This repo is a public overview and access-request entry point.
- It does not contain the SciNetX implementation code or downloadable binaries/containers.
