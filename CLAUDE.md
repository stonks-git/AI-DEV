# Project Name

> Fill project description here after bootstrap.

State: `state/` (charter.json, roadmap.json, devlog.ndjson, handoff.md).

## Mandatory Gates (NEVER SKIP)
**KB Gate:** Every code change affecting functionality/UI/flows -> update `KB/*.md` + `kb_update` devlog entry. No KB for module? Create one. **No commit without KB update.**

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

## Context Loss
If you don't remember current task/recent files/decisions: **STOP.** Read `state/handoff.md`. Tell user "Context lost, re-read state." Wait for confirmation.
