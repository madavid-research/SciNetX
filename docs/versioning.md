# Versioning & build identifiers

When reporting bugs, including a precise build identifier helps reproduce the
issue quickly.

## Public version record
The stable public version record for SciNetX is maintained in:
- [../VERSION](../VERSION)
- [../CHANGELOG.md](../CHANGELOG.md)
- [../CITATION.cff](../CITATION.cff)

These public files can be updated as versions change without publishing artifacts in this repository.

## Accepted identifiers
- **Semantic version** (if provided): for example, `1.0.0`
- **Licensed release ID**: a release identifier from [scinetx.com](https://scinetx.com) (if applicable)
- **Docker image digest**: for example, `sha256:...`
- **Desktop build identifier**: any build string shown in the application UI/about panel

## Where to find it
- **Desktop**: check the application “About” panel (or startup log) for a version/build string.
- **Docker**: use the image reference provided during onboarding; if using a digest, include the full `sha256:...` value.
- **Colab**: include the notebook version/date plus any referenced release ID.

## If no identifier is available
Include:
- artifact type (desktop/Docker/Colab)
- operating system and architecture
- approximate install/onboarding date

## Public update pattern
When the public version changes:
- update [../VERSION](../VERSION)
- update [../CHANGELOG.md](../CHANGELOG.md)
- update [../CITATION.cff](../CITATION.cff)
- update public references in [index.md](index.md) and [../README.md](../README.md)
- optionally create a matching Git tag such as `v1.0.1`
