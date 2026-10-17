# AI Feedback

> 文档语言：所有由 Workflow 生成或更新的文档，无论文档类型、所在目录、文件名或是否存在对应模板，均以中文为主；必要的 English 专有名词、专业技术术语、代码标识符、路径、命令、API/协议名、Skill 名、状态枚举、AC ID 及其他机器可解析固定值保留 English。

## Task Outcome

- Outcome: `PASS` / `PARTIAL` / `BLOCKED`
- Summary:

## Evidence Summary

- What was verified:
- What was not verified:
- Key evidence:

## Problems Observed

-

## Root Cause

- Problem:
- Root cause:
- Evidence:
- Confidence: `High` / `Medium` / `Low`

## Recovery and Decisions

- Recovery:
- Decision that worked:
- Decision that did not work:
- Why:

## Project Knowledge

- Project-specific fact worth preserving:

## Personal Engineering Experience

- Reusable experience:

## Decision Pattern

- When this condition occurs:
- Prefer:
- Avoid:

## Risk Pattern

- Risk pattern:
- Early signal:
- Prevention:

## Skill Improvement Gap

- Related Skill Execution record:
- Execution Result: `PASS` / `PARTIAL` / `NOT_RUN` / `BLOCKED`
- Existing Skill that was insufficient:
- Missing instruction or capability:
- Candidate Skill improvement:

本节不能代替 Skill Execution 状态；必须引用 `task.md` 中的具体执行记录。

## Workflow Gap

- Missing or weak stage / Gate:
- Evidence:
- Proposed Workflow improvement:

## Improvement Candidate

- Candidate change:
- Expected benefit:
- Cost / risk:
- Scope: `Knowledge` / `Project Rule` / `Skill` / `Workflow`

## Improvement Candidates

| ID | Type | Scope | Trigger | Recommendation | Evidence | Review |
| --- | --- | --- | --- | --- | --- | --- |
| FB-YYYYMMDD-01 | `Experience` / `Regression` / `Decision` / `Rule Change` | `Project` / `Cross-project` |  |  |  | `Pending` / `Accepted` / `Rejected` / `Needs More Evidence` |

候选必须引用当次任务的真实 Evidence。原始 feedback 不因候选被接受、拒绝或替代而改写；后续 Review 与发布记录只能追加。

## Feedback Review

只有存在候选时填写本节。`Accepted` 才允许按已配置知识库的目录规则发布；未配置时保留候选并说明缺少发布位置。`Pending`、`Rejected` 和 `Needs More Evidence` 不阻塞任务交付，也不得发布。

| Candidate | Decision | Reason | Destination | Published Experience ID / Page | Reviewer | Date |
| --- | --- | --- | --- | --- | --- | --- |
| FB-YYYYMMDD-01 | `Accepted` / `Rejected` / `Needs More Evidence` / `Pending` |  |  |  |  |  |

`Rule Change` 即使被接受，也只能创建独立改进任务，不得直接修改 Workflow、项目规则或 Skill。

## Human Review

- Reviewer:
- Decision: `Accepted` / `Rejected` / `Needs more evidence`
- Date:
- Notes:

## Historical Evidence Rule

- 历史执行、Review 和 Verification 记录不可覆盖。
- 重试、复核和恢复只能追加新记录，并引用原记录或证据位置。
