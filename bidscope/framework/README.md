# Construction Bidding Document Analysis Framework

A systematic agent pipeline for analyzing technical construction documents (drawings, BOQs, electrical schematics) and producing verified, actionable bidding documents.

**Domain:** HVAC, plumbing, electrical, thermal installations + finishing works (drywall, tiling, painting).

## Pipeline Overview

```
INTAKE → EXTRACT → ANALYZE → VERIFY → DEEPEN → DELIVER
  (1)      (2)      (3)       (4)      (5)       (6)
```

| Phase | Agent(s) | Parallel? | Output |
|-------|----------|-----------|--------|
| 1. INTAKE | `organizer` | No | Structured folder + inventory |
| 2. EXTRACT | `extractor` ×N | Yes (per doc) | Structured data per document |
| 3. ANALYZE | `analyzer` | No | Discrepancies, gaps, risks |
| 4. VERIFY | `verifier` ×N | Yes (per specialty) | Confirmed/refuted claims |
| 5. DEEPEN | `researcher`, `price-scout`, `estimator`, `counter` | Yes | Answers, prices, estimates |
| 6. DELIVER | `reporter` | No | Final documents per audience |

## Agents

### Pipeline agents (sequential, one instance)
| File | Role |
|------|------|
| [`pipeline-runner.md`](pipeline-runner.md) | Orchestrator — runs phases, launches agents, collects results |
| [`agents/01-organizer.md`](agents/01-organizer.md) | Intake, dedup, classify, structure |
| [`agents/03-analyzer.md`](agents/03-analyzer.md) | Cross-reference, gap analysis, risk quantification |
| [`agents/09-reporter.md`](agents/09-reporter.md) | Compile deliverables per audience |

### Worker agents (parallel, multiple instances)
| File | Role |
|------|------|
| [`agents/02-extractor.md`](agents/02-extractor.md) | Read 1 document, extract all structured data |
| [`agents/04-verifier.md`](agents/04-verifier.md) | Independently verify claims against source documents |
| [`agents/05-researcher.md`](agents/05-researcher.md) | Answer specific technical questions |
| [`agents/06-price-scout.md`](agents/06-price-scout.md) | Find market prices, suppliers, alternatives |
| [`agents/07-estimator.md`](agents/07-estimator.md) | Create missing BOQ from technical drawings |
| [`agents/08-counter.md`](agents/08-counter.md) | Count elements on drawings (outlets, fixtures, etc.) |

## Quick Start

1. Place your project documents (PDFs, XLSX) in a working folder
2. Load `pipeline-runner.md` as context
3. Tell the orchestrator: "Analyze these documents for bidding"
4. The pipeline runs automatically through all 6 phases

## How It Was Built

This framework was extracted from a real bidding analysis session where 18 technical files (10 drawings + 8 BOQs) were analyzed for a residential building in Bucharest. The ad-hoc process was formalized into reusable agent definitions.

**Proven results from first session:**
- 7 major price traps identified (~40-65k EUR risk)
- 7 probable errors in documentation
- 11 missing items from BOQ
- 34 claims verified (32 correct, 1 error caught and corrected)
- 11 specialist deep-dives completed
- Full bidding document generated in one session
