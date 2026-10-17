# Personal Workflow 改进说明

对比基线：`main@e07a3e2b7b4dda7caa765efe0d97f8d7144f6e00`（首版）。本次整理日期：2026-10-17。

本次同步可安装的核心包、README 和本说明。个人研究、项目经历、活动任务、历史归档和本机知识库正文不在公开范围。条目描述仓库规则与模板的能力；实际项目仍需保留对应执行证据。

## 主要改进

| 问题或限制 | 本次行为 | 可核验来源 |
| --- | --- | --- |
| 阶段需要人工反复提示 | 全局入口自动恢复状态、分流并加载阶段 Skill | [SKILL.md](SKILL.md) |
| 理解不足即可开始实现 | Understand Gate 只有 Passed 才能进入 Plan/Execute | [Workflow](.workflow/WORKFLOW.md)、[task](.workflow/templates/task.md) |
| 计划存在但未获确认 | 所有正式计划在执行前经过人工 Plan Gate | [Workflow](.workflow/WORKFLOW.md)、[state](.workflow/templates/state.md) |
| 声称用了 Skill 却无记录 | 配置/真实路径、时间、Attempted、Result、Evidence、Usage；历史只追加 | [task](.workflow/templates/task.md) |
| 计划、实现与验证无法对应 | 使用稳定 AC ID，验证记录方法、实际结果、证据与状态 | [plan](.workflow/templates/plan.md)、[verification](.workflow/templates/verification.md) |
| Review 与运行验证混淆 | 独立 review.md 与三种审查状态，不替代 Verify | [review](.workflow/templates/review.md) |
| 阻塞后上下文丢失 | Recovery Snapshot、回退矩阵、追加重试记录 | [Workflow](.workflow/WORKFLOW.md)、[state](.workflow/templates/state.md) |
| Feedback 流于总结或直接改规则 | 每任务必有反馈，候选分类型并接受人工审核；Rule Change 走独立任务 | [feedback](.workflow/templates/feedback.md) |
| 历史经验压过当前事实 | 受控召回最多三篇，记录适用性及具体影响，知识库路径由项目配置 | [Workflow](.workflow/WORKFLOW.md) |
| 仅凭文件类型扩大任务 | 页面级还原与源码资格分别判断；局部任务不额外审计 | [审计 Skill](skills/design-delivery-audit/SKILL.md)、[检测器](skills/design-delivery-audit/scripts/detect_delivery_package.py) |
| 页面还原只看截图 | Source-backed Reconstruction Evidence Contract：Structure、Style、Behavior、依赖图、Visual Baseline 分别留证 | [Workflow](.workflow/WORKFLOW.md)、[审计模板](.workflow/templates/design-delivery-audit.md) |
| 只验证触发控件，遗漏其他区域 | 强制运行态七步审计、Interaction State Graph、Cross-control Dependency Graph 与 13 列联动表 | [Skill 正文](skills/design-delivery-audit/SKILL.md)、[规范](skills/design-delivery-audit/references/audit-spec.md) |
| 原型与目标走了不同路径 | 相同路径/视口/初态回放；四类必要证据全通过才可还原 PASS | [验证模板](.workflow/templates/verification.md) |
| 用户必须重复输入完整还原要求 | HTML/CSS/JS 齐全且要求完整页面还原时自动补全 Effective Reconstruction Prompt | [Workflow](.workflow/WORKFLOW.md)、[入口](SKILL.md) |
| 生成的过程文件进入业务版本管理 | 首次生成 .workflow 时处理已有 .gitignore；无文件则跳过、不新建 | [入口](SKILL.md)、[任务初始化记录](.workflow/templates/task.md) |
| 产物语言与分发范围不明确 | 中文为主，固定标识保留；分发资源与用户活动材料分开 | [Workflow](.workflow/WORKFLOW.md)、[README](README.md) |

## 使用者可以观察到什么

输入一次研发目标后，Agent 应先恢复/创建任务，在 `task.md` 给出事实、未知项、AC 和 Skill 记录；Medium 计划展示后暂停。执行后 Review、Verify 与 Feedback 各自形成产物，最终完成门需要新的验证证据。运行态原型缺失时不能用静态推断补齐行为结论。

页面还原审计结果为 PASS，只代表基线审计已完成；目标实现还需四类证据验证。用户接受剩余风险不把缺失的证据改写为 PASS。新增的自动提示词规则不会将局部组件修改扩大为完整页面。

## 验证与交付边界

检测器的单元测试、Skill validator、原文契约比对、Markdown 链接与分发文件检查用于验证本次核心包；Git 忽略协议另以临时仓库的真实匹配结果核对。具体执行结果保存在本次任务证据中，不把仓库测试宣传为业务页面 E2E 通过。

本次未新增通用浏览器采集器或后台调度服务。首次忽略规则由 Agent 在初始化时执行；.gitignore 不取消既有 Git 跟踪。用户项目自己的 .workflow 可忽略，分发包中的 Workflow 与模板仍保留供安装使用。
