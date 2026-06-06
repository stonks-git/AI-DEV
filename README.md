# AI-DEV Framework Template

A reusable scaffold for bootstrapping AI-assisted software development projects using Claude Code.

## What This Is

This repo is a **framework template** -- not a project. Clone it to start a new project with a pre-built system for:

- **State management** -- charter, roadmap, devlog, and session handoff files
- **Knowledge base** -- tag-routed context loading with blueprint versioning
- **Decision tracking** -- Decision Journal captures why plans changed, not just what changed
- **Audit pipeline** -- 7 specialized auditors with SOTA protocol (security, architecture, database, code quality, frontend, ops, pattern scout)
- **Documentation discipline** -- mandatory gates enforce KB updates, blueprint versioning, and decision recording
- **Task validation** -- dependency-aware task management with topological sort and cycle detection

## Prerequisites

- Python 3.7+
- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)

## Quick Start

1. Clone or use this repo as a template
2. Fill in `state/charter.json` with your project details (name, constraints, tech stack)
3. Fill in the `CLAUDE.md` header with your project name and description
4. Start a Claude Code session -- the agent follows the bootstrap sequence in `CLAUDE.md` automatically
5. Run `python3 taskmaster.py validate` to verify state file integrity

## Directory Structure

```
CLAUDE.md                    # Single origin -- framework rules, gates, bootstrap sequence
taskmaster.py                # State validator + task manager (validate, order, ready, steps)
timesheet.py                 # Manual work-time tracker (punch in/out, status, report)

state/
  charter.json               # Project identity, constraints, tag taxonomy
  roadmap.json               # Tasks (DAG), decisions, open questions
  devlog.ndjson              # Append-only event journal (NDJSON)
  timesheet.ndjson           # Append-only punch journal (work time) -- ships empty
  handoff.md                 # Session context, memory marker, git status

KB/
  KB_index.md                # Context router -- controls what gets loaded and when
  KB_01_architecture.md      # Architecture overview + Decision Journal
  blueprints/
    BLUEPRINT_INDEX.md        # Version pointer (current plan)
    v0.1_initial_plan.md      # Scaffold plan snapshot (template)

prompts/
  supervisor.md              # Taskmaster supervisor behavior contract
  archeolog-prospector.md    # Codebase archaeology protocol
  ux-flow-reviewer.md        # UX review protocol
  auditors/
    runner.md                # Audit orchestrator + SOTA protocol
    1-security.md            # Security auditor
    2-archeologist.md        # Business logic mapper
    3-database.md            # Database auditor
    4-code-quality.md        # Code quality auditor
    5-frontend.md            # Frontend auditor
    6-ops.md                 # Ops auditor
    7-prospector.md          # Pre-build explorer (pattern scout)

.claude/
  settings.local.json        # Permission whitelist (local, not committed)
  agents/                    # Claude Code agent stubs (all point to prompts/)
    audit-*.md               # Audit agent stubs -> prompts/auditors/
    archeolog-prospector.md  # Stub -> prompts/archeolog-prospector.md
    pre-build-explorer.md    # Stub -> prompts/auditors/7-prospector.md
    ux-flow-reviewer.md      # Stub -> prompts/ux-flow-reviewer.md
  skills/
    doc/SKILL.md             # /doc command -- 9-step documentation gate
```

## Key Concepts

### Bootstrap Sequence
`CLAUDE.md` is the single origin. It defines a strict 7-step loading order that prevents context bloat while ensuring the agent has everything it needs. The agent loads state files, the KB router, then only the KB files relevant to the current task.

### Mandatory Gates
Four gates enforce documentation discipline:
- **KB Gate** -- code changes require KB updates
- **Blueprint Gate** -- architecture changes require a new blueprint version
- **Decision Journal Gate** -- superseded decisions require a DJ entry (Was/Now/Why/Lesson)
- **Doc Gate** -- completed tasks require running `/doc` to update all state files

### Agent Architecture
All agents follow the **stub/protocol** pattern:
- **Stubs** (`.claude/agents/*.md`) -- lightweight registration files for Claude Code (5-10 lines). Declare name, description, tools, model.
- **Protocols** (`prompts/`) -- full behavior contracts (80-130 lines). Portable and tool-agnostic.

This split keeps Claude Code registration clean while making protocols reusable outside Claude Code. Agent stub paths are relative to repository root.

### Taskmaster
`taskmaster.py` is a zero-dependency Python script with four commands:
- `validate` -- checks all state files against schema
- `order` -- topological sort of tasks by dependencies
- `ready` -- shows next available tasks (todo + all deps done)
- `steps T-001` -- shows decomposition for complex tasks

#### Extended task schema (for `steps`)

Tasks in `roadmap.json` can optionally include decomposition fields:

```json
{
  "id": "T-001",
  "title": "Deploy auth service",
  "complexity": "complex",
  "steps": [
    {
      "step": 1,
      "title": "Backup current DB",
      "status": "todo",
      "critical": true,
      "deliverable": "backup file verified",
      "verify": "run restore test",
      "rollback": "restore from previous backup"
    }
  ]
}
```

Fields: `steps` (array), `complexity` (string), and per-step: `step`, `title`, `status`, `critical`, `deliverable`, `verify`, `rollback`.

### Timesheet

`timesheet.py` is a zero-dependency manual work-time tracker, kept separate from the
devlog on purpose: the devlog is a *schema-validated event journal* (decisions,
features, bugfixes), whereas punches are raw time data that would otherwise trip
taskmaster's devlog event allow-list. Like the devlog, the timesheet is an
**append-only** journal (`state/timesheet.ndjson`) — a punch-out is a new appended
line, never an edit to the punch-in line. Totals are computed on read, never stored.

```bash
python3 timesheet.py in  --note "auth work"   # start a session (optional note)
python3 timesheet.py out                       # end it; prints the session duration
python3 timesheet.py status                    # are you punched in? for how long?
python3 timesheet.py report                    # sessions + per-day totals + grand total
```

Within a Claude Code session you can punch without leaving the prompt: `! python3 timesheet.py in`.

- Punches alternate strictly: `in` refuses if already in, `out` refuses if not in (keeps the journal consistent for reporting).
- Timestamps are local wall-clock with UTC offset (e.g. `2026-06-06T09:00:00+03:00`).
- `report` flags any open (unmatched) punch-in separately, so an unclosed session never silently corrupts totals.
- Sessions are attributed to the calendar date they *started* (a session crossing midnight counts toward its start day).
- `in` / `out` honor `--debug` (full trace to `data/timesheet_debug.log`, per the project's script-debug rule); read-only `status` / `report` do not mutate state and omit it.

### Charter Fields Reference

`state/charter.json` key fields under `project.constraints`:

| Field | Purpose |
|-------|---------|
| `app_code_dir` | Where application source code lives (e.g., `src/`, `app/`) |
| `infra_db` | Database technology (e.g., `PostgreSQL 15`, `SQLite`) |
| `infra_access` | How infrastructure is accessed (e.g., `SSH`, `AWS CLI`, `local only`) |
| `must_use` | Required technologies/libraries |
| `must_avoid` | Banned technologies/patterns |

## Customizing for Your Project

1. Edit `state/charter.json`: set project name, constraints, tech stack, tag taxonomy
2. Edit `CLAUDE.md`: update the header and description
3. Edit `.claude/settings.local.json`: adjust the permission whitelist for your tools
4. Add KB pages as needed: `KB/KB_XX_<topic>.md` + update `KB/KB_index.md`
5. Extend `charter.json` `tag_taxonomy` when you need new domain tags

## License

[Add your license here]
