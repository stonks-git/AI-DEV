<!-- Portable protocol: iterative downstream -> adversarial -> edit loop that hardens an artifact -->
<!-- until an adversarial reviewer accepts it (VERDICT: SOLID). Executed by hand by an orchestrating -->
<!-- agent; the two critics run as SEPARATE background agents (fresh context), not inline skills. -->

# Downstream -> Adversarial Review Loop

You are the **orchestrator**. Your job is to iteratively harden a target artifact by looping two
critics over it and applying their fixes, **without asking the user to re-prompt between passes**,
until the adversarial finds no more **blockers** (`VERDICT: SOLID`, or only non-blocker suggestions
remain — which are reported to you, not applied) — or a 12-pass safety cap.

This is the **evaluator-optimizer** pattern (Anthropic, *Building Effective Agents*): a generator
revises, a distinct evaluator critiques, loop until the evaluator is satisfied. Here **you** are the
generator (you apply the edits), and the two critics are the evaluator.

## Why the critics must be SEPARATE background agents

Self-refinement degrades when a model grades **its own** output in **its own** context (self-bias).
You avoid this entirely by running each critic as a **fresh, isolated background agent** — a
different context from the one applying the edits. So:

- **DO** spawn each critic with the `Agent` tool (`subagent_type: downstream` /
  `subagent_type: adversarial-review`), a new background agent every pass.
- **DO NOT** run the `/downstream` or `/adversarial-review` skills inline in your own context —
  that would collapse critic and author into one context and reintroduce self-bias.

## Input

- **Artifact** — a path to the text file to harden (plan / report / proposal / spec / message).
- **Goal** — one line on what the artifact is meant to achieve. If not given, infer it from the
  artifact and state your inference.

The **original file is never modified.** All edits are written to numbered version copies
`<name>_vNNN.md` **in the same folder** as the original, where `<name>` is the original artifact's
filename without its extension (e.g. `foo.md` → `foo_v001.md`).

## The Loop (max 12 passes)

Let `CURRENT` = the original artifact on pass 1; thereafter `CURRENT` = the latest `vNNN` you wrote.

For each pass `N` = 1, 2, … up to 12:

1. **Downstream (background agent).** Spawn `Agent(subagent_type: "downstream")` on `CURRENT`.
   Give it the artifact and what is changing; tell it it is running **headless** (no user to ask, so
   it proceeds on what you give it) and that it must **NOT spawn any sub-agents of its own** — it does
   its whole analysis in its own single context. It returns an **Impact Map** — the coupling /
   blast-radius (code *and* prose: consumers, dependents, assumptions others rest on). **Capture its
   returned text — that is the Impact Map; hold it for step 2.**

2. **Adversarial (background agent).** Spawn `Agent(subagent_type: "adversarial-review")` and give
   it **the WHOLE `CURRENT` artifact PLUS the Impact Map from step 1 as ammunition.** Tell it it is
   running **headless** (return its `VERDICT:` line + findings, do **not** wait on a user gate) and
   that it must **NOT spawn any sub-agents of its own** — it does its whole critique in its own single
   context. It returns a **verdict** and, if not solid, its **findings**.

3. **Sort the findings — blockers vs. the rest.** A finding is a **blocker** if *the artifact does
   not work, is incorrect, or breaks without the fix* — judge by that **functional test, not the
   critic's severity label.** Everything else (improvements, style, robustness, clarity — anything the
   artifact works correctly without) is a **non-blocker**. The loop **auto-applies only blockers**;
   **non-blockers are never auto-applied — collect them to report to the user.** Then, **in this order**:
   - **`WRONG_APPROACH` (check the verdict token FIRST, before the blocker test) → STOP the loop.** The
     artifact is judged fundamentally wrong; incremental editing can't repair it, so do not apply fixes.
     Then **spawn a background agent to research current SOTA best practices** for the problem this
     artifact addresses, and **present its suggested solution / redesign to the user** — together with
     the verdict, the findings, and `CURRENT`. The user decides the redesign; the loop does not continue.
   - **`SOLID`, or no blockers remain** (only non-blocker findings, or none) → **STOP.** `CURRENT` is
     the final version. Report it **plus the collected non-blocker suggestions for the user to decide
     on.** End.
   - **otherwise (there is at least one blocker) → go to step 4.**

4. **Apply + version.** **You (the orchestrator) apply only the blockers** from step 3 — the minimum
   edit that resolves each, nothing more — and write the result as **`<name>_v{N}.md`** in the same
   folder (pass 1 → `v001`, pass 2 → `v002`, …). Set `CURRENT` = that new file. Go to the next pass.

**Backstop.** If you reach **pass 12** without a `SOLID` verdict, stop. Report `<name>_v012.md` as
the best-so-far, clearly flagged **"did not converge in 12 passes."**

## Rules

- **Critics are fresh background agents every pass** — never the inline skill (see above).
- The adversarial **always** receives the whole current artifact **plus** the downstream Impact Map.
- **Blockers-only rule (the anti-drift guard):** the loop **auto-applies only blockers** — findings
  the artifact does not work / is incorrect / breaks without. **Every non-blocker finding is reported
  to the user, never auto-applied.** The critic will always surface "improvements"; you act only on
  what is functionally required and hand the rest to the user. Minimum edits, no opportunistic changes,
  no additions of your own.
- **Critics never nest.** Each critic is told (step 1/2) not to spawn its own sub-agents — its whole
  analysis runs in its single context.
- **Never modify the original file.** Every edit produces a new `vNNN` copy.
- **No scoring, no "best-version" logic.** You stop the instant the adversarial is satisfied; the
  version it blessed is the answer. The 12-pass cap is a safety net, not a target — healthy runs
  converge in a few passes.

## Output

Report: the **final version path**, the **pass count**, whether it **converged** (`SOLID` / no
blockers) or **hit the 12-pass cap**, and the **non-blocker suggestions** the critics raised that you
did NOT auto-apply (so the user can decide which, if any, to make). The deliverable is the final
`CURRENT`: if the artifact passed on pass 1 with no blockers, that is the **untouched original** (no
`vNNN` was written); otherwise it is the last `vNNN` you wrote.
