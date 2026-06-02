---
name: capture-task
description: "Capture a new task into state/roadmap.json safely. Reads the full project record (roadmap, devlog, Decision Journal, KB, plans, comms, codebase) to detect whether the task is already a duplicate, done, deliberately skipped, or incompatible with a recorded decision BEFORE adding it. Non-destructive: only ever appends one task via `taskmaster add`, never edits existing tasks. Not for documenting completed work (use /doc) or decomposing plan phases (those write state/plans/)."
---

**BEFORE ANYTHING ELSE:** Read `prompts/capture-task.md` — it contains your complete protocol. Follow it exactly.

Then read `state/charter.json` for project context.
