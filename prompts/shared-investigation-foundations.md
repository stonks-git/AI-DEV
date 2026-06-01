# Shared Investigation Foundations — Design-Time Reference

> **This file is NOT loaded at runtime.** It is the authoritative source of truth for shared patterns used across the investigation skills (investigate, debug-rca, troubleshoot, adversarial-review). When writing or updating skill protocols, consult this file. Those four protocols inline the INLINE BLOCK verbatim and reference the structural templates as needed.
>
> **`downstream` is an ADAPTING consumer, not a verbatim target.** It is enumerative (no hypotheses), so it inlines only the frame-neutral tables (Evidence Grading, Confidence, Uncertainty, Anti-Confabulation) and REPLACES the hypothesis-framed Self-Prompt and Handoff schema with enumerative equivalents. When the grading/confidence tables below change, port the change into `prompts/downstream.md` manually — do NOT propagate the hypothesis-framed sections to it.

---

<!-- === INLINE BLOCK START === -->
<!-- Copy this block verbatim into every skill protocol's "Shared Standards" section. -->

## Shared Standards

### Evidence Grading (applied at phase transitions, not during active collection)

| Grade | Meaning | Example |
|---|---|---|
| **E1** — Direct observation | Agent verified through tool use | Read the file and saw the value; ran the query and got the result |
| **E2** — Documented artifact | Exists in a verifiable document or log | Stack trace, error log entry, git commit, email, config file |
| **E3** — Corroborated report | Multiple independent sources agree | Two people report same behavior; two documents confirm the same fact |
| **E4** — Single-source report | One source, not independently verified | User says "it broke after Tuesday's deploy" |
| **E5** — Inference | Derived from reasoning, not direct evidence | "Based on the code structure, this module likely handles X" |
| **E6** — Assumption | Taken as true without evidence | "Assuming the database is configured correctly" |

**Enforcement gate:** Before exiting any phase that produces structured output (ACH matrix, fix plan, final report, handoff), present a graded summary. Claims without an evidence grade and confidence level cannot enter the next phase's structured output. This is a hard gate.

E5-E6 claims in structured outputs must be explicitly marked and either upgraded through further investigation or flagged as NEEDS EXTERNAL DATA.

### Per-Claim Confidence Scale

| Level | Meaning | When to use |
|---|---|---|
| **Verified** | Multiple corroborating E1-E2 sources | Direct observation confirmed by independent check |
| **Supported** | Single credible E1-E3 source | Read the file and saw the evidence, no second source |
| **Plausible** | Reasonable inference from evidence (E5) | Code structure suggests X, but not directly verified |
| **Speculative** | Limited evidence, logical but unverified | Possible based on pattern, no direct evidence |
| **Unknown** | Insufficient data to assess | Cannot determine from available information |

Confidence measures evidence strength. Report it per claim, not per report.

### Uncertainty Action Protocol

The violation is **hedging without action** — not hedging language itself. Before any phase exits, review claims for evidence basis. Any claim lacking E1-E3 evidence triggers one of three actions:

1. **Investigate further** — chase the thread to obtain E1-E3 evidence
2. **Flag as NEEDS EXTERNAL DATA** — specify: what data is needed, why the agent cannot obtain it
3. **Mark with confidence level + evidence grade** — claim stays but uncertainty is visible: e.g., `Plausible [E5]: based on code structure, this module likely handles X`

An uncertain claim properly marked is honest. An uncertain claim presented as certain is dangerous. An uncertain claim left as vague "probably" with no grade is the violation.

### Anti-Confabulation Check

At each checkpoint: "Has any evidence in my analysis been produced by my own reasoning rather than direct tool observation?" If yes → downgrade to E5-Inference or investigate further to obtain E1-E3 evidence.

### Self-Prompting (use at the start of each phase)

> My objective is [X]. Current leading hypothesis: [Y]. Unresolved items: [N]. My next action should discriminate between hypotheses, not confirm the leading one.

<!-- === INLINE BLOCK END === -->

---

## Structural Templates (reference material — not inlined)

### Prior-Art / Doc-Sweep Pointer (canonical — inlined PATH-FREE, frame-adapted per skill)

Investigations must consult the host project's decision-record layer (decisions, prior fixes, recorded rationale) before committing to hypotheses/contracts — not just the codebase. To preserve the portability of `prompts/*.md` (CLAUDE.md / README.md both declare protocols "portable / tool-agnostic"), the protocol bodies carry only a **path-free, advisory pointer**. The concrete routing (which files, how to grep DJ by tag, devlog, comms) lives ONLY in the host doc-gate (`CLAUDE.md` Pre-Modification Doc Gate). See decision D-001.

**Canonical pointer (the `<frame>` parenthetical is per-skill — see table):**

> If your project maintains a decision-record layer (decisions, prior fixes, recorded rationale), consult it before [hypotheses/contracts] (<frame>): flag any prior decision that **rejected** this approach (don't re-propose without a new decision entry) and any prior fix for the **same symptom** (regression signal); grade findings E2. If none exists, note "no prior art" and proceed.

| Skill | Inline anchor | `<frame>` |
|---|---|---|
| investigate | Phase 0 SCOPE (new step) | informs sub-questions / evidence-sufficiency |
| debug-rca | Phase 1 INVESTIGATE (step feeding IS/IS-NOT, not displacing it) | informs IS-NOT |
| troubleshoot | Phase 1 INVESTIGATE (step feeding IS/IS-NOT) | informs IS-NOT |
| adversarial-review | Phase 1 UNDERSTAND step 7 (Chesterton's Fence), codebase-conditional | informs constraints / assumptions |
| downstream | Phase 0 SCOPE step 2 (sub-bullet feeding contracts-at-risk) | informs contracts-at-risk |

**Maintainer rule:** the `<frame>` parenthetical is deliberately per-skill — do NOT enforce a byte-identical phrase across all five (that would re-import the hypothesis/IS-NOT frame into the enumerative `downstream`, which it deliberately omits). Verify "same canonical pointer, frame-adapted per skill." NEVER put concrete framework paths (`KB/`, `state/...`, `comms.md`) in protocol bodies — they live only in the host doc-gate. The pointer is intentionally **inert/advisory** when no doc-gate host is loaded (standalone / non-Claude runtime); that is an accepted tradeoff (D-001), not a bug.

### Diagnostic Timeout Checklist

Run at every checkpoint phase. Answer each question explicitly:

1. **What is my leading hypothesis?** State it in one sentence.
2. **What evidence supports it?** List with grades (E1-E6).
3. **What evidence contradicts it?** List up to 3 items. Zero is valid — justify why no contradicting evidence exists.
4. **What alternatives have I NOT tested?** List any hypothesis not yet investigated.
5. **Am I anchored to my first impression?** Was the leading hypothesis also my first hypothesis? If yes, extra scrutiny required.
6. **Anti-confabulation:** Has any evidence been produced by reasoning rather than tool observation?
7. **Update state tracker** with current phase, hypothesis status, and key evidence.

### ACH Matrix Template

Use when multiple hypotheses compete (mandatory for Investigate and Troubleshoot; optional for Debug RCA when 3+ hypotheses survive).

```
| Evidence | H1: [hypothesis] | H2: [hypothesis] | H3: [hypothesis] |
|----------|-------------------|-------------------|-------------------|
| [evidence item + grade] | C / I / N | C / I / N | C / I / N |
| [evidence item + grade] | C / I / N | C / I / N | C / I / N |
```

- **C** = Consistent (evidence fits this hypothesis)
- **I** = Inconsistent (evidence contradicts this hypothesis)
- **N** = Neutral (evidence neither supports nor contradicts)

**Selection rule:** Reject the hypothesis with the MOST inconsistencies. Do NOT select by most consistencies — that rewards vague hypotheses that explain everything. Focus on **diagnostic evidence**: items that are C for one hypothesis and I for another. Evidence that is C for all hypotheses tells you nothing.

### Convergent Evidence Stopping Criteria

An investigation phase is complete when ALL four tests pass:

1. **Convergence:** 3+ independent lines of evidence point to the same conclusion
2. **Elimination:** All plausible alternative hypotheses tested and rejected with evidence (not ignored)
3. **Explanatory completeness:** The surviving hypothesis explains ALL observed symptoms, not just the initial ones
4. **Predictive power:** The hypothesis correctly predicts something not yet examined — test this prediction

An investigation is NOT complete just because: the first plausible explanation was found, confidence "feels" high, one piece of strong evidence exists, or a deadline was reached.

### Loop Termination Rules

- **Max iterations:** Configurable per skill, default 3 for adversarial loops. The investigate→evaluate→checkpoint cycle has its own cap (default 5).
- **Fingerprinting:** If the last 2 iterations investigated the same files, generated the same hypotheses, or received the same adversarial verdict with the same findings — the loop is stuck. Surface to user.
- **No-progress detection:** If the last N steps produced no new evidence, no hypothesis status change, and no eliminated alternative — surface to user with current state.

### UNRESOLVED Output Format

When an adversarial loop hits max iterations without convergence:

```markdown
## UNRESOLVED after [N] iterations

### Best Hypothesis (not confirmed)
[hypothesis] — Confidence: [level] — Evidence grade: [E1-E6]
Weaknesses: [what the adversarial phase found wrong with it]

### Competing Hypotheses Still Active
| Hypothesis | Evidence For | Evidence Against |
|---|---|---|
| [h1] | [for] | [against] |
| [h2] | [for] | [against] |

### What Would Resolve This
- [specific data or test that would discriminate between remaining hypotheses]

### User Options
- `EXTEND [N]` — run N more iterations (default: 3)
- `ACCEPT BEST` — proceed with best hypothesis, record reduced confidence
- `SWITCH TO /investigate` — deeper research before continuing RCA
- `ABORT` — output findings so far in handoff format
```

### Handoff Output Schema

Standard output format for skill chaining. Every skill's final output follows this structure:

```markdown
## Handoff: <skill-name> → <date>

### Findings
- [claim] — Evidence: [E1-E6] — Confidence: [Verified/Supported/Plausible/Speculative/Unknown] — Source: [file:line / document / observation]

### Hypotheses
| Hypothesis | Status | Key Evidence |
|---|---|---|
| [hypothesis] | Active / Eliminated / Confirmed | [evidence summary] |

### Assumptions
| Assumption | Status | Evidence |
|---|---|---|
| [assumption] | Verified / Unverified / Disproven | [what verified/disproved it, or "NEEDS DATA: ..."] |

### Action Items
| Item | Severity | Evidence Grade | Detail |
|---|---|---|---|
| [item] | BLOCKER / MINOR / COSMETIC | E1-E6 | [description] |

### Open Questions (NEEDS EXTERNAL DATA)
- [question] — why agent cannot resolve: [reason] — what data is needed: [specific ask]
```

### Agent Tool Invocation Template (Adversarial Subagent)

Use this template when spawning adversarial subagents. Replace `[PLACEHOLDERS]` with actual content.

```
Agent({
  description: "[SKILL] adversarial [hypothesis/plan] review",
  prompt: `You are an adversarial reviewer. Your job is to DESTROY the [hypothesis/plan] below. You are NOT here to validate — you are here to find every way it is wrong, incomplete, or will fail.

## [Hypothesis/Plan] to Attack
[PASTE THE HYPOTHESIS STATEMENT OR PLAN HERE]

## Evidence Locations (read ALL of these independently)
[LIST ALL INVESTIGATED FILE PATHS / EVIDENCE LOCATIONS — INCLUDE BOTH SUPPORTING AND NON-SUPPORTING]

## Your Protocol
1. Read every evidence location listed above. Form your OWN assessment.
2. Generate at least 2 alternative [hypotheses/approaches] that also fit the evidence.
3. For each alternative: what evidence supports it? What would need to be true?
4. For the original [hypothesis/plan]: what evidence CONTRADICTS it?
5. Attempt to DISPROVE each of your findings before reporting them.

## Output Format (MANDATORY — verdict MUST be on the first line)
VERDICT: [SOLID|PARTIAL|FALSE] (for hypothesis) or [SOLID|NEEDS_ADJUSTMENT|WRONG_APPROACH] (for plan)

## Alternative Hypotheses
1. [alternative] — supported by: [evidence] — ruled out by: [evidence or "needs data"]
2. [alternative] — supported by: [evidence] — ruled out by: [evidence or "needs data"]

## Findings
- [finding] → [evidence location] → [why this undermines the hypothesis/plan]

## Recommendation
[If SOLID: proceed. If PARTIAL: re-investigate with these constraints. If FALSE: discard, start from these alternatives.]
`
})
```

**Evidence selection rule:** Pass ALL investigated evidence locations to the subagent — including evidence that did NOT support the leading hypothesis. The subagent decides what is relevant, not the parent agent. Passing only supporting evidence is framing that undermines isolation.

**Fallback:** If subagent output does not begin with a valid `VERDICT:` line, treat it as `PARTIAL` and extract whatever findings are present.

**Token budget:** Keep the subagent prompt under ~2000 tokens. The subagent needs context window for reading evidence files and reasoning.

### Session State Tracker Template

Update at each phase transition. Keep in conversation as a markdown block:

```markdown
### STATE TRACKER
- **Phase:** [current phase name and number]
- **Iteration:** [N of max]
- **Hypotheses:** [H1: status | H2: status | H3: status]
- **Key evidence:** [file:line or source — brief refs only, not full content]
- **Subagent verdicts:** [Phase 2: SOLID/PARTIAL/FALSE | Phase 5.2: ...]
- **User decisions:** [SKIP/GO/CORRECT/RETHINK — if any]
- **Skipped phases:** [list any, or "none"]
```

For long investigations spanning sessions, output this tracker to `state/investigations/` as a recoverable file.

### User Skip/Abort Commands

These are first-class commands, not error states. The agent must recognize and honor them at any point:

| Command | Effect | Recorded as |
|---|---|---|
| `SKIP ADVERSARIAL` | Bypass adversarial subagent phases (Phase 2, Phase 5.2) | `[ADVERSARIAL PHASE SKIPPED BY USER]` |
| `SKIP TO PLAN` | Jump to fix/resolution planning, bypass verify + attribute. **Mandatory:** run grading pass on all claims before proceeding (enforces D-004 gate even when phases are skipped). | `[PHASES SKIPPED: verify, attribute]` |
| `ABORT` | Stop skill entirely, output current findings in handoff format | `[INVESTIGATION ABORTED BY USER]` |

### Sync Propagation Note

Add to the top of each skill protocol:

```markdown
<!-- Shared patterns synced from prompts/shared-investigation-foundations.md on YYYY-MM-DD. Update source first, then propagate to all 4 protocols. -->
```

The four hypothesis-driven protocols carry the note above verbatim. `downstream` carries a different note (it adapts, rather than syncs, these tables) — see its top-of-file comment. When editing the grading/confidence tables, update those 4 **and** manually port the table change into `prompts/downstream.md`.

The **Prior-Art / Doc-Sweep Pointer** (above) is also carried in all five protocols — but **frame-adapted, not verbatim**: each skill uses its own `<frame>` parenthetical per the pointer table. Treat it like the `downstream` table-port rule: when the canonical pointer changes, update all five inline copies, preserving each skill's `<frame>`. This count ("4 verbatim + downstream adapts") is unchanged by the pointer; the pointer simply has five frame-adapted homes.
