---
title: Output Schema
---

# Output schema (`output/`)

SciNetX produces a filesystem workspace. The UI points at the workspace root (“Data root”) and reads these subfolders:

- `tables/`: CSV/TSV outputs (metrics, long-form entities, per-year counts, etc.)
- `figures/`: rendered plots (HTML and/or image formats depending on build settings)
- `networks/`: network exports (e.g., GEXF/GraphML/HTML)
- `report/`: small human-readable summaries (validation, run summaries)

Public preview: see a tiny, fabricated example at [docs/sample_output/](sample_output/).

## Minimum expected structure
At minimum, the UI expects:
- `tables/` with at least the core tables (articles/years/venues/authors depending on the run mode)
- `report/validation_summary.txt` (if validation is enabled)

If a tab appears empty, it usually means the expected table for that view was not produced by the run configuration.
