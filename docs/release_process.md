# Release process (public repo)

SciNetX implementation releases are distributed to licensed users via an institution portal.
This public repository does not build or publish artifacts.

This page documents how the public landing repository should be updated when a gated release happens.

## When a gated release is published
1) Update the public changelog entry in [CHANGELOG.md](../CHANGELOG.md) (high-level, non-sensitive).
2) Update [docs/releases.md](releases.md) if artifact types or portal packaging changed.
3) If the on-disk workspace contract changed, update:
   - [docs/output_schema.md](output_schema.md)
   - [docs/sample_output/](sample_output/) (keep fabricated/sanitized)
4) If new recurring issues emerge, update [docs/known_issues.md](known_issues.md).
5) If citation metadata changes, update [CITATION.cff](../CITATION.cff).

## Docs maintenance notes
- Output/table schema changes should be reflected in [docs/output_schema.md](output_schema.md) first, then mirrored in the fabricated sample under `docs/sample_output/`.
- Packaging-only changes (desktop/Docker/Colab delivery changes) usually affect [docs/requirements.md](requirements.md) and [docs/releases.md](releases.md), not the output schema.
- Support/routing updates should be kept consistent across [SUPPORT.md](../SUPPORT.md), issue templates, and [docs/contact.md](contact.md).

## What not to publish here
- Portal/registry URLs and credentials
- Non-public datasets or user workspaces
- Proprietary implementation details

## Optional: docs snapshot tags (public repo)
For stable references to the public landing documentation (for example, in manuscripts), a lightweight tag/release can be created in this public repository.

This should represent the state of the public docs at a point in time and should not be confused with gated SciNetX implementation releases.

Suggested naming:
- Tags: `landing-v0.1`, `landing-v0.2`, …
- GitHub Release title: “Landing docs snapshot: landing-v0.1”

Release notes should be limited to public-doc changes and links (no portal/registry details).
