# Workflow State

> 文档语言：所有由 Workflow 生成或更新的文档，无论文档类型、所在目录、文件名或是否存在对应模板，均以中文为主；必要的 English 专有名词、专业技术术语、代码标识符、路径、命令、API/协议名、Skill 名、状态枚举、AC ID 及其他机器可解析固定值保留 English。

## Active Task

- Task path:
- Task:
- Complexity:
- Area:

## Progress

- Current Stage: `Understand` / `Plan` / `Execute` / `Review` / `Verify` / `Feedback` / `Archive`
- Status: `Running` / `Waiting for Human` / `Blocked` / `Completed`
- Last completed stage:
- Last updated:

## Understand Gate

- Status: `Pending` / `Passed` / `Needs More Investigation` / `Blocked`
- Confirmed facts:
- Remaining unknowns:
- Decision:
- Evidence:

## Design Delivery Audit

- Applicable: `Yes` / `No`
- Reconstruction Intent: `Page-level` / `Feature-level` / `Not Reconstruction` / `Unclear`
- Requested Scope:
- Source Eligibility: `Eligible` / `Ineligible` / `Blocked` / `Not Checked`
- Audit Decision: `Triggered` / `Not Triggered` / `Blocked`
- Decision Reason:
- Artifact:
- Audit result: `PASS` / `PARTIAL` / `NOT_RUN` / `BLOCKED` / `Not Applicable`
- Package fingerprint:
- Fingerprint last checked:
- Critical conflicts resolved: `Yes` / `No` / `Not Applicable`

## Plan Gate

- Status: `Not Applicable` / `Pending` / `Confirmed` / `Revision Requested` / `Rejected`
- Decision:
- Decision date:

## Pause

- Pause reason:
- Human decision required:
- Blocking condition:

## Recovery Snapshot

- Current State:
- Blocker:
- Dependency:
- Recovery Condition:
- Next Action:

## Next Action

- Resume instruction:
- Expected next Skill:
- Expected output:
