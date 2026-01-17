import glob
import os
import re
import sys


def is_remote(target: str) -> bool:
    return target.startswith(("http://", "https://", "mailto:"))


def iter_markdown_files() -> list[str]:
    paths = [
        "README.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "REQUEST_ACCESS.md",
        "SECURITY.md",
        "SUPPORT.md",
        "LICENSE",
        "LICENSE_COMMERCIAL.md",
    ]
    paths.extend(glob.glob("docs/**/*.md", recursive=True))
    return [p for p in paths if os.path.isfile(p)]


LINK_RE = re.compile(r"(?P<prefix>!?)\[(?P<text>[^\]]*)\]\((?P<target>[^)]+)\)")


def main() -> int:
    broken: list[tuple[str, str, str]] = []
    for path in iter_markdown_files():
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        for match in LINK_RE.finditer(content):
            target = match.group("target").strip()
            if not target or target.startswith("#") or is_remote(target):
                continue

            target_no_fragment = target.split("#", 1)[0].split("?", 1)[0].strip()
            if not target_no_fragment:
                continue

            base_dir = os.path.dirname(path)
            resolved = os.path.normpath(os.path.join(base_dir, target_no_fragment))
            if not os.path.exists(resolved):
                broken.append((path, target, resolved))

    if broken:
        for src, target, resolved in broken:
            print(f"{src}: broken link '{target}' -> {resolved}")
        return 1

    print("OK: no broken relative markdown links found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
