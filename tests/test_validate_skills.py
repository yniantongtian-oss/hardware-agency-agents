"""Regression tests for skill discovery / README link validation."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".github" / "scripts" / "validate_skills.py"


def _load_validator():
    spec = importlib.util.spec_from_file_location("validate_skills", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_validator_script_passes_on_repo() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "Validated" in result.stdout


def test_skill_trees_are_discovered() -> None:
    mod = _load_validator()
    cn = mod._collect_skills(mod.CN_SKILL_ROOT, mod.CN_SKILL_DIR_NAMES)
    en = mod._collect_skills(mod.EN_SKILL_ROOT, mod.EN_SKILL_DIR_NAMES)
    review = mod._collect_review_skills()
    assert len(cn) == 47
    assert len(en) == 47
    assert len(review) == 16
