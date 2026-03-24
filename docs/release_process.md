# Release process (public record)

SciNetX implementation releases are distributed to licensed users through [portal.scinetx.com](https://portal.scinetx.com).
This public record repository does not build or publish artifacts.

This page documents how the public record repository should be updated when a gated release happens.

## When a gated release is published
1) Update the public changelog entry in [CHANGELOG.md](../CHANGELOG.md) (high-level, non-sensitive).
2) Update [docs/releases.md](releases.md) if artifact types or portal packaging changed.
3) If the user-facing description of delivered results changed, update:
   - [docs/what_you_get.md](what_you_get.md)
4) If the on-disk workspace contract changed, update:
   - [docs/output_schema.md](output_schema.md)
5) If new recurring issues emerge, update [docs/known_issues.md](known_issues.md).
6) If citation metadata changes, update [CITATION.cff](../CITATION.cff).

## Docs maintenance notes
- Changes to delivered result types should be reflected in [docs/what_you_get.md](what_you_get.md) and [docs/output_schema.md](output_schema.md).
- Packaging-only changes (desktop/Docker/Colab delivery changes) usually affect [docs/requirements.md](requirements.md) and [docs/releases.md](releases.md), not the output schema.
- Support/routing updates should be kept consistent across [SUPPORT.md](../SUPPORT.md), issue templates, and [docs/contact.md](contact.md).

## What not to publish here
- Portal/registry URLs and credentials
- Non-public datasets or user workspaces
- Proprietary implementation details

## Public GitHub release tag
For the stable public record in papers and citations, create a Git tag and GitHub Release in this repository that matches the public software version.

Suggested naming:
- Tags: `v1.0.0`, `v1.0.1`, ...
- GitHub Release title: "SciNetX v1.0.0"

Use [../RELEASE_NOTES_v1.0.0.md](../RELEASE_NOTES_v1.0.0.md) as the basis for the public GitHub Release body.

Release notes should be limited to public software, citation, and publication information (no portal/registry details).

## Suggested command sequence
After the public record repository changes are committed on the intended release commit:

```bash
git add -A
git commit -m "Prepare public release v1.0.0"
git tag -a v1.0.0 -m "SciNetX v1.0.0"
git push origin main
git push origin v1.0.0
```

If GitHub CLI is available, create the GitHub Release with:

```bash
gh release create v1.0.0 --title "SciNetX v1.0.0" --notes-file RELEASE_NOTES_v1.0.0.md
```

If GitHub CLI is not being used, create the GitHub Release in the repository UI and paste the contents of [../RELEASE_NOTES_v1.0.0.md](../RELEASE_NOTES_v1.0.0.md) into the release body.
