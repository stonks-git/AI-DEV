---
name: doc
description: Document session changes in tracking files (devlog, handoff, KB, roadmap). Use when the user says "document", "/doc", or asks to note what was done.
---

# Document Session

When the user asks to document, follow these steps **IN ORDER**:

## 1. devlog.ndjson (MANDATORY)

Add 1+ JSON lines to `state/devlog.ndjson`. Format:

```json
{"ts":"2026-01-07T12:00:00+02:00","event":"<type>","id":"<ID>","summary":"<short description>"}
```

**Event types:**
- `feature` - new functionality
- `bugfix` - bug fix
- `refactor` - code restructuring
- `kb_update` - KB documentation update
- `decision` - new decision (with `id: D-XXX`)
- `handoff` - session summary
- `verification` - smoke test passed
- `human_review` - approved by user

## 2. handoff.md (MANDATORY)

Update session sections in `state/handoff.md`:
- Previous Sessions: add current session summary
- Tasks DOING: update status
- Git Status: current branch, last commit, modified files

## 3. KB/*.md (CRITICAL - DO NOT SKIP!)

**NO EXCEPTIONS:** If code was modified, KB MUST be updated.

**Steps:**
1. List files: `ls KB/*.md`
2. Ask: "What module did I modify? Which KB describes it?"
3. Read the relevant KB and update it
4. If no KB exists for the modified module -> create one

**After KB update:** add entry in devlog with `event: kb_update`.

## 4. Git Status (MANDATORY)

Run git commands and add to handoff.md:

```bash
git status --short
git log --oneline -3
```

## 5. roadmap.json (IF APPLICABLE)

Update `state/roadmap.json` only if:
- A task changes status (doing -> done)
- New task added
- Dependencies changed

## 6. FINAL CHECKLIST (BEFORE COMMIT)

**STOP! Don't commit until you verify ALL:**

- [ ] `devlog.ndjson` - entry added for each change
- [ ] `handoff.md` - session sections updated
- [ ] **KB updated** - MANDATORY if code was modified
- [ ] `kb_update` entry in devlog (if KB was updated)
- [ ] `taskmaster validate` - exit 0

## Workflow Summary

```
1. Ask user WHAT was done (if you don't know)
2. Write entry in devlog.ndjson
3. Update handoff.md session sections
4. GATE: Identify and update relevant KB
   -> What modules did I touch? -> Which KB describes them? -> Update
   -> Add `kb_update` entry in devlog
5. Check git status, add to handoff
6. Check if roadmap needs updating
7. Run `python3 taskmaster.py validate` - exit 0
8. CHECKLIST COMPLETE? -> tell user documentation is done
```

## Timestamp format

Use ISO 8601 with timezone: `2026-01-07T12:00:00+02:00`
