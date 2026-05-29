# Briefings — Autonomous Agent Phase Execution Guides

Self-contained briefings for agents executing plan phases autonomously (e.g., overnight runs, parallel worktrees, delegated sub-tasks).

## When to Create a Briefing

Create a briefing when an agent will execute a plan phase without the user present to answer questions. The briefing must contain everything the agent needs — no assumptions about prior context.

## Convention

Each briefing is a standalone `.md` file in this directory. It includes:

1. **Mission** — one phase = one mission, stated precisely
2. **Prerequisite reads** — exact file paths the agent must read before starting (KB, patterns, plan section)
3. **Atomic tasks** — numbered, each with Files / Do / Verify
4. **Patterns to mimic** — pointers to existing code the agent should follow (e.g., `frontend/src/composables/mt/index.js`)
5. **Anti-drift gates** — explicit prohibitions (charter non-goals, scope boundaries)
6. **Report format** — standardized ~200-word output so the orchestrator can parse results consistently

## Naming

Use the task or phase ID: `t171-phase3-layout.md`, `t045-backend-bff.md`.

## Report Format (agents must follow)

```markdown
## Report Phase N — STATUS: success | partial | blocked

### Commits created
- <SHA> <message>

### Tests
- <framework>: X/Y passed (Z pre-existing failures if applicable)

### Risks / blockers discovered
- [P0/P1/P2/P3] description

### Next phase ready?
- YES / NO (reason + suggestion)
```
