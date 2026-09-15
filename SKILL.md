---
name: personal-ai-workflow
description: Use when the user asks to use the personal AI software R&D workflow, automate Understand Plan Execute Review Verify Feedback, or resume a paused development task
---

# Personal AI Software R&D Workflow

## Core Principle

This is the global orchestration entry for personal frontend, backend, and full-stack development. The user should describe the development goal once; do not ask them to repeat the phase prompts or choose Skills already defined below.

## Startup

When this Skill is selected:

1. Identify the current software project from the active working directory.
2. Read the project's `.workflow/current-task.md` if it exists. If it points to an unfinished task, resume it.
3. If there is no unfinished task, create `.workflow/tasks/YYYY-MM-DD-<short-name>/task.md` from the bundled task template or the project's existing template.
4. Read `.workflow/WORKFLOW.md` from the project when present; otherwise use the bundled workflow specification and bootstrap the project's `.workflow/` directory.
5. Classify the task as `Small`, `Medium`, `Large`, or `High Risk`, then follow only the corresponding path.

## Skill Routing

Load and follow the relevant Skill at the start of each phase:

| Phase | Required Skill |
| --- | --- |
| Understand | `sk-codebase-explore` |
| Frontend Plan | `kit-fe-write-plan` |
| Backend Plan | `sy-spec:go-plan` |
| General Review | `code-skill:kit-code-review` |
| Frontend Review | `deer-workflow:deer-code-review` |
| Go Review | `sy-spec:go-code-review` |
| Frontend Verify | `kit-fe-verify` |
| Frontend runtime/browser verification | `build-web-apps:frontend-testing-debugging` |
| Backend Verify | `kit-backend-feature-verify` |
| Final completion gate | `superpowers:verification-before-completion` |

`Feedback` is a mandatory built-in phase. It does not depend on a separate Skill and must generate `feedback.md` after verification, including when the task is partial, failed, or blocked.

If a required Skill is unavailable, record `BLOCKED` or `NOT_RUN`, explain the missing capability, and pause. Never claim that a Skill ran when it did not.

## Automatic Phase Loop

For each phase, use the previous artifact as input, perform the phase, write its output, update `.workflow/current-task.md`, and route to the next phase. The artifacts are:

```text
task.md -> plan.md -> implementation -> review result -> verification.md -> feedback.md
```

Keep facts, assumptions, unknowns, decisions, evidence, and remaining risks distinct. If implementation changes the API, data model, state, scope, or verification strategy, update the plan before continuing.

## Pause and Resume

Pause automatically when a human decision is required, a critical unknown remains, a Large / High Risk Gate is reached, the implementation exceeds scope, or verification is blocked. Before pausing, record the current stage, completed work, pause reason, required decision, and next action in both the task metadata and `.workflow/current-task.md`.

When the user says `继续当前任务`, reads a saved decision, or reports that a blocker is resolved, read the state and all task artifacts, then continue from the recorded stage. If the code no longer matches the recorded facts, return to Understand before changing code.

## Completion Contract

Do not report completion until the necessary verification items are `PASS` or the user explicitly accepts the remaining risk, the final completion gate has run, and `feedback.md` is complete. Use only `PASS`, `PARTIAL`, `NOT_RUN`, and `BLOCKED` for verification status.

After completion, archive `task.md`, `plan.md`, `verification.md`, and `feedback.md` under `.workflow/archive/`. Improvement candidates require human review before changing the Workflow, a project rule, a Skill, or the knowledge store.
