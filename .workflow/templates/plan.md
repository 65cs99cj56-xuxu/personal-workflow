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

### Production Reconstruction Mapping

仅在 `Audit Decision: Triggered` 时填写。使用审计中已确认的项目约定和源码行为；未知项继续列为风险或 Open Question。

| Project Convention / Asset | Confirmed Rule And Evidence | Production Use / Migration | Related AC |
| --- | --- | --- | --- |
| Framework / Style / Component Convention |  |  | `AC-xx` |
| Vue Page Directory / Components / Assets (Vue only; otherwise `Not Applicable`) |  |  | `AC-xx` |
| SVG / Image / Font Resolution And Destination |  |  | `AC-xx` |

Vue 页面还原的默认目录映射为 `src/pages/<page-name>/`，页面目录根部尽量只保留 `App.vue`、`main.ts`、`styles.less`。页面级样式集中写入 `styles.less` 并由 `App.vue` 导入，不在 `App.vue` 的 `<style>` 中维护页面级样式；组件局部样式可按项目规范留在组件内。其他内容按职责和复杂度选择放入页面 `components/`，或在页面目录下建立有明确职责的功能子目录；多文件组件在 `components/` 下建立组件子目录，图片/视频等页面素材放在 `assets/`。这三个根级文件是推荐形态，不是每个页面都必须有，也不排斥有理由的其他根级文件。先按目标项目已确认的目录和构建约定映射；只有项目没有相应约定时才采用此默认值。此规则不适用于 React。记录本次实际目录方案及其配置/代码证据：

```text
src/pages/<page-name>/
├── App.vue
├── main.ts
├── styles.less
├── components/
│   ├── <single-file-component>
│   └── <multi-file-component>/
├── <feature-module>/  # 仅在职责需要时新增
└── assets/
    ├── images/
    └── videos/
```

| Source / Anchor | Confirmed Semantic Structure / Behavior | Production Component Responsibility | State / Derived State / Action / Props / Events | Decision | Related AC |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  | `Keep` / `Adapt` / `Replace` / `Exclude` | `AC-xx` |

| Geometry-dependent Element | Positioning Reference / Verified Constraint | Production Positioning Strategy | States / Widths To Verify | Related AC |
| --- | --- | --- | --- | --- |
|  |  |  |  | `AC-xx` |

- Static-page interaction result: `Present` / `None confirmed` / `Unknown`; evidence or reason:
- Component boundaries follow responsibilities and reuse; they are not a one-to-one split of source DOM and do not collapse the whole page into a monolith without reason. Keep style ownership clear and avoid putting the whole page's styles in one file. Component count, naming, and style organization follow the target project.

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
