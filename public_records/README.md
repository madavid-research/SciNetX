# Public Records

This folder contains the maintained Zenodo and RRID public-record materials for SciNetX.

Use it when preparing or refreshing:

- the Zenodo citation record
- the RRID / SciCrunch software resource record

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

For the full workflow, release checklist, overrides, and post-assignment updates, see [../docs/public_records_workflow.md](../docs/public_records_workflow.md).

## Reuse and license scope

The public-record generation tooling and templates are available under the
scoped BSD-3-Clause license in
[../LICENSE-public-record-tools-BSD-3-Clause.txt](../LICENSE-public-record-tools-BSD-3-Clause.txt).

That scoped license applies to the generator workflow and related public-record
templates. It does not apply to the SciNetX software platform itself,
controlled-access materials, or SciNetX branding assets.
