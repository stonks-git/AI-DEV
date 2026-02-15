# Project Name

> Fill project description here after bootstrap.

State: `state/` (charter.json, roadmap.json, devlog.ndjson, handoff.md).

## Mandatory Gates (NEVER SKIP)
**KB Gate:** Every code change affecting functionality/UI/flows -> update `KB/*.md` + `kb_update` devlog entry. No KB for module? Create one. **No commit without KB update.**
**Blueprint Gate:** Scaffolding/architecture changes -> new version file in `KB/blueprints/` + update `BLUEPRINT_INDEX.md` pointer. No silent plan changes.
**DJ Gate:** Decision superseded or amended -> add DJ-XXX entry to `KB/KB_01_architecture.md`. Link the old and new decision IDs.

## Devlog
Append a single-line JSON to `state/devlog.ndjson` for: accepted decisions, scope changes, completed milestones, major blockers.

## Checkpoint
Save progress BEFORE autocompact eats it. Trigger: 3+ files read without save, important decision, task completed.
Actions: update `state/handoff.md` -> append devlog event -> `python3 taskmaster.py validate`.

## Verification (before marking done)
Task matches request. Tests/check pass. No regressions. Minimal changes only. KB updated.

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
- **ALWAYS warn the user** before running any long background task (tests, builds, indexing).
- Run with a **viewable progress bar** so the user can monitor from terminal.
- Never silently run long tasks in background — user may need to leave and restart later.

## Context Loading (token-efficient bootstrap)
1. `state/handoff.md` — always
2. `state/charter.json` — always
3. `KB/KB_index.md` — always (this is the context router)
4. Files marked `always` in KB_index `Load` column
5. `on-demand` files — ONLY when current task matches tags
6. Historical blueprint versions — ONLY to trace a specific evolution, never bulk-load

**Rule:** If unsure whether to load a file, read its one-line description in KB_index first. Load only if relevant to current task.

## Context Loss
If you don't remember current task/recent files/decisions: **STOP.** Read `state/handoff.md` then `KB/KB_index.md`. Tell user "Context lost, re-read state." Wait for confirmation.
