from __future__ import annotations

import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.hw_agents import (  # noqa: E402
    ROLE_DIR_DOMAIN,
    AgentError,
    integrity_errors,
    iter_agent_files,
    load_agents,
)

README_EN = ROOT / "README.md"
README_ZH = ROOT / "README.zh-CN.md"
CN_SKILL_ROOT = ROOT / "hardware-agency-agents-cn"
EN_SKILL_ROOT = ROOT / "hardware-agency-agents-en"


def _is_zh_dir(name: str) -> bool:
    return any("\u4e00" <= char <= "\u9fff" for char in name)


CN_SKILL_DIR_NAMES = {name for name in ROLE_DIR_DOMAIN if _is_zh_dir(name)}
EN_SKILL_DIR_NAMES = {name for name in ROLE_DIR_DOMAIN if name not in CN_SKILL_DIR_NAMES}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def _collect_skills(base: Path, allowed_dirs: set[str]) -> list[Path]:
    if not base.is_dir():
        fail(f"Missing skill tree directory: {base.relative_to(ROOT)}")
    skill_files = sorted(
        path for path in base.glob("*/*.md") if path.parent.name in allowed_dirs
    )
    if not skill_files:
        fail(f"No skill markdown files found under {base.relative_to(ROOT)}")
    return skill_files


def _collect_review_skills() -> list[Path]:
    review_root = ROOT / "hardware-design-review-validation"
    if not review_root.is_dir():
        return []
    return sorted(review_root.glob("*/*.md"))


def validate_readme(readme: Path, skill_files: list[Path]) -> None:
    if not readme.exists():
        fail(f"{readme.name} is missing")

    text = readme.read_text(encoding="utf-8")
    links = re_links(text)
    expected = {path.relative_to(ROOT).as_posix() for path in skill_files}
    found_local_skills = set()

    for link in links:
        relative = unquote(link[2:])
        target = (ROOT / relative).resolve()
        try:
            target.relative_to(ROOT)
        except ValueError:
            fail(f"{readme.name} contains a link outside the repository: {link}")
        if not target.exists():
            fail(f"{readme.name} points to a missing file: {link}")
        path_in_repo = target.relative_to(ROOT).as_posix()
        if path_in_repo in expected:
            found_local_skills.add(path_in_repo)

    missing = sorted(expected - found_local_skills)
    if missing:
        fail(
            f"{readme.name} is missing links for these skill files: "
            + ", ".join(missing)
        )


def re_links(text: str) -> list[str]:
    import re

    return re.findall(r"\]\((\.\/[^)]+\.md)\)", text)


def main() -> None:
    cn_skills = _collect_skills(CN_SKILL_ROOT, CN_SKILL_DIR_NAMES)
    en_skills = _collect_skills(EN_SKILL_ROOT, EN_SKILL_DIR_NAMES)
    review_skills = _collect_review_skills()

    discovered = {path.resolve() for path in iter_agent_files(ROOT)}
    expected = {path.resolve() for path in [*cn_skills, *en_skills, *review_skills]}
    if discovered != expected:
        fail("Agent discovery does not match the English, Chinese, and review trees")

    try:
        agents = load_agents(ROOT)
    except AgentError as exc:
        fail(str(exc))
    problems = integrity_errors(agents)
    if problems:
        fail("Agent frontmatter failed schema validation:\n" + "\n".join(problems))

    validate_readme(README_EN, en_skills + [p for p in review_skills if p.parent.name == "en"])
    validate_readme(README_ZH, cn_skills + [p for p in review_skills if p.parent.name == "cn"])

    print(
        "Validated "
        f"{len(cn_skills)} CN skills, {len(en_skills)} EN skills, "
        f"{len(review_skills)} review skills, and README links successfully."
    )


if __name__ == "__main__":
    main()
