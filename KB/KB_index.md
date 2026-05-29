# KB Index (Context Router)

> **LOAD THIS FILE ON EVERY BOOTSTRAP.** This is the routing table for all KB content.
> Obey the `Load` column. Do NOT load `on-demand` files unless current task matches the tags.

| # | File | Description | Tags | Load |
|---|------|-------------|------|------|
| B | `KB/blueprints/BLUEPRINT_INDEX.md` | Version pointer + history table | arch | always |
| B+ | `KB/blueprints/v0.1_initial_plan.md` | Current scaffolding plan | arch, scaffold | always (latest only) |
| 01 | `KB/KB_01_architecture.md` | Architecture + Decision Journal | arch, decisions | always: overview. on-demand: DJ entries by tag |
| 02 | `prompts/shared-investigation-foundations.md` | Shared patterns for investigation skills (design-time reference) | investigation | on-demand |
| 04 | `prompts/investigate.md` | Investigate skill protocol | investigation | on-demand |
| 05 | `prompts/debug-rca.md` | Debug RCA skill protocol | rca, investigation | on-demand |
| 06 | `prompts/troubleshoot.md` | Troubleshoot skill protocol | rca, investigation | on-demand |
| 07 | `prompts/adversarial-review.md` | Adversarial Review skill protocol | adversarial | on-demand |
| 08 | `prompts/downstream.md` | Downstream skill protocol — pre-change coupling / blast-radius mapping (enumerative, not hypothesis-driven) | impact | on-demand |

<!--
NOTE: KB_index routes KB/ files only. State files (charter.json, roadmap.json,
devlog.ndjson, handoff.md, plans/, schema_log.md) and project workflows (workflows/)
are loaded per Bootstrap order in CLAUDE.md, not through this router.

LOADING RULES (for the supervisor agent):

1. Bootstrap: load all "always" files. For "always (latest only)", check BLUEPRINT_INDEX.md for current version pointer.
2. During work: if current task touches a tag domain, grep DJ headers for matching [tag] and load those entries.
3. NEVER load all blueprint versions at once. Load historical versions ONLY to trace a specific decision evolution.
4. When adding new KB pages, assign tags and set Load column. Default = on-demand.

ADDING PAGES:
| XX | `KB/KB_XX_<topic>.md` | Description | tags | on-demand |
-->
