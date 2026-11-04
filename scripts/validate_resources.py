#!/usr/bin/env python3
"""Check that every local resource named by SKILL.md exists."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    skill = (root / "SKILL.md").read_text(encoding="utf-8")
    raw_paths = re.findall(r"`((?:references|assets|scripts)/[^`]+)`", skill)
    paths = sorted({item.split()[0] for item in raw_paths})
    missing = [item for item in paths if not (root / item).is_file()]
    if missing:
        print("RESOURCE VALIDATION FAILED")
        for item in missing:
            print(f"- missing: {item}")
        return 1
    required_runtime = {
        "references/academic-analysis-format.md",
        "references/direct-basis-gate.md",
        "references/claim-universe.md",
        "references/norm-application.md",
        "references/rule-library-index.md",
        "references/transaction-history-and-multiparty.md",
        "references/domain-contract-quasi.md",
        "references/domain-property-tort.md",
        "references/domain-security-creditor.md",
        "references/domain-special.md",
        "references/remedy-calculation.md",
        "references/source-map.md",
        "scripts/audit_rule_library.py",
    }
    missing_runtime = sorted(item for item in required_runtime if not (root / item).is_file())
    if missing_runtime:
        print("RESOURCE VALIDATION FAILED")
        for item in missing_runtime:
            print(f"- missing standalone runtime resource: {item}")
        return 1
    print(f"RESOURCE VALIDATION PASSED ({len(paths)} referenced files; standalone rule runtime present)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
