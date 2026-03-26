# Redaction & privacy guide

When filing a public issue, assume anything posted can be indexed and copied.
Please redact sensitive or restricted content before posting screenshots, logs,
or example files.

## Do not include
- Patient/participant data, PHI/PII, or any individual-level identifiers.
- Institution-internal hostnames, VPN addresses, registry URLs, or internal application URLs.
- Credentials (API keys, tokens, passwords), even if expired.
- Proprietary datasets or non-public bibliographic exports.
- Full `output/` workspaces from restricted projects (unless explicitly sanitized).

## Safer alternatives
- Replace identifiers with placeholders (for example, `ORG_A`, `USER_1`, `HOST_X`).
- Share minimal excerpts (a few lines) instead of full logs or full tables.
- Prefer the support email for anything sensitive: michael.david@cuanschutz.edu.

## Helpful to include
- Artifact type (desktop/Docker/Colab) and version/build identifier.
- Operating system and architecture.
- Exact steps to reproduce and expected vs actual behavior.
- A minimal description of the `output/` workspace structure (folders present/missing).
