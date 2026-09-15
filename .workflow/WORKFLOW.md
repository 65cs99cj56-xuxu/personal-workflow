# Personal AI Software R&D Workflow v0.1

> 适用对象：个人进行前端、后端或前后端联动开发的软件研发人员。
>
> 目标：让 AI 的开发过程可理解、可验证、可恢复、可复盘。v0.1 采用 Markdown 文档驱动，不引入自动编排、多 Agent 或自动修改规则。

## 1. 核心模型

Workflow 负责决定阶段、输入输出、Gate、回退和人工决策；Skill 负责在某个阶段完成具体工作；Artifact 负责把上下文从一个阶段传递到下一个阶段。

```text
任务分流
  -> Understand
  -> Understand Gate
  -> Plan
  -> Execute
  -> Review
  -> Verify
  -> 最终完成门
  -> Feedback
  -> Archive / Improve
```

小任务可以缩短路径，但不能省略 Verify、最终完成门和 Feedback。

## 1.1 自动编排协议

全局安装 `personal-ai-workflow` Skill 后，用户只需描述任务，Agent 按以下顺序自动执行。项目根目录的 `AGENTS.md` 仅用于补充项目特殊规则，不是本 Workflow 的必要入口：

1. 读取 `.workflow/current-task.md`。存在未完成任务时恢复该任务；不存在时按 `task.md` 模板创建新任务。
2. 在 `task.md` 中判断复杂度、记录事实和验收标准。
3. 进入当前阶段前，读取本文件对应的 Skill，并严格按 Skill 的输出要求执行。
4. 阶段完成后更新任务文档、验证状态和 `.workflow/current-task.md`，再根据复杂度路由到下一阶段。
5. 遇到人工 Gate、关键未知项、方案取舍或阻塞时，保存状态并暂停，不自行替用户做产品或风险决策。
6. 用户说“继续当前任务”或提供 Gate 决策后，从状态文件记录的阶段恢复，不重新开始已经完成的阶段。

Skill 不可用时必须明确记录为 `BLOCKED` 或 `NOT_RUN`，不能假装已经执行，也不能静默替换成未确认的能力。

## 2. 任务分流

开始时先判断任务规模和风险，不以代码行数作为唯一标准。

### Small

适用于局部、低风险、边界明确的改动，例如文案、样式、小范围逻辑修复。

```text
Understand -> Execute -> Verify -> 最终完成门 -> Feedback
```

### Medium

适用于单模块功能、接口变更、跨文件修复或需要明确实现顺序的任务。

```text
Understand -> Understand Gate -> Plan -> Execute -> Review -> Verify -> 最终完成门 -> Feedback
```

### Large / High Risk

适用于跨前后端契约、数据模型、权限、支付、核心链路、生产风险或需求不清晰的任务。

```text
Understand -> 人工确认 -> Plan -> 人工确认 -> Execute
  -> Independent Review -> Verify -> 最终完成门 -> Feedback -> Archive / Improve
```

满足以下任一条件时，至少按 Medium 处理：

- 同时影响前端和后端，或需要修改 API、字段、错误码、权限。
- 涉及数据库迁移、缓存、异步任务、外部服务或部署配置。
- 需要浏览器、真实数据库、Docker、网络请求或多服务联调才能证明正确。
- 失败后可能造成数据损坏、兼容性问题或难以回滚。
- AI 无法从现有代码和任务描述中确定验收标准。

## 3. 阶段与产物

### Understand：建立事实，而不是猜测方案

主 Skill：`sk-codebase-explore`。

按需补充调查 Skill，例如前端架构回溯、后端架构/领域知识、API 或测试相关 Skill。Understand 的结果写入 `task.md`，至少包括：目标、当前行为、相关代码、数据流、约束、未知项、影响范围、风险和验收标准。

必须区分：

- 已从代码、配置、测试或运行结果确认的事实。
- 根据事实作出的推断。
- 尚未确认的未知项。

禁止在关键未知项未被标记的情况下直接进入实现。

### Understand Gate：确认是否理解到可以动手

进入 Plan 或 Execute 前检查：

- 是否找到真正的入口、调用链和状态/数据流。
- 是否识别前后端、数据库、配置和外部依赖的影响。
- 是否写出可验证的验收标准。
- 是否列出关键未知项及其解决方式。
- 是否知道如何证明改动没有破坏原有行为。

未通过时，回到 Understand；如果需求本身不明确，先向用户确认，不用猜测补齐产品决策。

### Plan：把理解转成可执行上下文

前端主 Skill：`kit-fe-write-plan`。

后端主 Skill：`sy-spec:go-plan`。

前后端联动时分别产出前端和后端计划，使用同一份任务上下文对齐 API、数据结构、状态、错误处理和验收标准。计划写入 `plan.md`，至少说明选定方案、理由、替代方案、取舍、影响范围、实现顺序、验证策略、风险和不在范围内的内容。

Large / High Risk 任务在执行前必须人工确认计划；Medium 任务在计划存在明显取舍或契约变化时也应确认。

### Execute：按计划实现并保持状态同步

执行过程中：

- 按计划中的实现顺序推进，发现方案不成立时暂停并更新计划。
- 任何 API、字段、状态、错误处理或范围变化，都同步更新任务和计划。
- 先完成最小可验证闭环，再扩展非核心优化。
- 不把编译、静态检查或源码级测试单独当作完成证明。
- 不在没有证据时声称某项验证已通过。

### Review：独立检查设计和实现质量

通用 Review：`code-skill:kit-code-review`。

Go 后端 Review：`sy-spec:go-code-review`。

前端 Review：`deer-workflow:deer-code-review`。

Review 关注：需求覆盖、边界条件、兼容性、错误处理、数据一致性、安全性、可维护性、前后端契约和测试缺口。Review 不是 Verify 的替代品；代码看起来合理，不代表运行行为已经被证明。

### Verify：用真实证据证明验收标准

前端专项 Verify：`kit-fe-verify`；需要运行时、浏览器或调试时使用 `build-web-apps:frontend-testing-debugging`。

后端专项 Verify：`kit-backend-feature-verify`。

通用最终完成门：`superpowers:verification-before-completion`。

验证优先覆盖真实边界：实际构建、相关测试、真实数据库或 Docker、浏览器交互、Network 请求、接口响应、迁移结果和核心用户链路。每项验证必须记录实际命令/方法、结果、证据和状态。

状态只能使用：

- `PASS`：已执行且证据支持通过。
- `PARTIAL`：只验证了部分范围，仍有明确未覆盖项。
- `NOT_RUN`：尚未执行，不能声称通过。
- `BLOCKED`：因环境、依赖或权限无法执行，并记录阻塞原因。

只有所有与验收标准相关的必要项为 `PASS`，或者用户明确接受剩余风险，才可通过最终完成门。

### Feedback：Workflow 内置必经阶段

Feedback 不是可选的总结，也不由某一个 Skill 代替。每个任务在 Verify 和最终完成门之后都必须产出 `feedback.md`，即使任务失败、部分完成或被阻塞也一样。

AI 需要基于任务证据分析：任务结果、问题、根因、恢复过程、有效决策、可复用经验、风险模式、Skill Gap、Workflow Gap 和改进候选。Feedback 必须区分事实与推断，不能把一次偶然现象直接升级为正式规则。

Feedback 的结论先进入候选状态，由人审核后再沉淀到个人知识库、项目规则或 Skill。AI 不得自动修改正式 Workflow。

### Archive / Improve：完成后的可恢复沉淀

任务完成后，将任务、计划、验证和反馈文件一起归档到 `.workflow/archive/`，建议目录名为 `YYYY-MM-DD-任务名/`。归档内容应能回答：改了什么、为什么这样改、如何证明、还剩什么风险、下次遇到类似问题应复用什么经验。

只有经过人工审核的改进候选，才可以更新 Workflow、项目规则或 Skill。小任务可以只保留精简归档，但不能省略 Feedback 的结论。

## 4. 统一产物约定

每个任务使用一个独立目录，例如：

```text
.workflow/tasks/2026-09-15-user-login/
├── task.md
├── plan.md
├── verification.md
└── feedback.md
```

自动编排模式下，Agent 负责创建任务目录并维护 `.workflow/current-task.md`；手工模式仍可以复制 `.workflow/templates/` 下的模板。任务文件是当前工作上下文，归档后整体移动到 `.workflow/archive/`。

`.workflow/current-task.md` 只保存当前活动任务的路径、阶段、状态、暂停原因和下一步，不承载完整任务内容。默认只允许一个活动任务；需要并行任务时，应先人工扩展状态管理方案。

## 5. 回退矩阵

| 发现的问题 | 回退阶段 | 必须补充 |
| --- | --- | --- |
| 不知道入口、调用链或真实影响范围 | Understand | 新事实、相关文件、未知项 |
| 验收标准或需求含义不清 | Understand / 人工确认 | 用户决策或明确的验收条件 |
| 方案无法覆盖约束或契约不一致 | Plan | 新方案、取舍、影响范围 |
| 实现过程中发现范围或前置条件变化 | Plan | 更新计划并标明偏差原因 |
| Review 发现缺陷 | Execute | 修复内容和新增验证项 |
| Verify 失败 | Execute 或 Understand | 失败证据、根因、修复/阻塞说明 |
| Feedback 发现流程本身有缺口 | Archive / Improve | 改进候选，等待人工审核 |

## 6. 前后端协作约定

跨端任务必须把以下内容写入任务或计划，不以口头约定为准：

- 请求方法、路径、参数、响应结构和可空性。
- 错误码、错误展示、重试和幂等行为。
- 分页、排序、过滤、权限和状态转换。
- 数据库字段、迁移兼容性和默认值。
- 前端 loading、empty、error、partial success 等状态。
- 联调方式和 Network / 接口证据。

前端和后端可以并行实现，但必须先完成契约对齐；任何一方发现契约变化，都要回到 Plan 更新上下文。

## 7. 自动暂停与恢复

### 必须暂停的情况

- `Large / High Risk` 任务完成 Understand 后，等待人工确认事实和范围。
- 计划涉及 API、数据库、权限、兼容性或明显取舍，等待人工确认。
- 验收标准无法从需求和代码中确定，需要用户补充产品决策。
- Verify 处于 `BLOCKED`，继续执行需要环境、权限或外部依赖变化。
- AI 发现超出原定范围，或准备改变已确认的方案。

暂停前必须：

- 更新当前任务的 `Status`、`Current Stage`、`Human Decision Required` 和 `Next Action`。
- 更新 `.workflow/current-task.md`。
- 明确告诉用户已完成什么、需要决策什么、恢复后将做什么。

### 恢复规则

收到“继续当前任务”、明确的人工决策或阻塞条件已解除时：

- 读取 `.workflow/current-task.md` 和当前任务目录中的全部产物。
- 只从记录的阶段继续；如果上下文与代码不一致，先回退到 Understand。
- 继续前重新检查对应 Gate，不重复无关阶段。

### 一句话入口示例

```text
实现用户登录功能，遵循项目 Workflow。
```

这句话的前提是 Codex 已安装 `personal-ai-workflow` Skill。项目不需要预先安装 `.workflow/` 或 `AGENTS.md`；首次执行时由 Skill 按需创建和初始化任务状态。用户不需要再次指定 Skill；Skill 路由由编排协议执行。

## 8. v0.1 的边界

本版本的自动化通过项目级 Agent 指令和状态文档实现，不包含独立后台进程或外部调度服务。明确不包含：自动捕获会话、自动分类知识、自动召回历史经验、多 Agent 编排、自动修改 Workflow、自动提交代码。

它解决两件事：用一套轻量的阶段和文档留下上下文、验证证据和反馈；通过状态文件实现阶段路由、暂停和恢复。
