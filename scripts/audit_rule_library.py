#!/usr/bin/env python3
"""Audit the bundled rule library for portability and structural integrity."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REFERENCE_DIR = ROOT / "references"
RULE_DEFINITION = re.compile(r"^###\s+(RB-[A-Z]{3}-\d{3})\b", re.M)
RULE_TOKEN = re.compile(r"\b(RB-[A-Z]{3}-\d{3})\b")
FORBIDDEN = {
    "/Users/": "developer-specific absolute path",
    "原始材料转写": "raw-book conversion dependency",
}
REQUIRED_MODULES = {
    "academic-analysis-format.md",
    "direct-basis-gate.md",
    "claim-universe.md",
    "norm-application.md",
    "rule-library-index.md",
    "transaction-history-and-multiparty.md",
    "domain-contract-quasi.md",
    "domain-property-tort.md",
    "domain-security-creditor.md",
    "domain-special.md",
    "remedy-calculation.md",
    "source-map.md",
}
REQUIRED_PREFIXES = {"ACT", "CON", "CTY", "RET", "PRO", "POS", "TOR", "CRD", "SEC", "PER", "FAM", "INH", "SPC", "REM"}


def main() -> int:
    failures: list[str] = []
    warnings: list[str] = []

    missing_modules = sorted(name for name in REQUIRED_MODULES if not (REFERENCE_DIR / name).is_file())
    for name in missing_modules:
        failures.append(f"missing required rule module: references/{name}")

    public_files = [ROOT / "SKILL.md", *sorted(REFERENCE_DIR.glob("*.md"))]
    contents = {path: path.read_text(encoding="utf-8") for path in public_files if path.is_file()}

    for path, content in contents.items():
        for token, reason in FORBIDDEN.items():
            if token in content:
                failures.append(f"{path.relative_to(ROOT)} contains {reason}: {token}")

    definitions: list[str] = []
    definition_files: dict[str, Path] = {}
    for path, content in contents.items():
        for rule_id in RULE_DEFINITION.findall(content):
            definitions.append(rule_id)
            definition_files.setdefault(rule_id, path)

    duplicates = sorted(rule_id for rule_id, count in Counter(definitions).items() if count > 1)
    for rule_id in duplicates:
        failures.append(f"duplicate rule definition: {rule_id}")

    prefixes = {rule_id.split("-")[1] for rule_id in definitions}
    missing_prefixes = sorted(REQUIRED_PREFIXES - prefixes)
    for prefix in missing_prefixes:
        failures.append(f"missing rule family: RB-{prefix}")

    if len(definitions) < 105:
        failures.append(f"rule library too small for standalone baseline: {len(definitions)} definitions")

    all_tokens: set[str] = set()
    for content in contents.values():
        all_tokens.update(RULE_TOKEN.findall(content))
    undefined = sorted(all_tokens - set(definitions))
    for rule_id in undefined:
        failures.append(f"referenced but undefined rule: {rule_id}")

    for rule_id, path in definition_files.items():
        content = contents[path]
        start = re.search(rf"^###\s+{re.escape(rule_id)}\b", content, flags=re.M)
        if not start:
            continue
        end = re.search(r"^###\s+RB-[A-Z]{3}-\d{3}\b", content[start.end() :], flags=re.M)
        body_end = start.end() + end.start() if end else len(content)
        body = content[start.end() : body_end]
        if len(re.findall(r"^-\s+\*\*", body, flags=re.M)) < 2:
            warnings.append(f"thin rule card: {rule_id} in {path.name}")

    source_map = contents.get(REFERENCE_DIR / "source-map.md", "")
    if "https://flk.npc.gov.cn/" not in source_map or "https://www.court.gov.cn/" not in source_map:
        failures.append("source-map.md lacks primary official source entrypoints")

    if failures:
        print("RULE LIBRARY AUDIT FAILED")
        for item in failures:
            print(f"- {item}")
        for item in warnings:
            print(f"- warning: {item}")
        return 1

    print(f"RULE LIBRARY AUDIT PASSED ({len(definitions)} rule cards, {len(prefixes)} families)")
    for item in warnings:
        print(f"- warning: {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
