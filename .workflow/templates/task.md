# Task Context

> 文档语言：所有由 Workflow 生成或更新的文档，无论文档类型、所在目录、文件名或是否存在对应模板，均以中文为主；必要的 English 专有名词、专业技术术语、代码标识符、路径、命令、API/协议名、Skill 名、状态枚举、AC ID 及其他机器可解析固定值保留 English。

## Metadata

- Task:
- Date:
- Complexity: `Small` / `Medium` / `Large` / `High Risk`
- Area: `Frontend` / `Backend` / `Full-stack`
- Status: `Running` / `Waiting for Human` / `Blocked` / `Completed`
- Current Stage: `Understand` / `Plan` / `Execute` / `Review` / `Verify` / `Feedback` / `Archive`
- Human Decision Required:
- Next Action:
- Last Updated:

## Goal

用一句话描述要解决的问题和期望结果：

## Current State

描述当前已经存在的行为、限制或错误。只写已确认内容。

## 首次初始化记录

- `.workflow/` 创建前是否存在：
- 项目根目录 `.gitignore` 创建前状态：`Exists` / `Created` / `Path Conflict`
- Ignore setup：`Added` / `Already Ignored` / `Not Applicable — Existing .workflow` / `BLOCKED`
- 有效规则、Git 忽略检查或跳过证据：
- 已跟踪文件与恢复动作（不自动取消跟踪）：

## 页面还原请求自动补全

- Raw User Request：保留原始请求。
- Requested Scope：完整页面 / 功能局部 / 非还原 / 待确认。
- Source matches：HTML、独立 CSS、独立 JavaScript 的可读取路径。
- Expansion decision：`Expanded` / `Not Triggered` / `Needs Clarification`
- Decision reason：仅完整页面还原且 HTML、CSS、JavaScript 三类齐全时自动补全；不替代审计的 OR 条件。
- Effective Reconstruction Prompt：引用 Workflow 中的完整提示词并保留用户明确的页面、技术栈及其他约束；不要求用户重复输入。

## Known Facts

-

## Assumptions

-

## Unknowns

- 未知项：
- 解决方式：
- 结果：

## Relevant Code and Configuration

| Area | File / Module | Why it matters |
| --- | --- | --- |
|  |  |  |

## Data Flow / Call Chain

```text
入口 -> 调用方 -> 核心逻辑 -> 数据/API/外部依赖 -> 输出
```

## Cross-layer Contract

- API:
- Request:
- Response:
- Errors:
- State / permissions:
- Database / migration:

## Constraints

-

## Affected Scope

- Must change:
- May change:
- Must not change:

## Risks

- 风险：
- 影响：
- 预防或验证方式：

## Acceptance Criteria

- [ ] AC-01 可验证的验收标准
- [ ] AC-02 可验证的验收标准

每个 ID 必须唯一；后续 `plan.md` 和 `verification.md` 必须引用相同 ID，不得用无 ID 的自由文本替代。

## Initial Evidence

- Command / method:
- Result:
- Evidence location:

## Design Delivery Audit

- Applicable: `Yes` / `No`
- Reconstruction Intent: `Page-level` / `Feature-level` / `Not Reconstruction` / `Unclear`
- Requested Scope:
- Source Eligibility: `Eligible` / `Ineligible` / `Blocked` / `Not Checked`
- Source rule: `HTML && (CSS || JavaScript)`
- Audit Decision: `Triggered` / `Not Triggered` / `Blocked`
- Decision Reason:
- Delivery package root:
- Audit artifact: `design-delivery-audit.md` / `Not Applicable`
- Package fingerprint:
- Audit result: `PASS` / `PARTIAL` / `NOT_RUN` / `BLOCKED` / `Not Applicable`
- Recheck required before Plan / Resume / Execute: `Yes` / `No`

只有“页面级还原 + Source Eligibility 为 Eligible”才触发审计，并最低按 `Medium` 处理。功能级实现、功能级还原和页面级非还原任务都走原 Workflow；范围不清时先询问用户。只有截图或有 HTML 但没有可读取独立 CSS/JavaScript 源文件时不触发，并记录判定证据。

## Skill Execution

每次被要求或选择的 Skill 追加一行；历史记录不可覆盖，重试或复核只能新增行。

| Stage | Skill | Configured Path | Resolved Path | Attempted At | Attempted | Result | Evidence | Usage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  | `Yes` / `No` | `PASS` / `PARTIAL` / `NOT_RUN` / `BLOCKED` |  |  |

`PASS`=已执行并产生有效结果；`PARTIAL`=执行了但结果不完整；`NOT_RUN`=可用但未执行；`BLOCKED`=已尝试但因依赖、路径、权限或工具问题无法完成。`Usage` 只记录人工可验证的引用，不自动判断 Skill 是否被使用。

`NOT_RUN` 的 Attempted 必须为 `No`；其他三种 Result 的 Attempted 必须为 `Yes`。无法解析符号链接目标时，Resolved Path 写 `Unresolved` 并在 Evidence 中说明原因。

## Experience Recall

- Search Status: `PASS` / `PARTIAL` / `NOT_RUN` / `BLOCKED`
- Task profile: 项目、技术栈、改动范围和风险关键词
- Index query: 检索词；无命中也必须保留
- Matches: 页面 / Experience ID，或 `none`
- Candidates read: 最多 3 个页面
- No-match reason:

| Page / Experience ID | Applicability | Decision | Concrete impact | Evidence |
| --- | --- | --- | --- | --- |
|  |  | `Applied` / `Not Applicable` / `Needs Human Review` |  |  |

`Applied` 必须引用至少一个 `Known Facts`、`Constraints`、`Risks`、`plan.md`、`AC-xx` 或 `verification.md` 的具体位置；只阅读页面不能标记为 `Applied`。当前代码和配置事实优先于历史经验。

## Understand Gate

- Status: `Pending` / `Passed` / `Needs More Investigation` / `Blocked`
- Confirmed facts:
- Remaining unknowns:
- Decision:
- Evidence:

触发 `Design Delivery Audit` 时，Gate Evidence 必须引用审计报告中的 Source Coverage、来源锚点、状态转换、项目映射、关键冲突决定和当前 `package_fingerprint`。

只有 `Passed` 才能进入 Plan 或 Execute。

## Recovery Snapshot

- Current State:
- Blocker:
- Dependency:
- Recovery Condition:
- Next Action:
