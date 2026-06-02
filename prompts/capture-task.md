<!-- Role in the architecture: portable protocol for the /capture-task skill — the collision-checked,
non-destructive front door for adding a task to state/roadmap.json. NOT an investigation skill: it does
not use the shared evidence-grading/ACH apparatus. It detects, it surfaces, the human decides, it appends. -->

# Capture-Task — Collision-Checked Roadmap Task Capture

You add a new task to `state/roadmap.json` **safely**. Before anything is written, you read the full
project record and prove — to the user, not to yourself — whether the task they want to capture is already
covered: a duplicate, already done, deliberately skipped, or incompatible with a recorded decision. You are
a **gate and a scribe**, not an editor: you may only ever *append one new task* (or nothing). You NEVER
change an existing task's status, criteria, or dependencies.

## When to Use

- The user wants to add / capture / log a task to the roadmap backlog.
- Any time a new unit of work should enter `state/roadmap.json` as a tracked task.

## When NOT to Use

- Recording *completed* work or session bookkeeping → use `/doc`.
- Decomposing a plan phase into atomic sub-tasks → that writes plan files in `state/plans/`, not roadmap tasks.
- Changing an existing task (status, deps, supersede, merge, revive) → **this skill cannot do that** (see
  REPORT & STOP). Those are edits to existing tasks and go through `/doc` + the Decision Journal Gate.

## Tools Available

- `Read`, `Grep`, `Glob` — read the record and run the collision sweep.
- `Bash` — run `python3 taskmaster.py validate` (baseline) and `python3 taskmaster.py add --file <tmp> [--debug]` (the write).
- `Write` — only to write the candidate task object to a temp JSON file for `taskmaster add`. **Never** hand-edit `roadmap.json`.

> **Hard rule:** the ONLY way you write a task is via `python3 taskmaster.py add`. Hand-editing `roadmap.json`
> risks silently dropping or mutating existing tasks and is forbidden — `add` is deterministic, atomic,
> validated, and structurally non-destructive by construction.

---

## INPUT (collect before starting — all required)

| Field | Meaning | If missing |
|---|---|---|
| **Task intent** | One or two sentences: what the task is, in the user's words. | Ask the user. |
| **Why now** | The reason it should be on the roadmap (feeds `intent`). | Ask, or infer and confirm. |

Everything else (deliverable, acceptance criteria, verification, priority, deps, id) you DRAFT and confirm.

---

## Phase 0: PARSE

Restate the candidate task in one line and extract its **collision signal**:

1. Write a single-sentence normalized statement of the task.
2. Extract **keywords / identifiers**: domain nouns, feature names, file/module names, symbols, error codes —
   anything a real duplicate would also mention. These drive the grep sweep.
3. Note the **area** the task touches (UI, data, a module, ops, docs…).

Update state tracker.

## Phase 1: SWEEP (full coverage — never skip a source)

Goal: build a **candidate-collision list** mechanically, so the verdict does not rest on memory alone.
This skill is invoked deliberately when the user wants the full process — do the whole sweep every time.

For each keyword/identifier from Phase 0, search **every** source:

1. `state/roadmap.json` — **read in full** (it is the canonical task store; always read all of it). Note
   every existing task whose title/intent/deliverable overlaps, **with its `status`**. Also read `decisions[]`.
2. `state/devlog.ndjson` — full read + grep keywords (completed work, scope changes, prior decisions).
3. `KB/KB_01_architecture.md` — the **Decision Journal**: grep `[tag]` headers and keyword bodies for an
   approach that was **rejected or superseded** (this is the INCOMPATIBLE check).
4. `KB/*.md` — module docs that may show the work already exists / was designed differently.
5. `state/plans/*.md` — phases/tasks already planned or done.
6. `state/comms.md` — client statements that already cover, defer, or forbid this.
7. **The codebase** — grep the project source for evidence the work already exists. Scope: `charter.json`
   `project.constraints.app_code_dir` if set, else the repo root; respect `.gitignore`; exclude `.git/`,
   `node_modules/`, build/vendor dirs. On a template with no app code this is a no-op — note it and move on.

For every hit, record: `source:line · existing ref (task id / DJ id / commit) · status · why it might collide`.

Update state tracker.

## Phase 2: ADJUDICATE

Classify **each** candidate-collision hit. Cite evidence (`file:line`) for every classification.

| Class | Means | Evidence to cite |
|---|---|---|
| **NOVEL** | No real overlap. | — (the hit was a false positive) |
| **RELATED** | Overlaps an existing task but is genuinely different work. | the related task id |
| **DUPLICATE** | Same work as an existing **open** task (todo/doing/blocked). | the task id + status |
| **DONE** | Already completed (a `done` task, or present in code/devlog). | task id / commit / `file:line` |
| **SKIPPED** | Matches a `skipped` task. **Surface its recorded reason if one exists; if none is recorded, say so explicitly** — terminal tasks store no reason field, so "deliberately skipped" may be unverifiable. | task id (+ devlog/DJ if the why is there) |
| **INCOMPATIBLE** | A Decision Journal entry rejected/superseded this approach. | `DJ-XXX` |

Honesty rule: you are **assisting**, not proving. Token-disjoint duplicates (same work, different vocabulary)
can slip the grep — never claim "proven unique." Present what you found and let the user confirm.

Update state tracker.

## Phase 3: DECISION GATE (class-gated — the user chooses)

Present the adjudication, then offer **only the actions legal for the highest-severity class found**:

- **All NOVEL** → proceed to DRAFT (ADD).
- **RELATED (no harder class)** → offer **ADD-LINKED** (append the new task, stamped with an informational
  `related_to: <id>` field) or **CANCEL**.
- **DUPLICATE / DONE / SKIPPED / INCOMPATIBLE** → **default is CANCEL.** Adding is *suppressed*. The user may
  still add, but only via an **explicit typed override** (they type, e.g., `override: add as new`); the added
  task is stamped `related_to: <id>` so the deliberate collision is marked. This is the legitimate "redo a
  done task" / "revive as fresh work" path — never the default.
- **Any collision the user instead wants to resolve by changing the existing task** (supersede / merge /
  revive a skipped task) → **REPORT & STOP** (below). You do not perform it.

### REPORT & STOP (supersede / merge / revive)

You **write nothing**. Output, read-only:

1. The matched task: id, status, and its recorded *why* (or "no reason recorded").
2. **Every existing task whose `depends_on` includes the matched task** — enumerate them from `roadmap.json`.
   This is the dangerous part of any manual supersede and you are handing it to the user up front.
3. This exact caveat: *"Superseding/merging/reviving an existing task is not automated anywhere — there is no
   `superseded` task status, and `taskmaster` treats a `skipped` dependency as satisfied, so retiring a task
   without re-pointing its dependents silently marks them ready. Do this by hand via `/doc` + a Decision
   Journal entry, re-pointing the dependents listed above."*

Then stop. (Automating safe task-supersede is a known, out-of-scope gap — offer to capture it as its own task.)

Update state tracker.

## Phase 4: DRAFT (build a schema-valid task object — validate in memory before any write)

Only reached for ADD / ADD-LINKED. Construct the task object and confirm it with the user:

1. **id** — `T-<n>` where `n` = (max numeric suffix among existing `T-\d+` ids) + 1, zero-padded to the
   existing width (e.g. `T-001`). If existing ids don't match `T-\d+`, **ask** the user for the scheme; don't guess.
2. **title** — short imperative.
3. **intent** — why the task exists (from INPUT).
4. **deliverable** — non-empty; what concretely exists when done.
5. **acceptance_criteria** — list, ≥1 item; how "done" is judged.
6. **verification** — list, ≥1 item; the concrete check (command / observation).
7. **priority** — `P0`–`P9` (confirm with user; default `P2` if unstated).
8. **owner** — who owns it (default `ai` unless the user says otherwise).
9. **status** — `todo`.
10. **depends_on** — **suggest-only.** Propose candidate deps (existing task ids) with one-line rationale; the
    user confirms. Unconfirmed → `[]`. Never silently infer a dependency (a wrong one risks a write-time cycle).
11. `related_to` — include **only** for ADD-LINKED / override adds.

These fields mirror `taskmaster.py` `_validate_task` (6 base + 4 active). Show the full object; get a yes.
(`taskmaster validate` does **not** check tags — and tasks carry no tag field — so there is nothing tag-related
to validate on the object itself.)

Update state tracker.

## Phase 5: WRITE (deterministic, atomic, verified)

1. **Baseline:** run `python3 taskmaster.py validate`. If it exits **non-zero**, STOP and tell the user the
   roadmap already has errors to fix first — do not proceed (this prevents blaming the add for prior corruption).
   *Note:* WARN lines with exit 0 are expected on a fresh project and are **not** blocking — key off the exit code.
2. Write the confirmed task object to a temp JSON file (e.g. `data/.capture_task.json`).
3. Run `python3 taskmaster.py add --file <tmp>` (add `--debug` if the user wants a full trace). The command
   appends, validates the combined roadmap, runs a structural-preservation guard, writes atomically, and
   re-validates the on-disk file. **If it exits non-zero, the roadmap was NOT modified** — report the error.
4. On success, report: the new task id and total task count. Delete the temp file.

**Devlog:** a plain task capture writes **no** devlog event — the roadmap entry is the record (per project
decision; a new `todo` is not a completed task under PRIME DIRECTIVE 2). The Doc Gate's `/doc` run for the
*work* happens later, when the task is executed.

Update state tracker.

---

## User Commands (honored at any point)

| Command | Effect | Recorded as |
|---|---|---|
| `override: add as new` | Force ADD past a DUPLICATE/DONE/SKIPPED/INCOMPATIBLE verdict; stamps `related_to`. | the `related_to` field on the new task |
| `CANCEL` | Stop; write nothing. | — |

---

## State Tracker (update at each phase transition)

```markdown
### STATE TRACKER
- **Phase:** [current]
- **Candidate task:** [one-line normalized statement]
- **Keywords:** [list]
- **Collision hits:** [count] — [class breakdown: NOVEL/RELATED/DUPLICATE/DONE/SKIPPED/INCOMPATIBLE]
- **Chosen action:** [ADD / ADD-LINKED / override / REPORT&STOP / CANCEL / pending]
- **Write result:** [pending / added T-XXX / not modified]
```
