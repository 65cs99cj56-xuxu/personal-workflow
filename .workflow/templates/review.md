# Review Result

> 文档语言：所有由 Workflow 生成或更新的文档，无论文档类型、所在目录、文件名或是否存在对应模板，均以中文为主；必要的 English 专有名词、专业技术术语、代码标识符、路径、命令、API/协议名、Skill 名、状态枚举、AC ID 及其他机器可解析固定值保留 English。

## Scope Covered

- 计划范围：
- 实际检查文件 / 模块：
- 对应 Acceptance Criteria：`AC-xx`

## Findings

| Finding | Severity | Evidence | Required Fix |
| --- | --- | --- | --- |
|  | `High` / `Medium` / `Low` |  |  |

## Severity

- `High`：阻止进入 Verify，或存在明显正确性、安全性、兼容性风险。
- `Medium`：需要修复或明确风险后才能完成。
- `Low`：不阻止交付，但应记录为后续改进候选。

## Required Fixes

-

## Design Delivery Audit Compliance

仅在任务记录为 `Audit Decision: Triggered` 时填写；其他任务沿用普通 Review，不增加专项检查：

- Audit artifact reviewed:
- Confirmed specifications covered: `Yes` / `No`
- `Reuse / Adapt / Add` mapping followed: `Yes` / `No`
- `Keep / Adapt / Replace / Exclude` decisions followed: `Yes` / `No`
- Static HTML / GSAP / direct DOM / demo data mechanically copied: `Yes` / `No`
- Delivery package changed after audit: `Yes` / `No`
- Required rollback: `Understand` / `Plan` / `Execute` / `None`

## Rollback Stage

- `Execute` / `Plan` / `Understand` / `None`

## Review Status

`PASS` / `CHANGES_REQUIRED` / `BLOCKED`

## Recovery Snapshot

- Current State:
- Blocker:
- Dependency:
- Recovery Condition:
- Next Action:

Review 只判断方案和实现是否合理；运行行为、Acceptance Criteria 和实际 Evidence 必须在 `verification.md` 中单独证明。
