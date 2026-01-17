# Architecture overview (high-level)

SciNetX follows a two-phase workflow:

1) **Pipeline run**: consumes inputs and produces an `output/` workspace on disk.
2) **Exploration UI**: reads that `output/` workspace (“Data root”) and renders dashboards, tables, and networks.

This public repository does not include implementation code; the goal here is to explain the on-disk contract between the pipeline and the UI.

## Diagram

```
Inputs (PubMed/OpenAlex/CSV)
            |
            v
     SciNetX pipeline run
            |
            v
   output/ workspace folder
 (tables/figures/networks/report)
            |
            v
   Desktop UI or Docker UI
 (Data root = output/)
```

## Related docs
- Output schema: [output_schema.md](output_schema.md)
- How it works: [how_it_works.md](how_it_works.md)
- Sample output: [sample_output/](sample_output/)

