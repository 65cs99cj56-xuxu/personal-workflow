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
3. Read `.workflow/WORKFLOW.md` from the project when present; otherwise use the bundled workflow specification and bootstrap the project's `.workflow/` directory before creating task artifacts.
   Before any step first creates `.workflow/`, record whether it already exists. On first creation, immediately update the project's existing `.gitignore` file to effectively ignore `.workflow/`, before writing task artifacts. Preserve its contents and line endings; skip duplicate rules only after checking actual matching rules including later negations. In Git projects use `git check-ignore --no-index` for the directory and representative nested paths. If no `.gitignore` file exists, record `Skipped — No .gitignore` without creating one. Do not write to a directory named `.gitignore`, repeat completed bootstrap on resume, or automatically untrack files. Record `Added`, `Already Ignored`, a skip reason, or `BLOCKED` on write failure. Resume any previously `Pending` or `BLOCKED` ignore setup before proceeding. The bundled Workflow/templates are distribution resources and remain in the install package.
4. If there is no unfinished task, create `.workflow/tasks/YYYY-MM-DD-<short-name>/task.md` from the bundled task template or the project's existing template, then persist the bootstrap result there.
5. Classify the task as `Small`, `Medium`, `Large`, or `High Risk`, then follow only the corresponding path. Any task that produces a formal `plan.md` must pause at the Plan Gate for explicit human confirmation before Execute; Small tasks may skip the formal Plan and this Gate.
6. Before reading a routed Skill, use a readability check and real-path resolution that follow symlinks, such as `test -r` and `realpath` or their equivalents. Do not declare a Skill missing solely from a search that does not follow symlinks. Record both paths, attempt time, result, evidence, and later usage in `task.md`; preserve prior rows and append retries or recovery runs.
7. Use Design Delivery Audit only when the user's task is reconstruction of at least one complete page or view from the corresponding delivery attachment. Feature-level implementation or reconstruction, local comparison or modification, and page-level work that is not reconstruction continue through the ordinary Workflow without this extra audit. Only after confirming page-level reconstruction, resolve the bundled `skills/design-delivery-audit/SKILL.md` relative to this Skill and run its detector. `HTML && (CSS || JavaScript)` is a source-eligibility requirement, not the final routing decision. If scope is unclear, ask before triggering the audit.
8. When page-level reconstruction is requested and readable HTML, standalone CSS **and** standalone JavaScript are all present in the corresponding attachment, automatically expand the request with the exact Effective Reconstruction Prompt in the Workflow's “页面还原请求自动补全” section. Preserve the Raw User Request, source matches, and effective prompt in `task.md`, retaining the user's explicit constraints and intended page. Do not ask the user to resend the expanded prompt or broaden feature-only work into page reconstruction. This AND condition for prompt expansion does not replace the audit's OR condition.

## Skill Routing

Load and follow the relevant Skill at the start of each phase:

| Phase | Required Skill |
| --- | --- |
| Understand | `sk-codebase-explore` |
| Understand, eligible page-level reconstruction | bundled `skills/design-delivery-audit/SKILL.md` |
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

## Evidence and Gates

Every selected or required Skill gets one append-only execution row in `task.md` with `Stage`, `Skill`, `Configured Path`, `Resolved Path`, `Attempted At`, `Attempted`, `Result`, `Evidence`, and `Usage`. Use only `PASS`, `PARTIAL`, `NOT_RUN`, or `BLOCKED` for Skill and verification results.

The Understand Gate is persisted in `task.md` and `state.md` with `Pending`, `Passed`, `Needs More Investigation`, or `Blocked`, plus confirmed facts, remaining unknowns, decision, and evidence. Do not route to Plan or Execute until it is `Passed`.

When Design Delivery Audit is triggered, `design-delivery-audit.md` is required. The Gate must first confirm `Reconstruction Intent: Page-level`, a complete-page requested scope, eligible delivery sources, and a reasoned `Audit Decision: Triggered`; it must then confirm source coverage, source anchors, state transitions, visual/interaction/animation specifications, prototype-versus-production separation, target-project mapping, resolved critical conflicts, and a current package fingerprint.

Use the Workflow's Source-backed Reconstruction Evidence Contract: source and actual prototype behavior establish facts. Require separate Structure, Style, Behavior and Visual evidence, an Interaction State Graph, and a Cross-control Dependency Graph. JavaScript, interactive pseudo-classes or dynamic DOM require actual prototype interaction with DOM/style/geometry/focus/ARIA/Mutation/Console captures. Verify by replaying the same paths on prototype and target. All four necessary evidence classes must pass before reconstruction is `PASS`; screenshot similarity cannot override missing evidence. Unknown critical behavior is `BLOCKED`, uncovered non-critical behavior is `PARTIAL`; never infer full runtime behavior from static sources when the prototype cannot run.

All triggered page audits must also run the audit Skill's Source-driven Responsive Behavior Discovery, including CSS-only and fixed layouts. Discover rules from source and actual width changes, distinguish viewport/container/content triggers and DOM/CSS changes, then derive the Responsive Rule Register and Responsive State Matrix. Use rule-derived representative widths, transition boundaries on both sides, and widths not used in tuning; replay fresh loads, wide→narrow→wide transitions and interactions on prototype and target. Do not substitute device presets, arbitrary fixed test ranges or per-width special cases for the observed rules. Preserve unknown coverage and the existing BLOCKED/PARTIAL semantics.

## Plan Gate

After writing `plan.md`, present the selected approach, implementation order, affected scope, verification strategy, risks, and out-of-scope items to the user. For Medium, Large, and High Risk tasks, wait for an explicit confirmation before changing business code. If the user requests changes, update `plan.md` and present the revised plan again. If the user rejects the plan, record the decision and pause.

For an audited delivery package, the plan must consume `design-delivery-audit.md`, decide `Keep / Adapt / Replace / Exclude` for prototype mechanisms, and preserve the Workflow's required 11-stage implementation and verification sequence. Do not treat static HTML, GSAP, direct DOM operations, demo data, or prototype dependencies as the production design by default.

## Automatic Phase Loop

For each phase, use the previous artifact as input, perform the phase, write its output, update `.workflow/current-task.md`, and route to the next phase. The artifacts are:

```text
task.md -> [design-delivery-audit.md] -> plan.md -> implementation -> review.md -> verification.md -> feedback.md
```

Keep facts, assumptions, unknowns, decisions, evidence, and remaining risks distinct. If implementation changes the API, data model, state, scope, or verification strategy, update the plan before continuing.

The bracketed audit artifact is conditional. Before Plan, resume, or Execute, recompute its package fingerprint; if the package changed, return to Understand and append a new audit record.

## Pause and Resume

Pause automatically when a human decision is required, a critical unknown remains, a Plan Gate is reached, the implementation exceeds scope, or verification is blocked. Before pausing, record the current stage, completed work, pause reason, required decision, next action, and Recovery Snapshot in both the task metadata and `.workflow/current-task.md`.

When the user says `继续当前任务`, reads a saved decision, or reports that a blocker is resolved, read the state and all task artifacts, then continue from the recorded stage. If the code no longer matches the recorded facts, return to Understand before changing code.

## Completion Contract

Do not report completion until the necessary verification items are `PASS` or the user explicitly accepts the remaining risk, the applicable Review stage has produced `review.md` with an allowed Review Status, the final completion gate has run, and `feedback.md` is complete. Small tasks that use the shortened path may skip Review and therefore do not require `review.md`. Use only `PASS`, `PARTIAL`, `NOT_RUN`, and `BLOCKED` for verification status. `NOT_RUN`, `PARTIAL`, and `BLOCKED` require recovery actions and cannot silently become `PASS`.

After completion, archive `task.md`, `plan.md`, `verification.md`, and `feedback.md`, plus `review.md` when the Review stage was applicable and `design-delivery-audit.md` when its audit was triggered, under `.workflow/archive/`. Improvement candidates require human review before changing the Workflow, a project rule, a Skill, or the knowledge store.
