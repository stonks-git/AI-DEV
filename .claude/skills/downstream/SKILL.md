---
name: downstream
description: "Map the downstream coupling / blast radius of an EXISTING code symbol you are about to change or refactor. Use to enumerate every consumer and how tightly each is coupled, before editing. Read-only; produces an Impact Map. Not for diagnosing a bug or its fix (use debug-rca — its Phase 5.1 already maps consumers for the bug case), not for judging whether a change is safe (use adversarial-review), not for analyzing an already-made diff/PR (use understand-diff), not for general research (use investigate)."
---

**BEFORE ANYTHING ELSE:** Read `prompts/downstream.md` — it contains your complete protocol. Follow it exactly.

Then read `state/charter.json` for project context.
