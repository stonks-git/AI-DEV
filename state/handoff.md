# Supervisor Handoff

> **READ THIS FIRST.** You are the supervisor (queen agent) for this project.
>
> **Reading order (MANDATORY):**
> 1. This file (handoff.md) - bootstrap loader
> 2. `prompts/supervisor.md` - your supervisor contract
> 3. `state/charter.json` - project constraints (MANDATORY)
> 4. `python3 taskmaster.py ready` - available tasks
> 5. Sections below - previous session context
>
> **DO NOT explore the whole codebase.** Delegate exploration to workers (Task tool with subagent_type=Explore).

---

## Previous Sessions

_(No sessions yet. Fill this section after each work session.)_

<!--
### SESSION <date> (<number>) - <TITLE>

**STATUS:** DONE / DOING / TODO

**What was done:**
1. ...

**Verifications PASSED:**
- ...

| File | What was done |
|------|---------------|
| `path/to/file` | Description |

---
-->

## What is this project?

_(Fill after bootstrap. One paragraph describing the project.)_

---

## Tasks DOING now

| Task ID | Status |
|---------|--------|
| _(none)_ | - |

## Docker/Prod Status

_(Fill if applicable. Server IPs, container status, deploy state.)_

---

## Blockers or open questions

| Blocker/Question | Status |
|------------------|--------|
| (none) | - |

---

## Useful commands (copy-paste ready)

```bash
# Validate state
python3 taskmaster.py validate

# Ready tasks
python3 taskmaster.py ready

# Run checks (customize per project)
# python manage.py check
# npm test
# cargo test
```

---

## Checklist before handoff

- [ ] Updated task statuses in handoff
- [ ] Completed current session section above
- [ ] devlog updated (+1 entry per significant change)
- [ ] **Kept only last 3 sessions** (older ones archived in git)
- [ ] KB updated if code was changed

---

## Git Status

- **Branch:** main
- **Last commit:** _(fill)_
- **Modified:** _(fill)_

---

## Memory Marker

_(Fill after each task completion)_

```
MEMORY_MARKER: <timestamp> | <last_task_completed> | <next_task>
```
