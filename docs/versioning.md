---
title: Versioning & Build Identifiers
---

# Versioning & build identifiers

When reporting bugs, including a precise build identifier helps reproduce the
issue quickly.

## Accepted identifiers
- **Semantic version** (if provided): for example, `0.1.0`
- **Portal release ID**: an institution portal release identifier (if applicable)
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

