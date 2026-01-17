# Sample output (sanitized preview)

This folder contains a tiny, **fabricated** SciNetX-style workspace layout intended only to illustrate the on-disk schema described in [docs/output_schema.md](../output_schema.md).

It is not derived from any restricted dataset and is not intended for scientific use.

## Layout

- `output/tables/` – small example CSV files
- `output/figures/` – placeholder artifacts
- `output/networks/` – placeholder artifacts
- `output/report/` – small text summaries

See [manifest.md](manifest.md) for a file-by-file description.

## How this maps to the UI (conceptual)
Different SciNetX builds may show different tabs, but the general mapping is:
- **Tables views** read from `output/tables/` (for example, `articles.csv`, `years.csv`).
- **Report/validation views** read from `output/report/` (for example, `validation_summary.txt`).
- **Networks views** read from `output/networks/` (placeholder in this fabricated sample).
- **Figures/plots views** read from `output/figures/` (placeholder in this fabricated sample).
