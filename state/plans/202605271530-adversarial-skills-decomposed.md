# PLAN: Adversarial Investigation & Review Skills (Decomposed)
Status: active
Parent: 202605271430-adversarial-skills.md
Supersedes: none
Roadmap task: standalone

## Context

Decomposed implementation plan for the 4 adversarial investigation skills. The parent plan (202605271430-adversarial-skills.md) contains the full design — 17 design decisions (D-001 through D-017), adversarial review history (4 rounds on design, 1 round on decomposition), research-backed technique inventory, and phase structures for all skills. This file contains only the atomic tasks.

**Implementing agents MUST read the parent plan before starting any task.** Tasks reference design decisions (D-XXX) by number — the parent plan contains the full specifications. The parent plan is at `state/plans/202605271430-adversarial-skills.md`.

### Adversarial Review History (Decomposed Plan)

**Round 1:** Verdict: NEEDS FIXES. Found 3 blockers, 6 major, 7 minor.
- **B-1 (Task 1.1 too large):** Valid. Split into 1.1a (core patterns) and 1.1b (structural templates).
- **B-2 (Task 6.4 unexecutable by agent):** Partially valid. Trigger testing requires user in fresh sessions. Split into agent-executable checks (6.4a) and user-executable test script (6.4b).
- **B-3 (directory creation implicit):** Valid. Made explicit in each SKILL.md task.
- **M-1 (Task 3.1 too large):** Valid. Split into 3.1a (structure) and 3.1b (content).
- **M-2 (citation verify weak):** Valid. Added URL validation requirement.
- **M-3 (inline block not delineated):** Valid. Task 1.1a now produces a marked INLINE BLOCK.
- **M-4 (CLAUDE.md update vague):** Valid. Specified exact addition.
- **M-5 (tag taxonomy ad-hoc):** Valid. Concrete tags specified in Task 1.3.
- **M-6 (git diff verify imprecise):** Valid. Tightened.
- **Coverage gaps (self-prompting, loop fingerprinting, anti-confabulation, diagnostic timeout):** Valid. Added technique-presence verification to protocol task Verify steps.
- **Framework gates (/doc, blueprint, KB):** Per user directive: /doc, blueprint update, and KB update all happen once at end of process in a single documentation task (6.5).
- **SKILL.md stubs need D-009 descriptions inlined:** Valid. Each stub task now includes the exact description text.

---

## Phase 1: Shared Foundations (Design-Time Reference) — DOING

Write the authoritative reference document and citation index. These are the source of truth that all 4 skill protocols will inline from.

- [ ] **1.1a: Write shared foundations — core patterns**
  Files: `prompts/shared-investigation-foundations.md` (create new), parent plan (read D-003, D-004, D-005)
  Do: Write the first half of the design-time reference document. This section contains the core differentiating patterns that get inlined into every protocol. Structure clearly with a marked INLINE BLOCK section — this exact text block will be copied verbatim into each skill protocol:
  ```
  <!-- === INLINE BLOCK START === -->
  [content here]
  <!-- === INLINE BLOCK END === -->
  ```
  The INLINE BLOCK must contain (target: 45-60 lines — content math shows 40 is too tight with formatting):
  - Evidence grading table E1-E6 with 1-line example per grade (from D-004)
  - Per-claim confidence scale: Verified/Supported/Plausible/Speculative/Unknown with 1-line usage guideline each (from D-005)
  - Uncertainty action protocol: the 3 valid exits, what constitutes a violation (hedging without action, not hedging words), enforcement note (from D-003)
  - Evidence grading enforcement gate: "Before exiting any phase that produces structured output, present a graded summary. Ungraded claims cannot enter next phase." (from D-004)
  - Anti-confabulation check: "Has any evidence been produced by reasoning rather than direct tool observation? If yes, downgrade to E5 or investigate further."
  - Self-prompting template: `"My objective is [X]. Current hypothesis: [Y]. Unresolved items: [N]. Next action should discriminate between hypotheses."` — use at the start of each phase.

  OUTSIDE the inline block (rest of the document — these are reference material, not inlined):
  - Detailed evidence grading definitions with 2 full examples per grade
  - Confidence scale detailed usage guidelines with edge cases
  - Uncertainty action protocol — expanded with examples of each valid exit
  Verify: File exists. Contains `<!-- === INLINE BLOCK START === -->` and `<!-- === INLINE BLOCK END === -->` markers. Inline block is 45-60 lines. Each of the 6 items above is present in the inline block (grep for: "E1", "E2", "E3", "E4", "E5", "E6", "Verified", "Supported", "Plausible", "Speculative", "Unknown", "enforcement gate", "anti-confabulation", "self-prompting").

- [ ] **1.1b: Write shared foundations — structural templates**
  Files: `prompts/shared-investigation-foundations.md` (append to existing)
  Do: Append the structural templates section to the foundations document. These are NOT inlined — they are reference material that implementing agents consult when writing protocol phases. Include:
  - Diagnostic Timeout checklist template (from parent plan, full version)
  - ACH matrix template: hypothesis × evidence grid, C/I/N marking, diagnosticity analysis instructions, selection rule (fewest inconsistencies)
  - Convergent evidence stopping criteria: the 4 tests with concrete examples of pass/fail for each
  - Loop termination rules: max iterations (default 3), fingerprinting (what repeated sequences look like), no-progress detection (concrete definition: "no new evidence, no hypothesis status change, no eliminated alternative in last N steps")
  - UNRESOLVED output format: full template from D-014
  - Handoff output schema: full template from D-008
  - Agent tool invocation template: concrete copy-pasteable example with `[PLACEHOLDER]` markers for hypothesis/plan/evidence. Include: evidence selection rule ("pass ALL investigated locations, including non-supporting"), mandatory VERDICT output format on first line, fallback ("if output does not begin with VERDICT:, treat as PARTIAL"), token budget guidance (~2000 tokens for subagent prompt)
  - Session state tracker template: full template from D-010
  - User skip/abort command definitions: SKIP ADVERSARIAL, SKIP TO PLAN (with mandatory grading pass note), ABORT — with exact recording format for each
  - Sync propagation note template with date placeholder
  Verify: File now contains both the INLINE BLOCK section (from 1.1a) and all structural templates. Grep for: "ACH matrix", "UNRESOLVED", "VERDICT:", "SKIP ADVERSARIAL", "state tracker", "handoff", "Agent tool", "convergent evidence", "loop termination", "diagnostic timeout". All must be present.

- [ ] **1.2: Write research citations index**
  Files: `KB/KB_research_citations.md` (create new), parent plan (read technique references)
  Do: Create citation index organized by technique. For each key claim in the parent plan, provide: technique name, source paper/article title, URL, year, and the specific claim it supports. Use WebSearch to verify the 5 most specific quantitative claims (Cohen's d = 1.19, 30% pre-mortem improvement, +10-30% StateAct, <1% false positive, session isolation #1 factor). Cover at minimum:
  - HCCA session isolation research (D-002)
  - LLM anchoring bias Cohen's d = 1.19 (D-003)
  - ICD 203 intelligence confidence standards (D-005)
  - Kepner-Tregoe IS/IS-NOT methodology
  - ACH (Richards Heuer, CIA)
  - Strong Inference (John Platt, 1964)
  - Pre-mortem 30% improvement (Gary Klein / Mitchell, Russo, Pennington 1989)
  - FMEA methodology
  - Design by Contract (Bertrand Meyer)
  - ATAM (CMU SEI)
  - StateAct self-prompting (+10-30% over ReAct)
  - FAIR-RAG / Self-RAG / Don't Stop Early (Salesforce 2025)
  - SWE-PRM process reward models
  - STAMP/STPA (Nancy Leveson / Google SRE adoption)
  - Anthropic code review disproof pattern (<1% false positive)
  - D3 framework (EACL 2026) / MAST taxonomy (NeurIPS 2025)
  - Cognitive forcing strategies (Croskerry)
  - Convergent evidence / consilience
  Verify: File exists. At least 18 citations. Each has: technique, source title, URL (or "no URL — textbook/standard"), year, claim supported. The 5 quantitative claims above have been verified via WebSearch (note verification result next to each).

- [ ] **1.3: Update KB_index.md and tag taxonomy**
  Files: `KB/KB_index.md`, `state/charter.json`
  Do: First, add these tags to `state/charter.json` `tag_taxonomy` array: `investigation`, `rca`, `adversarial`, `research`. Then add KB_index rows for Phase 1 deliverables:
  - `prompts/shared-investigation-foundations.md` — tags: `investigation` — load: `on-demand`
  - `KB/KB_research_citations.md` — tags: `research` — load: `on-demand`
  Verify: Tags `investigation`, `rca`, `adversarial`, `research` exist in `state/charter.json` `tag_taxonomy`. KB_index has 2 new rows with correct tags.

---

## Phase 2: Investigate Skill — DOING

Build the deep investigation skill. First skill written — validates protocol structure, inline block, and size target.

- [ ] **2.1: Write investigate protocol**
  Files: `prompts/investigate.md` (create new), `prompts/shared-investigation-foundations.md` (read — copy INLINE BLOCK verbatim), parent plan (read Phase 2 section for phase details)
  Do: Write the full self-contained protocol for the Investigate skill. Structure per D-016 (shared standards block first, checkpoint/audit embedded in each phase, state tracker integrated into phase closings).
  1. Copy the INLINE BLOCK from `shared-investigation-foundations.md` (between the START/END markers) verbatim into the protocol's Shared Standards section.
  2. Write all phases from parent plan Phase 2:
     - Preamble: skill identity, when to use, when NOT to use (NOT for: bugs with known symptoms → use /debug-rca or /troubleshoot; plan review → use /adversarial-review), tools available (all tools including WebSearch, WebFetch, Read, Grep, Bash, Agent)
     - Phase 0: SCOPE (evidence sufficiency conditions BEFORE investigating, sub-question decomposition with checklists)
     - Phase 1: HYPOTHESIZE (3-5 competing, framework-driven: causal/systemic/temporal/structural, 1 unlikely-but-high-impact, Key Assumptions Check)
     - Phase 2: INVESTIGATE (Strong Inference discriminating searches, Contradiction-to-Consensus, investigation frontier, patch-leaving heuristic, Quality of Information Check, FAIR-RAG gap-audit, Self-RAG gating)
     - Phase 3: EVALUATE (ACH matrix MANDATORY, diagnosticity analysis)
     - Phase 4: CHECKPOINT (Diagnostic Timeout checklist, up to 3 contradictions — zero valid with justification, anti-confabulation audit, uncertainty action audit, state tracker update)
     - Phase 5: CONVERGE or LOOP (4 stopping criteria — all must pass; max iteration cap; loop fingerprinting; no-progress detection; UNRESOLVED format if cap hit)
     - Phase 6: REPORT (per-claim confidence + evidence grade, eliminated hypotheses, remaining uncertainties, handoff format)
  3. Add skip/abort commands section.
  4. Add sync note header: `<!-- Shared patterns synced from prompts/shared-investigation-foundations.md on YYYY-MM-DD. Update source first, then propagate. -->`
  Target: ≤450 lines.
  Verify: File exists. ≤450 lines (`wc -l`). INLINE BLOCK section matches source (`diff` the shared standards section against the INLINE BLOCK in foundations — must be identical). All 7 phases present (grep for "Phase 0" through "Phase 6"). Sync note header present. "when NOT to use" section present. Technique presence: grep for "FAIR-RAG", "Self-RAG", "patch-leaving", "Key Assumptions", "ACH", "Diagnostic Timeout", "anti-confabulation", "self-prompting", "convergent evidence", "UNRESOLVED", "fingerprinting" — all must appear.

- [ ] **2.2: Write investigate SKILL.md stub**
  Files: `.claude/skills/investigate/SKILL.md` (create new)
  Do: Create directory `.claude/skills/investigate/`. Write the skill registration stub per D-017:
  ```yaml
  ---
  name: investigate
  description: "Deep investigation and evidence gathering. Use when asked to research, investigate, find out, or deep-dive into any topic. Produces fully-evidenced analysis with per-claim confidence. Not for bugs (use debug-rca/troubleshoot) or plan review (use adversarial-review)."
  ---
  ```
  Body: `**BEFORE ANYTHING ELSE:** Read prompts/investigate.md — it contains your complete protocol. Follow it exactly.`
  Verify: Directory `.claude/skills/investigate/` exists and contains only `SKILL.md`. File has valid YAML frontmatter with name `investigate`. Description includes trigger phrases AND "not for" guidance. Body references `prompts/investigate.md`.

---

## Phase 3: Debug RCA Skill — DOING

Build the code-specific root cause analysis skill. Most complex — validates 450-line target.

- [ ] **3.1a: Write debug-rca protocol — structure and shared patterns**
  Files: `prompts/debug-rca.md` (create new), `prompts/shared-investigation-foundations.md` (read — copy INLINE BLOCK), `specific_framework/DebugRCA/README.md` (read as evolution source), parent plan (read Phase 3 section + D-002, D-012, D-014)
  Do: Write the protocol skeleton with all structural elements in place:
  1. Copy INLINE BLOCK verbatim into Shared Standards section.
  2. Write preamble: skill identity, when to use (code bugs, not-immediately-obvious cause), when NOT to use (NOT for: typos/config → fix directly; non-code problems → use /troubleshoot; research → use /investigate), tools available (Read, Grep, Glob, Bash for git/grep only, Agent for subagents).
  3. Write INPUT requirements section (5 required fields: bug description, observable data, suspect files, reproduction, scope).
  4. Write phase headings and structure for all phases (0.5 through 6) with technique assignments per phase — but leave detailed instructions as brief notes.
  5. Write 2 concrete Agent tool invocation examples from the foundations template:
     - Phase 2 example: adversarial hypothesis destruction (fill placeholders with debug-specific content)
     - Phase 5.2 example: adversarial plan review (fill placeholders with fix-plan-specific content)
  6. Write skip/abort section (SKIP ADVERSARIAL, SKIP TO PLAN with mandatory grading pass, ABORT).
  7. Write sync note header referencing shared foundations + troubleshoot protocol.
  Target: structure should use ~200-250 lines, leaving ~200 for detailed phase content in 3.1b.
  Verify: File exists. Has INLINE BLOCK matching source. Has all phase headings (grep for "Phase 0.5", "Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5.0", "Phase 5.1", "Phase 5.2", "Phase 5.3", "Phase 6"). Has 2 Agent tool invocation examples (grep for "Agent tool" or the Agent description/prompt pattern). Has INPUT section with 5 fields. Has skip/abort section. Has sync note.

- [ ] **3.1b: Write debug-rca protocol — detailed phase content**
  Files: `prompts/debug-rca.md` (edit existing from 3.1a), `specific_framework/DebugRCA/README.md` (reference for evolving), parent plan (read Phase 3 section for technique details)
  Do: Fill in detailed instructions for each phase. Read the original DebugRCA's Phase 1-6 sections thoroughly. For each phase, identify what the original does well (file:line precision, causal chain recursion, read-only Phase 3, adversarial independence), then add the research-backed enhancement while maintaining those strengths. Evolve, don't replace:
  - Phase 0.5: git log/diff instructions, config review checklist
  - Phase 1: IS/IS-NOT matrix template (WHAT/WHERE/WHEN/EXTENT), hypothesis generation rules (must explain every IS and IS-NOT), causal chain format (file:line evidence), counterfactual reasoning instructions, "list up to 3 contradictions" step, uncertainty action audit, state tracker update
  - Phase 2: subagent receives hypothesis + ALL evidence locations (supporting AND non-supporting), minimum 2 alternatives, optional ACH for complex cases (per D-012), disproof step on each finding, VERDICT parsing and loop logic
  - Phase 2→1 loop: re-investigation instructions, UNRESOLVED format after 3 iterations (from D-014 template)
  - Phase 3: read-only constraint, raw data format, REQUIRES MANUAL VERIFICATION flag
  - Phase 4: git blame instructions, classification categories
  - Phase 5.0: fix plan format (exact code, before/after, tests, verification, forbidden)
  - Phase 5.1: consumer search (grep callers), edge cases list, barrier inventory, STPA instructions (if interaction bug)
  - Phase 5.2: destruction questions, VERDICT parsing
  - Phase 5.3: user gate presentation format (root cause paragraph, adversarial verdict, fix plan, impact, plan adversarial)
  - Phase 6: implementation prompt format (optional, user-requested)
  If total exceeds 450 lines, trim by priority: cut STPA (narrow value) → cut Phase 6 detail (optional) → compress Phase 4 (low complexity) → compress Phase 3 (straightforward).
  Verify: File is ≤450 lines (`wc -l`). All phases have substantive instructions (not just headings). Technique presence: grep for "IS/IS-NOT", "counterfactual", "barrier inventory", "STPA", "Diagnostic Timeout", "anti-confabulation", "self-prompting", "UNRESOLVED", "disproof", "fingerprinting" — all should appear (STPA may be cut if over budget — acceptable). INLINE BLOCK still matches source (verify edit didn't corrupt it).

- [ ] **3.2: Write debug-rca SKILL.md stub**
  Files: `.claude/skills/debug-rca/SKILL.md` (create new)
  Do: Create directory `.claude/skills/debug-rca/`. Write stub per D-017:
  ```yaml
  ---
  name: debug-rca
  description: "Adversarial root cause analysis for code bugs. Use when asked to debug, find the bug, find root cause, or figure out why code is broken. Requires a codebase. Not for non-code problems (use troubleshoot) or research (use investigate)."
  ---
  ```
  Body: `**BEFORE ANYTHING ELSE:** Read prompts/debug-rca.md — it contains your complete protocol. Follow it exactly.` + `Then read state/charter.json for project context.`
  Verify: Directory `.claude/skills/debug-rca/` exists, contains only `SKILL.md`. Valid YAML frontmatter. Description includes trigger phrases and "not for" guidance. Body references both `prompts/debug-rca.md` and `state/charter.json`.

---

## Phase 4: Troubleshoot Skill — DOING

Domain-agnostic root cause analysis. Same backbone as Debug RCA, generalized evidence types.

- [ ] **4.1: Write troubleshoot protocol**
  Files: `prompts/troubleshoot.md` (create new), `prompts/shared-investigation-foundations.md` (read — copy INLINE BLOCK), parent plan (read Phase 4 section)
  Do: Write the full self-contained protocol. Copy INLINE BLOCK verbatim. Same adversarial backbone as Debug RCA but domain-agnostic. Backbone phase structure must match: INPUT → Phase 0.5 (Change Analysis) → Phase 1 (Investigate with IS/IS-NOT, hypotheses, causal chain) → Phase 2 (Adversarial Destroy, subagent) → Phase 2→1 Loop → Phase 3 (Verify, read-only) → Phase 4 (Attribute) → Phase 5.0-5.3 (Plan + Impact + Adversarial Plan Review + User Gate) → Phase 6 (optional handoff). Key differences from debug-rca:
  - Preamble: when NOT to use (NOT for: code bugs with clear symptoms → use /debug-rca; pure research → use /investigate; plan review → use /adversarial-review). Note: Troubleshoot CAN read code if available in the workspace for hybrid code+infrastructure incidents.
  - No git-specific tools — evidence from documents, data, logs, web research, observations
  - Phase 0.5: generic change analysis (timelines, deployments, personnel, process, external events)
  - Phase 1: IS/IS-NOT adapted for non-code; ACH matrix MANDATORY (per D-012, unlike Debug RCA where it's optional)
  - Phase 2: adversarial subagent with ACH mandatory
  - Phase 4: organizational attribution (human error / process failure / system defect / external factor / interaction)
  - Phase 5.0: resolution plan (what, who, resources, timeline)
  - Phase 6: handoff document
  Include Agent tool invocation example. Include sync note header referencing shared foundations + debug-rca. Verify backbone phase structure matches debug-rca.
  Target: ≤450 lines.
  Verify: File exists. ≤450 lines. INLINE BLOCK matches source. ACH matrix is mandatory (grep for "mandatory" near "ACH"). Sync note references both shared foundations and debug-rca. Phase structure matches debug-rca backbone (same phase numbers/names, different domain content). Agent tool invocation example present. "CAN read code" note present for hybrid incidents. Technique presence: grep for "IS/IS-NOT", "Diagnostic Timeout", "anti-confabulation", "self-prompting", "UNRESOLVED", "disproof", "fingerprinting" — all must appear.

- [ ] **4.2: Write troubleshoot SKILL.md stub**
  Files: `.claude/skills/troubleshoot/SKILL.md` (create new)
  Do: Create directory `.claude/skills/troubleshoot/`. Write stub per D-017:
  ```yaml
  ---
  name: troubleshoot
  description: "Adversarial root cause analysis for non-code problems. Use when asked to troubleshoot, diagnose, or figure out why something non-code is failing (systems, processes, infrastructure, business issues). Not for code bugs (use debug-rca) or research (use investigate)."
  ---
  ```
  Body: `**BEFORE ANYTHING ELSE:** Read prompts/troubleshoot.md — it contains your complete protocol. Follow it exactly.` + `Then read state/charter.json for project context.`
  Verify: Directory exists, contains only SKILL.md. Valid YAML frontmatter. Description includes trigger phrases and "not for" guidance.

---

## Phase 5: Adversarial Review Skill — DOING

Standalone plan/proposal stress-testing. Structurally different from RCA skills.

- [ ] **5.1: Write adversarial-review protocol**
  Files: `prompts/adversarial-review.md` (create new), `prompts/shared-investigation-foundations.md` (read — copy INLINE BLOCK), parent plan (read Phase 5 section)
  Do: Write the full self-contained protocol. Copy INLINE BLOCK verbatim. This is structurally different — no hypothesis testing, no ACH matrix. Uses pre-mortem, FMEA, inversion, structural analysis. Include:
  - Preamble: when to use (any plan/proposal before execution), when NOT to use (NOT for: active investigation → use /investigate, /debug-rca, or /troubleshoot), tools available (all tools — needs codebase access if plan references code)
  - Phase 1: UNDERSTAND (extract goals/assumptions/steps/dependencies/constraints, precondition/postcondition chain via Design by Contract, assumption mapping: importance × evidence, Chesterton's Fence on every change)
  - Phase 2: PRE-MORTEM ("it failed catastrophically, why?" — generate from: end user, ops engineer, security auditor, maintainer in 2 years, on-call at 3am. Rate each: likelihood × severity)
  - Phase 3: INVERSION ("how to GUARANTEE failure?" Reverse brainstorm each failure mode)
  - Phase 4: STRUCTURAL (FMEA template: per step → failure mode, effect, severity 1-10, occurrence 1-10, detectability 1-10 → RPN. Precondition/postcondition chain verification. Invariant check)
  - Phase 5: IMPACT (all consumers, 1st/2nd/3rd order consequences, blast radius, ATAM-style sensitivity/tradeoff points, reinforcing feedback loops)
  - Phase 6: ADVERSARIAL DESTROY (Agent tool invocation — plan + Phases 2-5 findings as facts, NOT reasoning. 7 mandatory questions: (1) structural fix or symptom patch? (2) missed consumers? (3) worse than doing nothing? (4) right abstraction level? (5) holds on edge cases? (6) what assumption collapses the plan? (7) reinforcing feedback loops? Disproof step on each finding. VERDICT)
  - Phase 7: VERDICT + USER GATE (all findings BLOCKER/MINOR/COSMETIC with evidence grade + confidence. GO/CORRECT/RETHINK)
  - Skip/abort section. Sync note header.
  Target: ≤450 lines.
  Verify: File exists. ≤450 lines. INLINE BLOCK matches source. All 7 phases present. FMEA template with RPN formula present. Pre-mortem has 5 perspectives listed. 7 destruction questions present (grep for each). Agent tool invocation example present. No ACH matrix (per D-012 — grep should NOT find "ACH"). Sync note present. Technique presence: grep for "pre-mortem", "FMEA", "RPN", "Design by Contract", "Chesterton", "assumption mapping", "blast radius", "feedback loop", "disproof" — all must appear.

- [ ] **5.2: Write adversarial-review SKILL.md stub**
  Files: `.claude/skills/adversarial-review/SKILL.md` (create new)
  Do: Create directory `.claude/skills/adversarial-review/`. Write stub per D-017:
  ```yaml
  ---
  name: adversarial-review
  description: "Adversarial stress-testing for plans and proposals. Use when asked to review a plan, stress test, proof, attack, or find what could go wrong with a proposal. Not for active investigation (use investigate, debug-rca, or troubleshoot)."
  ---
  ```
  Body: `**BEFORE ANYTHING ELSE:** Read prompts/adversarial-review.md — it contains your complete protocol. Follow it exactly.`
  Verify: Directory exists, contains only SKILL.md. Valid YAML frontmatter. Description includes trigger phrases and "not for" guidance.

---

## Phase 6: Integration, Migration & Verification — DOING

Verify everything works. Update documentation. Run all framework gates.

- [ ] **6.1: Update original DebugRCA with portability header**
  Files: `specific_framework/DebugRCA/README.md`
  Do: Add header at line 1 per D-015: `> **Portable version.** This is the platform-agnostic DebugRCA process. For Claude Code integration with subagent isolation, evidence grading, and skill chaining, see the \`/debug-rca\` skill at \`prompts/debug-rca.md\`.` followed by a blank line. Do NOT modify any other content.
  Verify: `git diff specific_framework/DebugRCA/README.md` shows only added lines at the top (no deletions, no modifications to existing lines).

- [ ] **6.2: Update KB_index.md, CLAUDE.md, and charter.json**
  Files: `KB/KB_index.md`, `CLAUDE.md`, `state/charter.json`
  Do:
  1. Verify tags `investigation`, `rca`, `adversarial`, `research` exist in charter.json (added in 1.3 — confirm).
  2. Add KB_index rows for all skill protocol files:
     - `prompts/investigate.md` — Investigate skill protocol — tags: `investigation` — load: `on-demand`
     - `prompts/debug-rca.md` — Debug RCA skill protocol — tags: `rca, investigation` — load: `on-demand`
     - `prompts/troubleshoot.md` — Troubleshoot skill protocol — tags: `rca, investigation` — load: `on-demand`
     - `prompts/adversarial-review.md` — Adversarial Review skill protocol — tags: `adversarial` — load: `on-demand`
  3. Add to CLAUDE.md Framework Structure section, after the "Full protocols" line:
     `- Investigation skills: \`.claude/skills/<name>/SKILL.md\` stubs → \`prompts/<name>.md\` protocols. Four skills: investigate, debug-rca, troubleshoot, adversarial-review.`
  Verify: KB_index has 6 new rows total (2 from Phase 1 + 4 from here). CLAUDE.md has the new Framework Structure line. Tags in KB_index rows exist in charter.json.

- [ ] **6.3: Verify protocol sizes and cross-skill consistency**
  Files: `prompts/investigate.md`, `prompts/debug-rca.md`, `prompts/troubleshoot.md`, `prompts/adversarial-review.md`, `prompts/shared-investigation-foundations.md`
  Do:
  1. Run `wc -l` on all 4 protocols — verify each ≤450 lines.
  2. Extract the shared standards / INLINE BLOCK section from each protocol. Diff against the INLINE BLOCK in `shared-investigation-foundations.md`. All 4 must be identical.
  3. Verify Debug RCA sync note references troubleshoot and vice versa.
  4. Verify all 4 SKILL.md stubs exist, have valid YAML, and reference correct protocol files.
  5. If shared patterns don't match: the INLINE BLOCK in `shared-investigation-foundations.md` is authoritative. Copy it into the mismatched protocol(s).
  Verify: All protocols ≤450 lines. Shared pattern blocks identical (diff output is empty). Sync notes bidirectional between debug-rca and troubleshoot. All SKILL.md stubs valid.

- [ ] **6.4a: Agent-executable validation checks**
  Files: all SKILL.md stubs, all protocol files
  Do: Verify everything the agent CAN check without fresh sessions:
  1. All 4 SKILL.md files exist at correct paths with valid YAML frontmatter.
  2. All 4 protocol files exist and are readable.
  3. Extract the Phase 2 Agent tool invocation example from `prompts/debug-rca.md`. Replace placeholders with real values (pick any file in the repo as evidence, use "test hypothesis: this file contains a bug" as hypothesis). Spawn the subagent using the filled template. Verify output begins with "VERDICT:" line and contains a "## Findings" section. This tests the actual protocol template, not a synthetic prompt.
  4. Verify all skip/abort commands are documented in each protocol (grep for "SKIP ADVERSARIAL", "SKIP TO PLAN", "ABORT" in each).
  5. Verify handoff schema is referenced in each protocol's report/output phase.
  Verify: All 4 SKILL.md paths exist. All 4 protocol paths exist. Subagent test returns VERDICT line. Skip/abort commands present in all protocols. Handoff schema referenced.

- [ ] **6.4b: Present user-executable validation checklist**
  Files: none (conversation output only — no file created)
  Do: Present the manual trigger-testing checklist to the user in conversation. The user runs these in fresh sessions at their discretion. Checklist covers:
  - Trigger tests: 1 phrase per skill, verify correct protocol activates
  - Boundary test: ambiguous phrase, document which skill activates
  - Skip test: SKIP ADVERSARIAL mid-investigation
  - Abort test: ABORT mid-investigation
  No file is created — this is a framework template repo, not a project. Test artifacts don't belong here.
  Verify: Checklist presented to user in conversation.
