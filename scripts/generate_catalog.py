"""Generate the README agent catalog and catalog/agents.json."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.hw_agents import (  # noqa: E402
    DOMAIN_LABELS,
    DOMAIN_ORDER,
    ROOT as REPO_ROOT,
    Agent,
    load_agents,
)

README_FILES = {
    "en": REPO_ROOT / "README.md",
    "zh": REPO_ROOT / "README.zh-CN.md",
}
CATALOG_PATH = REPO_ROOT / "catalog" / "agents.json"
BEGIN = "<!-- catalog:generated:start -->"
END = "<!-- catalog:generated:end -->"
INDEX_HEADING = "## 🧰 Skill Index\n"


def catalog_payload(agents: list[Agent]) -> dict:
    records = []
    for agent in sorted(agents, key=lambda item: (item.language, item.domain, item.kind, item.id)):
        records.append(
            {
                "id": agent.id,
                "name": agent.name,
                "description": agent.description,
                "summary": agent.summary,
                "domain": agent.domain,
                "kind": agent.kind,
                "tools": agent.tools,
                "language": agent.language,
                "color": agent.meta.get("color"),
                "path": agent.rel,
            }
        )
    return {
        "generated_from": "agent frontmatter",
        "agent_count": len(records),
        "agents": records,
    }


def render_markdown(agents: list[Agent], language: str) -> str:
    chosen = [agent for agent in agents if agent.language == language]
    role_count = sum(1 for agent in chosen if agent.kind == "role")
    review_count = sum(1 for agent in chosen if agent.kind == "review")
    if language == "en":
        intro = (
            f"Generated from agent frontmatter by `scripts/generate_catalog.py`. "
            f"Do not edit this section by hand.\n\n"
            f"{len(chosen)} English agents ({role_count} roles and {review_count} design reviews) "
            f"across {len(DOMAIN_ORDER)} domains. "
            f"The machine-readable catalog is [`catalog/agents.json`](./catalog/agents.json). "
            f"Chinese agents are indexed in [`README.zh-CN.md`](./README.zh-CN.md)."
        )
        agent_col, tools_col, summary_col = "Agent", "Tools", "Summary"
        review_label = "design review"
    else:
        intro = (
            "本段由 `scripts/generate_catalog.py` 根据 frontmatter 生成，请勿手工修改。\n\n"
            f"{len(chosen)} 个中文 agent（{role_count} 个岗位角色、{review_count} 个设计评审），"
            f"覆盖 {len(DOMAIN_ORDER)} 个方向。"
            f"机器可读目录见 [`catalog/agents.json`](./catalog/agents.json)。"
            f"英文索引见 [`README.md`](./README.md)。"
        )
        agent_col, tools_col, summary_col = "Agent", "工具", "摘要"
        review_label = "设计评审"
    sections = [intro, ""]
    for domain in DOMAIN_ORDER:
        group = [agent for agent in chosen if agent.domain == domain]
        roles = sorted((agent for agent in group if agent.kind == "role"), key=lambda item: item.id)
        reviews = sorted((agent for agent in group if agent.kind == "review"), key=lambda item: item.id)
        label = DOMAIN_LABELS[language][domain]
        sections.append(
            f"### {label} (`{domain}`) — {len(roles)} roles, {len(reviews)} {review_label}"
            if language == "en"
            else f"### {label}（`{domain}`）— {len(roles)} 个角色，{len(reviews)} 个{review_label}"
        )
        sections.append("")
        sections.append(f"| {agent_col} | {tools_col} | {summary_col} |")
        sections.append("| --- | --- | --- |")
        for agent in [*roles, *reviews]:
            href = "./" + quote(agent.rel, safe="/")
            tools = ", ".join(f"`{tool}`" for tool in agent.tools)
            summary = agent.summary.replace("|", "\\|")
            kind = "" if agent.kind == "role" else f" ({review_label})"
            sections.append(f"| [{agent.name}{kind}]({href}) | {tools} | {summary} |")
        sections.append("")
    return "\n".join(sections).rstrip() + "\n"


def splice(text: str, generated: str) -> str:
    wrapped = f"{BEGIN}\n{generated.rstrip()}\n{END}"
    if BEGIN in text and END in text:
        start = text.index(BEGIN)
        end = text.index(END, start) + len(END)
        return text[:start] + wrapped + text[end:]
    heading = text.find(INDEX_HEADING)
    if heading < 0:
        raise SystemExit("ERROR: README is missing the skill index heading")
    rest = text[heading + len(INDEX_HEADING) :]
    next_heading = rest.find("\n## ")
    if next_heading < 0:
        raise SystemExit("ERROR: README skill index has no following section")
    return (
        text[: heading + len(INDEX_HEADING)]
        + "\n"
        + wrapped
        + "\n\n"
        + text[heading + len(INDEX_HEADING) + next_heading + 1 :]
    )


def write_outputs(agents: list[Agent]) -> None:
    payload = catalog_payload(agents)
    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CATALOG_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    for language, path in README_FILES.items():
        updated = splice(path.read_text(encoding="utf-8"), render_markdown(agents, language))
        path.write_text(updated, encoding="utf-8")


def check_outputs(agents: list[Agent]) -> list[str]:
    errors = []
    payload = catalog_payload(agents)
    expected_json = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if not CATALOG_PATH.exists():
        errors.append("catalog/agents.json is missing")
    elif CATALOG_PATH.read_text(encoding="utf-8") != expected_json:
        errors.append("catalog/agents.json is out of date; run scripts/generate_catalog.py --write")
    for language, path in README_FILES.items():
        text = path.read_text(encoding="utf-8")
        expected = render_markdown(agents, language).rstrip()
        if BEGIN not in text or END not in text:
            errors.append(f"{path.name} is missing catalog markers")
            continue
        actual = text[text.index(BEGIN) + len(BEGIN) : text.index(END)].strip("\n")
        if actual != expected:
            errors.append(f"{path.name} catalog section is out of date")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="Rewrite the catalog and README sections")
    mode.add_argument("--check", action="store_true", help="Fail if generated files drifted")
    args = parser.parse_args(argv)
    agents = load_agents(REPO_ROOT)
    if args.write:
        write_outputs(agents)
        print(f"Wrote {CATALOG_PATH.relative_to(REPO_ROOT)} and README catalog sections.")
        return 0
    errors = check_outputs(agents)
    if errors:
        print("ERROR:\n" + "\n".join(errors), file=sys.stderr)
        return 1
    print(f"Catalog matches {len(agents)} agents.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
