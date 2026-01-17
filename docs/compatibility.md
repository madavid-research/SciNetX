# Compatibility

## Artifact types
SciNetX is distributed to licensed users through the institution portal in one or more of the following forms:
- Desktop bundle (macOS)
- Desktop bundle (Windows)
- Docker-based UI
- Colab notebook guidance (optional)

## Supported platforms (typical)
- **macOS desktop**: Apple Silicon and Intel builds may be provided depending on release.
- **Windows desktop**: 64-bit Windows builds may be provided depending on release.
- **Docker UI**: any platform supported by Docker Desktop / Docker Engine.

## Scale guidance (rough)
Performance depends on hardware, run settings, and the size/shape of the `output/` workspace.

Typical factors that affect runtime and UI responsiveness:
- number of records ingested (articles/works)
- size of network exports
- number and size of tables under `output/tables/`
- rendering settings for figures/networks

If a shared benchmark is needed for a specific environment, include hardware and data scale details in an access/support request.
