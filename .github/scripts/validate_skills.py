from __future__ import annotations

from pathlib import Path
import re
import sys
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
README_EN = ROOT / "README.md"
README_ZH = ROOT / "README.zh-CN.md"

CN_SKILL_ROOT = ROOT / "hardware-agency-agents-cn"
EN_SKILL_ROOT = ROOT / "hardware-agency-agents-en"
REVIEW_ROOT = ROOT / "hardware-design-review-validation"

CN_SKILL_DIR_NAMES = {
    "PCB 与板级实现方向",
    "可靠性 EMC 安规方向",
    "嵌入式硬件方向",
    "数字 : 模拟 : 混合信号方向",
    "测试与验证方向",
    "电源与功率电子方向",
    "芯片平台与底层板级协同方向",
    "通信与接口方向",
}

EN_SKILL_DIR_NAMES = {
    "PCB and Board-Level Implementation",
    "Reliability EMC and Safety",
    "Embedded Hardware",
    "Digital Analog and Mixed-Signal",
    "Testing and Validation",
    "Power and Power Electronics",
    "Chip Platforms and Low-Level Board Co-Design",
    "Communication and Interfaces",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def parse_frontmatter(text: str, path: Path) -> dict[str, str]:
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)} is missing YAML frontmatter")

    parts = text.split("---\n", 2)
    if len(parts) < 3:
        fail(f"{path.relative_to(ROOT)} has malformed frontmatter")

    raw = parts[1]
    data: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            fail(f"{path.relative_to(ROOT)} has invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def _collect_skills(base: Path, allowed_dirs: set[str]) -> list[Path]:
    if not base.is_dir():
        fail(f"Missing skill tree directory: {base.relative_to(ROOT)}")
    skill_files = sorted(
        path
        for path in base.glob("*/*.md")
        if path.parent.name in allowed_dirs
    )
    if not skill_files:
        fail(f"No skill markdown files found under {base.relative_to(ROOT)}")
    return skill_files


def _collect_review_skills() -> list[Path]:
    if not REVIEW_ROOT.is_dir():
        return []
    return sorted(REVIEW_ROOT.glob("*/*.md"))


def validate_skill_files(skill_files: list[Path], *, unique_names: bool) -> None:
    seen_names: dict[str, Path] = {}
    for path in skill_files:
        text = path.read_text(encoding="utf-8")
        meta = parse_frontmatter(text, path)
        for field in ("name", "description"):
            if not meta.get(field):
                fail(f"{path.relative_to(ROOT)} is missing required field: {field}")
        if not unique_names:
            continue
        name = meta["name"]
        if name in seen_names:
            other = seen_names[name].relative_to(ROOT)
            fail(
                f"Duplicate skill name '{name}' found in "
                f"{other} and {path.relative_to(ROOT)}"
            )
        seen_names[name] = path


def validate_readme(readme: Path, skill_files: list[Path]) -> None:
    if not readme.exists():
        fail(f"{readme.name} is missing")

    text = readme.read_text(encoding="utf-8")
    links = re.findall(r"\]\((\.\/[^)]+\.md)\)", text)
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


def main() -> None:
    cn_skills = _collect_skills(CN_SKILL_ROOT, CN_SKILL_DIR_NAMES)
    en_skills = _collect_skills(EN_SKILL_ROOT, EN_SKILL_DIR_NAMES)
    review_skills = _collect_review_skills()

    validate_skill_files(cn_skills, unique_names=True)
    validate_skill_files(en_skills, unique_names=True)
    if review_skills:
        # CN/EN review names intentionally differ by language; uniqueness within tree.
        validate_skill_files(review_skills, unique_names=True)

    validate_readme(README_EN, en_skills + [p for p in review_skills if p.parent.name == "en"])
    validate_readme(README_ZH, cn_skills + [p for p in review_skills if p.parent.name == "cn"])

    print(
        "Validated "
        f"{len(cn_skills)} CN skills, {len(en_skills)} EN skills, "
        f"{len(review_skills)} review skills, and README links successfully."
    )


if __name__ == "__main__":
    main()
