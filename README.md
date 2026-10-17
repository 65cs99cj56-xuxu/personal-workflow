# Personal Workflow

面向个人前端、后端和全栈开发的 AI 研发工作流。用户描述一次目标，Agent 按阶段加载 Skill、记录事实与证据，在人工 Gate 暂停，并用状态文件恢复任务。

```text
使用 personal-ai-workflow 实现用户登录，复用项目现有鉴权，覆盖错误提示与登录后恢复。
```

这是由 Agent 解释 Markdown 规则的编排方式。运行环境须支持读取/写入项目文件和执行必要工具；跨会话恢复通过用户发送“继续当前任务”启动。

## 核心能力

| 能力 | 行为 | 规则或产物 |
| --- | --- | --- |
| 自动分流 | 按范围与风险选择 Small / Medium / Large / High Risk | [Workflow](.workflow/WORKFLOW.md) |
| 事实调查 | 区分事实、推断与未知项，受控召回已有经验 | [任务模板](.workflow/templates/task.md) |
| 人工 Gate | 未理解清楚不能执行；正式计划须确认 | [计划模板](.workflow/templates/plan.md) |
| 可核验 Skill 执行 | 记录配置路径、真实路径、时间、状态、证据和用途；重试只追加 | [全局入口](SKILL.md) |
| 页面还原审计 | 源码和原型运行行为建立结构、样式、行为、依赖与视觉基线 | [审计 Skill](skills/design-delivery-audit/SKILL.md)、[审计模板](.workflow/templates/design-delivery-audit.md) |
| Review 与 Verify | 独立产出审查结果，再按 AC 验证实际行为 | [Review](.workflow/templates/review.md)、[验证模板](.workflow/templates/verification.md) |
| 暂停与恢复 | 保存阻塞、依赖、恢复条件及下一步 | [状态模板](.workflow/templates/state.md) |
| Feedback | 每个任务生成反馈；候选经审核才进入知识库 | [反馈模板](.workflow/templates/feedback.md) |

## 任务分流与阶段

```text
Small：Understand → Execute → Verify → 最终完成门 → Feedback → Archive
Medium：Understand → Understand Gate → Plan → 人工 Plan Gate
        → Execute → Review → Verify → 最终完成门 → Feedback → Archive
Large / High Risk：Understand → 人工确认 → Plan → 人工确认
                  → Execute → Independent Review → Verify → 最终完成门 → Feedback
```

Small 用于局部低风险改动，可省正式计划与 Review，但不能跳过验证和反馈。单模块功能、跨文件修复、完整页面源码还原至少为 Medium。跨层契约、权限、支付、迁移和生产风险按更高风险处理；完整判断条件见 [Workflow 的任务分流](.workflow/WORKFLOW.md#2-任务分流)。

| 阶段 | 责任 | Gate / 输出 |
| --- | --- | --- |
| Understand | 调查入口、调用链、约束、未知项、风险与验收标准 | `task.md`，适用时 `design-delivery-audit.md` |
| Understand Gate | 确认关键事实与未知项已处理 | 只有 `Passed` 能进入 Plan/Execute |
| Plan | 选定方案、顺序、文件、验证方式和不在范围内的内容 | `plan.md`；正式计划经人工确认后执行 |
| Execute | 依计划实现，范围或契约变化时同步产物 | 代码/配置/文档及证据 |
| Review | 检查需求、边界、兼容、安全和测试缺口 | 独立 `review.md`；不能代替运行验证 |
| Verify | 用实际命令、依赖和用户链路证明 `AC-xx` | `verification.md` |
| 最终完成门 | 执行 `superpowers:verification-before-completion` | 无新证据不能宣称通过 |
| Feedback / Archive | 记录结果、根因、经验候选与恢复过程 | `feedback.md`；归档本次全部适用产物 |

## 安装与首次运行

将本仓库安装为全局 Skill，使 `SKILL.md` 位于 `~/.codex/skills/personal-ai-workflow/` 根部。目标目录不存在时可执行：

```bash
git clone https://github.com/65cs99cj56-xuxu/personal-workflow.git \
  ~/.codex/skills/personal-ai-workflow
```

已有安装目录时先检查现有修改，再按自己的更新方式同步。新开 Codex 对话后可使用 `personal-ai-workflow`。其他 Agent 环境应使用其支持的 Skill 安装位置。

执行前需要安装或提供 [入口中的阶段 Skill](SKILL.md#skill-routing)，包括 `sk-codebase-explore`、前端/后端计划、Review、Verify 与最终完成门 Skill。仓库只内置 `design-delivery-audit`，不包含这些外部 Skill。源码资格检测脚本需要 `python3`；原型运行审计需要可运行交付页面的环境和浏览器工具。

项目无需先写 `AGENTS.md`。第一次使用时，Agent 将分发包的 Workflow/模板复制到项目，创建以下过程目录；已有项目规则优先读取并保留：

```text
.workflow/
├── WORKFLOW.md
├── templates/
├── current-task.md
├── tasks/YYYY-MM-DD-任务名/
└── archive/
```

首次创建 `.workflow/` 时，必须立即检查项目已有的 `.gitignore` **文件**：追加或确认有效的 `.workflow/` 忽略项并避免重复，检查后续否定规则。没有 `.gitignore` 文件则跳过，不新建文件。处理结果记录在任务中；不自动移除已跟踪文件，恢复既有目录不重复初始化。

使用者项目的 `.workflow/` 是本地过程材料；本分发仓库中的 `.workflow/WORKFLOW.md` 和模板则是安装资源，需要保留在包中。

## 给智能体的指令

建议提供目标、范围、不可改变项、依赖环境和可观察的验收结果。无需重复指定每个 Stage 或手工选择已有路由的 Skill。

### 首次发起

```text
使用 personal-ai-workflow 实现以下目标：<目标>。
范围：<页面/模块/接口>。
约束：<复用能力、兼容范围、不可改变项>。
验收：<用户操作与预期结果>。
先读取当前项目状态和 Workflow，按复杂度自动编排并保存阶段产物。
```

### 可选的项目 AGENTS.md

```text
软件研发任务先读取 .workflow/current-task.md 和 .workflow/WORKFLOW.md。
恢复未完成任务，自动判断复杂度并加载各阶段 Skill。
Understand Gate 只有 Passed 才能继续；正式计划须等待人工确认。
首次生成 .workflow 时，已有 .gitignore 文件就有效忽略 .workflow/；没有则跳过。
保存 Skill 的配置/真实路径、执行时间、证据和用途，历史记录只追加。
Verify 使用 AC ID、方法、实际结果、证据和状态，不用 build 代替全部验证。
适用时生成 review.md，每个任务必须生成 feedback.md 后才结束。
```

### 计划确认与恢复

```text
确认当前 plan.md 的方案、实施顺序、范围和验证策略，按计划执行。
```

```text
继续当前任务。先读取 current-task.md、task.md、state.md 和既有产物，
从记录阶段恢复；保留历史证据，发现事实变化时回到 Understand。
```

```text
阻塞已解除：<环境/依赖的具体变化>。复核恢复条件后继续当前任务。
```

### 完成验收与剩余风险

```text
对照 task.md 的每个 AC 核验实际结果、证据和最新状态，
运行最终完成门并生成 feedback.md，明确未覆盖项后再报告结果。
```

```text
我接受 <具体 AC/未覆盖范围> 的剩余风险，允许按已记录范围交付。
```

接受风险不把 `PARTIAL` / `BLOCKED` 改为 `PASS`；页面还原仍须四类必要证据全部通过才能判定还原 `PASS`。

## 页面还原：自动补齐请求与源码审计

用户提供可读取 HTML、独立 CSS、独立 JavaScript 并表达“还原页面”意图时，Workflow 自动补齐以下 Effective Reconstruction Prompt，同时保留原始请求、对应文件和用户明确约束。用户无需再复制发送这段内容。

```text
根据附件中的 HTML、CSS 和 JavaScript 还原完整页面。

以交付包源码和原型实际运行行为作为事实基线，不以截图作为唯一依据。
先执行 design-delivery-audit，提取 DOM 结构、computed style、响应式规则、
交互状态、动态 DOM mutation 及跨控件联动关系。

必须实际运行原型，覆盖 hover、click、focus、blur、输入、键盘及适用的
异步状态。每条交互记录触发控件、前置状态、共享状态变化、所有直接和
间接受影响区域、交互前后 DOM/style/focus/ARIA 差异。

实现后对原型和目标页面回放相同交互路径。Structure、Style、Behavior、
Visual 四类证据全部通过后，才能报告页面还原完成。
```

自动补全使用 `页面级还原 && HTML && CSS && JavaScript`。审计触发使用 `页面级还原 && HTML && (CSS || JavaScript)`。HTML + CSS 或 HTML + JavaScript 仍可能触发审计；检测器只证明源码资格，页面范围由 Workflow 判断。

“根据附件还原整个首页，重点检查筛选交互”是完整页面还原；“只修改筛选组件”属于功能级任务。只有截图、HTML-only、仅内联样式/脚本、非还原任务均不自动触发完整源码审计。范围不清先澄清，不因为文件齐全扩大用户任务。

审计分别建立 Structure Contract、Style Contract、Behavior Contract、Cross-control Dependency Graph 与 Visual Baseline。存在 JavaScript、交互伪类或动态 DOM 时，实际运行原型、形成 Interaction State Graph，并追踪触发控件之外的直接/间接影响。

每条交互保存前、中、后全页面 DOM、Mutation、受影响元素 computed style/bounding box、焦点/ARIA、Console 和截图，按可观察条件等待异步/动画。目标实现按相同路径回放；只有 Structure、Style、Behavior、Visual 四类必要证据均通过才可判还原 `PASS`。截图相似无法替代结构或行为证据；原型不能运行时禁止静态猜测，关键行为未知为 `BLOCKED`，非关键未覆盖为 `PARTIAL`。

审计期间不写业务实现。审计报告还要区分已确认事实、设计意图、原型机制、生产建议与待确认问题，对齐现有项目能力。Plan 必须消费审计结果，作出 `Keep / Adapt / Replace / Exclude` 决策，并保留 Workflow 的 11 个实施/验证阶段。交付包指纹变化须回到 Understand。

## 状态、产物和知识库

| 状态 | 含义 | 后续动作 |
| --- | --- | --- |
| `PASS` | 实际执行且证据支持通过 | 推进下一项 |
| `PARTIAL` | 已执行但覆盖不完整 | 补覆盖或记录具体风险决定 |
| `NOT_RUN` | 没有执行 | 补执行，禁止声称通过 |
| `BLOCKED` | 已尝试但受依赖/环境/权限阻塞 | 保存阻塞与恢复条件后暂停 |

Understand Gate 为 `Pending / Passed / Needs More Investigation / Blocked`；Plan Gate 为 `Not Applicable / Pending / Confirmed / Revision Requested / Rejected`；Review 为 `PASS / CHANGES_REQUIRED / BLOCKED`。这些是不同层面的状态，不能混用。

证据链为 `task.md → [design-delivery-audit.md] → plan.md → review.md → verification.md → feedback.md`。Small 允许省略正式计划和 Review；审计产物只在触发时生成。`current-task.md` 只保存活动指针，完整事实在任务目录，完成后归档。归档是过程证据，不等同于产品效果。

经验召回使用用户/项目配置的知识库，按其入口和目录规则最多精读三篇相关页面。没有配置或命中时如实记录。Feedback 候选只有审核接受后才能按知识库规则发布；修改 Workflow/Skill 需独立改进任务，不会因一次失败自动改规则。

## 验证与限制

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover \
  -s skills/design-delivery-audit/tests -v
python3 skills/design-delivery-audit/scripts/detect_delivery_package.py <交付包目录>
```

检测器退出 `0` 表示源码合格，`3` 表示不合格，`2` 表示路径/读取错误；源码资格不等于页面审计通过。Skill frontmatter 可用所安装 `skill-creator` 的 `quick_validate.py` 校验，该工具可能需要 PyYAML。

仓库的 Python 测试验证源码检测器，不证明任意项目的页面已还原，也不证明未来 Agent 必然遵守每条自然语言规则。运行证据需要在实际任务中采集；外部 Skill 或环境缺失必须记录状态。

Workflow 不自动提交/推送业务代码、不绕过人工 Gate、不公开个人历史任务或凭据。公开包仅含入口、Workflow、模板、bundled Skill 与说明文档。

相对首版的规则与交付变化见 [IMPROVEMENTS.md](IMPROVEMENTS.md)。
