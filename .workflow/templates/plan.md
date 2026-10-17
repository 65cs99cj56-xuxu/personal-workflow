# Implementation Plan

> 文档语言：所有由 Workflow 生成或更新的文档，无论文档类型、所在目录、文件名或是否存在对应模板，均以中文为主；必要的 English 专有名词、专业技术术语、代码标识符、路径、命令、API/协议名、Skill 名、状态枚举、AC ID 及其他机器可解析固定值保留 English。

## Selected Approach

说明准备采用的方案，以及它如何满足任务目标和现有约束。

## Why This Approach

-

## Alternatives Considered

| Alternative | Why not selected |
| --- | --- |
|  |  |

## Trade-offs

-

## Affected Areas

- Frontend:
- Backend:
- API / contract:
- Database / migration:
- Tests / tooling:
- Configuration / deployment:

## Implementation Order

1.
2.
3.

## Design Delivery Audit Handoff

仅在任务记录为 `Audit Decision: Triggered` 时填写；功能级实现、功能级还原及其他 `Not Triggered` 任务不填写，也不受下方 11 个阶段约束：

- Audit artifact:
- Package fingerprint rechecked: `Yes` / `No`
- Critical conflicts resolved: `Yes` / `No`

| Prototype Mechanism / Data | Decision | Production Approach | Related AC |
| --- | --- | --- | --- |
|  | `Keep` / `Adapt` / `Replace` / `Exclude` |  | `AC-xx` |

### Delivery Reconstruction Stages

| Stage | Input | Output | Dependencies | Acceptance Criterion ID | Expected Evidence | Applicable |
| --- | --- | --- | --- | --- | --- | --- |
| 1. 交付包审计与未知项确认 |  |  |  | `AC-xx` |  | `Yes` / `No` |
| 2. Design Token、单位、断点和素材规则 |  |  |  |  |  |  |
| 3. 项目架构及状态模型 |  |  |  |  |  |  |
| 4. 基础页面骨架 |  |  |  |  |  |  |
| 5. 一个代表性样板状态 |  |  |  |  |  |  |
| 6. 公共组件 |  |  |  |  |  |  |
| 7. 其他静态状态 |  |  |  |  |  |  |
| 8. 交互和动画 |  |  |  |  |  |  |
| 9. 真实接口与生产配置 |  |  |  |  |  |  |
| 10. 响应式、真实设备和低版本兼容 |  |  |  |  |  |  |
| 11. 截图、录屏和完整回归 |  |  |  |  |  |  |

不适用阶段必须填写理由。不得静默删除阶段，也不得把原型实现方式直接当成生产方案。

## API / Data / State Changes

- API:
- Data model:
- State transitions:
- Error handling:
- Compatibility:

## Verification Strategy

| Acceptance Criterion ID | Verification method | Expected evidence |
| --- | --- | --- |
| AC-01 |  |  |

## Risks and Rollback

- Risk:
- Detection:
- Rollback or mitigation:

## Out of Scope

-

## Plan Decisions

- Plan Gate Status: `Pending` / `Confirmed` / `Revision Requested` / `Rejected`
- Decision:
- Decided by:
- Date:

计划中的每个验收标准必须使用 `task.md` 已定义的 `AC-xx` ID；未映射到 AC 的计划项不能替代验收标准。
