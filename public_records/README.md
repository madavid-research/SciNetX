# Public Records

This folder contains the maintained Zenodo and RRID public-record materials for SciNetX.

This repository no longer uses a generator for these files. Update them manually when the public record changes.

Use this folder when preparing or refreshing:

- the Zenodo citation record
- the RRID / SciCrunch software resource record

## Manual update checklist

When the public record changes, review and manually update as needed:

- `README.md`
- `CITATION.cff`
- `CHANGELOG.md`
- `RELEASE_NOTES_v1.0.0.md` or the current release notes file
- `VERSION`
- files under `public_records/zenodo/`
- files under `public_records/rrid/`

Typical reasons to update:

- new public version or Git tag
- Zenodo DOI assignment or correction
- RRID wording or metadata updates
- citation metadata updates
- release-note or publication-link changes
- contact or affiliation changes

## Review before release

Before tagging or publishing a public-record update:

- review the Zenodo files under `public_records/zenodo/`
- review the RRID files under `public_records/rrid/`
- run `python3 scripts/check_markdown_links.py`
- confirm the DOI, RRID, version, and release-date values match across the public files

## Release notes

When publishing a public-record update:

- commit the updated public files
- create the matching Git tag and GitHub Release
- use the current `RELEASE_NOTES_*.md` file as the basis for the GitHub Release body
