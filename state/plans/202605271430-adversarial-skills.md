# PLAN: Adversarial Investigation & Review Skills
Status: draft
Parent: none
Supersedes: none
Roadmap task: standalone

## Context

Build four interconnected Claude Code skills for rigorous investigation, debugging, troubleshooting, and plan review. All skills enforce evidence-graded, uncertainty-intolerant analysis with adversarial verification phases executed in isolated subagent contexts to prevent anchoring bias.

The skills form a natural pipeline:
- **Investigate** gathers evidence and eliminates unknowns (upstream feeder)
- **Debug RCA** traces code bugs to structural root causes (code-specific)
- **Troubleshoot** traces any problem to root causes (domain-agnostic)
- **Adversarial Review** stress-tests plans/proposals before execution (downstream gate)

Each skill produces two files:
- Full protocol: `prompts/<skill-name>.md` — complete behavioral contract (self-contained; shared patterns inlined)
- Skill registration: `.claude/skills/<skill-name>/SKILL.md` — frontmatter + trigger conditions

8 skill files + 1 design-time reference = 9 files total.

### Source Material
- Existing DebugRCA protocol: `specific_framework/DebugRCA/README.md`
- Existing framework patterns: `.claude/agents/` stubs + `prompts/` protocols
- Existing skill pattern: `.claude/skills/doc/SKILL.md`
- Research synthesis from 6 parallel research agents covering: RCA methodologies, adversarial AI patterns, plan verification techniques, LLM debugging implementations, investigation methodologies, deep research agent patterns (~250 sources)

### Adversarial Review History

**Round 1 (v1 → v2):** Verdict: NEEDS ADJUSTMENT. Found 4 blockers, 6 major, 7 minor.
Key fixes applied: clarified subagent mechanism (D-002), specified shared foundations file path, defined trigger conditions (D-009), removed false Troubleshoot→Debug dependency, added handoff schema (D-008), cut experience bank, added DebugRCA deprecation step.

**Round 2 (v2 → v3):** Verdict: NEEDS ADJUSTMENT. Found 3 blockers, 6 major, 7 minor. Crucially, Round 2 found an entirely different CLASS of issues (operational mechanics, systems thinking, Chesterton's Fence violations) that Round 1 missed.
Key fixes applied (see below for details):

**Round 3 (v3 → v4):** Verdict: NEEDS ADJUSTMENT (one false blocker, valid refinements). The adversary's headline finding — "Agent tool doesn't exist" — was factually wrong (it searched ToolSearch which indexes deferred tools; Agent is a core tool used 8+ times during plan creation). This demonstrates the exact confabulation risk the skills are designed to counter. However, Round 3 produced genuinely valuable findings at the refinement level:
- **B-3 R3 (350-line target unvalidated):** Valid. Content math shows ~410 lines minimum for Debug RCA. Fixed — raised target to ≤450 lines. Phase 1 will validate by drafting one protocol before the others.
- **M-4 R3 (UNRESOLVED state undefined):** Valid. Fixed — D-014 defines UNRESOLVED output format and user options.
- **M-5 R3 (evidence grading has no enforcement gate):** Valid. Fixed — D-004 now includes mandatory graded summary before any phase transition to structured output.
- **M-6 R3 (research citations not stored):** Valid. Fixed — Phase 1 deliverables now include a citation index in `KB/`.
- **m-3 R3 (Chesterton's Fence in wrong phase):** Valid. Fixed — moved from INVERSION to UNDERSTAND in Adversarial Review.
- **m-7 R3 (original DebugRCA is platform-agnostic):** Valid. Fixed — D-015: original DebugRCA kept as portable standalone, NOT deprecated. New skills are Claude Code-specific additions, not replacements.
- **Cognitive load analysis:** Valuable insight that techniques most likely dropped under context pressure are the differentiators. Fixed — D-016 requires critical differentiators front-loaded in protocol structure.

Round 3 severity was declining (1 real blocker vs 3 in R2 vs 4 in R1). Findings were refinement-level, not architectural.

**Round 4 (v4 → v5):** Verdict: **SOLID** (first round to pass). Found 0 blockers, 4 major, 7 minor. Findings were refinement and UX-level. Scenario walkthroughs were the most valuable contribution.
Key fixes applied:
- **M-1 R4 (SKILL.md contents unspecified):** Valid. Fixed — D-017 specifies SKILL.md is a stub (frontmatter + "read prompts/X.md"), following the agent pattern. Protocols live in `prompts/` as the single maintainable source.
- **M-2 R4 (subagent prompt template missing):** Valid. Fixed — Phase 1 deliverables now include a concrete, copy-pasteable Agent tool invocation template with placeholders.
- **M-3 R4 (Phase 6 tests untestable):** Valid. Fixed — Phase 6 reframed as manual validation checklist with specific user actions and observable outcomes.
- **M-4 R4 (400-line target still tight):** Valid. Fixed — raised to ≤450 lines. Phase 1 validates by drafting Debug RCA first (most complex).
- **Scenario insights (simple bug overkill):** Noted for v2 — complexity triage at invocation is the #1 UX gap. Current plan defers to user via D-011 skip commands.
- **Scenario insights (hybrid code+infra):** Noted for v2 — trigger boundary for mixed-domain incidents. Troubleshoot should note it CAN read code if available.
- **Subtle: evidence selection as framing:** Valid. Fixed — D-002 now requires passing ALL investigated evidence locations to subagent, not just supporting ones.
- **Subtle: "list 3 contradictions" perverse incentive:** Valid. Fixed — changed to "list UP TO 3" — if fewer genuinely exist, list fewer. Zero is valid with justification.
- **D-011 × D-004 interaction:** Valid. Fixed — SKIP TO PLAN triggers mandatory grading pass on all claims before proceeding to fix plan.
- **m-5 R4 (contradiction count):** Addressed above.

Key fixes applied for Round 2:
- **B-1 R2 (context budget):** Valid. Redesigned — shared foundations becomes a *design-time reference* used while writing protocols, not a runtime file. Each skill protocol inlines the ~30-50 lines of shared patterns it needs (evidence grading table, confidence scale, uncertainty rules). Some duplication, but reliable execution and no runtime dependency on reading a second file. Protocols target ≤350 lines each.
- **B-2 R2 (subagent output parsing):** Valid. Fixed — D-002 now specifies exact output format for subagents (verdict on first line, structured sections), and fallback behavior when output is malformed.
- **B-3 R2 (state file dropped):** Valid Chesterton's Fence violation. Fixed — D-010 adds session state tracking back. Each skill maintains a lightweight state tracker for recoverability.
- **M-2 R2 (Troubleshoot is a Debug clone):** Accepted tradeoff. Skills stay separate. Each protocol gets a sync note listing what must stay consistent.
- **M-3 R2 (E1-E6 on every claim kills velocity):** Valid. Fixed — D-004 revised: evidence grading applies at phase transitions (when claims enter hypotheses, ACH matrix, or final report), not during active investigation. During collection, just gather fast.
- **M-4 R2 (ACH overkill for binary code evidence):** Valid. Fixed — full ACH mandatory for Investigate and Troubleshoot. For Debug RCA, keep original's "minimum 2 alternatives with evidence for/against" and make full ACH optional for complex multi-hypothesis bugs.
- **M-5 R2 ("Consider the Opposite" is weak for LLMs):** Valid. Fixed — replaced with "list 3 pieces of evidence that CONTRADICT the leading hypothesis." More actionable, less hand-wavy. The adversarial subagent already covers genuine independent opposition.
- **M-6 R2 (no user abort):** Valid. Fixed — D-011 adds skip mechanisms. User can say SKIP ADVERSARIAL at any point; recorded in output as `[ADVERSARIAL PHASE SKIPPED BY USER]`.
- **Loop 3 (uncertainty blocker → false certainty):** Valid and insightful. Fixed — D-003 redesigned: the blocker doesn't ban hedging WORDS, it requires the agent to ACT on uncertainty. Three valid exits: (a) investigate further, (b) flag NEEDS EXTERNAL DATA, (c) explicitly mark claim with confidence level and evidence grade. Hedging language without action is the violation, not hedging language itself.

### Key Design Decisions

**D-001: Four separate skills, not one mega-skill.**
Why: Different entry points, different tooling, different evidence types. Debug needs git blame/file:line; Troubleshoot needs domain-agnostic evidence; Investigate is pure research; Adversarial Review is plan-focused. Forcing them into one skill would mean loading irrelevant protocol for every invocation.

**D-002: Adversarial phases use spawned subagents via the Agent tool with controlled context.**
Why: HCCA research (2025) confirmed session isolation is the #1 factor for effective adversarial review — more important than prompt engineering. The adversary receives ONLY the hypothesis/plan + evidence locations, NOT the reasoning chain that produced them.

Mechanism: The skill protocol instructs the main agent to use the `Agent` tool (available in Claude Code) to spawn a subagent. The prompt passed to the Agent tool contains ONLY: (a) the adversarial protocol to follow, (b) the hypothesis or plan to attack, (c) evidence file paths or locations to read. The subagent gets its own context window and cannot see the parent conversation. This is the same mechanism used to spawn research agents — proven to work.

Subagent output format (mandatory): The subagent's response MUST begin with a verdict line in the format `VERDICT: SOLID|PARTIAL|FALSE` (for investigation) or `VERDICT: SOLID|NEEDS_ADJUSTMENT|WRONG_APPROACH` (for plan review). Following sections use the headings: `## Alternative Hypotheses`, `## Findings`, `## Recommendation`. The parent agent parses the verdict line to determine loop action. If the subagent output does not begin with a valid VERDICT line, the parent treats it as PARTIAL and extracts whatever findings are present.

Anti-anchoring enforcement: The protocol explicitly lists what the Agent tool prompt MUST include and MUST NOT include. The main agent is responsible for constructing the prompt correctly. The subagent reads the evidence independently and forms its own assessment.

Evidence selection rule (Round 4 finding): The main agent MUST pass ALL investigated evidence locations to the subagent — including evidence that did NOT support the leading hypothesis. Passing only supporting evidence is itself a form of framing that undermines isolation. The subagent decides what is relevant, not the main agent.

**D-003: Uncertainty requires action, not just language policing.**
Why: LLMs have measured anchoring bias (Cohen's d = 1.19) and 15-20% hallucination rate without grounding. But banning hedging words creates a perverse incentive for false certainty — the agent says "IS" instead of "might be" to pass the blocker, even when evidence only supports "might be."

Mechanism: Before any phase exits, the agent reviews each claim for its evidence basis. Any claim that lacks E1-E3 evidence (direct observation, documented artifact, or corroborated report) triggers one of three actions:
1. **Investigate further** — chase the thread to get E1-E3 evidence
2. **Flag as NEEDS EXTERNAL DATA** — with specific data needed and why the agent cannot obtain it
3. **Explicitly mark with confidence level and evidence grade** — the claim stays, but its uncertainty is visible (e.g., "Plausible [E5-Inference]: based on code structure, this module likely handles X")

The violation is not hedging language — it is **hedging language without action**. An uncertain claim that is properly marked (confidence + evidence grade) is honest and useful. An uncertain claim presented as certain is dangerous. An uncertain claim left as vague "probably" with no grade is the thing being blocked.

**D-004: Evidence grading (E1-E6) at phase transitions, not during active collection.**
Why: Grading every intermediate observation during active investigation transforms the agent from investigator into documenter. Intelligence analysis (ICD 203, the source for this system) applies evidence grading to analytic judgments in finished products, not to every observation during collection.

When to grade: Evidence is graded when it enters a structured output — hypotheses in the ACH matrix, claims in the final report, findings in the handoff schema. During active Phase 1/Phase 2 investigation, the agent collects fast and grades later.

Enforcement gate: Before exiting any phase that produces structured output (ACH matrix, fix plan, final report, handoff), the agent must present a graded summary. Any claim without an evidence grade and confidence level cannot enter the next phase's structured output. This is a hard gate, not a suggestion.

Evidence grades:
| Grade | Meaning | Example |
|---|---|---|
| E1 — Direct observation | Agent verified through tool use | Read the file, ran the query, saw the output |
| E2 — Documented artifact | Exists in verifiable document/log | Stack trace, error log, git commit, email |
| E3 — Corroborated report | Multiple independent sources agree | Two people report same behavior; two docs confirm |
| E4 — Single-source report | One source, unverified | User says "it broke Tuesday" |
| E5 — Inference | Derived from reasoning, not direct evidence | "Based on the architecture, this module likely..." |
| E6 — Assumption | Taken as true without evidence | "Assuming the API returns valid JSON..." |

E5-E6 claims in final outputs must be explicitly marked and either upgraded through investigation or flagged as NEEDS EXTERNAL DATA.

**D-005: Per-claim confidence, not per-report confidence.**
Why: RLHF training causes systematic overconfidence. Whole-report confidence is meaningless. Each claim in structured outputs gets: Verified / Supported / Plausible / Speculative / Unknown. Confidence (evidence strength) is kept separate from likelihood (probability of conclusion). Adapted from ICD 203 intelligence standards.

**D-006: Debug RCA keeps code-specific tooling; Troubleshoot is the generic parallel.**
Why: Stripping git blame, file:line, Bash tools from Debug to make it generic would weaken the code-specific version. Better to have two skills that share the philosophical backbone but diverge on evidence types and tooling. Both protocols carry a sync note listing shared sections that must stay consistent when either is updated.

**D-007: Implementation prompt is an optional exit step, not a mandatory phase.**
Why: The RCA's real output is the verified fix plan. Generating a self-contained implementation prompt for handoff is a formatting concern. The skill asks "Generate implementation prompt?" after the GO gate. User decides.

**D-008: Handoff interface is the common currency between skills.**
Why: Skills should chain naturally. Each skill's final output follows a standard structure so it can be consumed by the next skill in the pipeline without reformatting.

Handoff schema (markdown):

```markdown
## Handoff: <skill-name> → <date>

### Findings
- [claim] — Evidence: [E1-E6 grade] — Confidence: [Verified/Supported/Plausible/Speculative/Unknown] — Source: [file:line / document / observation]

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

**D-009: Trigger conditions designed together to prevent overlap.**
Each skill has a distinct trigger domain. When invocations are ambiguous, the skill description guides Claude Code's skill matching.

| Skill | Trigger phrase | Domain | NOT for |
|---|---|---|---|
| `/investigate` | "research this", "investigate", "find out", "what's going on with", "deep dive into" | Any domain. Pure evidence gathering and analysis. No fix planning. | Bugs with known symptoms (use debug/troubleshoot). Plan review (use adversarial-review). |
| `/debug-rca` | "debug this", "find the bug", "root cause", "why is this broken" (in code context) | Code bugs. Requires a codebase. Uses git, file:line, code tools. | Non-code problems (use troubleshoot). Research questions (use investigate). |
| `/troubleshoot` | "troubleshoot", "figure out why", "diagnose" (non-code context) | Any non-code problem: system failures, process breakdowns, business issues, infrastructure. | Code bugs (use debug-rca). Pure research (use investigate). |
| `/adversarial-review` | "review this plan", "stress test", "proof this", "what could go wrong", "attack this proposal" | Plans and proposals. Takes a plan as input, destroys it. | Active investigation (use investigate/debug/troubleshoot). |

**D-010: Session state tracking for recoverability.**
Why: The original DebugRCA had a JSON state file (`state/rca/YYYYMMDDHHMM-rca.json`) for session recovery. The new skills are more complex (more phases, more loops, subagent spawning) and MORE likely to exhaust context. Dropping state tracking was a Chesterton's Fence violation.

Mechanism: Each skill maintains a lightweight state tracker as a markdown section in the conversation (not a separate file — avoids file I/O overhead during investigation). The state tracker is updated at each phase transition and contains:
- Current phase and step
- Iteration count (for loops)
- Hypothesis status (active/eliminated/confirmed)
- Key evidence collected so far (file:line or source references, not full content)
- Subagent verdicts received
- User decisions made

If the conversation is lost or context is compressed, the agent can reconstruct where it was from the most recent state tracker block. For long investigations that span sessions, the skill outputs a recoverable state to `state/rca/` or `state/investigations/` that the next session can load.

**D-011: User can skip or abort at any point.**
Why: A user at 2am debugging a production outage cannot be locked into a 12-phase protocol with no exit ramp. Reduced rigor must be visible but allowed.

Mechanism: The user can say at any point:
- `SKIP ADVERSARIAL` — bypass adversarial subagent phases. Recorded as `[ADVERSARIAL PHASE SKIPPED BY USER]` in output.
- `SKIP TO PLAN` — jump from investigation directly to fix/resolution planning, bypassing verify and attribute. Recorded as `[PHASES SKIPPED: verify, attribute]`. **Mandatory grading pass:** before proceeding to fix plan, the agent must grade all accumulated claims (evidence grade + confidence level). This prevents SKIP TO PLAN from silently bypassing the D-004 enforcement gate.
- `ABORT` — stop the skill entirely and output whatever has been collected so far in handoff format.

The skill protocols treat these as first-class commands, not error states. Skipped phases are noted in the output so the reduced rigor is transparent.

**D-012: ACH matrix is domain-adaptive.**
Why: ACH was designed for intelligence analysis where evidence is ambiguous and interpretable multiple ways. In code debugging, most evidence is binary (a line executes or it doesn't). A full ACH matrix for every code bug is overhead without proportionate value.

Mechanism:
- **Investigate and Troubleshoot:** Full ACH matrix mandatory (evidence IS ambiguous in these domains).
- **Debug RCA:** Minimum 2 alternative hypotheses with evidence for/against each (the original DebugRCA's approach). Full ACH matrix optional — use when 3+ hypotheses survive initial discrimination and evidence is genuinely ambiguous.
- **Adversarial Review:** No ACH matrix (not hypothesis-based; uses pre-mortem/FMEA/inversion instead).

**D-013: Shared patterns inlined, not loaded from external file.**
Why (Round 2 finding): A runtime dependency on reading `prompts/shared-investigation-foundations.md` at every invocation creates an unverifiable enforcement gap. If the agent skips the file read (context pressure, model behavior), ALL shared standards silently degrade. Additionally, the shared file would be 800-1500 lines — too large to hold alongside the skill protocol AND actual investigation content.

Mechanism: The shared foundations file (`prompts/shared-investigation-foundations.md`) exists as a **design-time reference** — the authoritative source of truth for shared patterns, used while writing and updating protocols. Each skill protocol **inlines** the specific shared patterns it needs (~30-50 lines: evidence grading table, confidence scale, uncertainty action rules, subagent output format). This means some duplication across protocols, but each protocol is self-contained and works without reading any other file.

When shared foundations are updated, the sync must be propagated to all 4 skill protocols. Each protocol carries a header note: `<!-- Shared patterns synced from prompts/shared-investigation-foundations.md. Update source first, then propagate. -->`.

Target protocol sizes: ≤450 lines per skill protocol (validated by content math in Round 3 — 350 was aspirational, 400 is realistic). Phase 1 will draft one full protocol (Debug RCA, the most complex) to validate size before writing the others. Shared foundations reference: no size limit (it's not loaded at runtime).

**D-014: UNRESOLVED state has defined output and user options.**
Why (Round 3 finding): When the investigate↔adversarial loop hits max 3 iterations without convergence, "surface UNRESOLVED to user" is not an actionable instruction.

UNRESOLVED output format:
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

**D-015: Original DebugRCA kept as portable standalone.**
Why (Round 3 finding): The original at `specific_framework/DebugRCA/README.md` is platform-agnostic — usable in ChatGPT, other LLM tools, or as a human-readable procedure. The new skills are Claude Code-specific (depend on `.claude/skills/`, Agent tool, SKILL.md registration). Deprecating the portable version in favor of platform-locked versions reduces utility.

Mechanism: The original DebugRCA stays as-is with a header noting: "This is the portable, platform-agnostic version. For Claude Code integration with subagent isolation and skill chaining, see `/debug-rca` skill." Phase 6 adds this header instead of a deprecation notice.

**D-016: Critical differentiators front-loaded in protocol structure.**
Why (Round 3 cognitive load analysis): Under context pressure, LLMs drop instructions from the middle of long contexts first ("lost in the middle" effect). The techniques most likely to be dropped are precisely the ones that differentiate these skills from the original — evidence grading, contradiction listing, anti-confabulation checks, uncertainty action audit. If these are buried in Phase 4+ of the protocol, they'll be the first casualties.

Mechanism: Each skill protocol structures its phases so that:
1. The first section after the preamble is the **Shared Standards** block (~30-50 inlined lines) — evidence grading, confidence scale, uncertainty action rules. These are the differentiators.
2. Phase-specific instructions follow, with checkpoint/audit steps embedded IN each phase (not in a separate late-protocol phase).
3. The state tracker update is integrated into each phase's closing step, not a separate bookkeeping phase.

This means the critical differentiators are at the TOP of the protocol (best attention) and reinforced WITHIN each phase (distributed, not concentrated).

**D-017: SKILL.md is a stub pointing to prompts/, following the agent pattern.**
Why (Round 4 finding): The existing `doc` skill inlines its full protocol in SKILL.md (137 lines). The existing agents use stubs that point to `prompts/`. With protocols targeting 450 lines, inlining in SKILL.md would create very large skill files. The agent pattern (small stub + full protocol in prompts/) is more maintainable and keeps protocols editable in a single location.

Mechanism: Each `.claude/skills/<name>/SKILL.md` contains:
```yaml
---
name: <skill-name>
description: "<trigger description from D-009>"
---
```
Followed by: `**BEFORE ANYTHING ELSE:** Read prompts/<skill-name>.md — it contains your complete protocol. Follow it exactly.`

This is the same pattern as `.claude/agents/archeolog-prospector.md`. The full protocol lives in `prompts/` and is the single source of truth.

### Research-Backed Techniques Incorporated

**Across all skills (inlined in each protocol):**
- Evidence grading E1-E6 at phase transitions (intelligence analysis + journalism)
- Uncertainty action requirement (not language policing)
- Self-prompting at every step (StateAct, +10-30% over ReAct)
- Per-claim confidence scale (ICD 203 adapted)
- Convergent evidence stopping criteria (consilience)
- Anti-confabulation check ("has evidence been produced by reasoning, not observation?")
- Enhanced loop termination (max iterations + fingerprinting + no-progress detection)
- Diagnostic Timeout / Checkpoint (cognitive forcing, emergency medicine)
- "List up to 3 contradicting evidence items" at checkpoints (replaces weaker "consider the opposite"; zero valid with justification)
- Session state tracking for recoverability
- User skip/abort mechanisms

**Investigate-specific:**
- Evidence sufficiency conditions defined BEFORE investigating (Don't Stop Early, Salesforce 2025)
- Full ACH matrix mandatory (hypothesis × evidence, C/I/N, diagnosticity)
- FAIR-RAG gap-audit loop (confirmed vs. missing vs. contradicting)
- Self-RAG gating on evidence (relevant? supports claim? useful?)
- Contradiction-to-Consensus (retrieve evidence FOR and AGAINST)
- Investigation frontier with information foraging heuristics
- Patch-leaving heuristic for diminishing-returns threads
- Key Assumptions Check (CIA tradecraft)
- Quality of Information Check on each evidence item
- Max iteration cap on converge/loop cycle

**Debug RCA-specific:**
- Phase 0.5 Change Analysis (git log/diff before deep investigation)
- IS/IS-NOT matrix (Kepner-Tregoe) before hypothesis generation
- Minimum 2 alternative hypotheses (full ACH optional for complex cases)
- Counterfactual reasoning on suspect lines (CADET/CounterFault)
- Disproof step on adversarial findings (Anthropic <1% false positive pattern)
- Barrier inventory (what safeguards failed?)
- STPA control structure for interaction bugs (Google SRE adoption)

**Troubleshoot-specific:**
- Same backbone as Debug RCA but domain-agnostic evidence types
- Full ACH matrix mandatory (essential when evidence is less structured than code)
- IS/IS-NOT matrix (even more critical in fuzzier domains)
- Domain-adaptive attribution (organizational structure, process docs, system architecture)
- Universal Change Analysis ("what changed between working and broken?")
- Sync note referencing Debug RCA for shared sections

**Adversarial Review-specific:**
- Pre-mortem with "already failed" framing (30% more failure reasons, Klein)
- FMEA per plan step (failure mode, effect, severity, occurrence, detectability → RPN)
- Design by Contract (precondition/postcondition chaining between steps)
- Inversion thinking ("how to guarantee failure?")
- Chesterton's Fence (understand why current approach exists before changing)
- Assumption mapping (importance × evidence matrix)
- ATAM-style sensitivity/tradeoff point identification
- Blast radius / consequence mapping (1st/2nd/3rd order)
- Disproof step on adversarial findings
- Systems thinking (identify reinforcing feedback loops the plan creates)

---

## Phase 1: Shared Foundations (Design-Time Reference)

Intent: Write the authoritative reference document for shared patterns. This file is used while WRITING skill protocols, not loaded at runtime. It is the single source of truth — when updating shared patterns, update this file first, then propagate to the 4 skill protocols.

Depends on: nothing

Deliverables:
- `prompts/shared-investigation-foundations.md` — design-time reference document

Contents:
- Evidence grading definitions (E1-E6) with examples per grade
- Per-claim confidence scale with usage guidelines
- Uncertainty action protocol (the three valid exits)
- Evidence grading enforcement gate specification
- Anti-confabulation check protocol
- Self-prompting template (objective + hypothesis status + unresolved count)
- Diagnostic Timeout checklist template
- ACH matrix template with diagnosticity analysis
- Convergent evidence stopping criteria (the 4 tests: convergence, elimination, explanatory completeness, predictive power)
- Loop termination rules (max iterations + fingerprinting + no-progress)
- UNRESOLVED output format and user options (from D-014)
- Handoff output schema (the markdown template from D-008)
- Subagent spawning protocol: exact Agent tool invocation pattern, mandatory output format, what to include/withhold, anti-anchoring rules, fallback for malformed output
- Session state tracker template
- User skip/abort command definitions
- Citation index of research sources backing key design decisions

Additional Phase 1 deliverables:
- `KB/KB_research_citations.md` — index of research sources with URLs, organized by technique. Ensures claims like "Cohen's d = 1.19" and "session isolation is the #1 factor" are verifiable.
- Concrete Agent tool invocation template with placeholders for adversarial subagent spawning. This template gets inlined into each skill protocol. Must include: prompt structure, evidence selection instructions (pass ALL locations, not just supporting), mandatory VERDICT output format, and token budget guidance.

---

## Phase 2: Investigate Skill

Intent: Build the deep investigation skill — the upstream feeder for all other skills. Generic "eliminate all unknowns" engine. Takes a question or problem, produces fully-evidenced analysis with per-claim confidence. Keeps digging as long as unknowns remain.

Depends on: Phase 1 (shared foundations written → inline into protocol)

Deliverables:
- `prompts/investigate.md` — full self-contained protocol (≤450 lines, shared patterns inlined)
- `.claude/skills/investigate/SKILL.md` — skill registration

Phase structure in the protocol:
- Phase 0: SCOPE — define question, set evidence sufficiency conditions BEFORE investigating, decompose into sub-questions with explicit checklists
- Phase 1: HYPOTHESIZE — 3-5 competing explanations, framework-driven (causal/systemic/temporal/structural), include 1 "unlikely but high-impact", Key Assumptions Check on each
- Phase 2: INVESTIGATE — design searches that discriminate between hypotheses (Strong Inference), retrieve evidence FOR and AGAINST each hypothesis (Contradiction-to-Consensus), maintain investigation frontier (ranked leads), patch-leaving heuristic, Quality of Information Check, FAIR-RAG gap-audit (confirmed vs. missing vs. contradicting)
- Phase 3: EVALUATE — ACH matrix (mandatory; hypothesis × evidence, C/I/N), select by fewest inconsistencies, identify diagnostic evidence
- Phase 4: CHECKPOINT — Diagnostic Timeout checklist, list up to 3 contradicting evidence items (fewer is valid if fewer genuinely exist; zero requires explicit justification), anti-confabulation audit, uncertainty action audit (any ungraded E5/E6 claims?), update state tracker
- Phase 5: CONVERGE or LOOP — apply 4 stopping criteria; ALL must pass or return to Phase 2. Max iteration cap to prevent infinite loops.
- Phase 6: REPORT — per-claim confidence + evidence grade on all claims, eliminated hypotheses with what eliminated them, remaining uncertainties, what future information would change conclusion, handoff-format output

---

## Phase 3: Debug RCA Skill

Intent: Build the code-specific root cause analysis skill. Evolves the existing DebugRCA protocol. Keeps all code-specific tooling (git blame, file:line, Bash, Read, Grep). Adversarial phases spawn isolated subagents.

Depends on: Phase 1 (shared foundations written → inline into protocol)

Deliverables:
- `prompts/debug-rca.md` — full self-contained protocol (≤450 lines, shared patterns inlined)
- `.claude/skills/debug-rca/SKILL.md` — skill registration
- `<!-- Sync note -->` header referencing shared foundations + Troubleshoot protocol

Phase structure in the protocol:
- INPUT: Bug description, observable data, suspect files, reproduction, scope (all required)
- Phase 0.5: CHANGE ANALYSIS — git log/diff on suspect files, config changes. Cheap first pass.
- Phase 1: INVESTIGATE — IS/IS-NOT matrix → hypothesis generation (3-5, must explain every IS and IS-NOT) → causal chain with file:line evidence → counterfactual reasoning → list up to 3 contradicting evidence items (fewer is valid if fewer genuinely exist; zero requires explicit justification) → uncertainty action audit → update state tracker
- Phase 2: ADVERSARIAL DESTROY — **spawned subagent** (hypothesis + evidence locations ONLY; NOT reasoning chain). Subagent: reads evidence independently → 2+ alternatives → optional ACH matrix for complex cases → disproof step → `VERDICT: SOLID|PARTIAL|FALSE` on first line
- Phase 2→1 LOOP: PARTIAL/FALSE → re-investigate with findings. Max 3 iterations. Unresolved after 3 → surface to user.
- Phase 3: VERIFY — strictly read-only. Raw data only. Write required → REQUIRES MANUAL VERIFICATION.
- Phase 4: ATTRIBUTE — git blame, classify: our code / upstream / missing feature / interaction.
- Phase 5.0: FIX PLAN — exact code changes, tests, verification commands, forbidden actions
- Phase 5.1: IMPACT — consumers, edge cases, barrier inventory, STPA (if interaction bug)
- Phase 5.2: ADVERSARIAL PLAN REVIEW — **spawned subagent** (fix plan + impact ONLY; NOT investigation history). → destruction questions → disproof step → `VERDICT: SOLID|NEEDS_ADJUSTMENT|WRONG_APPROACH`
- Phase 5.3: USER GATE — GO / CORRECT / RETHINK
- Phase 6 (optional): IMPLEMENTATION PROMPT → `state/plans/YYYYMMDDHHMM-rca-<slug>.md`

User can SKIP ADVERSARIAL, SKIP TO PLAN, or ABORT at any point.

---

## Phase 4: Troubleshoot Skill

Intent: Domain-agnostic root cause analysis. Same adversarial backbone as Debug RCA, generalized evidence types. Works for business problems, system failures, process breakdowns, infrastructure issues.

Depends on: Phase 1 (shared foundations written → inline into protocol)

Deliverables:
- `prompts/troubleshoot.md` — full self-contained protocol (≤450 lines, shared patterns inlined)
- `.claude/skills/troubleshoot/SKILL.md` — skill registration
- `<!-- Sync note -->` header referencing shared foundations + Debug RCA protocol

Phase structure in the protocol:
- INPUT: Problem description, observable symptoms, affected systems/areas, timeline, scope
- Phase 0.5: CHANGE ANALYSIS — what changed between working and broken? Timelines, deployments, personnel, process, external events.
- Phase 1: INVESTIGATE — IS/IS-NOT matrix → hypothesis generation (3-5) → causal chain with evidence grading → counterfactual reasoning → list up to 3 contradicting evidence items (fewer is valid if fewer genuinely exist; zero requires explicit justification) → uncertainty action audit → update state tracker
- Phase 2: ADVERSARIAL DESTROY — **spawned subagent** → ACH matrix (mandatory) → disproof step → `VERDICT: SOLID|PARTIAL|FALSE`
- Phase 2→1 LOOP: Max 3 iterations.
- Phase 3: VERIFY — read-only from domain-appropriate sources.
- Phase 4: ATTRIBUTE — organizational ownership. Classify: human error / process failure / system defect / external factor / interaction.
- Phase 5.0: RESOLUTION PLAN — what, who, resources, timeline
- Phase 5.1: IMPACT — stakeholders, barrier inventory, consequence mapping
- Phase 5.2: ADVERSARIAL PLAN REVIEW — **spawned subagent**
- Phase 5.3: USER GATE — GO / CORRECT / RETHINK
- Phase 6 (optional): HANDOFF DOCUMENT

User can SKIP ADVERSARIAL, SKIP TO PLAN, or ABORT at any point.

---

## Phase 5: Adversarial Review Skill

Intent: Standalone plan/proposal stress-testing. Takes any plan and adversarially destroys it before execution. The downstream gate.

Depends on: Phase 1 (shared foundations written → inline into protocol)

Deliverables:
- `prompts/adversarial-review.md` — full self-contained protocol (≤450 lines, shared patterns inlined)
- `.claude/skills/adversarial-review/SKILL.md` — skill registration

Phase structure in the protocol:
- INPUT: Plan/proposal (file path or inline). Codebase access if plan references code.
- Phase 1: UNDERSTAND — extract goals/assumptions/steps/dependencies/constraints, precondition/postcondition chain (DbC), assumption mapping (importance × evidence), Chesterton's Fence on every change (understand why current approach exists BEFORE accepting the change)
- Phase 2: PRE-MORTEM — "it failed catastrophically, why?" Multi-perspective (end user, ops, security, maintainer, on-call). Rate likelihood × severity.
- Phase 3: INVERSION — "how to GUARANTEE failure?" Reverse brainstorm.
- Phase 4: STRUCTURAL — FMEA per step (→ RPN). Precondition/postcondition chain verification. Invariant check.
- Phase 5: IMPACT — consumers, 1st/2nd/3rd order consequences, blast radius, sensitivity/tradeoff points, feedback loops.
- Phase 6: ADVERSARIAL DESTROY — **spawned subagent** (plan + findings from Phases 2-5 as factual inputs; NOT reasoning process). 7 mandatory destruction questions. Disproof step. `VERDICT: SOLID|NEEDS_ADJUSTMENT|WRONG_APPROACH`.
- Phase 7: VERDICT + USER GATE — all findings classified BLOCKER/MINOR/COSMETIC with evidence grade + confidence. GO / CORRECT / RETHINK.

User can SKIP ADVERSARIAL or ABORT at any point.

---

## Phase 6: Integration, Migration & Verification

Intent: Verify all four skills work individually and chain together. Deprecate old DebugRCA. Update documentation.

Depends on: Phases 2-5

Manual validation checklist (these cannot be automated — skill matching and subagent spawning require interactive verification):

- [ ] **Trigger test:** Start fresh conversation, type "debug this React bug" → verify debug-rca protocol's INPUT collection activates
- [ ] **Trigger test:** Type "troubleshoot why our deploys are failing" → verify troubleshoot protocol activates
- [ ] **Trigger test:** Type "investigate what's going on with our API latency" → verify investigate protocol activates
- [ ] **Trigger test:** Type "review this migration plan" → verify adversarial-review protocol activates
- [ ] **Negative trigger:** Type "troubleshoot this code bug" → observe which skill activates (boundary test)
- [ ] **Integration:** Run investigate to completion, feed handoff output to debug-rca as context → verify debug-rca can consume the findings table
- [ ] **Integration:** Run debug-rca to Phase 5.3 GO, invoke adversarial-review on the fix plan → verify plan is consumed correctly
- [ ] **Subagent:** During any skill's adversarial phase, verify Agent tool spawns successfully, subagent output begins with VERDICT line, parent agent correctly parses verdict and takes loop action
- [ ] **Skip test:** Mid-investigation, say SKIP ADVERSARIAL → verify phase is bypassed and output records the skip
- [ ] **Abort test:** Mid-investigation, say ABORT → verify partial findings output in handoff format

Other deliverables:
- Update `specific_framework/DebugRCA/README.md` — add header: "This is the portable, platform-agnostic version. For Claude Code integration with subagent isolation and skill chaining, see `/debug-rca` skill at `prompts/debug-rca.md`." (NOT deprecated — kept as standalone per D-015)
- Update `KB/KB_index.md` with entries for all 4 skills + shared foundations + citation index
- Update CLAUDE.md framework structure section if needed
- Verify all protocols are ≤450 lines (hard cap — if any exceed, trim techniques by value-add priority from Round 3's analysis)
- Commit all files
