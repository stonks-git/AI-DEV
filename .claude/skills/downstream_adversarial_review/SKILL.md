---
name: downstream_adversarial_review
description: "Iteratively harden a text artifact (plan, report, proposal, spec, message): loop a downstream critic and an adversarial critic over it as separate background agents, applying fixes between passes with no re-prompting, until the adversarial reviewer is satisfied. Use when asked to iteratively refine/harden an artifact or 'run the downstream+adversarial loop'. The complete, authoritative protocol lives in prompts/downstream_adversarial_review.md — this stub defers to it for everything."
---

**Read `prompts/downstream_adversarial_review.md` and follow it exactly.** It is the complete and
authoritative protocol — inputs, the loop, what gets applied vs. reported, and every stop condition.
This stub intentionally states no rules of its own; defer to that file for everything.

Then read `state/charter.json` for project context.
