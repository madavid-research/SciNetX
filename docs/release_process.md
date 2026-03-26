# Release process (public record)

SciNetX implementation releases are distributed to licensed users through [scinetx.com](https://scinetx.com).
This public record repository does not build or publish artifacts.

This page documents how the public record repository should be updated when a gated release happens.

## Manual checks
The GitHub Actions workflows in this repository are configured for manual runs only through the Actions tab. They do not run on `push`, `pull_request`, or a timed schedule.

Use local commands before or alongside a manual Actions run:

```bash
make public-records-check
python3 scripts/check_markdown_links.py
```

## GitHub repository settings
Apply these settings manually in the GitHub repository UI as needed:

- About description: `Stable public software record for SciNetX with citation, publication, and access information.`
- Website: `https://scinetx.com`
- Social preview: `docs/img/SciNetX_logo_wordmark_below_square_1024.png`
- Topics: `bibliometrics`, `scientometrics`, `network-analysis`, `research-analytics`, `publication-analysis`, `citation-analysis`, `science-of-science`, `openalex`, `pubmed`
- Discussions: optional

Recommended labels:
- `bug`
- `question`
- `docs`
- `security`
- `access-request` only as a redirect marker for misfiled public access/licensing requests

## When a gated release is published
1) Update the public changelog entry in [CHANGELOG.md](../CHANGELOG.md) (high-level, non-sensitive).
2) Update [docs/releases.md](releases.md) if artifact types or licensed delivery packaging changed.
3) If the user-facing description of delivered results changed, update:
   - [docs/what_you_get.md](what_you_get.md)
4) If the on-disk workspace contract changed, update:
   - [docs/output_schema.md](output_schema.md)
5) If new recurring issues emerge, update [docs/known_issues.md](known_issues.md).
6) If citation metadata changes, update [CITATION.cff](../CITATION.cff).
7) Regenerate the public Zenodo and RRID materials in [../public_records/README.md](../public_records/README.md).

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

Release notes should be limited to public software, citation, and publication information (no internal application/registry details).

## Suggested command sequence
After the public record repository changes are committed on the intended release commit:

First regenerate the public records:

```bash
python3 scripts/generate_public_records.py --config public_records/config/scinetx.json
```

Or use the Make target:

```bash
make public-records
```

Then commit and tag the release:

```bash
git add -A
git commit -m "Prepare public release v1.0.0"
git tag -a v1.0.0 -m "SciNetX v1.0.0"
git push origin main
git push origin v1.0.0
```

Review the regenerated files under [../public_records/zenodo](../public_records/zenodo) and [../public_records/rrid](../public_records/rrid) before creating the GitHub Release.

If GitHub CLI is available, create the GitHub Release with:

```bash
gh release create v1.0.0 --title "SciNetX v1.0.0" --notes-file RELEASE_NOTES_v1.0.0.md
```

If GitHub CLI is not being used, create the GitHub Release in the repository UI and paste the contents of [../RELEASE_NOTES_v1.0.0.md](../RELEASE_NOTES_v1.0.0.md) into the release body.
