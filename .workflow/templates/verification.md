# Verification Report

> 文档语言：所有由 Workflow 生成或更新的文档，无论文档类型、所在目录、文件名或是否存在对应模板，均以中文为主；必要的 English 专有名词、专业技术术语、代码标识符、路径、命令、API/协议名、Skill 名、状态枚举、AC ID 及其他机器可解析固定值保留 English。

## Verification Goal

列出本次需要证明的验收标准和关键原有行为。

## Results

| Acceptance Criterion ID | Method / Command | Actual Result | Evidence | Status |
| --- | --- | --- | --- | --- |
| AC-01 |  |  |  | `PASS` / `PARTIAL` / `NOT_RUN` / `BLOCKED` |

验证重试或恢复必须使用相同 AC ID 追加新行；旧行不可覆盖。Completion Decision 以每个 AC 的最新一行为准，同时保留早期非 PASS 记录作为恢复证据。

## Design Delivery Verification Matrix

仅在任务记录为 `Audit Decision: Triggered` 时填写；其他任务沿用普通验证矩阵。每一行必须引用审计报告的 Evidence ID 或规格来源。

| Audit Evidence / Specification | Viewport / Device | State / Interaction | Method | Evidence Artifact | Status |
| --- | --- | --- | --- | --- | --- |
| `DA-xxx` |  |  | 截图 / 录屏 / 自动化 / DOM 测量 / Console / Network / 资源检查 / 真实设备 |  | `PASS` / `PARTIAL` / `NOT_RUN` / `BLOCKED` |

覆盖审计中标记为生产验收要求的视觉、状态、交互、动画、设备适配、素材和降级规则。按页面实际行为覆盖输入方式差异、状态转换与恢复、异常路径、可访问性和 `prefers-reduced-motion` 等适用维度，不为页面中不存在的能力补造验证项。

页面还原任务还需填写以下同路径证据和四类结果；非页面还原任务不创建这些专项验证记录。

### Source-backed Reconstruction Evidence Contract

原型与目标必须按同一 Interaction State Graph 和 Cross-control Dependency Graph 回放相同交互路径，使用一致的视口、输入方式、初始状态与可观察等待条件。引用审计交互 ID 和已确认的生产适配决策。

| AC ID / Interaction ID | Path / Viewport / Input | Prototype Before / Intermediate / After Evidence | Target Before / Intermediate / After Evidence | DOM / Mutation Delta | Computed Style / Bounding Box Delta | Focus / ARIA / Console | Direct / Indirect Effects / Recovery / Repeat | Visual Evidence | Decision / Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  | `PASS` / `PARTIAL` / `NOT_RUN` / `BLOCKED` |

证据必须包含全页面 DOM snapshot、受影响元素的 computed style/bounding box、`document.activeElement`、ARIA、Mutation、Console 错误与截图；不以固定等待时间代替状态确认。

| Evidence Class | Audit / Source Anchors | Prototype / Target Evidence | Uncovered Items | Status |
| --- | --- | --- | --- | --- |
| Structure |  |  |  | `PASS` / `PARTIAL` / `NOT_RUN` / `BLOCKED` |
| Style |  |  |  |  |
| Behavior |  |  |  |  |
| Visual |  |  |  |  |

四类必要证据均 `PASS` 才能判页面还原为 `PASS`。原型无法运行时不得静态推断完整行为；关键行为无法确认为 `BLOCKED`，非关键未覆盖为 `PARTIAL`。截图相似或用户接受风险不把缺失的结构/样式/行为证据变为通过。

## Failure or Blocker Analysis

- Failed or non-PASS item:
- Symptom:
- Root cause:
- Recovery attempted:
- Current state:

`PASS` requires a corresponding Evidence entry. `NOT_RUN`、`PARTIAL` 和 `BLOCKED` 不能自动升级为 `PASS`，必须按 Workflow Recovery Rules 记录下一步。

## Recovery Snapshot

- Current State:
- Blocker:
- Dependency:
- Recovery Condition:
- Next Action:

## Remaining Risk

-

## Completion Decision

- Necessary checks all `PASS`: `Yes` / `No`
- User accepted remaining risk: `Yes` / `No` / `Not applicable`
- Final decision: `Complete` / `Partial` / `Blocked`
