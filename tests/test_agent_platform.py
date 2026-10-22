"""Schema, export, catalog, and eval-stub checks."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from scripts.export_agents import export_all
from scripts.generate_catalog import check_outputs
from scripts.hw_agents import integrity_errors, load_agents, schema_errors
from evals.run_evals import load_cases, route, score_checklist

ROOT = Path(__file__).resolve().parents[1]


def test_every_agent_matches_schema_and_pairs() -> None:
    agents = load_agents(ROOT)
    assert len(agents) == 110
    assert integrity_errors(agents) == []
    assert {agent.language for agent in agents} == {"en", "zh"}
    assert sum(agent.kind == "review" for agent in agents) == 16


def test_schema_rejects_unknown_tool_and_missing_domain() -> None:
    meta = dict(load_agents(ROOT)[0].meta)
    meta["tools"] = ["not-a-tool", "dfm", "dfa"]
    assert any("not-a-tool" in error or "must be one of" in error for error in schema_errors(meta))
    del meta["domain"]
    assert any(error.endswith("domain is required") or ".domain is required" in error for error in schema_errors(meta))


def test_export_writes_three_host_formats(tmp_path: Path) -> None:
    counts = export_all(tmp_path, "en")
    assert counts == {"claude-code": 55, "cursor": 55, "codex": 55}
    claude = next((tmp_path / ".claude" / "agents").glob("*.md"))
    text = claude.read_text(encoding="utf-8")
    assert "tools: Read, Grep, Glob" in text
    assert "schematic-capture" not in text.split("---", 2)[1]
    assert "Operating contract:" in text
    cursor = next((tmp_path / ".cursor" / "rules").glob("*.mdc"))
    assert "alwaysApply: false" in cursor.read_text(encoding="utf-8")
    index = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert "agents/" in index
    for line in index.splitlines():
        if "](agents/" not in line:
            continue
        rel = line.split("](", 1)[1].split(")", 1)[0]
        assert (tmp_path / rel).is_file()


def test_catalog_matches_frontmatter() -> None:
    assert check_outputs(load_agents(ROOT)) == []


def test_eval_stub_routes_without_a_model() -> None:
    agents = load_agents(ROOT)
    cases = load_cases(ROOT / "evals" / "cases")
    assert len(cases) >= 5
    for case in cases:
        selected = route(case["task"], agents, case["language"])
        assert selected.name == case["primary_agent"]
        assert selected.domain == case["domain"]
    result = subprocess.run(
        [sys.executable, str(ROOT / "evals" / "run_evals.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "No model was called" in result.stdout


def test_checklist_score_reports_missing_mentions() -> None:
    checklist = [
        {"item": "Name the hot loop", "mentions": ["hot loop"]},
        {"item": "Show the bode evidence", "mentions": ["bode"]},
    ]
    result = score_checklist("The hot loop is small.", checklist)
    assert result["passed"] == 1
    assert result["items"][1]["missing"] == ["bode"]


def test_install_script_exports_to_dest(tmp_path: Path) -> None:
    result = subprocess.run(
        ["bash", str(ROOT / "install.sh"), "all", "--lang", "en", "--dest", str(tmp_path)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert (tmp_path / ".claude" / "agents").is_dir()
    assert (tmp_path / "AGENTS.md").is_file()
    payload = json.loads((ROOT / "catalog" / "agents.json").read_text(encoding="utf-8"))
    assert payload["agent_count"] == 110
