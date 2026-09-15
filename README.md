# Personal Workflow

个人 AI 软件研发 Workflow，面向前端、后端和全栈开发。

## 目标

安装一次后，在任意 Codex 对话中用一句话启动研发任务：

```text
使用 personal-ai-workflow 实现用户登录功能。
```

Workflow 会自动判断任务复杂度、调用对应 Skill、创建任务上下文，在人工决策点暂停，并通过状态文件恢复。`Feedback` 是每个任务的必经阶段。

## 安装

将本仓库作为 Codex 全局 Skill 安装到 `~/.codex/skills/personal-ai-workflow/`，使 `SKILL.md` 位于该目录根部。安装后新开 Codex 对话即可使用 `personal-ai-workflow`。

项目不需要预先配置 `AGENTS.md`。第一次执行任务时，Skill 会在当前项目中自动创建：

```text
.workflow/
├── current-task.md
├── tasks/
└── archive/
```

## 内容

- `SKILL.md`：全局入口和自动阶段路由。
- `.workflow/WORKFLOW.md`：流程、Gate、回退、验证和反馈规范。
- `.workflow/templates/`：任务、计划、状态、验证和反馈模板。

## 设计边界

这是 Agent 驱动的轻量编排，不是后台调度服务。Skill 可以根据规则加载其他 Skill，但跨会话恢复仍需要用户发送 `继续当前任务`。Workflow 不会自动修改自身规则，也不会自动提交代码。
