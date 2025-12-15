# How SciNetX works

SciNetX has two phases:

1) **Pipeline run** → produces an `output/` workspace:
   - `tables/`, `figures/`, `networks/`, `report/`
2) **Exploration UI** → points at that workspace (“Data root”) and renders dashboards, networks, and exports.

## Workflow diagram

```
Inputs (PubMed/OpenAlex or CSV)
            |
            v
     SciNetX pipeline
            |
            v
   output/ workspace folder
 (tables/figures/networks/report)
            |
            v
   Desktop UI or Docker UI
   (select Data root = output/)
```

The key idea is reproducibility: generate outputs once, then browse/share the output workspace.

