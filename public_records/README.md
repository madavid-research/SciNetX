# Public Records

This folder contains the maintained public-record materials for SciNetX.

Use it when preparing or refreshing:

- the Zenodo citation record
- the RRID / SciCrunch software resource record

The generator derives versioned Zenodo paths, release-note links, and release URLs from the resolved version. By default it prefers a semantic-version git tag on the current repository state and falls back to the version in the config when no tag is available.

Layout:

- `config/`: project-specific generator settings
- `zenodo/`: generated Zenodo-ready metadata and documentation bundle
- `rrid/`: generated RRID / SciCrunch-ready submission materials
- `build/`: generated distribution artifacts such as the Zenodo ZIP

Source of truth:

- `config/scinetx.json`

Generate or refresh the public records with:

```bash
python3 scripts/generate_public_records.py --config public_records/config/scinetx.json
```

Or use:

```bash
make public-records
```

Common overrides:

```bash
python3 scripts/generate_public_records.py --config public_records/config/scinetx.json --version 1.0.1
python3 scripts/generate_public_records.py --config public_records/config/scinetx.json --git-tag v1.0.1 --release-date 2026-04-01
```

Release checklist:

1. Create or confirm the release version or git tag.
2. Run the generator.
3. Review the regenerated files in `zenodo/` and `rrid/`.
4. Upload the Zenodo package from the current versioned folder or matching ZIP.
5. Submit or update the RRID / SciCrunch record with the generated submission text.
6. After DOI or RRID assignment, replace the placeholders in the config or generated references as needed and regenerate.
7. Refresh the root README badges after Zenodo DOI, RRID, or paper DOI assignment.

Detailed usage guidance:

- [../docs/public_records_workflow.md](../docs/public_records_workflow.md)
