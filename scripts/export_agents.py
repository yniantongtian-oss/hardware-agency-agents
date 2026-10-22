"""Export hardware agents to Claude Code, Cursor, and Codex formats."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.hw_agents import ROOT as REPO_ROOT  # noqa: E402
from scripts.hw_agents import Agent, AgentError, load_agents  # noqa: E402

CLAUDE_TOOLS = "Read, Grep, Glob"
CONTRACT_LINES = (
    "Tie every recommendation to a constraint, a physical mechanism, the evidence still missing, and a verification step.",
    "Use datasheets, calculations, layout evidence, and measurements you were actually given. Do not invent part values or test results.",
    "When the task crosses domains, name the adjacent role instead of absorbing its job.",
    "Do not call a design production-ready without a stated check.",
)


def select_agents(language: str) -> list[Agent]:
    agents = load_agents(REPO_ROOT)
    if language == "all":
        return agents
    return [agent for agent in agents if agent.language == language]


def export_all(dest: Path, language: str) -> dict[str, int]:
    agents = select_agents(language)
    counts = {
        "claude-code": export_claude(dest, agents),
        "cursor": export_cursor(dest, agents),
        "codex": export_codex(dest, agents),
    }
    return counts


def export_claude(dest: Path, agents: list[Agent]) -> int:
    folder = dest / ".claude" / "agents"
    folder.mkdir(parents=True, exist_ok=True)
    for agent in agents:
        description = f"[{agent.domain}/{agent.kind}] {agent.description}"
        front = "\n".join(
            [
                "---",
                f"name: {agent.id}",
                f"description: {json.dumps(description, ensure_ascii=False)}",
                f"tools: {CLAUDE_TOOLS}",
                "---",
                "",
            ]
        )
        (folder / f"{agent.id}.md").write_text(
            front + render_prompt(agent), encoding="utf-8"
        )
    return len(agents)


def export_cursor(dest: Path, agents: list[Agent]) -> int:
    folder = dest / ".cursor" / "rules"
    folder.mkdir(parents=True, exist_ok=True)
    for agent in agents:
        description = f"{agent.name}. {agent.summary}"
        front = "\n".join(
            [
                "---",
                f"description: {json.dumps(description, ensure_ascii=False)}",
                "alwaysApply: false",
                "---",
                "",
            ]
        )
        (folder / f"{agent.id}.mdc").write_text(
            front + render_prompt(agent), encoding="utf-8"
        )
    return len(agents)


def export_codex(dest: Path, agents: list[Agent]) -> int:
    agents_root = dest / "agents"
    agents_root.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Hardware Agency Agents",
        "",
        "Use the closest role file under `agents/` before giving hardware advice.",
        "Engineering tools in each file are the methods that role reasons with.",
        "Host tools for reading project files stay separate from those engineering tools.",
        "",
        "## Roles",
        "",
    ]
    ordered = sorted(agents, key=lambda agent: (agent.language, agent.domain, agent.kind, agent.id))
    for agent in ordered:
        role_dir = agents_root / agent.id
        role_dir.mkdir(parents=True, exist_ok=True)
        (role_dir / "AGENTS.md").write_text(render_prompt(agent), encoding="utf-8")
        lines.append(
            f"- [{agent.name}](agents/{agent.id}/AGENTS.md) "
            f"(`{agent.domain}`, `{agent.kind}`, `{agent.language}`): {agent.summary}"
        )
    lines.append("")
    (dest / "AGENTS.md").write_text("\n".join(lines), encoding="utf-8")
    return len(agents)


def render_prompt(agent: Agent) -> str:
    tools = ", ".join(f"`{tool}`" for tool in agent.tools)
    contract = "\n".join(f"- {line}" for line in CONTRACT_LINES)
    body = agent.body if agent.body.startswith("\n") else "\n" + agent.body
    return (
        f"You are {agent.name}, a hardware-engineering agent.\n"
        f"Domain: `{agent.domain}`\n"
        f"Kind: `{agent.kind}`\n"
        f"Engineering tools: {tools}\n"
        "\n"
        "Operating contract:\n"
        f"{contract}\n"
        f"{body}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "format",
        choices=("claude-code", "cursor", "codex", "all"),
        help="Agent host format to write",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=Path("dist"),
        help="Destination directory (default: ./dist)",
    )
    parser.add_argument(
        "--lang",
        choices=("en", "zh", "all"),
        default="all",
        help="Which language pair to export (default: all)",
    )
    args = parser.parse_args(argv)
    dest = args.dest.resolve()
    try:
        agents = select_agents(args.lang)
    except AgentError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    if args.format == "all":
        counts = export_all(dest, args.lang)
    elif args.format == "claude-code":
        counts = {"claude-code": export_claude(dest, agents)}
    elif args.format == "cursor":
        counts = {"cursor": export_cursor(dest, agents)}
    else:
        counts = {"codex": export_codex(dest, agents)}
    summary = ", ".join(f"{name}={count}" for name, count in counts.items())
    print(f"Exported {len(agents)} agents to {dest} ({summary}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
