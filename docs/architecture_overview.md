# Architecture overview (high-level)

SciNetX follows a two-phase workflow:

1) **Pipeline run**: consumes inputs and produces an `output/` workspace on disk.
2) **Exploration UI**: reads that `output/` workspace (“Data root”) and renders dashboards, tables, and networks.

This public record repository does not include implementation code; the goal here is to explain how results are created and then reviewed in the SciNetX interface.

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
- What you get: [what_you_get.md](what_you_get.md)
- Results package reference: [output_schema.md](output_schema.md)
- How it works: [how_it_works.md](how_it_works.md)
