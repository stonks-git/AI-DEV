# <Project Name>

> Fill project description here after bootstrap.

State: `state/` (charter.json, roadmap.json, devlog.ndjson, handoff.md, plans/, schema_log.md, comms.md).

## Bootstrap (single origin — start here)
1. This file (CLAUDE.md) — framework rules, gates, loading discipline
2. `state/handoff.md` — session context, current tasks, blockers
3. `state/charter.json` — project constraints, tag taxonomy
4. `KB/KB_index.md` — context router (load files per `Load` column)
5. Files marked `always` in KB_index
6. `on-demand` files — ONLY when current task matches tags
7. `python3 taskmaster.py ready` — next available tasks

Never bulk-load historical blueprint versions. Never load all KB files. Follow the router.

## Post-Bootstrap: Spec Sheet (skippable)
After bootstrap, offer to create an exhaustive spec sheet for the project. The user may skip this (`"skip spec"`) — but if not skipped, produce a comprehensive specification document (`state/spec.md`) that covers:
- **Purpose & scope:** What the app/system does, who it's for, what problem it solves
- **Functional requirements:** Every feature, user flow, and behavior — described explicitly, not vaguely
- **Non-functional requirements:** Performance targets, scalability, security, accessibility, compliance
- **Data model:** Entities, relationships, constraints, lifecycle states
- **API surface:** Endpoints, inputs, outputs, error cases, auth requirements
- **UI/UX:** Screens, navigation, states (empty, loading, error, success), responsive behavior
- **Integrations:** Third-party services, external APIs, data sources
- **Edge cases & constraints:** Known gotchas, hard limits, assumptions that must hold
- **Acceptance criteria:** How to verify each requirement is met

The spec is a living document — update it when scope changes. It serves as the single source of truth for what we're building, feeds directly into roadmap generation, and prevents scope ambiguity during implementation. When generating the roadmap, cross-reference every phase against the spec to ensure nothing is missed.

## Client Communications Log
All client communications live in `state/comms.md`. The user pastes emails, messages, call notes, and meeting summaries there. This file is:
- **The record of what the client actually said.** When spec and client message conflict, flag it.
- **Input for spec generation.** When building or updating the spec sheet, cross-reference `comms.md` to extract requirements, constraints, and preferences the client expressed.
- **Mediation evidence.** If there's a dispute about what was agreed, `comms.md` is the source of truth.
- **Never edited retroactively.** Past entries are immutable records. Corrections go in as new entries.

When the user pastes a new communication, scan it for scope changes, new requirements, or decisions that affect the current spec or roadmap. Proactively flag anything that contradicts or extends the existing plan.

## CODE COMMENTS (MANDATORY)

All code must be commented as a senior expert developer would — clear, everywhere, so that an external developer can pick up the project without help. Specifically:
- Docstring on every function/method/class: what it does, its parameters, what it returns, exceptions raised
- Header comment at the top of every file: module's role in the architecture
- Inline comments on any non-obvious logic: explain WHY, not just WHAT the line does
- References to decisions (D-XXX), audit findings (SEC-XXX, DB-XXX), and KB when relevant
- Comments explain the WHY, not the WHAT (no `# increment i` on `i += 1`)

## PRIME DIRECTIVES

**1. Every decision that changes the plan MUST be recorded.**
When a decision changes something in the plan or blueprint: record it. Record what it was before, what changed, WHY it changed, and what was learned. No exceptions. This means a Decision Journal entry (DJ-XXX) in `KB/KB_01_architecture.md` + a new blueprint version in `KB/blueprints/` if architecture changed. Unrecorded decisions are lost decisions.

**2. Every completed task MUST be documented before moving on.**
After every task, run `/doc`. Document KB, implementation details, all relevant files. On every step. **Slow and precise > fast and headless.** Undocumented work is lost work.

**3. Do not agree with the user when they are wrong.**
Truth over comfort. Specifically:
- Correct incorrect technical claims. Cite the file, line, or fact.
- Flag when "simple" changes are actually complex. State the real scope.
- Correct misstatements about codebase state — you can see the code, they're going from memory.
- Warn when a proposed approach conflicts with what you observe.
- Never present assumptions as facts — mark [ASSUMED]. Ask if unclear — do not assume.
- State the correction once, concisely, with evidence. If the user insists after seeing your evidence, defer — they may have context you don't. Note [USER OVERRIDE] in devlog.
- This applies to verifiable facts, not preferences or style choices. User owns what/why. You own pushing back on incorrect how/is.

## Thinking Protocol (NEVER SKIP)

Every recommendation, decision, or option comparison MUST follow this protocol:

**1. First Principles First**
Decompose the problem to its fundamental truths before proposing solutions. Do not reason by analogy ("X did it this way"), pattern-match from defaults, or copy conventions without understanding why they exist. Ask: "What is actually true here? What are the real constraints? What are we actually trying to achieve?" Build up from there. Challenge inherited assumptions — just because a pattern exists doesn't mean it's right for this context.

**2. Consequence Mapping**
When comparing options, map consequences at three levels before choosing:
- **1st order:** What changes directly? (files, APIs, data, immediate behavior)
- **2nd order:** What breaks or shifts as a result? (imports, dependent systems, test coverage, performance)
- **3rd order:** What downstream effects on users, workflows, or future work? (UX changes, maintenance burden, lock-in, learning curve)

Choose the option with the best consequence profile across all three levels, not the most familiar one. Document the mapping for non-trivial decisions.

**3. SOTA Verification**
Before recommending any approach, tool, pattern, or architecture decision — research current state-of-the-art best practices using WebSearch. Cite sources. If the recommendation deviates from SOTA, state why the deviation is justified for this specific context. "It's common" or "I've seen it before" is not justification. This applies to all agents — not just auditors.

## Pre-Build Gate (NEVER SKIP)
Before implementing ANY code change, run the **pre-build-explorer** agent first. It finds existing patterns, conventions, and reusable components so new code integrates naturally with the codebase. No coding without precedent analysis.

## Pre-Modification Doc Gate (NEVER SKIP)
After Pre-Build Gate, before writing code — **or before committing to a hypothesis/diagnosis in any investigation skill or audit** — read the existing documentation for the area being touched. This prevents re-introducing bugs already solved or contradicting decisions already recorded. The investigation skills (`prompts/investigate.md`, `debug-rca.md`, `troubleshoot.md`, `adversarial-review.md`, `downstream.md`) carry a path-free pointer to this gate; the concrete routing below is the host mapping they point at.

**Fresh-project escape:** If KB/DJ for the module don't exist yet, note "no prior art" and proceed.

**Doc-sweep routing (the concrete mapping the portable pointers reference):**
1. Map the subject to tags (`charter.json` `tag_taxonomy`).
2. Grep Decision Journal headers in `KB/KB_01_architecture.md` for matching `[tag]`; read only those DJ entries.
3. Read the KB module covering the area per the `KB/KB_index.md` Load column.
4. Check the current blueprint (`KB/blueprints/BLUEPRINT_INDEX.md` → current version only).
5. Scan `state/devlog.ndjson` for recent bugfix/decision/refactor entries touching this area.
6. For client/non-code problems, scan `state/comms.md`.
- Findings are E2 (documented artifact). **Flag** any prior decision that *rejected* this approach (do not re-propose without a new DJ entry) and any prior fix for the *same symptom* (regression signal).

**Effort scale:**
- 1-liner trivial (typo, format) → skip this gate
- Trivial fact-lookup investigation (single file, < 30s answer) → skip this gate
- 5-30 LOC → KB section for the module + 2-3 tagged DJ entries + relevant memories
- Multi-hypothesis or cross-module diagnosis / investigation → full doc-sweep routing above
- Feature / refactor → full KB module + DJ + current blueprint + devlog last 1-2 sessions
- Cross-module / architectural → exhaustive KB + pre-build-explorer agent

**Banned patterns:** fixing without reading KB, replacing a function without checking DJ entries that shaped it, reverting to an approach a DJ explicitly rejected without a new DJ entry.

## Mandatory Gates (NEVER SKIP)
**KB Gate:** Code change affecting functionality/UI/flows -> update `KB/*.md` + `kb_update` devlog entry. No KB for module? Create one. No commit without KB update.
**Blueprint Gate:** Scaffolding/architecture change -> new version file in `KB/blueprints/` + update `BLUEPRINT_INDEX.md` pointer. No silent plan changes. **Versioning rule:** any significant or major blueprint modification (new component, removed component, pattern change, new architectural decisions) MUST create a new version (v0.3, v0.4...). Set the old version's status to `superseded`. Minor updates (typo fixes, adding references to lists) may modify the current version without creating a new one.
**Decision Journal Gate:** Decision superseded or amended -> add DJ-XXX entry to `KB/KB_01_architecture.md`. Link old and new decision IDs. Record the WHY.
**Doc Gate:** Task completed -> run `/doc`. All state files updated. `python3 taskmaster.py validate` passes.
**Schema Log Gate (DB projects only):** New migration created -> update `state/schema_log.md`. Verify: check version control for new migration files.

## Plan Execution Gate (NEVER SKIP)
Working from a plan in `state/plans/`? Identify your session type:

**Brainstorm session:** Iterate on plan structure with user. Phases have intent only — no atomic tasks. Don't implement anything.

**Decomposition session:** Convert the next undecomposed phase into 3-4 atomic tasks (Files/Do/Verify). Explore codebase broadly to write precise tasks. Don't implement anything. **Versioning rule:** decomposition creates a new plan file (new timestamp, e.g. v3→v4). The new file contains the full plan: DONE phases preserved as-is, the newly decomposed phase with atomic tasks, and future phases still as intent. Set the previous plan's Status to `superseded`. Update handoff to point to the new plan.

**Implementation session:** Load only the current phase's tasks. Execute them in order. Tick checkboxes on completion. Run /doc when phase is done. Mark phase heading DONE. Don't decompose future phases. If `state/briefings/` contains a briefing for the current task, read it before starting.

Rules for all plan session types:
- Find the first unchecked task. Start there.
- Don't re-read or re-plan completed (checked) tasks.
- If a task's approach turns out wrong: update the task, note what you learned, adjust remaining tasks in the phase.
- When all phases are DONE: set plan Status to `done`.

See `state/plans/README.md` for full template and workflow.

## Devlog
Append single-line JSON to `state/devlog.ndjson` for: accepted decisions, scope changes, completed milestones, major blockers, blueprint versions, Decision Journal entries.

Event types: `feature`, `bugfix`, `refactor`, `kb_update`, `decision`, `handoff`, `verification`, `human_review`, `blueprint`, `dj_entry`.

## Checkpoint
Save progress BEFORE autocompact eats it. Trigger: 3+ files read without save, important decision, task completed.
Actions: update `state/handoff.md` (including `MEMORY_MARKER`) -> append devlog event -> `python3 taskmaster.py validate`.
The `MEMORY_MARKER` in handoff.md is a quick-recovery anchor: `<timestamp> | <last_task_completed> | <next_task>`. Update it after every task completion so context can be recovered after autocompact.
Session compression: keep only last 3 sessions in handoff.md. Older sessions are archived in git history and summarized in devlog.ndjson. This prevents handoff.md from bloating and wasting context window.

### Handoff Session Discipline
1 session = 1 handoff block. No `cont N` sub-sections. Each new conversation = session number +1 from last seen. One MEMORY_MARKER per session, updated incrementally via Edit. Devlog stays fine-grained (one entry per action).

## Verification (before marking done)

| # | Check | How |
|---|-------|-----|
| 1 | **Matches request** | Deliverable = what was asked |
| 2 | **Works** | Runs/tests pass, no regressions |
| 3 | **Minimal** | `git diff` shows only necessary changes |
| 4 | **Documented** | KB updated if code changed, blueprint if arch changed, DJ if decision changed |

## Root Cause Diagnostic Discipline (MANDATORY)
Any time something is broken — code bug, pipeline stuck, test failing, environment misbehaving, flaky behavior, user-reported issue — start from first principles and find the actual root cause. Not the symptom. Not the most visible failure. The real origin.

**Diagnostic chain (follow in order):**
1. **Capture** — observe the broken state read-only. Don't mutate anything yet.
2. **Trace** — follow the causal chain to the origin: the line, the logic flaw, the wrong assumption, the missing validation, the stale state. Keep going until you can explain *why* it broke, not just *what* broke.
3. **Fix** — fix the root cause. Minimum necessary change.
4. **Test** — verify the fix against the original broken case.
5. **Document** — record the causal chain in the commit message or devlog: what broke, why, and what the actual fix was.

Don't assume the fix because you've "seen this before." Decompose what's actually happening — the symptom that looks familiar may have a completely different cause this time.

**Only acceptable exception:** root cause is in a dependency or external system you can't change — document explicitly why the workaround is the only option.

## Anti-Drift (CRITICAL)
- Work ONLY on the current task. Nothing else.
- Minimum necessary edits. No extra changes.
- No opportunistic refactors/cleanup/reformatting.
- No "while I'm here" improvements.
- Do not change scope without explicit user approval.
- Ask if unclear -- do not assume.
- Never present assumptions as facts -- mark [ASSUMED].
- Do not rewrite existing content in ways that drop context.


## Long-Running Tasks
- ALWAYS warn the user before running any long background task.
- Run with a viewable progress bar so the user can monitor.
- Never silently run long tasks in background.

## Scripts: Debug Flag (MANDATORY)

Every script created in this project — regardless of language (Python, Bash, Node, Go, etc.) — MUST have a `--debug` flag that:
- Writes a hyper-precise, complete log of absolutely every action taken by the script
- Logs to a file (e.g. `data/<script_name>_debug.log`) AND to stdout
- Without `--debug`, the script runs normally with minimal output
- With `--debug`, every micro-step is logged: file reads, classifications, API calls, DB queries, decisions, skips, errors with full tracebacks
- Use a `log(msg, debug_only)` helper pattern — `debug_only` for verbose steps, non-debug for important messages shown in both modes. Adapt to the language idiom (e.g. Python: `log(msg, debug_only=True)`, Bash: `log "msg" --debug-only`, Node: `log(msg, { debugOnly: true })`)
- The log file is flushed after each line for real-time `tail -f` monitoring

## Tag Taxonomy
Tags are defined in `state/charter.json` under `project.tag_taxonomy`. All tags used in KB_index `Tags` column and Decision Journal entry `[tag]` headers MUST exist in the taxonomy. To add a new tag, add it to charter.json first, then use it.

## Context Loss
If you don't remember current task/recent files/decisions: **STOP.** Follow Bootstrap order above. Tell user "Context lost, re-read state." Wait for confirmation.

## Framework Structure
- Agent stubs: `.claude/agents/` — lightweight registration files for Claude Code. Point to full protocols in `prompts/`.
- Full protocols: `prompts/` — portable behavior contracts. Usable by any tool, not just Claude Code.
- Investigation skills: `.claude/skills/<name>/SKILL.md` stubs → `prompts/<name>.md` protocols. Five skills: investigate, debug-rca, troubleshoot, adversarial-review (hypothesis-driven, convergent), and downstream (enumerative, divergent — maps pre-change code coupling / blast radius).
- State-write skills (mutate `state/`, unlike the read-only investigation skills above): `capture-task` — collision-checked, non-destructive task capture into `state/roadmap.json` via the deterministic `taskmaster add` command (stub `.claude/skills/capture-task/SKILL.md` → `prompts/capture-task.md`); and `doc` — documents completed work across state files (`.claude/skills/doc/SKILL.md`, inlined protocol).
- Audit orchestrator: `prompts/auditors/runner.md` — manual use prompt for running full audit sequences. Not a subagent (can't call sub-subagents).
- Supervisor contract: `prompts/supervisor.md`
- Project workflows: `workflows/` — on-demand project-specific workflow templates (deploy ceremonies, architecture checks, custom gates). Loaded when task matches.
- Agent briefings: `state/briefings/` — self-contained phase execution guides for autonomous agents. See `state/briefings/README.md` for convention.
- Operational plans: `state/plans/` — multi-phase execution scripts with tracked progress. Naming: `YYYYMMDDHHMM-topic.md`. See `state/plans/README.md` for template and workflow.
- All agents inherit this CLAUDE.md automatically.
- Agent stub paths are relative to repository root.
