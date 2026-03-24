# Public Records Workflow

This workflow explains how to maintain the SciNetX Zenodo and RRID public-record materials without editing the generated outputs by hand.

## Source of truth

Edit the project configuration here:

- [../public_records/config/scinetx.json](../public_records/config/scinetx.json)

That file controls the reusable project metadata:

- fallback version and release date
- website and GitHub URLs
- DOI and RRID placeholders
- author, affiliation, contact email, and ORCID
- subjects / keywords
- branding assets
- the root location for generated public-record artifacts

Versioned Zenodo paths, release-note links, and GitHub release URLs are derived automatically from the resolved version, so they do not need to be edited separately.

## Generate the public records

Run:

```bash
python3 scripts/generate_public_records.py --config public_records/config/scinetx.json
```

Or:

```bash
make public-records
```

By default, the script prefers a semantic-version git tag on the current repository state, such as `v1.0.1`. If no suitable tag is found, it falls back to the `version` field in the config.

Optional overrides:

```bash
python3 scripts/generate_public_records.py --config public_records/config/scinetx.json --version 1.0.1
python3 scripts/generate_public_records.py --config public_records/config/scinetx.json --git-tag v1.0.1 --release-date 2026-04-01
```

## Release checklist

1. Create or confirm the release version or git tag.
2. Run the generator.
3. Review the regenerated files under [../public_records/zenodo](../public_records/zenodo) and [../public_records/rrid](../public_records/rrid).
4. Upload the refreshed Zenodo package.
5. Submit or update the RRID / SciCrunch record.
6. After assignment, replace the DOI or RRID placeholders and regenerate again if you want the local files to reflect the assigned identifiers.

This command regenerates:

- a versioned Zenodo bundle under [../public_records/zenodo](../public_records/zenodo)
- RRID materials under [../public_records/rrid/SciNetX](../public_records/rrid/SciNetX)
- a versioned Zenodo ZIP under [../public_records/build](../public_records/build)

The script also:

- copies the configured branding assets into the Zenodo and RRID folders
- refreshes the root README DOI badge placeholder
- validates that generated files are non-empty
- validates the generated JSON metadata files
- rebuilds the current versioned Zenodo ZIP

## What to submit

For Zenodo:

- Upload the contents of the current versioned folder under [../public_records/zenodo](../public_records/zenodo), or use the matching ZIP from [../public_records/build](../public_records/build)

For RRID / SciCrunch:

- Paste [../public_records/rrid/SciNetX/scicrunch-submission.txt](../public_records/rrid/SciNetX/scicrunch-submission.txt) into the SciCrunch submission form

## After assignment

After Zenodo assigns a DOI:

1. Update `doi_placeholder` in [../public_records/config/scinetx.json](../public_records/config/scinetx.json)
2. Regenerate the public records
3. Re-upload only if you want the deposited package to include the assigned DOI inside the files themselves

After SciCrunch assigns an RRID:

1. Replace the RRID placeholder where needed
2. Regenerate if you want the local public-record files to reflect the assigned RRID

## Editing guidance

Edit by hand:

- [../public_records/config/scinetx.json](../public_records/config/scinetx.json)

Do not normally edit by hand:

- generated files in [../public_records/zenodo](../public_records/zenodo)
- generated files in [../public_records/rrid](../public_records/rrid)
- generated ZIP files in [../public_records/build](../public_records/build)

If you need to change the wording of the generated Zenodo or RRID documents, update the templates in [../scripts/generate_public_records.py](../scripts/generate_public_records.py) and regenerate.
