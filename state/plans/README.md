# Plans

Multi-phase strategies that don't fit as roadmap tasks or KB entries. Use for migration strategies, audit fix plans, feature rollout plans, and other operational documents that span multiple tasks.

## Naming Convention

```
YYYYMMDDHHMM-topic.md
```

Examples:
- `202602141023-reception-audit.md`
- `202602180900-api-migration-v2.md`

The timestamp prefix ensures chronological sorting and allows multiple plans about the same topic on the same day.

## Linking

Each plan starts with a header block:

```markdown
# PLAN: <topic>
Parent: YYYYMMDDHHMM-topic.md  (or "none")
Supersedes: YYYYMMDDHHMM-topic.md  (or "none")
```

- **Parent**: the plan that spawned this one (a sub-plan or follow-up)
- **Supersedes**: the plan this one replaces (new version of same strategy)

## When to Create a Plan

- Strategy spans 3+ tasks and needs a coherent narrative
- Multi-phase rollout with dependencies between phases
- Audit findings that need a structured fix sequence
- Architecture change that requires a migration path
