# Design Delivery Audit

> 本产物属于 Understand 阶段。审计期间只读取、运行和分析交付包及目标项目，不修改业务代码，不开始页面还原。
>
> 仅当主 Workflow 已结合页面级还原范围与源码资格记录 `Audit Decision: Triggered` 时创建本产物。功能级实现、功能级还原及其他 `Not Triggered` 任务不创建本文件。

## Audit Metadata

- Task:
- Delivery package root:
- Target project root:
- Audited at:
- Reconstruction Intent: `Page-level`
- Requested Scope:
- Source Eligibility: `Eligible`
- Source rule: `HTML && (CSS || JavaScript)`
- Audit Decision: `Triggered`
- Decision Reason:
- Package fingerprint:
- Previous fingerprint:
- Fingerprint changed: `Yes` / `No` / `Not Applicable`
- Audit result: `PASS` / `PARTIAL` / `NOT_RUN` / `BLOCKED`

## Source Coverage

| Source Type | Files / Scope | Read Status | Extracted Result | Missing / Conflict | Evidence |
| --- | --- | --- | --- | --- | --- |
| README / 验证记录 / 说明 |  | `PASS` / `PARTIAL` / `NOT_RUN` / `BLOCKED` / `Not Applicable` |  |  |  |
| HTML 页面与状态 |  |  |  |  |  |
| CSS / 预处理器源码 |  |  |  |  |  |
| JavaScript / TypeScript 源码 |  |  |  |  |  |
| 参考截图 |  |  |  |  |  |
| 图片 / SVG / 字体 / 其他素材 |  |  |  |  |  |
| 页面生成脚本 / 构建配置 |  |  |  |  |  |
| 资源映射 / 校验文件 |  |  |  |  |  |

文件存在但未读取内容不能标记为 `PASS`。不存在的输入需标记 `Not Applicable` 或说明缺失风险。

## Evidence Register

| ID | Classification | Specification | Source | Anchor | Confidence |
| --- | --- | --- | --- | --- | --- |
| DA-001 | `Confirmed Fact` / `Inferred Intent` / `Prototype Mechanism` / `Production Recommendation` / `Open Question` |  |  |  | `High` / `Medium` / `Low` / `Unresolved` |

## Delivery Scope

### Baseline And Target Environment

| Item | Confirmed Value | Source / Anchor | Open Question |
| --- | --- | --- | --- |
| Design baseline size |  |  |  |
| Target devices |  |  |  |
| Browser / system / WebView |  |  |  |

### Target Project Organization

记录目标项目的框架及页面、组件、素材目录约定。若目标为 Vue，说明该页面是否适合集中到 `src/pages/<page-name>/`，并以页面目录根部尽量只保留 `App.vue`、`main.ts`、`styles.less` 为默认建议；页面级样式集中在 `styles.less` 并由 `App.vue` 导入，默认不写入 `App.vue` 的 `<style>`；组件局部样式仍按组件职责和项目规范组织。其他内容按职责决定放在 `components/` 或页面目录下职责明确的功能子目录。记录页面专属组件与图片/视频等素材的位置，以及多文件组件是否按组件建立独立子目录。默认示例不要求每页必须具备全部三个根级文件，也不排斥有依据的其他根级文件。必须引用路由、目录、构建配置或现有页面代码证据。已有项目约定优先于默认目录建议；React 标记为 `Not Applicable`，不据此规定 React 目录结构。

| Concern | Confirmed Convention / Proposed Vue Default | Evidence / Anchor | Adaptation / Open Question |
| --- | --- | --- | --- |
| Page directory | Vue default: `src/pages/<page-name>/` |  |  |
| Page root files | Vue default: keep root files to `App.vue`, `main.ts`, `styles.less` where applicable |  |  |
| Page style ownership | Vue default: page-level rules in `styles.less`, imported by `App.vue`; component-local styles follow project conventions |  |  |
| Page feature organization | Vue default: choose page-local `components/` or a purpose-specific page subdirectory based on responsibility |  |  |
| Page components | Vue default: page-local `components/`; multi-file component gets its own subdirectory |  |  |
| Page assets | Vue default: page-local `assets/`, optionally grouped by type |  |  |

### Pages, Overlays And States

| Page / Module | State / Overlay | Entry Condition | Exit / Transition | Requirement Type | Source / Anchor |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  | 正式设计 / 原型演示 / 演示数据 / 待接入 |  |

### State Transition Diagram

```text
State A --event--> State B --event--> State C
```

### Version Differences And Conflicts

| Conflict ID | Sources | Difference | Production Impact | Decision Required | Status |
| --- | --- | --- | --- | --- | --- |
| DC-001 |  |  |  |  | `Pending` / `Resolved` / `Blocked` |

## Static Visual Specification

### Structure Contract

记录页面语义结构、内容顺序、控件角色、关键属性、动态节点、浮层及状态节点。不能只用截图证明结构。

| ID | State | Semantic Structure / Content Order | Control Role / Key Attributes | Dynamic / Overlay Nodes | Source Anchor | Full-page DOM Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ST-001 |  |  |  |  |  |  | `PASS` / `PARTIAL` / `NOT_RUN` / `BLOCKED` |

### Structure And Layout

| Area | Structure / Grid / Width / Position / Overflow | Source / Anchor |
| --- | --- | --- |
|  |  |  |

### Design Tokens

| Token Type | Value / Rule | Scope | Source / Anchor |
| --- | --- | --- | --- |
| Color / Font / Size / Weight / Line Height / Spacing / Radius / Border / Shadow / Z-index |  |  |  |

### Style Contract

Style Contract 覆盖 Design Token、布局几何、computed style、断点、伪类、层级、overflow、transform 和动画规则；记录受影响元素而非只测触发控件。

| ID | Viewport / State / Pseudo-class | Affected Selector | Token / Layout / Overflow / Transform / Stacking / Animation | Computed Style | Bounding Box | Source Anchor | Runtime Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SC-001 |  |  |  |  |  |  |  | `PASS` / `PARTIAL` / `NOT_RUN` / `BLOCKED` |

### Units, Breakpoints And Scaling

| Viewport / Device | Unit | Breakpoint / Continuous Rule | Synchronized Changes | Fallback | Source / Anchor |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### Asset Inventory

此处的素材与下方响应式规律关联，记录资源切换及裁切变化。

| Asset | Purpose | Intrinsic / Display Size | Ratio / Transparent Area | Crop / Compression | References | Suggested Location | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

## Source-driven Responsive Behavior Discovery

从源码和原型实际表现先发现规律，再生成验证宽度。纯 CSS、无显式断点和固定布局也必须运行；不得预填常见设备宽度或把自定区间视为支持范围。

- 探索起点与依据（源码约束 / 用户明确范围）：
- 实际探索范围、连续调宽与变化区间加密探测记录：
- 原型运行环境 / viewport 配置 / 控制变量：
- 未确认或未覆盖范围及 Open Question：

### Responsive Rule Register

| Rule ID / Area | Trigger: Viewport / Container / Content | Fixed / Continuous Rule / Transition Condition | Source Anchor | Observed Range / Sampling Rationale / Measurements | DOM Delta | CSS Visibility / Visual Order / Geometry Delta | Runtime Evidence | Unknowns / Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RR-001 |  |  |  |  |  |  |  | `PASS` / `PARTIAL` / `NOT_RUN` / `BLOCKED` |

区分实际 DOM 重排与仅 CSS 视觉顺序变化；固定布局/窄屏溢出也按来源记录，不自行补造适配。

### Responsive State Matrix

| Case ID / Rule ID | Width / Container / Content Conditions | Selection Rationale: Representative / Boundary Side / Unused In Tuning | Fresh Load / Wide→Narrow→Wide Sequence | State / Interaction / Dependency Graph IDs | Full-page DOM / Mutation Evidence | Computed Style / Bounding Box Evidence | State Retention / Recovery / Overflow / Focus / ARIA | Console / Screenshot Evidence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RS-001 / RR-001 |  |  |  |  |  |  |  |  | `PASS` / `PARTIAL` / `NOT_RUN` / `BLOCKED` |

首次加载与连续切换分别验证；无 DOM Mutation 也记录证据。取点依据来自规律，覆盖代表点、转换边界两侧和未用于调试的宽度。关联全部必要页面状态/交互路径；目标回放相同条件，未确认范围不宣称通过。

## Interaction And Animation Specification

只检查当前页面范围内实际存在的交互与动画，不预设页面必须包含某种业务模块。按需覆盖：输入与触发、状态与反馈、显示与层级、导航与位置、直接操作、时间行为、数据与异常、环境适配、可访问性与降级。

### Behavior Contract：交互联动表

| ID | Source Control | Trigger | Preconditions | Shared State Mutation | Direct Target | Indirect Affected Regions | DOM Delta | Style Delta | Focus/ARIA | Recovery | Source Anchor | Runtime Evidence |
| -- | -------------- | ------- | ------------- | --------------------- | ------------- | ------------------------- | --------- | ----------- | ---------- | -------- | ------------- | ---------------- |
| IN-001 |  |  |  |  |  |  |  |  |  |  |  |  |

### 状态、动画与生产验收补充

| Interaction ID | Initial State | Intermediate State | End State / Observable Wait Condition | Timing / Order | Interrupt / Repeat | Environment Difference | Accessibility / Fallback | Prototype Mechanism | Production Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IN-001 |  |  |  |  |  |  |  |  | `Required` / `Recommended` / `Exclude` / `Pending` |

### Interaction State Graph

```text
IN-001：初始状态 --触发事件/前置条件--> 中间状态 --可观察条件--> 最终状态 --恢复操作--> 初始状态
```

### Cross-control Dependency Graph

```text
触发控件 -> 共享状态写入 -> 选择器依赖/状态读取 -> 直接目标 -> 间接受影响区域/浮层/后续操作
                                                     -> 异步回调 -> 后续控件状态
```

每条边注明交互 ID、来源锚点和运行证据；追踪 Tab、focus、Checkbox、hover、异步共享状态等实际存在的联动，不要求页面存在所有示例。

### Runtime Evidence Register

- 原型启动命令 / URL / 浏览器环境：
- JavaScript / 交互伪类 / 动态 DOM 发现结果与来源：
- 原型可运行性与限制：
- 运行审计适用性、不能执行/解释的路径与 Open Question：

| Interaction ID | Phase | Viewport / Input / State | Full-page DOM Snapshot | Mutation | Affected Elements Computed Style / Bounding Box | document.activeElement / ARIA | Console Errors | Screenshot / Recording | Observable Condition | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IN-001 | Before / Intermediate / After / Recovery / Repeat |  |  |  |  |  |  |  |  | `PASS` / `PARTIAL` / `NOT_RUN` / `BLOCKED` |

事件前开始记录 Mutation；无变化也需证据。等待可观察状态，不用固定等待替代。原型不能运行时不得静态猜测完整行为，关键行为未知为 `BLOCKED`，非关键缺失为 `PARTIAL`。无 DOM、computed style 和状态转换证据的交互不能为 `PASS`。

## Visual Baseline

| Baseline ID | Page / Viewport / Device / Input | State / Interaction ID | Screenshot / Recording | Related Structure / Style / Behavior Evidence | Status |
| --- | --- | --- | --- | --- | --- |
| VB-001 |  |  |  |  | `PASS` / `PARTIAL` / `NOT_RUN` / `BLOCKED` |

截图/录屏仅补充 Structure、Style、Behavior，不能替代它们。目标实现必须回放相同路径，四类必要证据均通过后才可判页面还原 `PASS`；审计通过本身不代表目标完成。

不存在或与页面无关的行为无需为了满足清单而补齐，也不要求逐项写 `Not Applicable`；实际存在的行为必须完成源码检查和来源锚定。

## Engineering Inventory And Project Mapping

### Modules And Components

| Delivery Module | Existing Project Entry / Component / Adapter / Store / Theme | Decision | Reason | Production Notes |
| --- | --- | --- | --- | --- |
|  |  | `Reuse` / `Adapt` / `Add` |  |  |

### Target Project Build And Asset Contract

| Concern | Confirmed Rule | Target Project Source / Anchor | Production Application | Unknown / Risk |
| --- | --- | --- | --- | --- |
| Framework / Language |  |  |  |  |
| Styling / Component Convention |  |  |  |  |
| SVG Resolution: URL / Component / Sprite / Other |  |  |  |  |
| Image / Font Aliases, Loaders, Plugins |  |  |  |  |
| Resource Destination / Build Constraints |  |  |  |  |

### Prototype Technology Decisions

| Prototype Mechanism / Data | Decision | Production Replacement / Constraint | Reason | Owner |
| --- | --- | --- | --- | --- |
|  | `Keep` / `Adapt` / `Replace` / `Exclude` / `Pending` |  |  |  |

静态 HTML、GSAP、直接 DOM 操作、演示数据和原型依赖不得默认标记为 `Keep`。

## Risks And Open Questions

| ID | Risk / Question | Evidence | Impact | Owner | Decision Needed | Blocking Stage | Recovery Condition | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DQ-001 |  |  |  |  |  | `Understand` / `Plan` / `Execute` / `Verify` |  | `Open` / `Resolved` / `Accepted Risk` |

至少检查设备与系统范围、字体 fallback、不同输入方式、接口与鉴权、导航、内容或远程配置、动画性能、低版本降级、资源体积、重复资源、无障碍和焦点管理。

## Implementation Readiness

| Stage | Audit-derived Input | Expected Output | Acceptance Anchor | Applicable |
| --- | --- | --- | --- | --- |
| 1. 交付包审计与未知项确认 |  |  |  | `Yes` / `No` |
| 2. Design Token、单位、断点和素材规则 |  |  |  |  |
| 3. 项目架构及状态模型 |  |  |  |  |
| 4. 基础页面骨架 |  |  |  |  |
| 5. 一个代表性样板状态 |  |  |  |  |
| 6. 公共组件 |  |  |  |  |
| 7. 其他静态状态 |  |  |  |  |
| 8. 交互和动画 |  |  |  |  |
| 9. 真实接口与生产配置 |  |  |  |  |
| 10. 响应式、真实设备和低版本兼容 |  |  |  |  |
| 11. 截图、录屏和完整回归 |  |  |  |  |

不适用阶段必须说明理由。此处只记录审计约束，具体文件、任务和实现顺序由 `plan.md` 决定。

## Separated Conclusions

### 已确认事实

-

### 从源码推导的设计意图

-

### 原型实现方式

-

### 建议的生产实现方式

-

### 待确认问题

-

## Audit Gate Checklist

- [ ] 已记录页面级还原范围、`source_eligible`、`Audit Decision: Triggered` 和 `package_fingerprint`。
- [ ] 已逐类读取全部适用来源，并记录实际提取结果。
- [ ] 已梳理页面、浮层、状态和转换关系。
- [ ] 主要视觉、响应式、素材、交互和动画规格均有来源锚点。
- [ ] 已从源码和原型表现发现适配规律并建立 Rule Register/Responsive State Matrix，未用固定设备宽度替代探索。
- [ ] 已区分 DOM/CSS 变化及视口/容器/内容触发，覆盖首次加载、连续切换、边界两侧和未用于调试的宽度，未知范围明确。
- [ ] 已分别建立 Structure、Style、Behavior、Cross-control Dependency Graph 与 Visual Baseline。
- [ ] 适用交互已按 Interaction State Graph 实际运行，直接和间接受影响区域有前/中/后证据。
- [ ] 无法执行/解释的交互已记入 Open Question，关键行为未知时不通过 Gate。
- [ ] 已区分正式要求、设计意图、原型机制、演示数据和待接入内容。
- [ ] 已登记版本差异与冲突，关键冲突已获人工决定。
- [ ] 已完成目标项目 `Reuse / Adapt / Add` 映射。
- [ ] 已记录目标项目资源解析规则及证据锚点，未确认项未被当作事实。
- [ ] 已识别风险、未知项和生产验收建议。
- [ ] 审计期间未修改业务代码。

## Handoff Decision

- Ready for Understand Gate: `Yes` / `No`
- Blocking items:
- `task.md` facts / risks / AC updated:
- Next action:
