> **Portable version.** This is the platform-agnostic DebugRCA process. For Claude Code integration with subagent isolation, evidence grading, and skill chaining, see the `/debug-rca` skill at `prompts/debug-rca.md`.

# Debug RCA Adversarial (v2)

A rigorous, adversarial root cause analysis process for non-trivial bugs. Designed to eliminate symptom masking, false root causes, and plans that break downstream consumers.

The process runs as a single agent executing all phases sequentially. It is explicitly **not** an automated multi-agent pipeline — the adversarial phases require independent reasoning within one invocation, not parallel agents. User decision gates are real blocking points where the human reads findings and decides whether to proceed.

---

## When to Use

**Use this process for:**
- Any bug where the cause is not immediately obvious from reading the code
- Bugs that have been "fixed" before and came back
- Bugs with multiple possible causes
- Bugs where a wrong fix could break other things
- Bugs in shared/critical code paths

**Do NOT use for:**
- Typos and wrong strings (fix directly)
- Pure config changes
- Anything where you can read the cause in one file in under 30 seconds

---

## Process Overview

```
INPUT (bug description + suspects + observable data)
  │
  ▼
PHASE 1 — INVESTIGATE
  Trace causal chain from symptom to root cause.
  Output: hypothesis + causal chain + file:line evidence
  │
  ▼
PHASE 2 — ADVERSARIAL DESTROY
  Independent agent destroys Phase 1's hypothesis.
  Output: SOLID / PARTIAL / FALSE
  │
  ├── FALSE or PARTIAL → loop back to Phase 1 with findings
  │
  ▼
PHASE 3 — VERIFY (read-only)
  Collect raw factual data that resolves remaining hypotheses.
  Output: raw values from DB, logs, files — no interpretation
  │
  ├── Data contradicts hypothesis → loop back to Phase 1
  │
  ▼
PHASE 4 — ATTRIBUTE
  git blame the faulty lines. Identify who, when, which branch.
  Output: our code / upstream / missing feature / interaction
  │
  ▼
PHASE 5 — PLAN + ADVERSARIAL LOOP
  5.0 Write fix plan
  5.1 Impact analysis (all downstream consumers)
  5.2 Adversarial review of the plan
  5.3 ← USER GATE → GO / CORRIGER / REPENSER
  │
  ├── CORRIGER → revise plan, loop 5.0 → 5.1 → 5.2 → 5.3
  ├── REPENSER → root cause wrong, loop back to Phase 1
  │
  ▼
PHASE 6 — IMPLEMENTATION PROMPT
  Generate a self-contained implementation prompt for an execution agent.
  Output: state/plans/YYYYMMDDHHMM-rca-<slug>.md
```

**Loop exit conditions:**
- Phase 1→2 loop: max 3 iterations. If hypothesis still PARTIAL/FALSE after 3, escalate to user with UNRESOLVED status.
- Phase 5 loop: user decides — no automatic termination.

---

## INPUT Requirements

Before starting, collect all of the following. Do not begin with partial input.

```
Bug description:    What is the observed behavior? What was expected?
Observable data:    Logs, screenshots, error messages, stack traces — exact, not paraphrased
Suspect files:      Files or modules where the bug likely lives (can be broad)
Reproduction:       Steps to reproduce, or conditions under which it appears
Scope:              Is this only in production? Staging? After a specific deploy?
```

---

## Phase 1 — Investigate

**Agent:** Investigator (Opus, read-only tools: Read, Grep, Glob, Bash for git/grep only)

**Job:** Trace the complete causal chain from the observable symptom to the structural root cause.

### Protocol

1. Start from the observable symptom. Identify the exact code path that produces it.
2. For each cause identified, ask: **"Why is this line/condition wrong?"** — recurse until you reach a structural defect.
3. Stopping criterion: the answer to "why?" is a **structural fact** — missing data, broken API contract, substituted mechanism without replacement — not a derived behavior. The first level found is almost always a symptom, not the root.
4. Every claim must be verified by reading code. No "probably" or "likely" — either cite `file:line` or state "NEEDS STAGING DATA: [what data]."
5. Do not trust summaries from other agents. Read the files yourself.

### Output

```markdown
## Root Cause Hypothesis
[One-paragraph statement of the structural defect]

## Causal Chain
1. Observable symptom: [description] → [file:line]
2. Caused by: [claim] → [file:line]
3. Which exists because: [claim] → [file:line]
...
N. Root defect: [structural fact] → [file:line]

## Evidence
- [file:line] — [exact quote or command output]
- [file:line] — [exact quote or command output]

## Unverified items (need staging data)
- [what data is needed and why]
```

---

## Phase 2 — Adversarial Destroy

**Agent:** Adversary (Opus, read-only tools: Read, Grep, Glob)

**Job:** Destroy Phase 1's hypothesis. Find every reason it is wrong, incomplete, or does not explain the observed behavior. This agent's job is NOT to validate — it is to DESTROY.

### Critical constraint: no anchoring

The adversary receives ONLY:
- The root cause hypothesis (one paragraph)
- The list of file:line evidence locations

It does NOT receive Phase 1's causal chain reasoning. Seeing the chain of reasoning anchors the adversary to Phase 1's framing, causing convergence instead of genuine critique. The adversary must reconstruct the chain independently.

### Protocol

1. Read every file:line cited by Phase 1. Verify each claim independently.
2. **Mandatory: generate at least 2 alternative hypotheses** that also fit the observable evidence. An adversary that finds no alternatives is almost certainly anchored — it has not genuinely searched.
3. For each alternative hypothesis: what evidence supports it? What would need to be true?
4. For the original hypothesis: if you fix that specific line/defect, does the upstream defect persist? Can it produce the same bug through another path?
5. Check: is the identified root cause truly structural, or is it itself a symptom of something deeper?

### Verdict

| Verdict | Meaning |
|---|---|
| **SOLID** | Hypothesis explains the bug. Alternatives have been ruled out. Causal chain is structurally complete. |
| **PARTIAL** | Hypothesis is partially correct but incomplete. Missing a co-cause, or the root is one level too shallow. Include specific findings. |
| **FALSE** | Hypothesis does not explain the bug, or a different hypothesis better explains all evidence. |

### Output

```markdown
## Verdict: [SOLID / PARTIAL / FALSE]

## Alternative Hypotheses
1. [hypothesis] — supported by: [file:line], ruled out by: [file:line or "needs data"]
2. [hypothesis] — supported by: [file:line], ruled out by: [file:line or "needs data"]

## Findings against Phase 1 hypothesis
- [finding] → [file:line evidence]
- [finding] → [file:line evidence]

## Recommendation
[If SOLID: proceed to Phase 3]
[If PARTIAL: re-investigate with these additional constraints: ...]
[If FALSE: discard hypothesis, re-investigate starting from: ...]
```

**Loop:** PARTIAL or FALSE → pass the Adversary findings back to Phase 1. Phase 1 re-investigates incorporating the adversarial findings. Max 3 iterations. If unresolved after 3, surface UNRESOLVED to user with all findings.

---

## Phase 3 — Verify (Read-Only)

**Agent:** Verifier (Sonnet, strictly read-only: Read, Grep, Glob only — NO Bash, NO mutations of any kind)

**Job:** Collect raw factual data that resolves any remaining ambiguity between the surviving hypotheses. Report data only — no interpretation.

### Hard constraint: no mutations

This phase must never modify any state. No database writes, no file edits, no API calls that have side effects. If a verification step would require a write, note it as "REQUIRES MANUAL VERIFICATION" and skip it.

This constraint is behavioral (prompt-level), not platform-enforced. The agent must treat it as absolute.

### Protocol

1. Read the surviving hypothesis and any unverified items from Phase 1.
2. For each unverified item: collect the raw data. Quote exactly — no summarizing.
3. SQL queries: SELECT only. Report raw result rows.
4. Log files: quote the relevant lines with timestamps. No interpretation.
5. Config files: quote the relevant keys and values.
6. Do not conclude. Do not recommend. Report data only.

### Output

```markdown
## Raw Evidence

### DB Query: [query text]
Result: [raw rows]

### Log excerpt: [file path, line range]
[exact quoted lines]

### Config: [file:line]
[exact quoted values]

## Unverified items (require manual access)
- [item] — why manual access is needed
```

**Loop:** If raw data contradicts the surviving hypothesis → return to Phase 1 with the contradicting evidence. State explicitly: "Phase 3 data contradicts hypothesis at: [specific field/value]."

---

## Phase 4 — Attribute

**Agent:** Attributor (Sonnet, tools: Read, Bash for git commands only)

**Job:** Identify who introduced the bug, when, on which branch, and whether it's in our code or upstream.

### Protocol

1. Run `git blame` on every faulty file:line identified in Phase 1.
2. If the project has a fork/upstream: compare branches with `git log fork..upstream` or `git diff fork upstream -- file`.
3. Identify the relevant commit(s): hash, author, date, message.
4. Classify the source:

| Classification | Meaning |
|---|---|
| **Our code** | Bug introduced in a commit on our branch by our team |
| **Upstream** | Bug exists in the upstream dependency/fork we track |
| **Missing feature** | Expected functionality was never implemented |
| **Interaction** | Correct code in two places, broken interaction between them |

### Output

```markdown
## Attribution

Faulty lines:
- [file:line] — commit [hash], author [name], date [date]
  Commit message: [message]

Classification: [Our code / Upstream / Missing feature / Interaction]

Relevant diff:
[git diff or blame excerpt]

Branch context:
[fork vs upstream comparison if applicable]
```

---

## Phase 5 — Plan + Adversarial Loop

This phase has three sub-phases that loop until the user gives a GO.

### Phase 5.0 — Write Fix Plan

**Agent:** Planner (Opus, tools: Read, Grep, Glob)

Write the fix plan. Be precise — this plan feeds into an autonomous implementation agent in Phase 6.

```markdown
## Fix Plan

### Root cause being fixed
[One sentence — what structural defect is being corrected]

### Files to modify
- [file:line] — [what changes and why]
- [file:line] — [what changes and why]

### Files NOT to touch
- [file] — [why it must remain unchanged]

### Proposed code
[Exact code, not paraphrase. The implementation agent writes what is here.]

### Tests to write
- [test name] — [what it verifies] — [expected input/output]

### Verification
- [command or assertion] — [expected result]

### Forbidden
- [what this fix must not do]
```

---

### Phase 5.1 — Impact Downstream

**Agent:** Impact Analyst (Opus, tools: Read, Grep, Glob)

**Job:** Find EVERY consumer of the changed code. Assess impact on each. This must be exhaustive — the adversary in 5.2 will attack gaps.

For each consumer:

| Field | Content |
|---|---|
| Consumer | `file:line` — function/class name |
| Impact | NONE / POSITIVE / NEGATIVE / RISK |
| Detail | Exact description of what changes for this consumer |

**Edge cases to cover explicitly:**
- Empty inputs / null values
- Single-element collections (off-by-one corner cases)
- Unexpected data formats or types
- Fallback paths and error handling branches
- Mutable state shared across calls
- Race conditions (if any async code is involved)
- Callers in test code vs. production code

---

### Phase 5.2 — Adversarial Plan Review

**Agent:** Plan Adversary (Opus, tools: Read, Grep, Glob)

**Job:** Destroy the fix plan. Use the Impact Analyst's findings as ammunition. Do not validate.

Mandatory questions — answer each one explicitly:

1. **Does the fix correct the structural defect from Phase 1, or does it add an external filter at the caller?** A fix that patches the symptom at the call site instead of fixing the broken contract is not a fix.
2. **Did the Impact Analyst miss any consumer?** Search the codebase yourself. Do not trust the 5.1 summary.
3. **Is there a scenario where this fix produces a WORSE result than the current bug?** Partial fixes that corrupt state are worse than bugs that simply fail.
4. **Is the fix at the right level of abstraction?** If the contract is broken in module A, fixing module B's caller is wrong even if it works.
5. **Does the fix hold on the domain's edge cases?** Use the specific data types, ranges, and states that exist in this codebase — not generic edge cases.

### Output

```markdown
## Plan Adversarial Report

### BLOCKER findings (fix plan cannot proceed)
- [finding] → [file:line] → [required change]

### MINOR findings (fix plan can proceed with adjustment)
- [finding] → [file:line] → [suggested change]

### COSMETIC findings (no change needed, noted for awareness)
- [finding]

### Verdict: [SOLID / NEEDS ADJUSTMENT / WRONG APPROACH]
```

---

### Phase 5.3 — User Decision Gate

**This is a hard blocking point. Do not proceed to Phase 6 without explicit user decision.**

Present the user with:
1. The root cause hypothesis (Phase 1 output, one paragraph)
2. The adversarial verdict on the hypothesis (Phase 2)
3. The fix plan (Phase 5.0)
4. The impact summary (Phase 5.1) — number of consumers affected, risk level
5. The plan adversarial report (Phase 5.2)

Ask for one of three decisions:

| Decision | Next action |
|---|---|
| **GO** | Proceed to Phase 6. Generate implementation prompt. |
| **CORRIGER** | User provides specific corrections. Revise plan (5.0), re-run impact (5.1) and adversarial (5.2), return here. |
| **REPENSER** | The root cause identification is wrong. Start over at Phase 1 with what we've learned. |

---

## Phase 6 — Implementation Prompt

**Agent:** Implementation Prompter (Sonnet)

**Job:** Generate a self-contained implementation prompt for an autonomous execution agent. This prompt must be complete — the execution agent receives nothing except this document.

The prompt must contain:

```markdown
## Implementation Prompt

### Context
[What bug is being fixed. One paragraph.]

### Root cause
[Structural defect, one sentence, with file:line]

### Exact changes required
[For each file: exact code to write. Not paraphrase — the exact final code.]

### Files to modify
- [file] — [what to change, with before/after if modifying existing code]

### Files NOT to touch
[Explicit list with reason for each]

### Tests to write
[Test name, file to create/modify, exact assertions, expected inputs/outputs]

### Verification commands
[Exact commands to run, exact expected output]

### Forbidden actions
[What the implementation agent must NOT do]

### Done criteria
[Exact conditions under which the task is complete — no ambiguity]
```

### Output

Save to: `state/plans/YYYYMMDDHHMM-rca-<bug-slug>.md`

---

## State File Schema

Each RCA session maintains a single JSON state file at `state/rca/YYYYMMDDHHMM-rca.json`.

```json
{
  "session_id": "YYYYMMDDHHMM",
  "bug_slug": "short-kebab-description",
  "phase": "investigate | destroy | verify | attribute | plan | implement",
  "iteration": 0,
  "max_iterations": 3,

  "input": {
    "description": "",
    "observable_data": "",
    "suspect_files": [],
    "reproduction": "",
    "scope": ""
  },

  "hypothesis": {
    "status": "proposed | weakened | destroyed | confirmed",
    "statement": "",
    "causal_chain": [
      {"step": 1, "claim": "", "file": "", "line": "", "evidence": ""}
    ],
    "unverified_items": []
  },

  "adversarial": {
    "verdict": "SOLID | PARTIAL | FALSE",
    "alternatives": [],
    "findings": []
  },

  "raw_evidence": {
    "sql": [],
    "logs": [],
    "files": []
  },

  "attribution": {
    "commit": "",
    "author": "",
    "date": "",
    "classification": "our_code | upstream | missing_feature | interaction",
    "diff_excerpt": ""
  },

  "fix_plan": {
    "root_cause_statement": "",
    "files_to_modify": [],
    "files_not_to_touch": [],
    "proposed_code": "",
    "tests": [],
    "verification": [],
    "forbidden": []
  },

  "impact_analysis": {
    "consumers": [],
    "edge_cases_checked": []
  },

  "plan_adversarial": {
    "verdict": "SOLID | NEEDS_ADJUSTMENT | WRONG_APPROACH",
    "blockers": [],
    "minors": [],
    "cosmetics": []
  },

  "user_decision": null,
  "user_feedback": "",

  "implementation_prompt_path": ""
}
```

---

## Transversal Principles

These apply at every phase. Violating them invalidates the output.

**1. Hypothesis ≠ fact.**
Every claim must be backed by `file:line` evidence or marked "NEEDS STAGING DATA." "Probably," "likely," "should" are not evidence.

**2. The adversarial phase destroys, it does not validate.**
An adversary that confirms the hypothesis without producing at least 2 alternatives has not done its job. It is anchored.

**3. Recurse until structural.**
The first level of "why?" gives a symptom. Keep asking why until the answer is a structural fact: missing data, broken contract, mechanism substituted without replacement. That is the root.

**4. Adversarial on the fix, not just the diagnosis.**
Phase 5.2 exists because fixes that address the wrong level silently re-introduce the same bug class.

**5. Phase 3 is strictly read-only.**
No mutations. Not even "harmless" ones. If a verification requires a write, mark it REQUIRES MANUAL VERIFICATION.

**6. Fail-fast on false hypothesis.**
When Phase 2 returns FALSE or Phase 3 data contradicts the hypothesis — stop immediately and re-investigate. Do not proceed with a hypothesis that has been invalidated.

**7. 5.1 before 5.2.**
Impact analysis feeds the adversarial review. Running 5.2 without 5.1 means the adversary has no consumer map to attack.

**8. The user decides, not the agent.**
Phase 5.3 is not a formality. The user reads the adversarial report and makes the GO / CORRIGER / REPENSER call. The agent does not proceed without it.
