# hardware-agency-agents

![License](https://img.shields.io/badge/license-MIT-green)
![Agents](https://img.shields.io/badge/agents-110-blue)
![Domains](https://img.shields.io/badge/domains-8-orange)
![Language](https://img.shields.io/badge/language-bilingual-purple)

Are you already used to AI giving hardware advice with great confidence while clearly not understanding hardware at all?

If you are tired of suggestions like "just make the ground trace wider" or "place the capacitor anywhere first and tune it later", this repository is built for you.

`hardware-agency-agents` is an open-source library of hardware engineering skills organized by real engineering roles. Each skill document focuses on a specific role boundary, technical constraints, workflows, communication style, and expected deliverables, so hardware tasks can be approached with more rigorous engineering judgment instead of generic assistant-style advice.

This repository is inspired by the organizational clarity of strong skill libraries, and it maintains English engineering roles alongside historical translation resources, with a focus on board-level constraints and production-oriented design thinking.

## 📚 Table of Contents

- [Quick Start](#-quick-start)
- [Public Notes](#-public-notes)
- [Overview](#-overview)
- [How To Use](#-how-to-use)
- [Repository Structure](#-repository-structure)
- [Skill Index](#-skill-index)
- [How To Choose A Skill](#-how-to-choose-a-skill)
- [What Makes This Repository Different](#-what-makes-this-repository-different)
- [License](#-license)
- [Contributing](#-contributing)
- [GitHub Checks](#-github-checks)

## ⚡ Quick Start

1. Clone the repository:

   ```bash
   git clone https://github.com/yniantongtian-oss/hardware-agency-agents.git
   cd hardware-agency-agents
   ```

2. Export the agents into the host you actually run. `install.sh` reads this checkout and writes only under `--dest`:

   ```bash
   ./install.sh claude-code --lang en --dest "$HOME"   # $HOME/.claude/agents
   ./install.sh cursor --lang en --dest .              # ./.cursor/rules
   ./install.sh codex --lang en --dest .               # ./AGENTS.md and ./agents/*/AGENTS.md
   ./install.sh all --lang all --dest dist/agents      # every language, all three formats
   ```

   Claude Code receives `name`, `description`, and host tools `Read, Grep, Glob`. Engineering tools from frontmatter stay in the prompt. They are not passed through as host tool names. Cursor rules are agent-requestable (`alwaysApply: false`). Codex gets one index `AGENTS.md` plus a role file per agent.

3. Pick the closest skill for your task from the generated index below.
4. Read that skill as the primary engineering role.
5. Add one or two adjacent skills when the task crosses domains.
6. Use the skill content to frame review comments, design constraints, debug hypotheses, and validation plans.

Suggested starting points:

- Board implementation: `PCB Hardware Engineer`
- STM32 boards: `STM32 Hardware Engineer`
- Power design: `Power Hardware Engineer`
- EMC and corrective action: `EMC Hardware Engineer`
- Validation closure: `Hardware Validation Engineer`
- Hardware design review: choose the matching review skill from `hardware-design-review-validation/en/` before board release, EVT/DVT issue closure, or production introduction

## 📢 Public Notes

- This repository is a collection of hardware skill documents, not an official built-in library for any single agent platform
- The content is intended for role selection, design discussion, review guidance, and engineering analysis, not as an automatic guarantee of project correctness
- Users should still validate all conclusions against datasheets, standards, measurements, and project-specific constraints
- This repository is not officially affiliated with ST, TI, NXP, ADI, Altium, KiCad, or other vendors and platforms mentioned in hardware workflows

## 📦 Overview

- 110 agent prompts: 47 hardware roles and 8 design-review roles, each in English and Chinese
- 8 engineering domains, with `domain`, `kind`, and `tools` in every frontmatter block
- Machine-readable catalog at [`catalog/agents.json`](./catalog/agents.json), regenerated into the index below
- Coverage across PCB implementation, embedded hardware, power, EMC/compliance, validation, SoC/FPGA platforms, and communication interfaces
- Suitable for schematic review, PCB constraint analysis, hardware design review, debug work, validation planning, and production-readiness discussions

## 🧭 How To Use

You can treat each `.md` file in this repository as a reusable specialist role template:

1. When the task boundary is clear, choose the most relevant skill as the primary role.
2. When the problem crosses domains, choose one primary skill and add one or two closely related supporting skills.
3. When the task is in review, validation, debug, or production handoff stages, prefer skills that emphasize constraints, verification, and deliverables instead of pure functional discussion.

Typical examples:

- STM32 control board schematic review: start with `STM32 Hardware Engineer`, optionally add `PCB Hardware Engineer` and `EMC Hardware Engineer`
- Buck converter stability and thermal analysis: start with `Power Hardware Engineer`
- High-speed board layout and impedance constraints: start with `High-Speed PCB Engineer` or `SI/PI Engineer`
- EVT/DVT validation closure: start with `Hardware Validation Engineer` or `EVT/DVT Engineer`
- Hardware design review before board release or production introduction: start with the matching skill in `hardware-design-review-validation/en/`

## 🗂️ Repository Structure

```text
hardware-agency-agents/
├── hardware-agency-agents-en/
│   ├── PCB and Board-Level Implementation/
│   ├── Reliability EMC and Safety/
│   ├── Embedded Hardware/
│   ├── Digital Analog and Mixed-Signal/
│   ├── Testing and Validation/
│   ├── Power and Power Electronics/
│   ├── Chip Platforms and Low-Level Board Co-Design/
│   └── Communication and Interfaces/
├── hardware-agency-agents-cn/   # Historical translation assets
├── hardware-design-review-validation/
│   ├── en/
│   └── cn/
├── schema/agent.schema.json
├── catalog/agents.json
├── evals/
├── scripts/
└── install.sh
```

Notes:

- `README.md` is the default English landing page
- `README.zh-CN.md` is the matching Simplified Chinese page
- `hardware-agency-agents-en` stores the English skill set
- `hardware-agency-agents-cn` stores the Chinese skill set
- `hardware-design-review-validation` stores hardware design review skills in English and Chinese

## 🧰 Skill Index

<!-- catalog:generated:start -->
Generated from agent frontmatter by `scripts/generate_catalog.py`. Do not edit this section by hand.

55 English agents (47 roles and 8 design reviews) across 8 domains. The machine-readable catalog is [`catalog/agents.json`](./catalog/agents.json). Chinese agents are indexed in [`README.zh-CN.md`](./README.zh-CN.md).

### PCB and Board-Level Implementation (`pcb-board`) — 9 roles, 1 design review

| Agent | Tools | Summary |
| --- | --- | --- |
| [DFA Engineer](./hardware-agency-agents-en/PCB%20and%20Board-Level%20Implementation/DFA%20Engineer.md) | `dfa`, `assembly-process`, `footprint-check` | Design for assembly, soldering risk, component spacing, orientation, and reworkability |
| [DFM Engineer](./hardware-agency-agents-en/PCB%20and%20Board-Level%20Implementation/DFM%20Engineer.md) | `dfm`, `fabrication-notes`, `panelization` | Design for manufacturability, process limits, panelization, via process, and fabrication data review |
| [Hardware Process Engineer](./hardware-agency-agents-en/PCB%20and%20Board-Level%20Implementation/Hardware%20Process%20Engineer.md) | `smt-process`, `assembly-process`, `dfm` | SMT/DIP process, manufacturing introduction, and process coordination |
| [High-Speed PCB Engineer](./hardware-agency-agents-en/PCB%20and%20Board-Level%20Implementation/High-Speed%20PCB%20Engineer.md) | `pcb-layout`, `impedance-control`, `length-matching`, `signal-integrity` | High-speed board constraints, differential routing, length matching, impedance, and crosstalk control |
| [PCB Footprint Library Engineer](./hardware-agency-agents-en/PCB%20and%20Board-Level%20Implementation/PCB%20Footprint%20Library%20Engineer.md) | `footprint-library`, `padstack`, `datasheet-review` | Footprint library quality, pad rules, 3D models, and naming standards |
| [PCB Hardware Engineer](./hardware-agency-agents-en/PCB%20and%20Board-Level%20Implementation/PCB%20Hardware%20Engineer.md) | `schematic-capture`, `pcb-layout`, `signal-integrity`, `power-integrity`, `dfm` | End-to-end board implementation from schematic to manufacturable PCB with SI, PI, EMC, DFM, and outputs |
| [PCB Layout Engineer](./hardware-agency-agents-en/PCB%20and%20Board-Level%20Implementation/PCB%20Layout%20Engineer.md) | `pcb-layout`, `stackup`, `impedance-control` | Layout and routing quality, stackup planning, constraints, impedance, vias, and return paths |
| [RF Hardware Engineer](./hardware-agency-agents-en/PCB%20and%20Board-Level%20Implementation/RF%20Hardware%20Engineer.md) | `rf-matching`, `vna`, `spectrum-analyzer` | RF front-end implementation, impedance matching, antenna coordination, and RF debug |
| [SI/PI Engineer](./hardware-agency-agents-en/PCB%20and%20Board-Level%20Implementation/SI-PI%20Engineer.md) | `signal-integrity`, `power-integrity`, `field-solver` | Signal integrity and power integrity modeling, simulation, diagnosis, and correction |
| [PCB and Board-Level Design Review Engineer (design review)](./hardware-design-review-validation/en/PCB%20and%20Board-Level%20Design%20Review%20Engineer.md) | `design-review`, `pcb-layout`, `dfm`, `signal-integrity` | Board implementation review for schematics, PCB layout, stackup, impedance, manufacturing data, and test points |

### Reliability, EMC, and Safety (`reliability-emc-safety`) — 8 roles, 1 design review

| Agent | Tools | Summary |
| --- | --- | --- |
| [Certification Engineer (CE FCC UL and More)](./hardware-agency-agents-en/Reliability%20EMC%20and%20Safety/Certification%20Engineer%20-%20CE%20FCC%20UL%20and%20More.md) | `certification-dossier`, `emc-scan`, `safety-report` | Regulatory certification documents, lab coordination, and corrective support |
| [EMC Hardware Engineer](./hardware-agency-agents-en/Reliability%20EMC%20and%20Safety/EMC%20Hardware%20Engineer.md) | `emc-scan`, `spectrum-analyzer`, `esd-test` | EMC design, diagnosis, and closure from board level to system level |
| [EMI Remediation Engineer](./hardware-agency-agents-en/Reliability%20EMC%20and%20Safety/EMI%20Remediation%20Engineer.md) | `emi-debug`, `spectrum-analyzer`, `near-field-probe` | EMI problem localization, interference source analysis, and corrective actions |
| [Environmental Test Engineer](./hardware-agency-agents-en/Reliability%20EMC%20and%20Safety/Environmental%20Test%20Engineer.md) | `environmental-chamber`, `vibration-test`, `thermal-chamber` | Temperature, vibration, drop, aging, and environmental stress testing |
| [ESD Protection Engineer](./hardware-agency-agents-en/Reliability%20EMC%20and%20Safety/ESD%20Protection%20Engineer.md) | `esd-test`, `tvs-selection`, `interface-protection` | ESD protection schemes, TVS selection, discharge paths, and interface protection |
| [Failure Analysis Engineer](./hardware-agency-agents-en/Reliability%20EMC%20and%20Safety/Failure%20Analysis%20Engineer.md) | `failure-analysis`, `microscope`, `decapsulation` | Failure reproduction, root cause analysis, component failure modes, and stress-related faults |
| [Hardware Reliability Engineer](./hardware-agency-agents-en/Reliability%20EMC%20and%20Safety/Hardware%20Reliability%20Engineer.md) | `derating`, `fmea`, `mtbf` | Derating, lifetime, thermal stress, environmental robustness, and MTBF-related methods |
| [Safety Compliance Engineer](./hardware-agency-agents-en/Reliability%20EMC%20and%20Safety/Safety%20Compliance%20Engineer.md) | `safety-spacing`, `hipot`, `insulation-coordination` | Electrical safety design, insulation boundaries, risk assessment, and certification preparation |
| [Reliability EMC and Safety Design Review Engineer (design review)](./hardware-design-review-validation/en/Reliability%20EMC%20and%20Safety%20Design%20Review%20Engineer.md) | `design-review`, `derating`, `emc-scan`, `safety-spacing` | Risk review for derating, temperature rise, ESD, surge, EMC, safety distances, and certification data |

### Embedded Hardware (`embedded`) — 7 roles, 1 design review

| Agent | Tools | Summary |
| --- | --- | --- |
| [Automation Control Hardware Engineer](./hardware-agency-agents-en/Embedded%20Hardware/Automation%20Control%20Hardware%20Engineer.md) | `io-module`, `industrial-bus`, `relay-drive` | Automation control hardware, IO, relays, industrial buses, drives, and sensing |
| [Control Board Hardware Engineer](./hardware-agency-agents-en/Embedded%20Hardware/Control%20Board%20Hardware%20Engineer.md) | `schematic-capture`, `protection-circuit`, `power-tree` | Controller main boards, functional boards, drive/protection design, and bring-up |
| [Embedded Hardware Engineer](./hardware-agency-agents-en/Embedded%20Hardware/Embedded%20Hardware%20Engineer.md) | `schematic-capture`, `peripheral-interface`, `power-tree` | Board-level embedded hardware with MCU/MPU peripherals, interfaces, power, and joint debug |
| [Embedded Systems Hardware Engineer](./hardware-agency-agents-en/Embedded%20Hardware/Embedded%20Systems%20Hardware%20Engineer.md) | `ddr-bringup`, `flash-boot`, `timing-analysis` | Complex embedded platforms, DDR, Flash, buses, timing, and system architecture |
| [Industrial Control Hardware Engineer](./hardware-agency-agents-en/Embedded%20Hardware/Industrial%20Control%20Hardware%20Engineer.md) | `isolation`, `surge-protection`, `wide-temperature` | Industrial anti-interference, isolation, surge, lightning, and wide-temperature design |
| [MCU Hardware Engineer](./hardware-agency-agents-en/Embedded%20Hardware/MCU%20Hardware%20Engineer.md) | `mcu-minimum-system`, `clock-reset`, `swd-jtag` | MCU minimum system, reset, clocks, download interface, and board debug |
| [Microcontroller Hardware Engineer](./hardware-agency-agents-en/Embedded%20Hardware/Microcontroller%20Hardware%20Engineer.md) | `mcu-minimum-system`, `logic-level`, `protection-circuit` | Single-chip control hardware, buses, logic levels, pull-up/down handling, and protection |
| [Embedded Hardware Design Review Engineer (design review)](./hardware-design-review-validation/en/Embedded%20Hardware%20Design%20Review%20Engineer.md) | `design-review`, `mcu-minimum-system`, `clock-reset`, `boot-config` | Review for MCU/MPU minimum systems, reset and clock circuits, boot configuration, interfaces, and debug access |

### Digital, Analog, and Mixed-Signal (`mixed-signal`) — 7 roles, 1 design review

| Agent | Tools | Summary |
| --- | --- | --- |
| [Analog Hardware Engineer](./hardware-agency-agents-en/Digital%20Analog%20and%20Mixed-Signal/Analog%20Hardware%20Engineer.md) | `analog-front-end`, `filter-design`, `noise-analysis` | Op-amp circuits, filtering, signal conditioning, noise, and stability analysis |
| [Digital Hardware Engineer](./hardware-agency-agents-en/Digital%20Analog%20and%20Mixed-Signal/Digital%20Hardware%20Engineer.md) | `timing-analysis`, `logic-analyzer`, `schematic-capture` | Digital logic, timing constraints, interfaces, board implementation, and debug |
| [High-Speed Digital Circuit Engineer](./hardware-agency-agents-en/Digital%20Analog%20and%20Mixed-Signal/High-Speed%20Digital%20Circuit%20Engineer.md) | `signal-integrity`, `timing-analysis`, `oscilloscope` | High-speed interfaces, timing margin, reference planes, and board-level debug |
| [Low-Power Hardware Engineer](./hardware-agency-agents-en/Digital%20Analog%20and%20Mixed-Signal/Low-Power%20Hardware%20Engineer.md) | `power-budget`, `sleep-current`, `battery-profile` | Battery-powered low-power planning, sleep/wake design, and power budgeting |
| [Mixed-Signal Hardware Engineer](./hardware-agency-agents-en/Digital%20Analog%20and%20Mixed-Signal/Mixed-Signal%20Hardware%20Engineer.md) | `analog-front-end`, `grounding`, `adc-reference` | Mixed-signal partitioning, grounding, sampling synchronization, and interference control |
| [Signal Chain Hardware Engineer](./hardware-agency-agents-en/Digital%20Analog%20and%20Mixed-Signal/Signal%20Chain%20Hardware%20Engineer.md) | `analog-front-end`, `filter-design`, `adc-reference` | Sensor-to-processor signal conditioning, filtering, isolation, and error-chain analysis |
| [STM32 Hardware Engineer](./hardware-agency-agents-en/Digital%20Analog%20and%20Mixed-Signal/STM32%20Hardware%20Engineer.md) | `mcu-minimum-system`, `swd-jtag`, `adc-reference` | STM32 minimum system, Boot, SWD, ADC reference, and peripheral board design |
| [Digital Analog and Mixed-Signal Design Review Engineer (design review)](./hardware-design-review-validation/en/Digital%20Analog%20and%20Mixed-Signal%20Design%20Review%20Engineer.md) | `design-review`, `signal-integrity`, `analog-front-end`, `adc-reference` | Review for high-speed digital, analog chains, ADC/DAC, references, noise, and crosstalk |

### Testing and Validation (`test-validation`) — 6 roles, 1 design review

| Agent | Tools | Summary |
| --- | --- | --- |
| [Automated Test Hardware Engineer](./hardware-agency-agents-en/Testing%20and%20Validation/Automated%20Test%20Hardware%20Engineer.md) | `fixture-design`, `instrument-control`, `boundary-scan` | Test fixtures, interface control, production test links, and automation platforms |
| [Board-Level Debug Engineer](./hardware-agency-agents-en/Testing%20and%20Validation/Board-Level%20Debug%20Engineer.md) | `oscilloscope`, `logic-analyzer`, `power-on-debug` | Power-up, clocks, reset, interfaces, and fault localization |
| [EVT/DVT Engineer](./hardware-agency-agents-en/Testing%20and%20Validation/EVT-DVT%20Engineer.md) | `evt-dvt`, `test-plan`, `issue-tracker` | Engineering sample validation, risk identification, and maturity judgment |
| [Hardware Test Engineer](./hardware-agency-agents-en/Testing%20and%20Validation/Hardware%20Test%20Engineer.md) | `test-plan`, `oscilloscope`, `boundary-test` | Functional, performance, boundary, and stability testing |
| [Hardware Validation Engineer](./hardware-agency-agents-en/Testing%20and%20Validation/Hardware%20Validation%20Engineer.md) | `validation-plan`, `evt-dvt`, `issue-tracker` | Validation planning, defect closure, and EVT/DVT/PVT gate decisions |
| [Lab Test Engineer](./hardware-agency-agents-en/Testing%20and%20Validation/Lab%20Test%20Engineer.md) | `oscilloscope`, `lab-notebook`, `instrument-control` | Lab instruments, execution discipline, data capture, and repeatability |
| [Testing and Validation Review Engineer (design review)](./hardware-design-review-validation/en/Testing%20and%20Validation%20Review%20Engineer.md) | `design-review`, `evt-dvt`, `test-plan`, `validation-plan` | Review for EVT, DVT, PVT, test coverage, sample size, data records, and issue closure |

### Power and Power Electronics (`power`) — 5 roles, 1 design review

| Agent | Tools | Summary |
| --- | --- | --- |
| [BMS Hardware Engineer](./hardware-agency-agents-en/Power%20and%20Power%20Electronics/BMS%20Hardware%20Engineer.md) | `bms-sensing`, `cell-balancing`, `isolation` | Cell sensing, balancing, protection, high-voltage safety, and isolated communication |
| [Energy Storage Hardware Engineer](./hardware-agency-agents-en/Power%20and%20Power%20Electronics/Energy%20Storage%20Hardware%20Engineer.md) | `power-conversion`, `thermal-design`, `protection-circuit` | Energy storage modules, power conversion, protection, and thermal management |
| [Motor Drive Hardware Engineer](./hardware-agency-agents-en/Power%20and%20Power%20Electronics/Motor%20Drive%20Hardware%20Engineer.md) | `inverter-bridge`, `current-sense`, `gate-drive` | Half-bridge/full-bridge topology, current sensing, protection, and motor-drive control boards |
| [Power Electronics Engineer](./hardware-agency-agents-en/Power%20and%20Power%20Electronics/Power%20Electronics%20Engineer.md) | `gate-drive`, `magnetics`, `loss-analysis`, `thermal-design` | Mid/high-power conversion, gate drive, magnetics, thermal design, and loss analysis |
| [Power Hardware Engineer](./hardware-agency-agents-en/Power%20and%20Power%20Electronics/Power%20Hardware%20Engineer.md) | `power-tree`, `loop-compensation`, `electronic-load` | AC/DC, DC/DC, LDO, power trees, compensation, thermal design, and protection strategies |
| [Power and Power Electronics Design Review Engineer (design review)](./hardware-design-review-validation/en/Power%20and%20Power%20Electronics%20Design%20Review%20Engineer.md) | `design-review`, `power-tree`, `loop-compensation`, `thermal-design` | Review for power trees, power stages, loops, ripple, transients, protection, thermal behavior, and EMI |

### Chip Platforms and Board Co-Design (`chip-platform`) — 4 roles, 1 design review

| Agent | Tools | Summary |
| --- | --- | --- |
| [Chip Applications Engineer (Hardware-Focused FAE AE)](./hardware-agency-agents-en/Chip%20Platforms%20and%20Low-Level%20Board%20Co-Design/Chip%20Applications%20Engineer%20-%20Hardware%20Focused%20FAE%20AE.md) | `datasheet-review`, `reference-design`, `schematic-capture` | Application support, reference design adaptation, and customer-facing hardware analysis |
| [CPLD Engineer](./hardware-agency-agents-en/Chip%20Platforms%20and%20Low-Level%20Board%20Co-Design/CPLD%20Engineer.md) | `programmable-logic`, `io-level`, `timing-analysis` | Basic programmable logic, interface conversion, IO levels, timing, and configuration |
| [FPGA Hardware Engineer](./hardware-agency-agents-en/Chip%20Platforms%20and%20Low-Level%20Board%20Co-Design/FPGA%20Hardware%20Engineer.md) | `fpga-config`, `power-tree`, `high-speed-io` | FPGA power rails, clocks, configuration, multi-voltage domains, and high-speed IO |
| [SoC Hardware Platform Engineer](./hardware-agency-agents-en/Chip%20Platforms%20and%20Low-Level%20Board%20Co-Design/SoC%20Hardware%20Platform%20Engineer.md) | `ddr-bringup`, `pmic-sequencing`, `boot-config` | SoC/MPU platforms, DDR, power sequencing, PMIC coordination, and boot configuration |
| [Chip Platform and Board Co-Design Review Engineer (design review)](./hardware-design-review-validation/en/Chip%20Platform%20and%20Board%20Co-Design%20Review%20Engineer.md) | `design-review`, `ddr-bringup`, `pmic-sequencing`, `boot-config` | Review for SoC, FPGA, DDR, PMIC, boot chains, and reference-design adaptation |

### Communication and Interfaces (`communications`) — 1 roles, 1 design review

| Agent | Tools | Summary |
| --- | --- | --- |
| [Communications Hardware Engineer](./hardware-agency-agents-en/Communication%20and%20Interfaces/Communications%20Hardware%20Engineer.md) | `ethernet-phy`, `usb-signal`, `can-rs485`, `transmission-line` | Communication boards, high-speed interfaces, link debug, transmission lines, and EMC-aware design |
| [Communications and Interface Design Review Engineer (design review)](./hardware-design-review-validation/en/Communications%20and%20Interface%20Design%20Review%20Engineer.md) | `design-review`, `ethernet-phy`, `usb-signal`, `can-rs485` | Review for Ethernet, USB, CAN, RS485, LVDS, connectors, cables, and interface protection |
<!-- catalog:generated:end -->

## 🎯 How To Choose A Skill

If your task is mainly about the following areas, start here:

- Schematic-to-board implementation: `PCB Hardware Engineer`, `PCB Layout Engineer`, `High-Speed PCB Engineer`
- Control boards and embedded platforms: `MCU Hardware Engineer`, `STM32 Hardware Engineer`, `Embedded Systems Hardware Engineer`
- Precision analog and signal-chain work: `Analog Hardware Engineer`, `Signal Chain Hardware Engineer`, `Mixed-Signal Hardware Engineer`
- Power, storage, and drives: `Power Hardware Engineer`, `Power Electronics Engineer`, `Motor Drive Hardware Engineer`, `BMS Hardware Engineer`
- Compliance, reliability, and corrective work: `EMC Hardware Engineer`, `Safety Compliance Engineer`, `Hardware Reliability Engineer`, `Certification Engineer (CE FCC UL and More)`
- Debug and validation closure: `Board-Level Debug Engineer`, `Hardware Test Engineer`, `Hardware Validation Engineer`, `EVT/DVT Engineer`
- Board-release, design-review, EVT/DVT issue-closure, and production-introduction reviews: use the matching `Hardware Design Review and Validation` skill

## ✨ What Makes This Repository Different

- It is organized by real hardware roles rather than by abstract knowledge topics
- It emphasizes engineering rules, constraints, verification logic, and deliverables instead of glossary-style descriptions
- It covers a full lifecycle from design and review to debug, validation, and production handoff
- It can be used both as an agent role library and as an internal capability map for hardware teams

## ⚖️ License

This repository is released under the [MIT License](./LICENSE). You may copy, modify, distribute, and use it commercially, as long as the original copyright and license notice are preserved.

## 🤝 Contributing

If you want to add skills, expand domains, refine role boundaries, or improve repository structure, read [CONTRIBUTING.md](./CONTRIBUTING.md) first.

Before submitting changes, keep these standards in mind:

- Skill names should be clear and role boundaries should be explicit
- Frontmatter must include `id`, `name`, `description`, `summary`, `domain`, `kind`, and `tools`, and must satisfy [`schema/agent.schema.json`](./schema/agent.schema.json)
- Regenerate the index with `python scripts/generate_catalog.py --write` after adding or renaming an agent
- Content should emphasize constraints, workflows, deliverables, and application scope
- Do not submit internal company materials, customer-sensitive content, or copyrighted assets you do not own

## ✅ GitHub Checks

GitHub Actions validates this repository on pull requests and manual runs:

- frontmatter against `schema/agent.schema.json`
- unique `id` and `name` values, and English/Chinese pairs that share `domain`, `kind`, and `tools`
- the generated catalog and local skill links in `README.md` and `README.zh-CN.md`
- the eval stub in `evals/` (no model call)

These workflows only check the repository. They do not install agents into a local host directory.
## 🚀 Possible Next Steps

If you continue expanding this repository, these are strong next improvements:

- add cross-skill composition examples such as `STM32 + EMC + Validation`
- score the eval checklist against a real model response, using `evals/run_evals.py --response`
- clarify primary vs secondary roles where skill boundaries overlap
