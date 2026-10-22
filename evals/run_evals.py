"""Stub runner for hardware-agent eval cases.

Loads evals/cases/*.json and the agent catalog. It does not call a model.
It checks that each case names real agents and that a keyword router selects
the expected primary agent. Pass --response to score one case's checklist
against a saved answer.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.hw_agents import Agent, load_agents  # noqa: E402

CASES = Path(__file__).resolve().parent / "cases"
GENERIC = {
    "and",
    "board",
    "design",
    "engineer",
    "focused",
    "from",
    "hardware",
    "level",
    "more",
    "review",
    "system",
    "that",
    "the",
    "this",
    "with",
}


def load_cases(folder: Path = CASES) -> list[dict]:
    cases = []
    for path in sorted(folder.glob("*.json")):
        case = json.loads(path.read_text(encoding="utf-8"))
        case["_path"] = path
        cases.append(case)
    if not cases:
        raise SystemExit(f"ERROR: no eval cases in {folder}")
    return cases


def case_errors(case: dict, agents: list[Agent]) -> list[str]:
    errors = []
    label = case.get("id") or str(case.get("_path"))
    for field in ("id", "language", "task", "domain", "primary_agent", "checklist"):
        if not case.get(field):
            errors.append(f"{label}: missing {field}")
    if errors:
        return errors
    if case["language"] not in {"en", "zh"}:
        errors.append(f"{label}: language must be en or zh")
    checklist = case["checklist"]
    if not isinstance(checklist, list) or len(checklist) < 4:
        errors.append(f"{label}: checklist needs at least 4 items")
        return errors
    for index, item in enumerate(checklist, start=1):
        if not isinstance(item, dict) or not str(item.get("item", "")).strip():
            errors.append(f"{label}: checklist item {index} needs text")
            continue
        mentions = item.get("mentions")
        if not isinstance(mentions, list) or not mentions or not all(isinstance(m, str) and m.strip() for m in mentions):
            errors.append(f"{label}: checklist item {index} needs mentions")
    pool = [agent for agent in agents if agent.language == case["language"]]
    by_name = {agent.name: agent for agent in pool}
    primary = by_name.get(case["primary_agent"])
    if primary is None:
        errors.append(f"{label}: unknown primary agent {case['primary_agent']}")
    elif primary.domain != case["domain"]:
        errors.append(
            f"{label}: {primary.name} is domain {primary.domain}, case expects {case['domain']}"
        )
    for name in case.get("supporting_agents", []):
        if name not in by_name:
            errors.append(f"{label}: unknown supporting agent {name}")
    return errors


def route(task: str, agents: list[Agent], language: str) -> Agent:
    text = task.casefold()
    review_task = "design review" in text or "设计评审" in text
    scored: list[tuple[int, int, str, Agent]] = []
    for agent in agents:
        if agent.language != language:
            continue
        score = 0
        corpus = " ".join([agent.name, agent.summary, agent.description, " ".join(agent.tools)]).casefold()
        name_tokens = {
            token
            for token in re.findall(r"[a-z0-9][a-z0-9/+-]{2,}", agent.name.casefold())
            if token not in GENERIC and token in text
        }
        score += 5 * len(name_tokens)
        for tool in agent.tools:
            phrase = tool.replace("-", " ")
            if phrase in text or tool in text:
                score += 4
        corpus_tokens = {
            token
            for token in re.findall(r"[a-z0-9][a-z0-9/+-]{4,}", corpus)
            if token not in GENERIC and token not in name_tokens and token in text
        }
        score += len(corpus_tokens)
        if review_task and agent.kind == "review":
            score += 8
        elif review_task:
            score -= 2
        elif agent.kind == "review":
            score -= 3
        scored.append((score, sum(len(token) for token in name_tokens), agent.id, agent))
    if not scored:
        raise SystemExit(f"ERROR: no agents for language {language}")
    scored.sort(key=lambda item: (-item[0], -item[1], item[2]))
    return scored[0][3]


def score_checklist(response: str, checklist: list[dict]) -> dict:
    folded = response.casefold()
    items = []
    for entry in checklist:
        mentions = [mention for mention in entry["mentions"]]
        missing = [mention for mention in mentions if mention.casefold() not in folded]
        items.append({"item": entry["item"], "passed": not missing, "missing": missing})
    passed = sum(1 for item in items if item["passed"])
    return {
        "passed": passed,
        "total": len(items),
        "coverage": passed / len(items) if items else 0.0,
        "items": items,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", help="Run a single case id")
    parser.add_argument("--response", type=Path, help="Score this answer against --case")
    args = parser.parse_args(argv)
    agents = load_agents(ROOT)
    cases = load_cases()
    if args.case:
        cases = [case for case in cases if case["id"] == args.case]
        if not cases:
            print(f"ERROR: unknown case {args.case}", file=sys.stderr)
            return 1
    if args.response and not args.case:
        print("ERROR: --response requires --case", file=sys.stderr)
        return 1

    failures = 0
    for case in cases:
        problems = case_errors(case, agents)
        if problems:
            failures += 1
            print("FAIL " + case.get("id", "?"))
            for problem in problems:
                print("  " + problem)
            continue
        selected = route(case["task"], agents, case["language"])
        if selected.name != case["primary_agent"]:
            failures += 1
            print(
                f"FAIL {case['id']}: router selected {selected.name} ({selected.id}), "
                f"expected {case['primary_agent']}"
            )
            continue
        line = f"PASS {case['id']}: {selected.id}"
        if args.response:
            result = score_checklist(args.response.read_text(encoding="utf-8"), case["checklist"])
            line += f" coverage={result['passed']}/{result['total']}"
            if result["coverage"] < 1:
                failures += 1
                print("FAIL " + line)
                for item in result["items"]:
                    if not item["passed"]:
                        print(f"  missing {item['missing']} for: {item['item']}")
                continue
        print(line)
    if failures:
        print(f"{failures} eval case(s) failed.", file=sys.stderr)
        return 1
    print(f"Eval stub passed {len(cases)} case(s). No model was called.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
