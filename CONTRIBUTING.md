# Contributing

感谢你为这个硬件 skill 仓库补充内容。这个仓库的目标不是堆积术语，而是沉淀可复用、边界清晰、适合真实工程协作的角色化 skill。

## 提交前先确认

- 你新增的内容对应一个真实且可独立承担任务的硬件岗位或子角色
- 该 skill 与现有 skill 没有明显重复，只是命名不同
- 文档强调工程约束、工作流程、交付物和适用场景，而不是泛化介绍
- 不包含公司内部规范、客户资料、保密设计、受版权限制的截图或大段复制内容

## Skill 文件要求

每个 skill 当前以独立 Markdown 文件维护，建议放在最合适的方向目录下。

文件开头必须包含 YAML frontmatter，并满足 `schema/agent.schema.json`：

```yaml
---
id: example-engineer
name: 示例工程师
description: 示例领域与任务协同 skill。用于典型任务、典型对象、常见问题、关键约束和交付物输出。
summary: 一句话说明岗位边界。
domain: embedded
kind: role
tools: [schematic-capture, mcu-minimum-system, clock-reset]
color: teal
---
```

要求如下：

- `id`：稳定 slug。中文配对使用对应英文 id 加 `-zh`
- `name`：在同一语言和 kind 内必须唯一，直接使用用户最容易搜索到的岗位名称
- `description`：触发文本，说明何时应选择这个角色
- `summary`：目录里的一行摘要
- `domain`：八个方向之一，且与所在目录一致
- `kind`：岗位为 `role`，设计评审为 `review`
- `tools`：3 到 6 个 schema 中列出的工程工具 id，不是宿主的 Read/Grep 工具
- `color`：可选，但须使用 schema 里已有的颜色

中文 agent 的 `domain`、`kind`、`tools` 必须与英文配对相同。

## Description 写作规范

每个 skill 的 `description` 建议统一采用 Agent 更容易触发的写法：

```text
[角色领域] skill。用于 [任务类型]、[典型对象]、[常见问题]、[关键约束] 和 [交付物]。
```

建议同时满足以下要求：

- 包含明确的领域词、任务词、对象词、问题词和输出词
- 优先写用户会搜索的对象、故障现象、评审动作和输出结果

## 内容要求

- 以“工程判断框架”写作，而不是教科书式知识罗列
- 强调输入条件、边界、失效机制、验证要求和交付结果
- 避免空泛表达，如“需要注意稳定性”“注意 EMI 问题”
- 尽量写成可执行的规则、流程和沟通方式
- 不要使用占位文本、未完成标题或省略号式残缺内容

## 命名与分组

新增 skill 时，请优先复用现有目录体系：

- `PCB 与板级实现方向`
- `可靠性 EMC 安规方向`
- `嵌入式硬件方向`
- `数字-模拟-混合信号方向`
- `测试与验证方向`
- `电源与功率电子方向`
- `芯片平台与底层板级协同方向`
- `通信与接口方向`

如果你认为必须新增一个新方向，请在 PR 描述中说明：

- 为什么现有目录不适合
- 新方向与已有方向的边界差异
- 预期后续还会容纳哪些 skill

## README 更新要求

如果你新增、删除或重命名了 skill，请运行：

```bash
python scripts/generate_catalog.py --write
```

这会更新 `catalog/agents.json` 以及两份 README 里标记之间的索引。手写索引会被下一次生成覆盖。选型建议仍然手工维护。

## Pull Request 建议

一个 PR 最好只做一类事情：

- 新增一个或一组相关 skill
- 修正文案和边界定义
- 调整目录结构
- 修复元数据或链接问题

这样更方便评审和回滚。
