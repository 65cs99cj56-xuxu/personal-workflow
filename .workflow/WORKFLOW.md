# Personal AI Software R&D Workflow v0.1

> 适用对象：个人进行前端、后端或前后端联动开发的软件研发人员。
>
> 目标：让 AI 的开发过程可理解、可验证、可恢复、可复盘。采用 Agent 解释 Markdown 的阶段编排，不依赖后台调度服务；改进规则需要用户授权。

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
3. 进入当前阶段前，读取本文件对应的 Skill，并严格按 Skill 的输出要求执行；读取前使用可跟随符号链接的可读性检查和真实路径解析（例如 `test -r`、`realpath` 或等价工具），任务中同时记录 `Configured Path` 和 `Resolved Path`。不能仅凭不跟随符号链接的文件搜索结果判定 Skill 不存在。
4. 阶段完成后更新任务文档、验证状态和 `.workflow/current-task.md`，再根据复杂度路由到下一阶段。
5. 遇到人工 Gate、关键未知项、方案取舍或阻塞时，保存状态并暂停，不自行替用户做产品或风险决策。
6. 用户说“继续当前任务”或提供 Gate 决策后，从状态文件记录的阶段恢复，不重新开始已经完成的阶段。

Skill 不可用时必须明确记录为 `BLOCKED` 或 `NOT_RUN`，不能假装已经执行，也不能静默替换成未确认的能力。每次执行或跳过都在 `task.md` 的 Skill Execution 表中追加一行；历史行不可覆盖，复核只能追加新行。

### 首次初始化与 Git 忽略

首次生成项目 `.workflow/` 前，记录该目录是否已存在。仅在第一次创建该目录时，必须立即检查项目根目录的 `.gitignore` **文件**，在写入任务产物前完成以下处理：

- 已有 `.gitignore`：保留原内容、换行和其他规则，在末尾追加 `.workflow/`；若现有有效规则已忽略目录及其内容则不重复追加。检查后续否定规则，不能仅因文本中出现 `.workflow/` 就认为有效。
- 没有 `.gitignore` 文件：记录 `Skipped — No .gitignore`，不新建该文件。若同名路径是目录，不把它当文件写入。
- 在 Git 仓库中，用 `git check-ignore --no-index` 检查 `.workflow/` 及代表性子路径（如 `.workflow/current-task.md`、`.workflow/tasks/probe.md`）的实际匹配规则；非 Git 项目保留追加规则的文件证据。记录 `Added`、`Already Ignored` 或跳过原因。
- 写入失败时记录 `BLOCKED` 和恢复动作，不宣称忽略配置完成。恢复既有 `.workflow/` 不重复执行已完成的首次初始化；若先前忽略设置为 `Pending` 或 `BLOCKED`，先恢复该未完成步骤。已跟踪文件不会因 `.gitignore` 自动消失，不自动运行 `git rm --cached`。

此规则用于使用者项目生成的过程目录；分发仓库内的 `.workflow/WORKFLOW.md` 与模板是安装资源，不应从分发包中排除。

### 页面还原请求自动补全

在 Understand 开始时，根据用户意图和对应附件确定完整页面范围。附件同时存在可读取的 HTML、独立 CSS、独立 JavaScript，且用户要求“还原页面”或同义的完整页面还原时，自动补齐下列 Effective Reconstruction Prompt。用户不必再次发送此文本。

在 `task.md` 保存 `Raw User Request`、`Effective Reconstruction Prompt`、匹配的文件路径和判定理由。保留原始目标页面、技术栈、重点与明确限制；补全不覆盖用户的明确约束。用户明确只要求局部组件或功能时不自动扩大为完整页面；范围不清时先澄清。

自动补全条件是 `页面级还原 && HTML && CSS && JavaScript`。Design Delivery Audit 的触发仍是 `页面级还原 && HTML && (CSS || JavaScript)`；未命中自动补全不代表跳过审计。

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

必须从交付源码及原型连续宽度变化中发现响应式规律，区分视口、容器、
内容触发及 DOM 与 CSS 视觉变化，不预设固定设备宽度或测试范围代替探索。
按发现的规律生成验证点，覆盖区间代表点、转换边界两侧及未用于调试的
宽度；对原型和目标回放相同条件下的首次加载、宽→窄→宽及交互路径。
记录状态保留、恢复和未确认范围，不以针对少量宽度的特例判定完成。
```

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
Understand -> Understand Gate -> Plan -> Plan Gate（人工确认） -> Execute -> Review -> Verify -> 最终完成门 -> Feedback
```

### Large / High Risk

适用于跨前后端契约、数据模型、权限、支付、核心链路、生产风险或需求不清晰的任务。

```text
Understand -> 人工确认 -> Plan -> 人工确认 -> Execute
  -> Independent Review -> Verify -> 最终完成门 -> Feedback -> Archive / Improve
```

满足以下任一条件时，至少按 Medium 处理：

- 根据交付附件进行至少一个完整页面的还原，且附件包含 HTML 与可读取的 CSS 或 JavaScript 源文件。
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

#### Design Delivery Audit：从可运行交付包建立实现前设计基线

`Design Delivery Audit` 只用于根据交付附件进行的页面级还原，是 Understand 的条件子阶段，不新增顶级 Stage。任务语义和范围优先于文件形态；不能因为输入包含 HTML、CSS 或 JavaScript 就自动触发。

最终触发必须同时满足：

1. 用户任务是根据对应交付附件进行还原；
2. 任务范围至少覆盖一个完整页面或完整视图，而不是单个功能、组件、区域、状态或行为；
3. 附件中至少存在一个可读取的 `.html` 或 `.htm` 文件；
4. 附件中至少存在一个可读取的独立 CSS 或 JavaScript 源文件。

完整条件可表示为：`页面级还原 && HTML && (CSS || JavaScript)`。CSS 与 JavaScript 按 OR 判断，不要求同时存在。HTML 内联 `<style>` 或 `<script>` 不单独满足源码条件。

功能级实现和功能级还原、局部对比修改、页面级但非还原任务，都直接走原 Workflow，不增加专项 Skill、Artifact、Gate 或固定阶段。页面级还原中点名某个重点功能时，任务对象仍是完整页面，因此继续触发；重点只改变审计优先级。任务范围无法判断时必须先询问用户，不得仅凭文件条件自动升级。

只有任务语义和范围符合页面级还原后，才运行 bundled `skills/design-delivery-audit/scripts/detect_delivery_package.py` 检查 `Source Eligibility`。脚本输出的 `source_eligible` 只表示附件源码条件是否满足，不代表最终触发决定。只有 `Audit Decision: Triggered` 时才读取完整审计 Skill 并生成 `design-delivery-audit.md`。此类任务最低按 `Medium` 处理，必须生成正式 `plan.md` 并经过 Plan Gate。

只有截图、没有 HTML，或有 HTML 但没有可读取的独立 CSS/JavaScript 源文件时，不触发完整源码审计，继续使用普通 Understand 或现有 UI 视觉契约流程。

审计阶段只允许读取、运行和分析交付包及目标项目，不得修改业务代码或开始页面还原。审计必须完整检查 README/验证记录、HTML、CSS、JavaScript、截图、素材、字体、生成脚本和资源校验文件；文件存在但未读取内容不能视为完成。每项规格必须引用来源文件及选择器、函数、变量、事件处理器或行号等锚点，并分开记录：

- `Confirmed Fact`：已确认事实。
- `Inferred Intent`：从源码推导的设计意图。
- `Prototype Mechanism`：原型实现方式。
- `Production Recommendation`：建议的生产实现方式。
- `Open Question`：待确认问题。

README、截图、HTML、CSS 和 JavaScript 冲突时，只记录各自证据和生产影响，不预设全局优先级。涉及生产行为、目标设备、兼容范围或验收要求的关键冲突必须由用户决定。静态 HTML、GSAP、直接 DOM 操作、演示数据和原型依赖不得默认成为生产实现方案。

检测脚本输出的 `source_eligible`、文件分类和 `package_fingerprint` 必须写入审计报告。在进入 Plan、恢复任务或开始 Execute 前重新计算；指纹变化表示交付包已更新，原审计失效，必须追加检测记录并回到 Understand 重新审计。

#### Source-backed Reconstruction Evidence Contract

对于包含 HTML、CSS、JavaScript 的页面级还原任务，交付包源码及其实际运行行为是设计事实来源。截图只用于验证最终视觉结果，不得单独作为结构、样式或交互还原完成的证明。

审计必须分别建立以下证据：

1. Structure Contract：页面语义结构、内容顺序、控件角色、关键属性、
   动态节点、浮层及状态节点。
2. Style Contract：Design Token、布局几何、computed style、断点、
   伪类、层级、overflow、transform 和动画规则。
3. Behavior Contract：触发事件、前置状态、中间状态、最终状态、
   DOM mutation、焦点、ARIA、恢复及重复操作行为。
4. Cross-control Dependency Graph：记录一个控件或共享状态的变化
   会影响哪些其他控件、区域、浮层和后续操作。
5. Visual Baseline：在指定视口和状态下保存截图或录屏，作为前三类
   证据的补充，不替代前三类证据。

存在 JavaScript、交互伪类或动态 DOM 行为时，必须运行原始交付页面，
按状态图实际触发适用交互，并保存交互前后的全页面 DOM snapshot、
受影响元素的 computed style、bounding box、焦点/ARIA 状态和截图。

原始交付页面无法运行时，不得根据静态源码猜测完整运行行为。
关键行为无法确认时标记 BLOCKED；非关键行为未覆盖时标记 PARTIAL。

目标实现验证时，必须对原型和目标页面执行相同的交互路径。
只有 Structure、Style、Behavior 和 Visual 四类必要证据均通过，
才能将页面还原判定为 PASS。截图相似不能覆盖结构或行为缺失。

所有 `Audit Decision: Triggered` 任务均按适用来源建立本契约；缺 JavaScript 不免除 CSS 交互伪类的运行审计。另形成页面级 Interaction State Graph 和 Cross-control Dependency Graph，覆盖直接、间接及异步影响。

#### Source-driven Responsive Behavior Discovery

所有已触发的页面级审计都必须实际运行原型，执行审计 Skill 的同名章节，包括纯 CSS、无显式断点和固定布局。先从源码及连续宽度变化发现固定量、连续关系、内容换行与布局/节点/交互模式的转换条件，区分视口/容器/内容触发及 DOM 变化/CSS 视觉变化；变化区间加密探测并记录来源、实测值和探索限制。不以预设设备宽度、自定固定测试范围或少量截图代替规律分析，不把工具默认视口当作支持边界。

建立 Responsive Rule Register 和 Responsive State Matrix，依据发现的规律生成各区间代表点、转换边界两侧及未用于调试的宽度。分别记录首次加载与宽→窄→宽切换、状态保留/恢复及跨控件影响，保留 DOM/Mutation/style/geometry/focus/ARIA/Console/截图证据并关联两类图。原型固定布局/窄屏溢出按事实记录，不自行设计新适配冒充还原；无法确认的范围进入 Open Question，关键适配不明为 `BLOCKED`，非关键未覆盖为 `PARTIAL`。

#### Experience Recall

完成当前代码、配置和调用链调查后，AI 必须执行一次受控经验召回。已接受的长期经验使用用户或项目配置的唯一知识库根目录；没有配置时记录无可检索来源，不猜测路径，不得扫描全部历史归档，也不得另建平行的 `.workflow/experience.md`。

1. 从任务目标、项目、技术栈、改动范围和风险提取 3 至 8 个检索词。
2. 按知识库自身的 AGENTS/索引规则读取根入口、对应领域入口及经验/阶段索引，检索 `status`、`scope`、`triggers` 和 `tags`，排除 `deprecated` 条目；不得固定假设经验正文位于 `knowledge/`。
3. 按“同项目 decision/problem、同风险 problem、跨项目 knowledge”的优先级，最多精读 3 个页面。
4. 在 `task.md` 的 `Experience Recall` 中记录查询、命中页面、适用性和决策。无命中时也必须记录查询与 `Matches: none`。
5. `Applied` 必须明确影响至少一项 `Known Facts`、`Constraints`、`Risks`、`plan.md`、验收标准或验证项，并在表中引用具体位置；只阅读页面不能标记为 `Applied`。

`Decision` 只能为 `Applied`、`Not Applicable` 或 `Needs Human Review`。当前代码和配置事实优先于历史经验；二者冲突或经验会改变兼容性、安全、权限、数据保留等关键风险时，标记 `Needs Human Review` 并暂停等待决定。经验召回只能补充调查和验证，不能替代代码调查、Review 或 Verify。

#### Skill Execution Evidence

每个被要求或选择的 Skill 都必须在 `task.md` 追加执行记录，至少包含：

| Stage | Skill | Configured Path | Resolved Path | Attempted At | Attempted | Result | Evidence | Usage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Understand | `sk-codebase-explore` | 配置路径 | 解析后的真实目标 | 时间 | `Yes` / `No` | `PASS` / `PARTIAL` / `NOT_RUN` / `BLOCKED` | 命令、读取路径、输出或阻塞原因 | 输出影响了哪个事实、决策或后续产物 |

状态语义固定为：

- `PASS`：Skill 已执行，并产生了有效结果。
- `PARTIAL`：Skill 已执行，但结果不完整或只覆盖部分要求。
- `NOT_RUN`：Skill 可用但本次未执行，不能据此声称完成。
- `BLOCKED`：已尝试执行，但因路径、依赖、权限或工具问题无法完成。

`NOT_RUN` 的 `Attempted` 必须为 `No`；`PASS`、`PARTIAL` 和 `BLOCKED` 的 `Attempted` 必须为 `Yes`。无法解析真实目标时，`Resolved Path` 写 `Unresolved` 并在 Evidence 中说明原因。

`Usage` 只记录人工可验证的引用，不自动判断 Skill 输出是否被使用。`Skill Gap` 只能作为 Feedback 分类，不能代替上述执行状态。

### Understand Gate：确认是否理解到可以动手

Gate 状态必须持久化在 `task.md` 和 `state.md`：

```markdown
## Understand Gate

- Status: `Pending` / `Passed` / `Needs More Investigation` / `Blocked`
- Confirmed facts:
- Remaining unknowns:
- Decision:
- Evidence:
```

进入 Plan 或 Execute 前检查：

- 是否找到真正的入口、调用链和状态/数据流。
- 是否识别前后端、数据库、配置和外部依赖的影响。
- 是否写出可验证的验收标准。
- 是否列出关键未知项及其解决方式。
- 是否知道如何证明改动没有破坏原有行为。

`Audit Decision: Triggered` 时还必须检查：

- `Reconstruction Intent` 是否为 `Page-level`，`Requested Scope` 是否至少覆盖一个完整页面，`Audit Decision` 是否有明确理由。
- 交付包读取范围和每类来源的实际提取结果是否完整记录。
- 页面、弹窗、浮层、业务状态及状态转换是否已梳理。
- 静态视觉、响应式、素材、交互和动画主要规格是否具有来源锚点。
- 正式要求、设计意图、原型机制、演示数据和待接入内容是否已区分。
- 版本差异和冲突是否已登记，关键冲突是否已有人工决定。
- 是否完成交付包与现有项目入口、组件、API adapter、主题配置和状态管理的 `Reuse / Adapt / Add` 映射。
- `package_fingerprint` 是否仍与当前交付包一致。
- Structure、Style、Behavior 与 Visual Baseline 是否分别有证据；适用交互是否已在原型实际运行，Interaction State Graph 和 Cross-control Dependency Graph 是否覆盖所有受影响区域。
- 是否从源码/运行发现响应式规律并建立 Rule Register/Responsive State Matrix；宽度取点是否有规律依据，纯 CSS/固定布局是否运行，首次加载/尺寸切换及未知范围是否有证据。
- 无法运行或无法解释的行为是否进入 Open Question；关键行为未知时不得通过 Understand Gate。

只有 `Passed` 才能进入 Plan 或 Execute。`Pending` 和 `Needs More Investigation` 回到 Understand；`Blocked` 保存阻塞和恢复信息并暂停。如果需求本身不明确，先向用户确认，不用猜测补齐产品决策。

### Plan：把理解转成可执行上下文

前端主 Skill：`kit-fe-write-plan`。

后端主 Skill：`sy-spec:go-plan`。

前后端联动时分别产出前端和后端计划，使用同一份任务上下文对齐 API、数据结构、状态、错误处理和验收标准。计划写入 `plan.md`，至少说明选定方案、理由、替代方案、取舍、影响范围、实现顺序、验证策略、风险和不在范围内的内容。

`Audit Decision: Triggered` 的页面还原任务，前端 Plan 必须读取 `design-delivery-audit.md`，明确每项原型机制的 `Keep / Adapt / Replace / Exclude` 决策，并按以下顺序给出每阶段的输入、产出、依赖、对应 `AC-xx` 和验收证据：

1. 交付包审计与未知项确认。
2. Design Token、单位、断点和素材规则。
3. 项目架构及状态模型。
4. 基础页面骨架。
5. 一个代表性样板状态。
6. 公共组件。
7. 其他静态状态。
8. 交互和动画。
9. 真实接口与生产配置。
10. 响应式、真实设备和低版本兼容。
11. 截图、录屏和完整回归。

确实不适用的阶段可以标记 `Not Applicable`，但必须说明理由，不得静默删除。计划必须说明哪些行为按原型保留、哪些改用项目现有能力、哪些演示数据改接真实 API、哪些原型行为不进入生产。

所有生成正式 `plan.md` 的任务，在进入 Execute 前都必须经过 Plan Gate。Medium、Large / High Risk 任务必须暂停等待人工确认计划；Small 任务可以跳过正式 Plan，因此不经过该 Gate。

人工确认至少应明确以下内容：选定方案、实现顺序、影响范围、验证方式、风险和不在范围内的内容。用户可以确认执行、要求修改计划，或拒绝当前方案；未收到确认前不得修改业务代码。

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

`Audit Decision: Triggered` 时，Review 还必须对照 `design-delivery-audit.md` 检查实现是否偏离已确认规格，`Reuse / Adapt / Add` 与 `Keep / Adapt / Replace / Exclude` 决策是否落实，以及是否机械搬运静态 HTML、GSAP、直接 DOM 操作、原型依赖或演示数据。Execute 中发现新的设计规格或交付包变化时，应回退 Understand，不得在实现中静默决定。

Review 必须产出独立的 `review.md`，状态只能是 `PASS`、`CHANGES_REQUIRED` 或 `BLOCKED`。`CHANGES_REQUIRED` 默认回退 Execute；`BLOCKED` 必须记录阻塞和恢复条件。

### Verify：用真实证据证明验收标准

前端专项 Verify：`kit-fe-verify`；需要运行时、浏览器或调试时使用 `build-web-apps:frontend-testing-debugging`。

后端专项 Verify：`kit-backend-feature-verify`。

通用最终完成门：`superpowers:verification-before-completion`。

验证优先覆盖真实边界：实际构建、相关测试、真实数据库或 Docker、浏览器交互、Network 请求、接口响应、迁移结果和核心用户链路。每项验证必须引用 `task.md` 中的 `AC-xx`，并记录 Method、Actual Result、Evidence 和 Status。没有对应 Evidence 不能判定 `PASS`。

`Audit Decision: Triggered` 时，Verify 必须从审计规格派生视觉、状态、交互、动画、设备适配、资源和降级验证矩阵。证据按场景保留截图、录屏、浏览器自动化结果、DOM/computed style 测量、Console、Network、资源体积或真实设备结果；覆盖审计中标记为生产验收要求的实际行为，以及适用的输入方式差异、状态恢复、异常路径、可访问性和 `prefers-reduced-motion` 降级。

#### Source-backed Reconstruction Evidence Contract：验证完成门

Verify 必须执行 Understand 中同名契约：以交付包源码和原型实际运行行为为事实基线，逐条对原型和目标页面回放相同的 Interaction State Graph 路径，使用相同视口、输入方式、初始状态和可观察终态。按 Cross-control Dependency Graph 核对全部直接/间接影响区域及恢复、重复操作和异步路径。

每条路径分别保留原型与目标的前、中、后全页面 DOM snapshot、Mutation、受影响元素 computed style、bounding box、`document.activeElement`、ARIA、Console 错误和截图/录屏，并记录差异与已确认的生产适配决策。等待可观察状态条件成立，不以任意固定等待时间代替状态确认。截图相似不能覆盖结构、样式或行为缺失。

响应式验证必须消费 Responsive Rule Register/Responsive State Matrix，按发现的规律选择区间代表点、转换边界两侧及未用于调试的宽度，原型/目标回放相同宽度、容器/内容条件、首次加载与宽→窄→宽序列及交互。核对连续关系、转换条件、DOM/CSS 差异及状态保留/恢复，不以固定设备列表或针对少量宽度的特例代替规律。四类证据包含这些结果，未确认范围不能宣称通过，关键适配未知为 `BLOCKED`，非关键覆盖缺失为 `PARTIAL`。

只有 Structure、Style、Behavior、Visual 四类必要证据均为 `PASS`，才能把页面还原判为 `PASS`。关键行为无法确认时为 `BLOCKED`，非关键行为未覆盖时为 `PARTIAL`；原型无法运行时不得根据静态源码猜测完整行为。完全静态页面的无交互事实需有来源证据，不能以空白行为表冒充通过。用户接受剩余风险不改变四类证据的实际状态，也不能将未通过的页面还原标成 `PASS`。

状态只能使用：

- `PASS`：已执行且证据支持通过。
- `PARTIAL`：只验证了部分范围，仍有明确未覆盖项。
- `NOT_RUN`：尚未执行，不能声称通过。
- `BLOCKED`：因环境、依赖或权限无法执行，并记录阻塞原因。

只有所有与验收标准相关的必要项为 `PASS`，或者用户明确接受剩余风险，才可通过最终完成门。

### Recovery Rules

| Result | 含义 | 默认动作 | 必须记录 |
| --- | --- | --- | --- |
| `NOT_RUN` | 尚未执行 | 回到负责该项的 Stage 补执行；例如 Understand Skill 回到 Understand，验证项回到 Execute 或 Verify | 补执行方法和证据 |
| `PARTIAL` | 已执行但覆盖不完整 | 补充未覆盖项，或由用户明确接受剩余风险 | 未覆盖范围、补执行或人工决策 |
| `BLOCKED` | 已尝试但当前无法完成 | 保存状态并暂停，阻塞解除后从记录 Stage 恢复并重新检查 Gate | `Blocker`、`Dependency`、`Recovery Condition`、`Next Action` |

以上状态不能自动升级为 `PASS`。暂停时必须保存完整 Recovery Snapshot。

### Feedback：Workflow 内置必经阶段

Feedback 不是可选的总结，也不由某一个 Skill 代替。每个任务在 Verify 和最终完成门之后都必须产出 `feedback.md`，即使任务失败、部分完成或被阻塞也一样。Feedback 不得覆盖任何历史执行记录。

AI 需要基于任务证据分析：任务结果、问题、根因、恢复过程、有效决策、可复用经验、风险模式、Skill Improvement Gap、Workflow Gap 和改进候选。Skill Improvement Gap 必须引用具体 Skill Execution 记录，不能代替执行状态。Feedback 必须区分事实与推断，不能把一次偶然现象直接升级为正式规则。

Feedback 的结论先进入候选状态，由人审核后再沉淀到个人知识库、项目规则或 Skill。AI 不得自动修改正式 Workflow。

#### Feedback Candidate 与 Review

候选必须在 `feedback.md` 的 `Improvement Candidates` 表中以唯一 `FB-YYYYMMDD-NN` ID 记录，并包含：`Type`、`Scope`、`Trigger`、`Recommendation`、真实 `Evidence` 和 `Review`。`Type` 只能为 `Experience`、`Regression`、`Decision` 或 `Rule Change`；`Scope` 只能为 `Project` 或 `Cross-project`；`Review` 只能为 `Pending`、`Accepted`、`Rejected` 或 `Needs More Evidence`。

只有候选存在时才进入 Feedback Review：

- `Accepted`：AI 可以按已配置知识库的目录和写入规则发布经验、问题或决策页面，并在 `feedback.md` 追加发布位置、Experience ID、审核人和日期；未配置知识库时保留候选并记录缺少发布位置。
- `Rejected`、`Needs More Evidence` 或 `Pending`：只保留在历史 feedback，不发布，不阻塞任务交付。
- `Rule Change`：即使已 `Accepted`，也只能创建独立改进任务，走 Understand、Plan、人工确认、Execute、Review 和 Verify；不得直接修改 Workflow、项目规则或 Skill。

发布前必须检查知识库索引和相关目录，优先更新已有同主题页面并在 `source` 追加来源，避免同义重复。新发布的页面必须有 `type`、`scope`、`status`、`triggers`、`source`、`accepted_at` 和 `tags` metadata；`status` 为 `active`、`deprecated` 或 `superseded`。过时经验保留历史页面，改为 `deprecated` 或 `superseded` 并链接替代页，不删除来源证据。

### Archive / Improve：完成后的可恢复沉淀

任务完成后，将任务、计划、验证和反馈文件，以及适用 Review 阶段产生的 `review.md`，一起归档到 `.workflow/archive/`，建议目录名为 `YYYY-MM-DD-任务名/`。归档内容应能回答：改了什么、为什么这样改、如何证明、还剩什么风险、下次遇到类似问题应复用什么经验。

`Audit Decision: Triggered` 的任务还必须归档 `design-delivery-audit.md`，保留其 `package_fingerprint`、来源锚点、冲突决策和项目映射。

只有经过人工审核的改进候选，才可以更新知识库；更新 Workflow、项目规则或 Skill 仍需创建独立改进任务。小任务可以只保留精简归档，但不能省略 Feedback 的结论。

## 4. 统一产物约定

每个任务使用一个独立目录，例如：

```text
.workflow/tasks/2026-09-15-user-login/
├── task.md
├── design-delivery-audit.md # 条件产物：触发 Design Delivery Audit 时生成
├── plan.md
├── review.md
├── verification.md
└── feedback.md
```

自动编排模式下，Agent 负责创建任务目录并维护 `.workflow/current-task.md`；手工模式仍可以复制 `.workflow/templates/` 下的模板。任务文件是当前工作上下文，归档后整体移动到 `.workflow/archive/`。

`.workflow/current-task.md` 只保存当前活动任务的路径、阶段、状态、暂停原因和下一步，不承载完整任务内容。默认只允许一个活动任务；需要并行任务时，应先人工扩展状态管理方案。

### 文档语言约定

所有由 Workflow 生成或更新的文档，无论文档类型、所在目录、文件名或是否存在对应模板，均以中文为主。必要的 English 专有名词、专业技术术语、代码标识符、文件路径、命令、API 或协议名称、Skill 名、状态枚举、AC ID 及其他机器可解析的固定值保留 English；不得为了语言统一而翻译或改写这些固定值。

该约定只前瞻性约束后续由 Workflow 生成或更新的文档，不要求回写 `.workflow/archive/` 中的历史 Artifact、既有证据或用户已有文档。

## 5. 回退矩阵

| 发现的问题 | 回退阶段 | 必须补充 |
| --- | --- | --- |
| 不知道入口、调用链或真实影响范围 | Understand | 新事实、相关文件、未知项 |
| 交付包发生变化或设计规格缺少来源锚点 | Understand | 新 `package_fingerprint`、追加审计记录、受影响事实和 AC |
| 交付包关键来源冲突尚未决策 | Understand / 人工确认 | 冲突来源、生产影响、用户决策和恢复条件 |
| 验收标准或需求含义不清 | Understand / 人工确认 | 用户决策或明确的验收条件 |
| 方案无法覆盖约束或契约不一致 | Plan | 新方案、取舍、影响范围 |
| 实现过程中发现范围或前置条件变化 | Plan | 更新计划并标明偏差原因 |
| Review 发现缺陷 | Execute | 修复内容和新增验证项 |
| Verify 失败 | Execute 或 Understand | 失败证据、根因、修复/阻塞说明 |
| Skill / 验证为 `NOT_RUN` | 负责该项的 Stage | 补执行动作和证据 |
| Skill / 验证为 `PARTIAL` | 当前阶段 | 未覆盖范围、补执行或风险接受决定 |
| Skill / 验证为 `BLOCKED` | 当前阶段并暂停 | Blocker、Dependency、Recovery Condition、Next Action |
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
- Medium、Large / High Risk 任务完成 Plan 后，等待人工确认计划。
- 计划涉及 API、数据库、权限、兼容性或明显取舍时，补充说明影响并继续等待确认。
- 验收标准无法从需求和代码中确定，需要用户补充产品决策。
- Verify 处于 `BLOCKED`，继续执行需要环境、权限或外部依赖变化。
- AI 发现超出原定范围，或准备改变已确认的方案。

暂停前必须：

- 更新当前任务的 `Status`、`Current Stage`、`Human Decision Required`、`Next Action` 和 Recovery Snapshot。
- 更新 `.workflow/current-task.md`。
- 明确告诉用户已完成什么、需要决策什么、恢复后将做什么。

### 恢复规则

收到“继续当前任务”、明确的人工决策或阻塞条件已解除时：

- 读取 `.workflow/current-task.md` 和当前任务目录中的全部产物。
- 只从记录的阶段继续；如果上下文与代码不一致，先回退到 Understand。
- 继续前重新检查对应 Gate，不重复无关阶段。
- 原始执行记录和验证记录只读；重试、复核和恢复结果追加新记录，不覆盖旧记录。

### 一句话入口示例

```text
实现用户登录功能，遵循项目 Workflow。
```

这句话的前提是 Codex 已安装 `personal-ai-workflow` Skill。项目不需要预先安装 `.workflow/` 或 `AGENTS.md`；首次执行时由 Skill 按需创建和初始化任务状态。用户不需要再次指定 Skill；Skill 路由由编排协议执行。

## 8. v0.1 的边界

本版本的自动化通过项目级 Agent 指令和状态文档实现，不包含独立后台进程或外部调度服务。明确不包含：自动捕获会话、自动分类知识、自动召回历史经验、多 Agent 编排、自动修改 Workflow、自动提交代码。

它解决两件事：用一套轻量的阶段和文档留下上下文、验证证据和反馈；通过状态文件实现阶段路由、暂停和恢复。
