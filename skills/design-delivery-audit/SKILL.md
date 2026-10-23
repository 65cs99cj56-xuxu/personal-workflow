---
name: design-delivery-audit
description: Use when reconstructing at least one complete page or view from a readable HTML delivery package with standalone CSS or JavaScript, especially when fidelity depends on responsive styles, interactive states, dynamic DOM mutations, or cross-control effects.
---

# Design Delivery Audit

## Purpose

在页面级还原实现前，从完整交付包源码中提取可追溯的设计、状态、交互、动画、素材和适配规格，并将原型事实与生产实现建议分开。此 Skill 属于 Workflow 的 Understand 子阶段。

## Hard Boundary

- 本阶段只读取、运行和分析交付包及目标项目，不修改业务代码，不开始页面还原。
- 不得只确认文件存在，不得用 README 概括代替 HTML、CSS 和 JavaScript 源码检查。
- 静态 HTML、GSAP、直接 DOM 操作、演示数据和原型依赖不是默认生产方案。
- 关键冲突或未知项未解决时，Understand Gate 不得判定为 `Passed`。

## Routing Boundary

进入本 Skill 前必须先由主 Workflow 确认：

1. 用户任务是根据对应交付附件进行还原；
2. 请求范围至少覆盖一个完整页面或完整视图。

功能级实现、功能级还原、局部组件/区域/状态/行为的检查修改，以及页面级但非还原任务，均不使用本 Skill，直接走原 Workflow。页面级还原中额外点名重点功能仍属于页面级任务。范围不清时先询问用户。

## Source Eligibility

页面级还原任务的对应附件还必须同时满足：

1. 至少存在一个可读取的 `.html` 或 `.htm` 文件；
2. 至少存在一个可读取的独立 CSS 或 JavaScript 源文件。

CSS 源扩展名：`.css`、`.scss`、`.sass`、`.less`、`.styl`、`.stylus`。

JavaScript 源扩展名：`.js`、`.mjs`、`.cjs`、`.jsx`、`.ts`、`.tsx`。

HTML 内联 `<style>` 或 `<script>` 不单独满足第二项。CSS 与 JavaScript 按 OR 判断，不要求同时存在。文件条件只是 `Source Eligibility`，不能单独触发本 Skill。

先使用 `test -r` 与 `realpath` 解析当前 Skill 的真实路径，再使用解析后的绝对脚本路径运行：

```bash
python3 <resolved-design-delivery-audit-dir>/scripts/detect_delivery_package.py <delivery-root>
```

退出码只描述源码资格：

- `0`：`source_eligible: true`。
- `3`：`source_eligible: false`，记录检测结果并返回普通 Understand/UI 视觉契约流程。
- `2`：路径或读取错误，记录 `BLOCKED`。

脚本输出包含 `source_eligible`、文件分类和 `package_fingerprint`。最终 `Audit Decision` 由主 Workflow 结合页面级还原语义和源码资格作出。审计完成后必须保存指纹；进入 Plan、恢复任务或开始 Execute 前重新计算。指纹变化时原审计失效，追加检测记录并回到 Understand。

## Required Inputs

- 交付包根目录。
- 目标项目根目录。
- 已确认为页面级还原的目标和完整页面范围。
- 当前任务目录，用于写入 `design-delivery-audit.md`。

缺少交付包路径或目标项目路径时，记录缺失项并暂停，不猜测目录。

## Audit Process

1. 记录 `Reconstruction Intent: Page-level`、`Requested Scope` 和主 Workflow 的 `Audit Decision`。
2. 运行源码资格检测并保存 `source_eligible`、文件分类与交付包指纹。
3. 读取 [references/audit-spec.md](references/audit-spec.md) 全文。
4. 建立 Source Coverage，逐类读取 README/说明、验证记录、HTML、CSS、JavaScript、截图、图片、SVG、字体、生成脚本和资源校验文件。
5. 必须实际运行原始交付页面，执行 Source-driven Responsive Behavior Discovery；纯 CSS 或固定布局页面也不能跳过。存在 JavaScript、交互伪类或动态 DOM 行为时，还必须执行 Runtime Interaction And Cross-control Audit。记录启动命令、环境、视口与实际结果。原型无法运行时禁止用静态源码推断完整行为，关键行为不明为 `BLOCKED`，非关键覆盖缺失为 `PARTIAL`；不得因此修改目标业务代码。
6. 从 HTML/CSS/JavaScript 源码提取页面结构、状态、响应式、交互和动画规格。每一项写明来源文件及选择器、函数、变量、事件处理器或行号锚点。
7. 对照 README、截图与源码，登记版本差异、过时说明和冲突。不得自行设定来源优先级。
8. 调查目标项目入口、组件、API adapter、主题配置和状态管理，形成 `Reuse / Adapt / Add` 映射；同时检查框架/语言、样式和组件约定，以及 SVG、字体、图片的 alias、loader、plugin 和实际构建解析方式。Vue 页面还原需记录页面目录、页面根文件、页面级样式归属、功能/组件和图片/视频素材的目标位置，并判断多文件组件是否应使用组件子目录；默认建议是页面集中于 `src/pages/<page-name>/`，根部尽量只放 `App.vue`、`main.ts`、`styles.less`，页面级样式在 `styles.less` 中维护并由 `App.vue` 导入，其他内容按职责放入 `components/` 或页面下的专用功能子目录，素材放 `assets/`。组件局部样式按项目约定处理。项目约定优先，且不要求三个根级文件必须齐全。此目录建议不应用于 React。所有结论引用目标项目配置或代码锚点。
9. 按任务模板生成 `design-delivery-audit.md`，并把关键事实、风险、未知项和 AC 回填 `task.md`。
10. 对照 Audit Gate Checklist 自检；只有满足 Gate 才能将审计结果标记为 `PASS`。

## Source-driven Responsive Behavior Discovery

所有进入本 Skill 的页面级还原任务均须执行本节，不以是否存在 JavaScript 或交互伪类为条件。响应式还原必须从交付源码及原型实际表现中发现适配规律，不得以预设设备宽度、固定测试区间或少量截图代替规律分析。

1. 分析 HTML、CSS、JavaScript 中影响适配的规则，包括 viewport、单位、min/max/clamp、媒体查询、容器查询、内容换行、响应式资源、matchMedia、resize 和条件渲染。根据源码约束和明确的目标范围确定探索起点，记录其依据；源码范围不明时保持 Open Question，不把工具默认视口当作适配边界。
2. 实际运行原型，连续调整视口宽度，在观察到变化的区间内加密探测，结合源码定位布局、显示隐藏、节点、资源及交互模式的转换条件。分别识别视口、容器尺寸和内容触发的变化；没有媒体查询不代表没有适配行为。记录探索范围、采样依据和未覆盖范围，不擅自把初始探索区间固定为完整支持范围。
3. 提炼各区域的适配规律：哪些固定、哪些连续伸缩、哪些达到条件后换行、重排、替换或改变操作方式。分别记录 DOM 新增/删除/替换/重排/属性变化，与 DOM 不变时的 CSS 显隐、视觉顺序、布局和尺寸变化。提供源码锚点、实测值和运行证据；不得把视觉重排误记为 DOM 重排，或将少量观测点直接外推为整个区间的规律。
4. 在发现的各规则区间分别首次加载原型，再执行宽→窄→宽连续切换，验证初始化与运行中变化的差异、状态保留/恢复、滚动与溢出、控件可操作性、焦点/ARIA 和跨控件影响。把尺寸变化及其状态转换纳入 Interaction State Graph 和 Cross-control Dependency Graph。等待可观察条件成立，不用固定等待代替确认。
5. 根据已发现的规律生成 Responsive State Matrix，覆盖各规则区间代表点、转换边界两侧及区间内未用于调试的宽度，关联页面状态、交互路径、首次加载与尺寸切换。保存全页面 DOM snapshot、Mutation（无变化也记录）、受影响元素 computed style/bounding box、焦点/ARIA、Console 和截图证据。验证宽度是规律发现的结果，不是预先限定还原行为的依据。
6. 目标实现必须复现相同的适配规律、状态转换及恢复行为，并回放相同宽度、容器/内容条件、加载方式、尺寸切换和交互路径；不得针对若干测试宽度编写特例后判定完成。关键适配行为无法确认标记 `BLOCKED`，非关键覆盖缺失标记 `PARTIAL`；未确认范围进入 Open Question，不宣称任意宽度均已验证。附件若是固定布局或窄屏溢出，按实际证据记录，不自行设计新的适配方案冒充还原。

## Runtime Interaction And Cross-control Audit

当交付包存在 JavaScript、交互伪类或动态 DOM 行为时，本节为强制步骤。

1. 静态发现 CSS 中的 :hover、:focus、:focus-visible、:focus-within、
   :active、:checked、:disabled、:has()、兄弟选择器和状态属性选择器。
   同时关联上节发现的媒体/容器查询及连续布局规则。
2. 静态发现 JavaScript 中的事件监听、事件委托、共享状态写入、
   classList、style、hidden、dataset、aria-*、DOM 插入删除及条件渲染。
   包括 matchMedia、resize 和尺寸相关的初始化/条件渲染分支。
3. 不得只记录事件所在控件。必须沿状态写入和选择器依赖追踪所有直接、
   间接受影响的控件、页面区域、浮层和后续可操作状态。
4. 形成页面级 Interaction State Graph 和 Cross-control Dependency Graph。
   包含尺寸变化对状态、控件和区域的影响，并引用 Responsive State Matrix。
5. 在原型运行态逐条执行交互路径，记录交互前、中、后的全页面 DOM、
   Mutation、computed style、bounding box、document.activeElement、
   ARIA 状态、Console 错误及截图。
   按响应式规律生成的矩阵覆盖不同宽度的首次加载及连续尺寸切换。
6. 对延时、动画、异步更新和连续操作，等待可观察状态条件成立，
   不使用任意固定等待时间代替状态确认。
7. 无法执行或无法解释的交互必须记录为 Open Question，
   不得省略或推断为没有变化。

截图只能证明特定时刻的视觉输出。没有对应 DOM、computed style
和状态转换证据的交互，不得标记为 PASS。

## Source-backed Reconstruction Evidence Contract

以源码及原型实际运行行为为设计事实，按 Workflow 同名契约分别建立 Structure Contract、Style Contract、Behavior Contract、Cross-control Dependency Graph 和 Visual Baseline。详细字段与运行证据组织见 [references/audit-spec.md](references/audit-spec.md)。截图仅补充前三类证据。

目标实现 Verify 必须消费相同状态图，在原型和目标回放相同交互路径。只有 Structure、Style、Behavior、Visual 四类必要证据都通过，页面还原才能为 `PASS`；审计 `PASS` 只说明基线已建立，不等于目标实现已经验证。

四类证据必须包含 Source-driven Responsive Behavior Discovery 的规律、状态矩阵和同条件回放结果；仅在预设设备宽度下截图相似不足以通过。

## Evidence Classification

所有结论必须属于以下一种：

| Classification | Meaning |
| --- | --- |
| `Confirmed Fact` | 由源码、配置、素材属性或实际运行直接确认 |
| `Inferred Intent` | 从多个事实推导出的设计意图，必须说明推导依据和置信度 |
| `Prototype Mechanism` | 原型当前采用的 HTML/CSS/JavaScript/库实现方式 |
| `Production Recommendation` | 结合目标项目提出的生产实现建议，不得伪装成交付包事实 |
| `Open Question` | 来源缺失、冲突或需要产品/设计/研发决定的问题 |

推荐证据表：

| Classification | Specification | Source | Anchor | Confidence |
| --- | --- | --- | --- | --- |
| `Confirmed Fact` |  |  |  | `High` / `Medium` / `Low` |

## Result Semantics

- `PASS`：触发条件成立，所有适用来源已检查，五类契约/基线证据与来源完整，响应式规律与状态矩阵已由源码和运行建立，适用运行态交互已执行并形成两类图，关键冲突已解决，项目映射与风险完整。
- `PARTIAL`：已执行审计，但存在非关键缺失或无法覆盖的来源；必须列出未覆盖范围。
- `NOT_RUN`：Skill 可用但没有执行，不能声称完成交付包审计。
- `BLOCKED`：路径、权限、损坏文件、关键依赖或关键冲突导致无法完成。

CSS 或 JavaScript 其中一类不存在时仍可触发：

- 缺 CSS：静态样式源码覆盖标记为 `PARTIAL` 或明确 `Not Applicable`，不能从 JavaScript 猜测视觉规格。
- 缺 JavaScript：动态交互源码覆盖标记为 `PARTIAL` 或明确 `Not Applicable`，不能从 HTML/CSS 猜测完整行为。

## Audit Gate Checklist

- [ ] `Reconstruction Intent: Page-level`、完整页面范围和 `Audit Decision: Triggered` 已记录。
- [ ] `source_eligible` 和 `package_fingerprint` 已记录。
- [ ] Source Coverage 对所有适用来源给出状态和实际提取结果。
- [ ] 页面、弹窗、浮层、业务状态及转换关系已列出。
- [ ] 静态视觉、响应式、素材、交互和动画规格具有来源锚点。
- [ ] 已从源码及原型实际表现发现适配规律，区分 DOM/CSS 变化及视口/容器/内容触发，探索范围与未确认范围明确；纯 CSS/固定布局未跳过运行。
- [ ] Responsive State Matrix 由规律生成，覆盖区间代表点、转换边界两侧、未用于调试的宽度，以及首次加载/宽→窄→宽切换；证据与两类图关联。
- [ ] 已分别建立 Structure、Style、Behavior、Cross-control Dependency Graph 与 Visual Baseline，截图未替代前三类证据。
- [ ] 适用交互已按 Interaction State Graph 实际运行；已保存前/中/后 DOM、Mutation、computed style、bounding box、焦点/ARIA、Console 与截图证据。
- [ ] 已追踪所有直接/间接影响，不能解释或执行的交互已进入 Open Question；关键问题未确认时 Gate 不通过。
- [ ] 正式要求、设计意图、原型机制、演示数据和待接入内容已区分。
- [ ] README、截图和源码冲突已登记；关键冲突已有人工决定。
- [ ] 已完成与目标项目的 `Reuse / Adapt / Add` 映射。
- [ ] 已从项目配置确认框架/语言、样式/组件约定和 SVG/字体/图片资源解析方式；未知项已保留为 Open Question。
- [ ] 风险、未知项、生产验收建议和不进入生产的原型行为已明确。
- [ ] 审计过程未修改业务代码。

## Handoff

完成后：

1. 在 `task.md` 的 Skill Execution 追加执行记录。
2. 在 `task.md` 引用 `design-delivery-audit.md` 中影响事实、风险和 AC 的具体章节。
3. Understand Gate 通过后，将审计报告作为前端 Plan 的强制输入。
4. Plan 必须明确原型行为的 `Keep / Adapt / Replace / Exclude` 决策，并按 Workflow 规定的 11 个实施阶段组织输入、产出和验收标准。
