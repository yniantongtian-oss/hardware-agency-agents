"""Load hardware-agent prompts and validate their frontmatter schema."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "agent.schema.json"

ROLE_ROOTS = ("hardware-agency-agents-en", "hardware-agency-agents-cn")
REVIEW_ROOT = "hardware-design-review-validation"

ROLE_DIR_DOMAIN = {
    "PCB and Board-Level Implementation": "pcb-board",
    "PCB 与板级实现方向": "pcb-board",
    "Reliability EMC and Safety": "reliability-emc-safety",
    "可靠性 EMC 安规方向": "reliability-emc-safety",
    "Embedded Hardware": "embedded",
    "嵌入式硬件方向": "embedded",
    "Digital Analog and Mixed-Signal": "mixed-signal",
    "数字-模拟-混合信号方向": "mixed-signal",
    "Testing and Validation": "test-validation",
    "测试与验证方向": "test-validation",
    "Power and Power Electronics": "power",
    "电源与功率电子方向": "power",
    "Chip Platforms and Low-Level Board Co-Design": "chip-platform",
    "芯片平台与底层板级协同方向": "chip-platform",
    "Communication and Interfaces": "communications",
    "通信与接口方向": "communications",
}

REVIEW_DOMAIN_BY_ID = {
    "pcb-board-design-review": "pcb-board",
    "reliability-emc-safety-design-review": "reliability-emc-safety",
    "embedded-hardware-design-review": "embedded",
    "mixed-signal-design-review": "mixed-signal",
    "test-validation-review": "test-validation",
    "power-design-review": "power",
    "chip-platform-design-review": "chip-platform",
    "communications-design-review": "communications",
}

DOMAIN_LABELS = {
    "en": {
        "pcb-board": "PCB and Board-Level Implementation",
        "reliability-emc-safety": "Reliability, EMC, and Safety",
        "embedded": "Embedded Hardware",
        "mixed-signal": "Digital, Analog, and Mixed-Signal",
        "test-validation": "Testing and Validation",
        "power": "Power and Power Electronics",
        "chip-platform": "Chip Platforms and Board Co-Design",
        "communications": "Communication and Interfaces",
    },
    "zh": {
        "pcb-board": "PCB 与板级实现方向",
        "reliability-emc-safety": "可靠性、EMC 与安规",
        "embedded": "嵌入式硬件方向",
        "mixed-signal": "数字、模拟与混合信号方向",
        "test-validation": "测试与验证方向",
        "power": "电源与功率电子方向",
        "chip-platform": "芯片平台与底层板级协同方向",
        "communications": "通信与接口方向",
    },
}

DOMAIN_ORDER = list(DOMAIN_LABELS["en"])
FIELD_ORDER = ("id", "name", "description", "summary", "domain", "kind", "tools", "color")
_STRING_KEYS = {"id", "name", "description", "summary", "domain", "kind", "color"}


class AgentError(ValueError):
    """One agent file or catalog record failed validation."""


@dataclass(frozen=True)
class Agent:
    path: Path
    rel: str
    meta: dict
    body: str

    @property
    def id(self) -> str:
        return self.meta["id"]

    @property
    def name(self) -> str:
        return self.meta["name"]

    @property
    def description(self) -> str:
        return self.meta["description"]

    @property
    def summary(self) -> str:
        return self.meta["summary"]

    @property
    def domain(self) -> str:
        return self.meta["domain"]

    @property
    def kind(self) -> str:
        return self.meta["kind"]

    @property
    def tools(self) -> list[str]:
        return list(self.meta["tools"])

    @property
    def language(self) -> str:
        return language_of(self.rel)


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def language_of(rel: str) -> str:
    parts = Path(rel).parts
    if parts[0] == "hardware-agency-agents-en":
        return "en"
    if parts[0] == "hardware-agency-agents-cn":
        return "zh"
    if parts[0] == REVIEW_ROOT and len(parts) > 1 and parts[1] == "en":
        return "en"
    if parts[0] == REVIEW_ROOT and len(parts) > 1 and parts[1] == "cn":
        return "zh"
    raise AgentError(f"{rel} is not in an English or Chinese agent tree")


def expected_kind(rel: str) -> str:
    return "review" if rel.startswith(f"{REVIEW_ROOT}/") else "role"


def expected_domain(rel: str, agent_id: str) -> str:
    path = Path(rel)
    if expected_kind(rel) == "role":
        domain = ROLE_DIR_DOMAIN.get(path.parent.name)
        if domain is None:
            raise AgentError(f"{rel} is in an unknown role directory")
        return domain
    base = agent_id[:-3] if agent_id.endswith("-zh") else agent_id
    try:
        return REVIEW_DOMAIN_BY_ID[base]
    except KeyError as exc:
        raise AgentError(f"{rel} has review id {agent_id!r} with no domain mapping") from exc


def iter_agent_files(root: Path = ROOT) -> list[Path]:
    files: list[Path] = []
    for folder in ROLE_ROOTS:
        base = root / folder
        files.extend(sorted(base.glob("*/*.md")))
    review = root / REVIEW_ROOT
    files.extend(sorted(review.glob("*/*.md")))
    return files


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise AgentError("missing YAML frontmatter")
    end = text.find("\n---\n", 3)
    if end < 0:
        raise AgentError("malformed YAML frontmatter")
    raw = text[4:end]
    body = text[end + 5 :]
    meta: dict = {}
    for line_no, line in enumerate(raw.splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise AgentError(f"invalid frontmatter line {line_no}: {line}")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key in meta:
            raise AgentError(f"duplicate frontmatter key: {key}")
        if value.startswith("[") and value.endswith("]"):
            meta[key] = _parse_flow_list(value, line_no)
        elif len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            meta[key] = _unquote(value)
        else:
            meta[key] = value
    return meta, body


def dump_frontmatter(meta: dict, body: str) -> str:
    lines = ["---"]
    for key in FIELD_ORDER:
        if key not in meta:
            continue
        value = meta[key]
        if key == "tools":
            lines.append("tools: [" + ", ".join(value) + "]")
        elif key in _STRING_KEYS:
            lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
        else:
            raise AgentError(f"do not know how to write frontmatter key {key}")
    lines.append("---")
    body = body.lstrip("\n")
    if not body.endswith("\n"):
        body += "\n"
    return "\n".join(lines) + "\n\n" + body


def schema_errors(instance: object, schema: dict | None = None, path: str = "$") -> list[str]:
    schema = load_schema() if schema is None else schema
    errors: list[str] = []
    declared = schema.get("type")
    if declared == "object":
        if not isinstance(instance, dict):
            return [f"{path} must be an object"]
        allowed = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{path}.{key} is required")
        if schema.get("additionalProperties") is False:
            for key in instance:
                if key not in allowed:
                    errors.append(f"{path}.{key} is not allowed")
        for key, value in instance.items():
            if key in allowed:
                errors.extend(schema_errors(value, allowed[key], f"{path}.{key}"))
        return errors
    if declared == "string":
        if not isinstance(instance, str):
            return [f"{path} must be a string"]
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{path} is shorter than {schema['minLength']}")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errors.append(f"{path} is longer than {schema['maxLength']}")
        if "pattern" in schema and re.fullmatch(schema["pattern"], instance) is None:
            errors.append(f"{path} does not match {schema['pattern']}")
        if "enum" in schema and instance not in schema["enum"]:
            errors.append(f"{path} must be one of {', '.join(schema['enum'])}")
        return errors
    if declared == "array":
        if not isinstance(instance, list):
            return [f"{path} must be an array"]
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"{path} needs at least {schema['minItems']} items")
        if "maxItems" in schema and len(instance) > schema["maxItems"]:
            errors.append(f"{path} has more than {schema['maxItems']} items")
        if schema.get("uniqueItems") and len(instance) != len(set(map(_hashable, instance))):
            errors.append(f"{path} contains duplicate items")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(instance):
                errors.extend(schema_errors(item, item_schema, f"{path}[{index}]"))
        return errors
    return [f"{path} uses an unsupported schema keyword"]


def load_agent(path: Path, root: Path = ROOT) -> Agent:
    text = path.read_text(encoding="utf-8")
    try:
        meta, body = parse_frontmatter(text)
    except AgentError as exc:
        raise AgentError(f"{path.relative_to(root).as_posix()}: {exc}") from exc
    return Agent(path=path, rel=path.relative_to(root).as_posix(), meta=meta, body=body)


def load_agents(root: Path = ROOT) -> list[Agent]:
    return [load_agent(path, root) for path in iter_agent_files(root)]


def integrity_errors(agents: list[Agent]) -> list[str]:
    schema = load_schema()
    errors: list[str] = []
    by_id: dict[str, Agent] = {}
    names: dict[tuple[str, str], dict[str, str]] = {}
    for agent in agents:
        for problem in schema_errors(agent.meta, schema):
            errors.append(f"{agent.rel}: {problem}")
        if "id" not in agent.meta or "domain" not in agent.meta or "kind" not in agent.meta:
            continue
        kind = expected_kind(agent.rel)
        if agent.kind != kind:
            errors.append(f"{agent.rel}: kind is {agent.kind}, expected {kind}")
        try:
            domain = expected_domain(agent.rel, agent.id)
        except AgentError as exc:
            errors.append(str(exc))
        else:
            if agent.domain != domain:
                errors.append(f"{agent.rel}: domain is {agent.domain}, expected {domain}")
        if agent.id in by_id:
            errors.append(f"duplicate id {agent.id} in {by_id[agent.id].rel} and {agent.rel}")
        else:
            by_id[agent.id] = agent
        bucket = names.setdefault((agent.language, agent.kind), {})
        if agent.name in bucket:
            errors.append(
                f"duplicate name {agent.name!r} in {bucket[agent.name]} and {agent.rel}"
            )
        else:
            bucket[agent.name] = agent.rel

    english = {agent.id: agent for agent in agents if agent.language == "en" and "id" in agent.meta}
    for agent in agents:
        if agent.language != "zh" or "id" not in agent.meta:
            continue
        if not agent.id.endswith("-zh"):
            errors.append(f"{agent.rel}: Chinese id {agent.id} must end with -zh")
            continue
        base = english.get(agent.id[:-3])
        if base is None:
            errors.append(f"{agent.rel}: no English agent with id {agent.id[:-3]}")
            continue
        if base.domain != agent.domain or base.kind != agent.kind or base.tools != agent.tools:
            errors.append(
                f"{agent.rel}: domain, kind, or tools differ from {base.rel}"
            )
    for agent_id, agent in english.items():
        if agent_id.endswith("-zh"):
            errors.append(f"{agent.rel}: English id must not end with -zh")
        partner = agent_id + "-zh"
        if partner not in by_id:
            errors.append(f"{agent.rel}: missing Chinese pair {partner}")
    return errors


def _parse_flow_list(value: str, line_no: int) -> list[str]:
    inner = value[1:-1].strip()
    if not inner:
        return []
    items: list[str] = []
    for part in inner.split(","):
        item = part.strip()
        if not item:
            raise AgentError(f"empty list item on line {line_no}")
        if len(item) >= 2 and item[0] == item[-1] and item[0] in {'"', "'"}:
            item = _unquote(item)
        items.append(item)
    return items


def _unquote(value: str) -> str:
    quote = value[0]
    inner = value[1:-1]
    if quote == "'":
        return inner.replace("''", "'")
    return json.loads(value)


def _hashable(value: object) -> object:
    if isinstance(value, list):
        return tuple(value)
    if isinstance(value, dict):
        return tuple(sorted(value.items()))
    return value
