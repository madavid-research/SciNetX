#!/usr/bin/env python3
"""Generate public-facing Zenodo and RRID record bundles for SciNetX.

This script keeps the editable source of truth in a small JSON config and
rebuilds the user-facing public-record materials from templates. The generated
outputs are intentionally metadata-only and should not contain operational
software artifacts.

Licensing note: this public-record tooling is covered by the scoped BSD-3-Clause
license in LICENSE-public-record-tools-BSD-3-Clause.txt. That license does not
apply to the SciNetX software platform itself or to SciNetX branding assets.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path
from textwrap import dedent
from zipfile import ZIP_DEFLATED, ZipFile

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_config(path: Path) -> dict:
    """Load the JSON config that defines project metadata and output settings."""
    return json.loads(path.read_text(encoding="utf-8"))


SEMVER_TAG_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")


def ensure_parent(path: Path) -> None:
    """Create the parent directory for an output path when it does not yet exist."""
    path.parent.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    """Write a UTF-8 text file with exactly one trailing newline."""
    ensure_parent(path)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, payload: dict) -> None:
    """Write stable, pretty-printed UTF-8 JSON."""
    ensure_parent(path)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def bullet_list(items: list[str], tick: bool = False) -> str:
    """Render a Markdown bullet list and optionally wrap each item in backticks."""
    if tick:
        return "\n".join(f"- `{item}`" for item in items)
    return "\n".join(f"- {item}" for item in items)


def semicolon_list(items: list[str]) -> str:
    """Render items as a semicolon-delimited string for form-style text fields."""
    return "; ".join(items)


def human_list(items: list[str]) -> str:
    """Render a short human-readable list for narrative prose."""
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return f"{', '.join(items[:-1])}, and {items[-1]}"


def is_placeholder_value(value: str) -> bool:
    """Return True when an identifier still contains placeholder marker text."""
    return "XXXX" in value


def rrid_assigned(cfg: dict) -> bool:
    """Return True when the configured RRID is a real assigned identifier."""
    return not is_placeholder_value(cfg["rrid_placeholder"])


def rrid_citation_guidance(cfg: dict) -> str:
    """Build citation wording that reflects whether the RRID is assigned yet."""
    if rrid_assigned(cfg):
        return f"For citation, use the Zenodo DOI for the software record, cite the associated paper where relevant, and include RRID `{cfg['rrid_placeholder']}`."
    return "For citation, use the Zenodo DOI for the software record, cite the associated paper where relevant, and include the RRID once assigned."


def normalize_version_tag(tag: str) -> str:
    """Normalize a tag like v1.2.3 to the plain version string 1.2.3."""
    match = SEMVER_TAG_RE.fullmatch(tag.strip())
    if not match:
        raise ValueError(f"Unsupported version/tag format: {tag!r}. Expected vMAJOR.MINOR.PATCH or MAJOR.MINOR.PATCH.")
    return ".".join(match.groups())


def version_sort_key(version: str) -> tuple[int, int, int]:
    """Return a sortable semantic-version key for a normalized version string."""
    major, minor, patch = normalize_version_tag(version).split(".")
    return int(major), int(minor), int(patch)


def run_git(workspace: Path, args: list[str]) -> str:
    """Run a git command in the repository workspace and return trimmed stdout."""
    result = subprocess.run(
        ["git", *args],
        cwd=workspace,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def detect_git_version(workspace: Path) -> str | None:
    """Resolve the best semantic version from git tags for the current workspace."""
    try:
        exact_tags = [tag for tag in run_git(workspace, ["tag", "--points-at", "HEAD"]).splitlines() if tag]
    except subprocess.CalledProcessError:
        exact_tags = []
    semver_exact = [normalize_version_tag(tag) for tag in exact_tags if SEMVER_TAG_RE.fullmatch(tag)]
    if semver_exact:
        return sorted(semver_exact, key=version_sort_key)[-1]

    try:
        all_tags = [tag for tag in run_git(workspace, ["tag", "--list"]).splitlines() if tag]
    except subprocess.CalledProcessError:
        all_tags = []
    semver_tags = [normalize_version_tag(tag) for tag in all_tags if SEMVER_TAG_RE.fullmatch(tag)]
    if semver_tags:
        return sorted(semver_tags, key=version_sort_key)[-1]
    return None


def resolve_runtime_config(cfg: dict, workspace: Path, cli_version: str | None, cli_tag: str | None, cli_release_date: str | None) -> dict:
    """Resolve versioned fields from CLI overrides, git tags, and config defaults."""
    resolved = dict(cfg)
    version_source = cfg.get("version_source", "tag_or_config")

    if cli_version:
        version = normalize_version_tag(cli_version)
    elif cli_tag:
        version = normalize_version_tag(cli_tag)
    elif version_source in {"git-tag", "tag_or_config"}:
        git_version = detect_git_version(workspace)
        if git_version:
            version = git_version
        elif version_source == "git-tag":
            raise ValueError("No semver git tag was found, but version_source is set to 'git-tag'.")
        else:
            version = normalize_version_tag(cfg["version"])
    else:
        version = normalize_version_tag(cfg["version"])

    release_date = cli_release_date or cfg["release_date"]
    tag = f"v{version}"
    public_root = cfg.get("public_records_root", "public_records").rstrip("/")
    zenodo_record_name = f"{cfg['name']}-v{version}-zenodo-record"

    resolved["version"] = version
    resolved["release_date"] = release_date
    resolved["git_tag"] = tag
    resolved["public_records_root"] = public_root
    resolved["github_release_url"] = f"{cfg['github_url']}/releases/tag/{tag}"
    resolved["release_notes_url"] = f"{cfg['github_url']}/blob/main/RELEASE_NOTES_{tag}.md"
    resolved["zenodo_dir"] = f"{public_root}/zenodo/{zenodo_record_name}"
    resolved["rrid_dir"] = f"{public_root}/rrid/{cfg['name']}"
    resolved["zenodo_zip"] = f"{public_root}/build/{zenodo_record_name}.zip"
    return resolved


def indent_block(text: str, spaces: int = 8) -> str:
    """Indent interpolated blocks so generated Markdown keeps its intended layout."""
    prefix = " " * spaces
    return "\n".join(f"{prefix}{line}" if line else "" for line in text.splitlines())


def copy_branding_assets(workspace: Path, source_rels: list[str], outputs: list[Path]) -> list[str]:
    """Copy configured branding assets into each generated output directory."""
    copied: list[str] = []
    for source_rel in source_rels:
        source = workspace / source_rel
        if not source.exists():
            raise FileNotFoundError(f"Branding asset not found: {source}")
        for output_dir in outputs:
            output_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, output_dir / source.name)
        copied.append(source.name)
    return copied


def build_zenodo_readme(cfg: dict, branding_names: list[str]) -> str:
    """Build the main README for the Zenodo metadata-only bundle."""
    refs = [
        f"- Main website: <{cfg['website']}>",
        f"- Stable public GitHub record: <{cfg['github_url']}>",
        f"- Paper repository: <{cfg['paper_repo_url']}>",
        f"- Release notes: <{cfg['release_notes_url']}>",
    ]
    if branding_names:
        refs.extend([f"- Included branding asset: `{name}`" for name in branding_names])

    provenance = [
        f"- Version: `{cfg['version']}`",
        f"- Release date: `{cfg['release_date']}`",
        f"- Maintainer/publisher: {cfg['author_name']}",
        f"- Affiliation: {cfg['affiliation']}",
        f"- Contact email: <{cfg['contact_email']}>",
        f"- ORCID: `{cfg['orcid']}`",
    ]
    refs_block = indent_block("\n".join(refs))
    provenance_block = indent_block("\n".join(provenance))
    subjects_block = indent_block(bullet_list(cfg["subjects"], tick=True))

    return dedent(
        f"""\
        # {cfg['name']} v{cfg['version']} Zenodo Record

        This package is the citable Zenodo record for **{cfg['name']} v{cfg['version']}**.

        {cfg['name']} is a {cfg['platform_summary']}. It supports reproducible workflows for {cfg['workflow_summary']}, and may integrate sources such as {human_list(cfg['data_sources'])}.

        {cfg['name']} can also operate on custom datasets with or without associated literature papers, including broader general network analysis workflows outside literature-centered use cases.

        {cfg['name']} is distributed through a controlled academic/commercial access model. This Zenodo package is a **public citation record only**. It contains metadata, provenance, access information{", and branding assets" if branding_names else ""}, not the software itself.

        ## Scope and exclusions

        This record includes high-level software description, citation metadata, version details, provenance, and access guidance.

        It does not include source code, executables, model weights, proprietary workflows, internal configuration, private schemas, deployment details, or other controlled delivery artifacts. Feature availability may vary by approved access pathway and license terms.

        ## Public references

{refs_block}

        For access, licensing, or onboarding inquiries, use the contact pathways listed at <{cfg['website']}>.

        ## Provenance

{provenance_block}

        ## Subjects and categories

{subjects_block}

        ## Citation guidance

        Use the Zenodo DOI once assigned. Placeholder DOI:

        - DOI: `{cfg['doi_placeholder']}`
        - DOI URL: <https://doi.org/{cfg['doi_placeholder']}>

        Recommended software citation wording:

        > {cfg['author_citation_name']} {cfg['name']} (Version {cfg['version']}) [Software]. Zenodo. https://doi.org/{cfg['doi_placeholder']}

        {rrid_citation_guidance(cfg)}

        ## Access and rights

        Access to operational software artifacts is managed separately through the {cfg['name']} licensing and onboarding process.

        This record is descriptive, not distributive. It does not grant source access, redistribution rights, sublicensing rights, commercial use rights, or any implied open-source license.
        """
    )


def build_zenodo_cff(cfg: dict) -> str:
    """Build the CFF citation file for the Zenodo record bundle."""
    keywords = "\n".join(f"  - {item}" for item in cfg["subjects"])
    return dedent(
        f"""\
        cff-version: 1.2.0
        message: "If you use {cfg['name']}, please cite the Zenodo software record."
        title: "{cfg['name']}"
        type: software
        version: "{cfg['version']}"
        doi: "{cfg['doi_placeholder']}"
        date-released: {cfg['release_date']}
        authors:
          - family-names: "{cfg['author_family_name']}"
            given-names: "{cfg['author_given_names']}"
            affiliation: "{cfg['affiliation']}"
            email: "{cfg['contact_email']}"
            orcid: "https://orcid.org/{cfg['orcid']}"
        contact:
          - family-names: "{cfg['author_family_name']}"
            given-names: "{cfg['author_given_names']}"
            affiliation: "{cfg['affiliation']}"
            email: "{cfg['contact_email']}"
            website: "{cfg['website']}"
            orcid: "https://orcid.org/{cfg['orcid']}"
        publisher: "{cfg['author_name']}"
        abstract: >-
          {cfg['name']} is a {cfg['platform_summary']}. It supports
          end-to-end workflows for {cfg['workflow_summary']}
          for reproducible research analytics. It can also be applied to
          custom datasets with or without associated literature papers,
          including broader general network analysis workflows.
        keywords:
        {keywords}
        url: "{cfg['website']}"
        repository-code: "{cfg['github_url']}"
        repository-artifact: "{cfg['github_release_url']}"
        license: "LicenseRef-{cfg['name']}-Controlled-Access"
        """
    )


def build_zenodo_license(cfg: dict) -> str:
    """Build the rights notice that clarifies the Zenodo bundle is metadata-only."""
    return dedent(
        f"""\
        {cfg['name']} is distributed under a controlled academic/commercial licensing model.

        This Zenodo archive contains metadata and documentation only. It does not
        include the {cfg['name']} software source code, executables, model weights,
        proprietary pipelines, or internal implementation materials.

        This archive is descriptive, not distributive. Publication of these metadata
        and documentation files does not constitute distribution of the operational
        software.

        Nothing in this archive should be interpreted as a grant of source access,
        redistribution rights, sublicensing rights, commercial use rights, or any
        implied open-source license.

        Availability and licensing for the software itself are managed separately
        through the official {cfg['name']} access and licensing process at
        {cfg['website']}. The stable public software record is
        {cfg['github_url']}.
        """
    )


def build_zenodo_description(cfg: dict, branding_names: list[str]) -> str:
    """Build the concise software description used in the Zenodo package."""
    metadata_lines = [
        f"Main website: {cfg['website']}",
        f"Stable public GitHub record: {cfg['github_url']}",
        f"Paper repository: {cfg['paper_repo_url']}",
        f"Release notes: {cfg['release_notes_url']}",
    ]
    if branding_names:
        metadata_lines.extend([f"Branding asset: {name}" for name in branding_names])
    metadata_lines.extend(
        [
            f"Version: {cfg['version']}",
            f"Affiliation: {cfg['affiliation']}",
            f"Contact: {cfg['contact_email']}",
            f"ORCID: {cfg['orcid']}",
            f"Subjects and categories: {semicolon_list(cfg['subjects'])}",
        ]
    )
    metadata_block = indent_block("\n".join(metadata_lines))
    return dedent(
        f"""\
        # Software Description

        {cfg['name']} is a {cfg['platform_summary']}. It supports reproducible workflows for {cfg['workflow_summary']}.

        {cfg['name']} can integrate literature data sources such as {human_list(cfg['data_sources'])} and is intended for reproducible bibliometric, scientometric, and research network analytics over scientific literature.

        The platform can also be applied to custom datasets with or without associated literature papers, including broader general network analysis workflows outside literature-centered applications.

        {cfg['name']} is distributed through a controlled academic/commercial access model. This Zenodo record provides public metadata, provenance, citation information{", and branding assets" if branding_names else ""} only; it does not distribute the software itself or other controlled-access materials.

        Public materials are limited to high-level software description, citation metadata, provenance details, and access guidance. Internal implementation details and operational software artifacts remain outside this archive.

{metadata_block}

        For access, licensing, or onboarding inquiries, use the contact pathways provided at {cfg['website']}. This record does not grant source access, redistribution rights, or commercial use rights.
        """
    )


def build_link_to_download(cfg: dict) -> str:
    """Build the short access and download reference file for the Zenodo bundle."""
    return dedent(
        f"""\
        Main website:
        {cfg['website']}

        Stable public GitHub record:
        {cfg['github_url']}

        Official access/download URL:
        {cfg['website']}

        Paper repository:
        {cfg['paper_repo_url']}

        Release notes:
        {cfg['release_notes_url']}

        Contact:
        {cfg['contact_email']}

        Access to {cfg['name']} may require registration, review, or license approval.
        For access, licensing, or onboarding questions, use the inquiry pathways at {cfg['website']}.

        This public record is descriptive only and does not grant access to software artifacts or redistribution rights.
        """
    )


def build_codemeta(cfg: dict, branding_names: list[str]) -> dict:
    """Build CodeMeta JSON for the Zenodo metadata package."""
    person = {
        "@type": "Person",
        "givenName": cfg["author_given_names"],
        "familyName": cfg["author_family_name"],
        "name": cfg["author_name"],
        "affiliation": cfg["affiliation"],
        "email": cfg["contact_email"],
        "@id": f"https://orcid.org/{cfg['orcid']}",
    }
    payload = {
        "@context": "https://doi.org/10.5063/schema/codemeta-2.0",
        "@type": "SoftwareSourceCode",
        "name": cfg["name"],
        "version": cfg["version"],
        "author": [person],
        "maintainer": {**person, "url": cfg["website"]},
        "publisher": {
            "@type": "Person",
            "givenName": cfg["author_given_names"],
            "familyName": cfg["author_family_name"],
            "name": cfg["author_name"],
            "affiliation": cfg["affiliation"],
            "@id": f"https://orcid.org/{cfg['orcid']}",
        },
        "programmingLanguage": "Python",
        "description": f"{cfg['name']} is a bibliometric, scientometric, and network analysis platform for scientific literature and custom datasets, including broader general network analysis workflows.",
        "applicationCategory": "Research analytics software",
        "audience": {
            "@type": "Audience",
            "audienceType": "Researchers and research analytics teams",
        },
        "usageInfo": f"Intended for reproducible bibliometric, scientometric, and research network analytics over scientific literature, as well as custom datasets with or without associated literature papers.",
        "keywords": cfg["subjects"],
        "identifier": f"https://doi.org/{cfg['doi_placeholder']}",
        "doi": cfg["doi_placeholder"],
        "license": "Controlled academic/commercial access model",
        "codeRepository": cfg["github_url"],
        "url": cfg["website"],
        "downloadUrl": cfg["website"],
        "releaseNotes": cfg["release_notes_url"],
        "datePublished": cfg["release_date"],
        "isAccessibleForFree": False,
        "email": cfg["contact_email"],
        "about": cfg["subjects"],
        "relatedLink": [cfg["paper_repo_url"], cfg["release_notes_url"]],
        "conditionsOfAccess": f"Access to operational software artifacts is managed separately through a controlled academic/commercial licensing and onboarding process.",
        "copyrightNotice": "This record is descriptive only and does not grant source access, redistribution rights, sublicensing rights, or commercial use rights.",
    }
    if branding_names:
        payload["thumbnailUrl"] = branding_names[0]
    return payload


def build_rrid_submission(cfg: dict, branding_names: list[str]) -> str:
    """Build paste-ready SciCrunch / RRID submission text."""
    branding_block = ""
    if branding_names:
        branding_block = "\n" + indent_block("Branding assets:\n" + "\n".join(branding_names)) + "\n"
    return dedent(
        f"""\
        Name:
        {cfg['name']}

        Resource type:
        Software Tool

        Short description:
        {cfg['name']} is a Python-based software platform for bibliometric, scientometric, and network analysis of scientific literature.

        Public availability clarification:
        {cfg['name']} is a controlled-access software resource. Public-facing materials support discovery and citation; access to the software itself is managed separately through an academic/commercial licensing pathway.

        Expanded description:
        {cfg['name']} supports reproducible workflows for literature data ingestion, cleaning, analysis, and visualization across citation, co-authorship, keyword, institutional, and related research networks, and can integrate literature data sources such as {human_list(cfg['data_sources'])}.

        {cfg['name']} can also be applied to custom datasets with or without associated literature papers, including broader general network analysis workflows outside literature-centered use cases.

        Intended use:
        Reproducible bibliometric, scientometric, and research network analytics over scientific literature, as well as custom datasets with or without associated literature papers.

        Public record scope:
        This public record documents the software purpose, citation metadata, provenance, and access pathway for {cfg['name']}. It is descriptive and not a software distribution.

        Public materials:
        High-level software description, citation metadata, version/provenance information, and access guidance.

        Non-public materials:
        Source code, executables, model weights, proprietary workflows, internal configuration, private schemas, deployment details, and controlled delivery artifacts.

        Function:
        Bibliometric analysis; scientometric analysis; network analysis; literature mining; research analytics

        Suggested keywords:
        {semicolon_list(cfg['subjects'])}

        Developer:
        {cfg['author_name']}

        Organization / affiliation:
        {cfg['affiliation']}

        Contact email:
        {cfg['contact_email']}

        ORCID:
        {cfg['orcid']}

        Public project URL:
        {cfg['website']}

        Stable public GitHub record:
        {cfg['github_url']}

        Paper repository:
        {cfg['paper_repo_url']}

        Release notes:
        {cfg['release_notes_url']}
{branding_block}
        Provenance:
        Version {cfg['version']}; release date {cfg['release_date']}; maintainer/publisher {cfg['author_name']}

        Subjects / categories:
        {semicolon_list(cfg['subjects'])}

        License / availability:
        {cfg['name']} is available through a controlled academic/commercial access model and custom academic licensing arrangements. Public metadata and citation materials are available online, but the software itself is distributed separately.

        Availability note:
        Feature availability and delivery artifacts may vary by approved access pathway and license terms.

        Access / licensing contact:
        Use the inquiry and contact pathways at {cfg['website']}.

        Rights statement:
        This public record does not grant source access, redistribution rights, sublicensing rights, commercial use rights, or any implied open-source license.

        Citation policy:
        {rrid_citation_guidance(cfg)}

        {"Assigned RRID" if rrid_assigned(cfg) else "Identifier placeholder"}:
        {cfg['rrid_placeholder']}
        """
    )


def build_rrid_description(cfg: dict, branding_names: list[str]) -> str:
    """Build the public RRID-facing narrative description."""
    extras = [
        f"Main website: {cfg['website']}",
        f"Stable public GitHub record: {cfg['github_url']}",
        f"Paper repository: {cfg['paper_repo_url']}",
        f"Release notes: {cfg['release_notes_url']}",
    ]
    if branding_names:
        extras.extend([f"Branding asset: {name}" for name in branding_names])
    extras_block = indent_block("\n\n".join(extras))
    return dedent(
        f"""\
        # {cfg['name']} RRID Description

        ## Short version

        {cfg['name']} is a Python-based software platform for bibliometric, scientometric, and network analysis of scientific literature. This RRID-facing record supports discovery and citation for a controlled-access software resource; it is not a software distribution.

        ## Long version

        {cfg['name']} is a Python-based software resource for bibliometric, scientometric, and network analysis of scientific literature. It supports reproducible workflows for literature data ingestion, cleaning, analysis, and visualization across citation, co-authorship, keyword, institutional, and related research networks. {cfg['name']} can integrate literature data sources such as {human_list(cfg['data_sources'])} and is intended for reproducible bibliometric, scientometric, and research network analytics at large scale.

        {cfg['name']} can also be applied to custom datasets with or without associated literature papers, including broader general network analysis workflows outside literature-centered use cases.

        {cfg['name']} is made available through a controlled academic/commercial access model or custom academic licensing pathway. This public-facing description supports discovery and citation, while software access is managed separately.

        Scope of public record: this public description documents the existence, purpose, citation metadata, provenance, and access pathway for {cfg['name']}. It is descriptive and not a software distribution.

        Public-facing materials include high-level software description, citation metadata, version/provenance information, and access guidance. Non-public materials include source code, executables, proprietary workflows, internal configuration, deployment details, and other controlled distribution artifacts.

        Availability note: feature availability and delivery artifacts may vary by approved access pathway and license terms.

{extras_block}

        Provenance: version {cfg['version']}; release date {cfg['release_date']}; maintainer/publisher {cfg['author_name']}; {cfg['affiliation']}; ORCID {cfg['orcid']}.

        Contact email: {cfg['contact_email']}.

        Subjects and categories: {semicolon_list(cfg['subjects'])}.

        Access and licensing contact: use the inquiry pathways at {cfg['website']}.

        Rights statement: this public record does not grant source access, redistribution rights, sublicensing rights, commercial use rights, or any implied open-source license.

        Citation policy: {rrid_citation_guidance(cfg)}

        {"Assigned RRID" if rrid_assigned(cfg) else "RRID placeholder"}: `{cfg['rrid_placeholder']}`
        """
    )


def build_rrid_metadata(cfg: dict, branding_names: list[str]) -> dict:
    """Build structured RRID metadata for reuse in forms, websites, or portals."""
    payload = {
        "name": cfg["name"],
        "resourceType": "Software Tool",
        "resourceSubtype": "software resource",
        "shortDescription": f"{cfg['name']} is a Python-based software platform for bibliometric, scientometric, and network analysis of scientific literature.",
        "publicAvailabilityClarification": "This public-facing record supports discovery and citation only. The software itself is managed through a controlled academic/commercial access model and is not represented here as an open-source distribution.",
        "expandedDescription": f"{cfg['name']} provides end-to-end workflows for literature data ingestion, cleaning, analysis, and visualization. It supports citation, co-authorship, keyword, institutional, and related research networks, and is designed for reproducible large-scale research analytics. It can integrate literature data sources such as {human_list(cfg['data_sources'])}. It can also be applied to custom datasets with or without associated literature papers, including broader general network analysis workflows.",
        "intendedUse": "Reproducible bibliometric, scientometric, and research network analytics over scientific literature, as well as custom datasets with or without associated literature papers.",
        "publicRecordScope": f"This public record documents the software purpose, citation metadata, provenance, and access pathway for {cfg['name']}. It is descriptive and not a technical distribution.",
        "publicMaterials": [
            "High-level software description",
            "Citation metadata",
            "Version and provenance information",
            "Access guidance",
        ],
        "nonPublicMaterials": [
            "Source code",
            "Executables",
            "Model weights",
            "Proprietary workflows",
            "Internal configuration",
            "Private schemas",
            "Deployment details",
            "Controlled delivery artifacts",
        ],
        "function": [
            "Bibliometric analysis",
            "Scientometric analysis",
            "Network analysis",
            "Literature mining",
            "Research analytics",
        ],
        "keywords": cfg["subjects"],
        "developer": cfg["author_name"],
        "organization": cfg["affiliation"],
        "url": cfg["website"],
        "repository": cfg["github_url"],
        "paperUrl": cfg["paper_repo_url"],
        "releaseNotesUrl": cfg["release_notes_url"],
        "version": cfg["version"],
        "releaseDate": cfg["release_date"],
        "publisher": cfg["author_name"],
        "contact": cfg["contact_email"],
        "orcid": cfg["orcid"],
        "subjects": cfg["subjects"],
        "availability": "Available through a controlled academic/commercial access model or custom academic license; not represented as an open-source distribution.",
        "availabilityNote": "Feature availability, interfaces, and delivery artifacts may vary by approved access pathway, license terms, and onboarding context.",
        "dataSourceTransparency": f"May integrate literature data sources such as {human_list(cfg['data_sources'])}. This public record does not disclose internal ingestion or processing implementation.",
        "rightsStatement": "Nothing in this public record should be interpreted as a grant of source access, redistribution rights, sublicensing rights, commercial use rights, or any implied open-source license.",
        "citationPolicy": rrid_citation_guidance(cfg),
        "identifier": cfg["rrid_placeholder"],
        "identifierStatus": "assigned" if rrid_assigned(cfg) else "placeholder",
    }
    if branding_names:
        payload["brandingAsset"] = branding_names[0]
        payload["brandingAssets"] = branding_names
    return payload


def build_zip(zip_path: Path, source_dir: Path) -> None:
    """Create the Zenodo upload ZIP from the generated versioned record directory."""
    ensure_parent(zip_path)
    if zip_path.exists():
        zip_path.unlink()
    with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zf:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(source_dir.parent))


def reset_output_dir(path: Path) -> None:
    """Replace an existing generated output directory with a clean empty directory."""
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def validate_non_empty(paths: list[Path]) -> None:
    """Fail fast if any expected generated file is missing or empty."""
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"Expected generated file is missing: {path}")
        if path.is_file() and path.stat().st_size == 0:
            raise ValueError(f"Generated file is empty: {path}")


def validate_json_files(paths: list[Path]) -> None:
    """Confirm that generated JSON files parse successfully."""
    for path in paths:
        json.loads(path.read_text(encoding="utf-8"))


def update_root_readme_badge(workspace: Path, cfg: dict) -> None:
    """Insert or refresh the DOI badge line in the root project README."""
    readme_path = workspace / "README.md"
    if not readme_path.exists():
        return
    placeholder = (
        f"[![DOI](https://img.shields.io/badge/DOI-{cfg['doi_placeholder'].replace('/', '%2F')}-blue)]"
        f"(https://doi.org/{cfg['doi_placeholder']})"
    )
    lines = readme_path.read_text(encoding="utf-8").splitlines()
    if any(line.startswith("[![DOI](") for line in lines):
        lines = [placeholder if line.startswith("[![DOI](") else line for line in lines]
    else:
        insert_at = 1 if lines and lines[0].startswith("# ") else 0
        lines.insert(insert_at + 1, placeholder)
    readme_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def generate(cfg: dict, workspace: Path) -> None:
    """Generate, validate, and package the Zenodo and RRID public-record outputs."""
    zenodo_dir = workspace / cfg["zenodo_dir"]
    rrid_dir = workspace / cfg["rrid_dir"]
    reset_output_dir(zenodo_dir)
    reset_output_dir(rrid_dir)
    branding_sources = cfg.get("branding_assets")
    if branding_sources is None:
        branding_sources = [cfg["branding_asset"]] if cfg.get("branding_asset") else []
    branding_names = copy_branding_assets(workspace, branding_sources, [zenodo_dir, rrid_dir]) if branding_sources else []

    write_text(zenodo_dir / "README.md", build_zenodo_readme(cfg, branding_names))
    write_text(zenodo_dir / "CITATION.cff", build_zenodo_cff(cfg))
    write_text(zenodo_dir / "LICENSE.txt", build_zenodo_license(cfg))
    write_text(zenodo_dir / "software-description.md", build_zenodo_description(cfg, branding_names))
    write_text(zenodo_dir / "link_to_download.txt", build_link_to_download(cfg))
    write_json(zenodo_dir / "codemeta.json", build_codemeta(cfg, branding_names))

    write_text(rrid_dir / "scicrunch-submission.txt", build_rrid_submission(cfg, branding_names))
    write_text(rrid_dir / "rrid-description.md", build_rrid_description(cfg, branding_names))
    write_json(rrid_dir / "rrid-metadata.json", build_rrid_metadata(cfg, branding_names))

    if cfg.get("update_root_readme_doi_badge", True):
        update_root_readme_badge(workspace, cfg)

    zip_path = workspace / cfg["zenodo_zip"]
    build_zip(zip_path, zenodo_dir)
    generated_files = [
        zenodo_dir / "README.md",
        zenodo_dir / "CITATION.cff",
        zenodo_dir / "LICENSE.txt",
        zenodo_dir / "software-description.md",
        zenodo_dir / "link_to_download.txt",
        zenodo_dir / "codemeta.json",
        rrid_dir / "scicrunch-submission.txt",
        rrid_dir / "rrid-description.md",
        rrid_dir / "rrid-metadata.json",
        zip_path,
    ]
    if branding_names:
        generated_files.extend(
            [path for name in branding_names for path in (zenodo_dir / name, rrid_dir / name)]
        )
    validate_non_empty(generated_files)
    validate_json_files(
        [
            zenodo_dir / "codemeta.json",
            rrid_dir / "rrid-metadata.json",
        ]
    )


def main() -> None:
    """Parse CLI arguments, resolve runtime config, and regenerate public records."""
    parser = argparse.ArgumentParser(description="Generate Zenodo and RRID public record bundles.")
    parser.add_argument(
        "--config",
        default="public_records/config/scinetx.json",
        help="Path to the public record config JSON file.",
    )
    parser.add_argument(
        "--version",
        help="Override the release version (for example, 1.0.1).",
    )
    parser.add_argument(
        "--git-tag",
        help="Override the release tag (for example, v1.0.1).",
    )
    parser.add_argument(
        "--release-date",
        help="Override the release date in YYYY-MM-DD format.",
    )
    args = parser.parse_args()

    workspace = Path.cwd()
    config_path = (workspace / args.config).resolve()
    cfg = load_config(config_path)
    validate_config(cfg)
    resolved_cfg = resolve_runtime_config(cfg, workspace, args.version, args.git_tag, args.release_date)
    generate(resolved_cfg, workspace)


def validate_config(cfg: dict) -> None:
    """Validate the minimum config shape up front and raise actionable errors."""
    required_keys = [
        "name",
        "release_date",
        "author_name",
        "author_citation_name",
        "author_given_names",
        "author_family_name",
        "affiliation",
        "contact_email",
        "orcid",
        "website",
        "github_url",
        "paper_repo_url",
        "doi_placeholder",
        "rrid_placeholder",
        "platform_summary",
        "workflow_summary",
        "data_sources",
        "subjects",
        "version",
    ]
    missing = [key for key in required_keys if key not in cfg or cfg[key] in ("", None, [])]
    if missing:
        raise ValueError(f"Missing required config fields: {', '.join(missing)}")
    if not isinstance(cfg["data_sources"], list) or not all(isinstance(item, str) and item for item in cfg["data_sources"]):
        raise ValueError("'data_sources' must be a non-empty list of strings")
    if not isinstance(cfg["subjects"], list) or not all(isinstance(item, str) and item for item in cfg["subjects"]):
        raise ValueError("'subjects' must be a non-empty list of strings")
    if not DATE_RE.fullmatch(cfg["release_date"]):
        raise ValueError("'release_date' must use YYYY-MM-DD format")
    branding_assets = cfg.get("branding_assets")
    branding_asset = cfg.get("branding_asset")
    if branding_assets is not None:
        if not isinstance(branding_assets, list) or not all(isinstance(item, str) and item for item in branding_assets):
            raise ValueError("'branding_assets' must be a list of non-empty strings")
    elif branding_asset is not None and not isinstance(branding_asset, str):
        raise ValueError("'branding_asset' must be a string when provided")
    version_source = cfg.get("version_source", "tag_or_config")
    if version_source not in {"config", "tag_or_config", "git-tag"}:
        raise ValueError("'version_source' must be one of: config, tag_or_config, git-tag")


if __name__ == "__main__":
    main()
