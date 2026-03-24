# How SciNetX works

SciNetX works in two steps:

1) **Create the results package**: SciNetX processes the selected inputs and produces a results folder with tables, figures, network files, and run summaries.
2) **Review the results in the UI**: the desktop or Docker interface opens that results folder and turns it into dashboards, visual views, and exports.

## Workflow diagram

```
Supported inputs
            |
            v
      SciNetX analysis
            |
            v
   results workspace
 (tables/figures/networks/report)
            |
            v
   Desktop UI or Docker UI
   (select the results folder)
```

The key idea is repeatability: create the results once, then return to the same results package for review, export, and sharing.
