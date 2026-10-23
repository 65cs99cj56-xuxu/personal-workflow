# Design Delivery Audit Specification

审计必须覆盖本文件的适用项目。某项不适用时写明 `Not Applicable` 和理由，不得静默删除。

## 1. Source Coverage

逐类列出文件、读取状态、提取结果和问题：

- README、验证记录、版本说明和其他文档。
- 全部 HTML 页面、变体和状态文件。
- 全部 CSS 及预处理器源码，包括主题、响应式、动画和降级规则。
- 全部 JavaScript/TypeScript，包括交互、状态切换、滚动、轮播和动画逻辑。
- 参考截图及其对应页面、视口和状态。
- 图片、SVG、字体、视频和其他素材。
- 页面生成脚本、构建配置、资源映射和校验文件。

状态使用 `PASS / PARTIAL / NOT_RUN / BLOCKED`。文件存在但未读取内容不能标记 `PASS`。

## 1.1 Target Project Organization

调查目标项目的框架、路由和实际目录约定。对 Vue 页面还原，记录单页目录、页面根文件、页面级样式归属、功能/组件、多文件组件和图片/视频素材的落点，并引用现有页面、路由或构建配置证据。项目没有相应约定时，默认建议为 `src/pages/<page-name>/`，根部尽量只保留 `App.vue`、`main.ts`、`styles.less`；页面级样式集中写入 `styles.less` 并由 `App.vue` 导入，默认不在 `App.vue` 的 `<style>` 中维护页面级样式；组件局部样式按组件职责组织。其他内容按职责放入 `components/` 或页面下职责明确的功能子目录。多文件组件在 `components/` 下建立组件级子目录，页面专属素材放入 `assets/`。三个根级文件是建议的默认形态，不要求每页必须齐全，也不排斥有理由的其他根级文件。已有项目约定优先，冲突时适配项目并说明理由。该默认建议仅针对 Vue，React 标记为 `Not Applicable`，不推导 React 的目录组织方式。

## 2. Delivery Scope

- 设计基准尺寸、目标设备、浏览器、操作系统和 WebView 范围。
- 全部页面、弹窗、抽屉、菜单、Toast、遮罩、浮层和业务状态。
- 每个状态的进入条件、退出方式和转换事件。
- 正式设计要求、原型演示行为、演示数据、占位配置和研发待接入内容。
- 包内版本差异、过时说明、废弃页面和冲突规则。

产出页面/状态矩阵和文本状态转换图。

## 3. Static Visual Specification

- 页面结构、布局、栅格、最大宽度、内容区域和安全区。
- 颜色、字体、字号、字重、行高、间距、圆角、边框、阴影和层级。
- PC、Pad 及其他视口的单位、断点、容器规则和连续缩放方式。
- 字体或容器变化时，文字、图标、间距和素材的联动规则。
- 定位参照、stacking context、遮罩范围、裁切、滚动和 overflow。
- 素材用途、显示尺寸、宽高比、透明区域、`object-fit`、裁切和压缩要求。

至少形成：Token 表、单位/断点表、素材表和视觉基线表。

### Source-driven Responsive Behavior Discovery

所有页面级审计都执行 Skill 正文同名章节，包括纯 CSS、没有显式断点和固定布局页面。先从源码及原型连续尺寸变化发现规律，再生成验证宽度；设备预设或工具默认宽度不得代替发现过程，也不得自行限制支持范围。

形成 Responsive Rule Register，按规则记录：ID、影响区域、触发依据（视口/容器/内容）、固定量/连续关系/转换条件、源码锚点、观测范围和采样理由、实测值、DOM Delta、CSS 视觉变化、运行证据、未知或未覆盖范围。静态声明是发现线索，仍需运行确认；流式布局和内容换行不依赖显式媒体查询。

形成 Responsive State Matrix，按规则 ID 关联首次加载、宽→窄→宽、页面状态和交互路径。代表点、边界两侧与未用于调试的宽度均从发现的规律派生，不预填固定数值。容器查询记录实际容器尺寸；内容触发记录原型内容及其加载条件；控制其他变量以识别原因。

记录不同宽度下 DOM 新增/删除/替换/重排/属性变化，以及 DOM 不变时的 CSS 显隐、视觉顺序、几何/overflow 变化。没有变化也保留证据。采集全页面 DOM、Mutation、computed style、bounding box、焦点/ARIA、Console 和截图；首次加载与运行中切换分别检查状态保留、恢复和跨控件影响，引用两类状态/依赖图。

目标页面在相同宽度、容器/内容条件、加载方式、尺寸序列、输入和状态路径下回放，比较规律及转换条件，不只比较取样点截图。固定布局/溢出按原型事实记录，新增适配属于生产决策。关键行为不明为 `BLOCKED`，非关键未覆盖为 `PARTIAL`；未确认范围不得外推为已支持任意宽度。

### Source-backed Reconstruction Evidence Contract

交付包源码及原型实际运行行为为事实来源，按以下五类分别登记来源锚点、运行证据与状态：

| 契约 | 必须提取的内容 | 证据要求 |
| --- | --- | --- |
| Structure Contract | 页面语义结构、内容顺序、控件角色、关键属性、动态节点、浮层及状态节点 | HTML/JS 来源锚点及各适用状态的全页面 DOM snapshot |
| Style Contract | Design Token、布局几何、computed style、断点、伪类、层级、overflow、transform、动画规则 | 选择器/Token 锚点、受影响元素 computed style 与 bounding box |
| Behavior Contract | 触发事件、前置/中间/最终状态、DOM mutation、焦点、ARIA、恢复及重复操作 | 状态转换与原型实际路径的前/中/后状态证据 |
| Cross-control Dependency Graph | 一个控件或共享状态对其他控件、区域、浮层、后续操作的直接/间接及异步影响 | 状态写入与选择器/读取依赖锚点，运行态变化引用 |
| Visual Baseline | 指定视口、设备、输入方式与状态下的截图/录屏 | 仅补充前三类证据，记录视口与状态，不能代替 DOM/style/行为 |

缺失单独的 CSS 或 JavaScript 源不等于该类运行行为不存在。无交互的静态页面需由源码与初始运行证据确认；缺来源的结论仍保留未知。

## 4. Interaction And Animation Specification

只检查当前页面范围内实际存在的交互与动画，不预设页面必须包含某种业务模块。不存在或与页面无关的行为无需为了满足清单而补齐，也不要求逐项写 `Not Applicable`。

按实际行为检查：

- 输入与触发：点击、触摸、Hover、键盘、滚轮、滚动、拖拽、手势、定时器、系统事件和生命周期事件。
- 状态与反馈：默认、中间、选中、展开、禁用、加载、成功、失败、空态和恢复状态之间的转换。
- 显示与层级：显示、隐藏、进出场、遮罩、浮层、焦点进入、焦点约束、焦点归还和关闭行为。
- 导航与位置：页面跳转、路由变化、锚点定位、滚动联动、固定或吸附行为，以及返回后的状态恢复。
- 直接操作：拖动、滑动、缩放、排序、切换、连续输入及其边界反馈。
- 时间行为：自动执行、持续时间、延迟、缓动、执行顺序、暂停、恢复、取消、中断和重复触发。
- 数据与异常：异步加载、提交反馈、失败重试、超时、空数据、部分成功和异常恢复。
- 环境适配：不同视口、输入设备、屏幕方向和运行环境下的行为差异。
- 可访问性与降级：键盘可操作性、焦点可见性、语义反馈、`prefers-reduced-motion`、性能限制和低版本降级。

每项使用交互联动主表，不能只记录触发控件：

| ID | Source Control | Trigger | Preconditions | Shared State Mutation | Direct Target | Indirect Affected Regions | DOM Delta | Style Delta | Focus/ARIA | Recovery | Source Anchor | Runtime Evidence |
| -- | -------------- | ------- | ------------- | --------------------- | ------------- | ------------------------- | --------- | ----------- | ---------- | -------- | ------------- | ---------------- |

按同一 ID 补充 Initial / Intermediate / End State、Timing、Order、Interrupt / Repeat、Environment Difference、Accessibility / Fallback、Prototype Mechanism 和 Production Acceptance，不能因替换主表丢失动画或生产要求。

### Interaction State Graph 与 Cross-control Dependency Graph

先静态发现 Skill 正文列出的 CSS 伪类、兄弟/状态选择器，以及 JS 事件监听、委托、共享状态写入、classList/style/hidden/dataset/aria-* 和 DOM 插入删除/条件渲染。然后沿状态写入、读取和选择器依赖追踪直接及间接受影响区域。

Interaction State Graph 的节点记录页面及控件状态，边记录 Trigger、Preconditions、可观察等待条件和恢复操作。Cross-control Dependency Graph 使用“控件 → 状态写入 → 选择器/状态读取 → 直接目标 → 间接区域/浮层/后续操作”的关系；异步边记录回调或可观察状态条件。两类图共享交互 ID。

例如 Tab 可同时改变内容区、下划线和按钮权限；focus 可联动父容器、提示文字和提交按钮；Checkbox 可控制其他字段出现/禁用；卡片 hover 可改变兄弟节点、浮层和预览区；控件 A 写状态后，控件 B 可在异步回调中变化。按页面实际行为追踪，不补造不存在的模块。

### Runtime Evidence

存在 JavaScript、交互伪类或动态 DOM 时，必须实际运行原始页面，逐条回放状态图中的适用路径。每条路径保存：

- 原型启动命令/URL、浏览器环境、视口、输入方式、数据与初始状态。
- 前、中、后的全页面 DOM snapshot，而非只有点击元素的局部 outerHTML。Shadow DOM/iframe 等若存在需记录采集范围和限制。
- 在事件前开始观察的 Mutation 记录及时间/顺序；无 Mutation 也需实际记录零变化，CSS 伪类可能仅改变样式。
- 全部直接和间接受影响元素的 computed style、bounding box，以及 `document.activeElement`、ARIA 属性与状态。
- Console 错误和对应截图/录屏；文件或记录必须以交互 ID、阶段和视口关联。

延时、动画、异步更新和连续操作等待可观察条件，不以固定 sleep 代替完成判定。无法执行或解释的路径进入 Open Question，记录关键性、阻塞阶段与恢复条件；关键行为未知为 `BLOCKED`，非关键未覆盖为 `PARTIAL`。原型无法运行时不得推断完整行为。截图缺少 DOM、computed style 和状态转换佐证的交互不得为 `PASS`。

目标实现使用相同路径、视口、输入方式和初始状态，分别保存原型/目标证据与差异，引用已确认的 Keep / Adapt / Replace / Exclude 决策。最终只有 Structure、Style、Behavior、Visual 四类必要证据全部通过，页面还原才能判为 `PASS`。

## 5. Asset Inventory

记录素材路径、类型、尺寸、比例、透明区、引用位置、建议目标目录和生产处理建议。检查：

- 缺失引用、未引用资源、重复资源和不同版本同名资源。
- 大图体积、错误格式、压缩机会和响应式资源需求。
- SVG viewBox、字体授权/来源和 fallback。
- 生成脚本是否会覆盖、变换或遗漏资源。

## 6. Project Mapping

先从目标项目入口、配置和现有组件确认框架/语言、样式方案、组件组织约定、公共组件边界及状态管理，再将交付包模块映射到目标项目。对 SVG、字体、图片，核对 alias、loader、plugin 和构建规则，确认其实际作为 URL、组件、sprite 或其他形式解析；不得仅按扩展名推断用法。

将交付包模块映射到目标项目：

| Delivery Module | Existing Entry / Component / Adapter / Store / Theme | Decision | Reason | Production Notes |
| --- | --- | --- | --- | --- |
|  |  | `Reuse` / `Adapt` / `Add` |  |  |

同时形成：

- 页面模块和公共组件清单。
- 目标项目框架、样式、组件约定及资源构建/引用规则的证据清单。
- Design Token 和主题配置清单。
- 页面状态矩阵与转换图。
- 素材清单及建议存放位置。
- 动画与交互清单。
- API adapter、真实配置和演示数据替换清单。

原型机制需单独给出 `Keep / Adapt / Replace / Exclude` 建议，不得默认复制。

## 7. Risks And Open Questions

至少检查：

- 缺失或冲突的设计信息。
- PC、Pad、iPad 和 Android 平板范围。
- 最低系统、浏览器和 WebView 要求。
- 字体来源与 fallback。
- Hover、触摸、鼠标和键盘行为差异。
- 接口、鉴权、导航、内容配置、远程配置和其他生产依赖。
- 动画性能与低版本降级。
- 大图体积、未引用资源和资源重复。
- 无障碍、语义、键盘操作和焦点管理。
- 哪些原型行为需要进入生产。

关键问题写明 Owner、Decision Needed、Blocking Stage 和 Recovery Condition。

## 8. Implementation Readiness

按以下顺序给出阶段约束，每项只描述审计所得的输入、预期产出和验收锚点，具体文件与实现方案交给 `plan.md`：

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

## 9. Separated Conclusions

报告最后必须分开列出：

- 已确认事实（`Confirmed Fact`）。
- 从源码推导的设计意图（`Inferred Intent`）。
- 原型实现方式（`Prototype Mechanism`）。
- 建议的生产实现方式（`Production Recommendation`）。
- 待确认问题（`Open Question`）。

不得把推断、原型机制或生产建议写入“已确认事实”。
