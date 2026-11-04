#!/usr/bin/env python3
"""Structural lint for quick or full civil claim-basis review reports."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


COMMON_REQUIRED = {
    "summary": r"执行摘要|一句话方向",
    "facts": r"事实模型|已知事实|事实与暂定假设",
    "procedure": r"程序闸门|程序风险",
    "claims": r"候选请求权|诉请与候选请求权|候选路径",
    "defenses": r"抗辩|防御覆盖",
    "evidence": r"待证事实|证据矩阵|材料与证据|立即动作与材料",
    "strategy": r"诉讼策略|行动计划|立即动作",
    "sources": r"法源核验|已核现行法|待核法源",
}

MODE_REQUIRED = {
    "full": {
        "document_control": r"文档控制|报告版本|case_id",
        "normative_part": r"第一部分.{0,10}规范鉴定",
        "case_section": r"(^|\n)#{1,4}\s*(一、)?案情",
        "question_section": r"(^|\n)#{1,4}\s*(二、)?问题",
        "outline_section": r"(^|\n)#{1,4}\s*(三、)?大纲|请求权树",
        "solution_section": r"(^|\n)#{1,4}\s*(四、)?解题",
        "hypothesis": r"假设[:：]|可能依据.+请求",
        "three_layers": r"请求权已产生[\s\S]{0,12000}请求权未消灭[\s\S]{0,12000}请求权可实行",
        "practice_part": r"第二部分.{0,10}律师实务检视",
        "source_register": r"材料账本|材料登记|source_id",
        "elements": r"请求权逐项检视|构成要件|要件",
        "red_team": r"对方最强版本|压力测试|最强攻击",
        "readiness": r"就绪闸门|就绪判断|可提交|暂不建议提交",
    },
    "quick": {
        "normative_summary": r"规范鉴定摘要|请求权已产生",
        "three_layers": r"请求权已产生[\s\S]{0,3000}请求权未消灭[\s\S]{0,3000}请求权可实行",
        "urgent_risk": r"紧急风险|P0|P1",
        "variables": r"改变结论的变量|关键变量",
        "red_team": r"对方最强攻击|最强防御",
        "readiness": r"当前就绪判断|可提交|暂不建议提交",
    },
    "update": {
        "document_control": r"文档控制|报告版本|case_id",
        "new_sources": r"新增材料|本次材料|source_id",
        "fact_changes": r"新增事实|修正事实|被推翻|事实变化",
        "claim_changes": r"受影响.*claim|请求权变化|claim_id",
        "evidence_changes": r"证据变化|证明力变化|issue_id",
        "version_delta": r"版本变化|旧结论.*新结论|变化摘要",
        "actions": r"下一动作|行动账本|action_id",
    },
}

PLACEHOLDERS = [
    r"\[基于目前信息",
    r"\[对象＋材料",
    r"^\s*TODO\s*$",
    r"^\s*TBD\s*$",
]
RISKY_ABSOLUTES = ["保证胜诉", "一定胜诉", "百分之百胜诉", "法院必然支持"]
DIRECT_BASIS_LINE = re.compile(
    r"^\s*(?:[-*]\s*)?直接请求权基础\s*[:：]\s*(.+)$",
    re.I | re.M,
)
LEAKED_INTERNAL_ABBREVIATION = re.compile(
    r"(?<![A-Za-z0-9_-])(?:AG|SUP|ATTR|CALC|PROOF|DEF|PROC)(?![A-Za-z0-9_-])"
)
EXACT_SOURCE = re.compile(
    r"(?:"
    r"《[^》\n]{1,120}》[^。；\n]{0,80}?第[零〇一二三四五六七八九十百千万两0-9.]+条"
    r"(?:第[零〇一二三四五六七八九十百千万两0-9.]+款)?"
    r"(?:第[零〇一二三四五六七八九十百千万两0-9.]+项)?"
    r"|"
    r"《[^》\n]{1,120}》[^。；\n]{0,120}(?:条款|约定)[^。；\n]{0,120}"
    r"(?:source_id\s*)?SRC-[A-Z0-9-]+[^。；\n]{0,80}(?:第\d+页|段落|定位|时间戳)"
    r")",
    re.I,
)
VAGUE_BASIS_PHRASES = (
    "依据合同关系",
    "依据合同规则",
    "建设工程合同规则",
    "依据侵权规则",
    "依据相关法律",
    "依据相关规定",
    "相关司法解释",
    "设计变更规则",
    "公平原则",
)


def basis_solution_blocks(normative: str) -> list[tuple[str, str]]:
    """Return solution blocks headed by a BASIS id, excluding outline rows."""
    heading = re.compile(
        r"^#{2,6}\s+[^\n]*?\b(BASIS-[A-Z0-9-]+)\b[^\n]*$", re.I | re.M
    )
    matches = list(heading.finditer(normative))
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(normative)
        blocks.append((match.group(1).upper(), normative[match.start() : end]))
    return blocks


def audit_direct_basis(text: str, mode: str, failures: list[str]) -> None:
    """Require an exact, role-labelled direct source instead of a vague field label."""
    lines = DIRECT_BASIS_LINE.findall(text)
    if not lines:
        failures.append("missing labelled direct claim basis")
        return

    for value in lines:
        if any(phrase in value for phrase in VAGUE_BASIS_PHRASES):
            failures.append(f"vague wording used as direct claim basis: {value.strip()}")
        if not EXACT_SOURCE.search(value):
            failures.append(
                "direct claim basis lacks exact instrument and article locator: "
                f"{value.strip()}"
            )

    if not re.search(r"该条款能否直接推出本项请求\s*[:：].*(?:能|不能)", text, flags=re.I):
        failures.append("missing direct-claim-effect check result")
    if not re.search(r"请求权基础完整性\s*[:：].*(?:单条规范完整|规范组合完整)", text, flags=re.I):
        failures.append("missing claim-basis completeness result")

    if mode == "full":
        practice_match = re.search(r"第二部分.{0,10}律师实务检视", text, flags=re.I)
        normative = text[: practice_match.start()] if practice_match else text
        question_match = re.search(r"(^|\n)#{1,4}\s*(二、)?问题", normative, flags=re.I | re.M)
        outline_match = re.search(r"(^|\n)#{1,4}\s*(三、)?大纲", normative, flags=re.I | re.M)
        solution_match = re.search(r"(^|\n)#{1,4}\s*(四、)?解题", normative, flags=re.I | re.M)
        question_text = (
            normative[question_match.end() : outline_match.start()]
            if question_match and outline_match
            else ""
        )
        outline_text = (
            normative[outline_match.end() : solution_match.start()]
            if outline_match and solution_match
            else ""
        )
        if not EXACT_SOURCE.search(question_text):
            failures.append("question section lacks an exact instrument and article locator")
        if not EXACT_SOURCE.search(outline_text):
            failures.append("outline lacks an exact instrument and article locator")

        blocks = basis_solution_blocks(normative)
        if not blocks:
            failures.append("no solution block headed by a basis_id")
            return
        for basis_id, block in blocks:
            block_lines = DIRECT_BASIS_LINE.findall(block)
            if not block_lines:
                failures.append(f"{basis_id} lacks a labelled direct claim basis")
                continue
            if not any(EXACT_SOURCE.search(value) for value in block_lines):
                failures.append(f"{basis_id} lacks an exact instrument and article locator")
            else:
                direct_sources = {
                    source.group(0)
                    for value in block_lines
                    for source in EXACT_SOURCE.finditer(value)
                }
                for source in sorted(direct_sources):
                    if source not in question_text:
                        failures.append(f"{basis_id} direct source is missing from question: {source}")
                    if source not in outline_text:
                        failures.append(f"{basis_id} direct source is missing from outline: {source}")
            for required_label in ("法定法律效果", "请求权基础完整性", "该条款能否直接推出本项请求", "现行法核验"):
                if required_label not in block:
                    failures.append(f"{basis_id} lacks required basis-card field: {required_label}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--mode", choices=("quick", "full", "update"), default="full")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    text = args.report.read_text(encoding="utf-8")
    failures: list[str] = []
    warnings: list[str] = []

    required = (
        {**COMMON_REQUIRED, **MODE_REQUIRED[args.mode]}
        if args.mode in {"full", "quick"}
        else MODE_REQUIRED[args.mode]
    )
    for name, pattern in required.items():
        if not re.search(pattern, text, flags=re.I):
            failures.append(f"missing section/concept: {name}")

    for pattern in PLACEHOLDERS:
        if re.search(pattern, text, flags=re.I | re.M):
            failures.append(f"unresolved placeholder: {pattern}")

    for phrase in RISKY_ABSOLUTES:
        if phrase in text:
            failures.append(f"unsupported absolute wording: {phrase}")

    if args.mode in {"full", "quick"}:
        audit_direct_basis(text, args.mode, failures)
        leaked = sorted(set(LEAKED_INTERNAL_ABBREVIATION.findall(text)))
        if leaked:
            failures.append(
                "user-facing report leaks internal abbreviations: " + ", ".join(leaked)
            )

    if args.mode != "update" and (
        not re.search(r"已知事实|无争议事实", text)
        or not re.search(r"待核|未知|假设", text)
    ):
        failures.append("facts are not visibly separated from assumptions/unknowns")

    if args.mode in {"full", "update"}:
        identifiers = ("source_id", "claim_id", "basis_id", "issue_id", "action_id") if args.mode == "full" else ("source_id", "claim_id", "issue_id", "action_id")
        for identifier in identifiers:
            if not re.search(rf"\b{identifier}\b|{identifier}[_-]?\d+", text, flags=re.I):
                failures.append(f"missing stable identifier: {identifier}")
        if not re.search(r"页码|段落|时间戳|材料定位|source_id\s*[＋+]\s*定位", text, flags=re.I):
            warnings.append("no visible source locator convention")

    if args.mode != "update" and not re.search(r"通过|附条件|阻断|不适用", text):
        warnings.append("readiness or conclusion conditions may be under-specified")

    if args.mode == "full":
        order_patterns = [
            r"第一部分.{0,10}规范鉴定",
            r"(^|\n)#{1,4}\s*(一、)?案情",
            r"(^|\n)#{1,4}\s*(二、)?问题",
            r"(^|\n)#{1,4}\s*(三、)?大纲",
            r"(^|\n)#{1,4}\s*(四、)?解题",
            r"第二部分.{0,10}律师实务检视",
        ]
        positions = []
        for pattern in order_patterns:
            match = re.search(pattern, text, flags=re.I | re.M)
            positions.append(match.start() if match else -1)
        if all(pos >= 0 for pos in positions) and positions != sorted(positions):
            failures.append("full report order must be normative analysis first, then practical review")
        if not re.search(r"满足|不满足|待证|无需检视|待核法源", text):
            failures.append("normative analysis lacks element-level status labels")
        if not re.search(r"可行|附条件可行|目前不可行|已排除|待核法源", text):
            failures.append("normative conclusion lacks allowed conclusion status")

        practice_match = re.search(r"第二部分.{0,10}律师实务检视", text, flags=re.I)
        outline_match = re.search(r"(^|\n)#{1,4}\s*(三、)?大纲", text, flags=re.I | re.M)
        solution_match = re.search(r"(^|\n)#{1,4}\s*(四、)?解题", text, flags=re.I | re.M)
        if practice_match:
            normative = text[: practice_match.start()]
            practical = text[practice_match.end() :]
            for prefix in ("CLAIM", "BASIS"):
                id_pattern = rf"(?<![A-Z0-9-]){prefix}-[A-Z0-9-]+(?=$|[^A-Z0-9-])"
                first_ids = set(re.findall(id_pattern, normative, flags=re.I))
                second_ids = set(re.findall(id_pattern, practical, flags=re.I))
                missing_in_practice = sorted(first_ids - second_ids)
                if missing_in_practice:
                    failures.append(f"{prefix.lower()} ids not carried into practical review: {', '.join(missing_in_practice)}")
                new_in_practice = sorted(second_ids - first_ids)
                if new_in_practice:
                    failures.append(f"{prefix.lower()} ids introduced only in practical review: {', '.join(new_in_practice)}")
            if "待证" in normative and not re.search(r"\bISSUE-[A-Z0-9-]+\b|\bissue_id\b", practical, flags=re.I):
                failures.append("normative pending-proof findings are not mapped to practical issue_id")

        if outline_match and solution_match and practice_match and outline_match.start() < solution_match.start():
            outline = text[outline_match.end() : solution_match.start()]
            solution = text[solution_match.end() : practice_match.start()]
            basis_pattern = r"(?<![A-Z0-9-])BASIS-[A-Z0-9-]+(?=$|[^A-Z0-9-])"
            outline_bases = set(re.findall(basis_pattern, outline, flags=re.I))
            solution_bases = set(re.findall(basis_pattern, solution, flags=re.I))
            if outline_bases != solution_bases:
                failures.append("outline and solution basis_id sets are not isomorphic")

    if not re.search(r"期限|触发条件|完成标准", text):
        warnings.append("actions may lack deadline/trigger or completion criteria")

    if failures:
        print("REPORT AUDIT FAILED")
        for item in failures:
            print(f"- {item}")
        for item in warnings:
            print(f"- warning: {item}")
        return 1

    print(f"REPORT AUDIT PASSED ({args.mode})")
    for item in warnings:
        print(f"- warning: {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
