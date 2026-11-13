# Rigor Review of Organoid Intelligence Research

Working files for a critical review of how rigorous organoid intelligence (OI) and biocomputing research is. A separate Pong replication tests one paper's claim directly: see [PONG_REPLICATION.md](PONG_REPLICATION.md).

## Overview

OI claims that living neurons can compute or learn, sometimes more efficiently than AI. Our group first planned an argumentative paper. About a month ago we changed it to a metascience review: instead of arguing for or against OI, we check how well the field's claims are supported. The questions are:

- Does each claim match the system that was actually tested (2D cultures vs organoids, whole brain vs organoid)?
- Are the controls, statistics and comparisons to AI fair?
- Do reviews and company pages keep the original authors' caveats, or drop them?
- Has anyone outside the original team reproduced the result?

## Where it stands (9 Nov 2026)

Method: LLM-assisted rigor appraisal, validated against blind human raters. Details in [method_v1_2.md](oi-review/method_v1_2.md).

Done:
- Rubric v1.1 (review-track items, tighter NA rule) and a v1.2 draft that splits items into factual checks scored by a fixed rule and judgment items with anchors ([rubric_v1_2_checks.md](oi-review/rubric_v1_2_checks.md)).
- Reproducible search strings (Search_Log tab), 20-source random validation set, pre-set acceptance rule, and the analysis script ([agreement.py](oi-review/analysis/agreement.py)), tested on synthetic data.
- An AI pilot on four papers (`oi-review/pilot/`). It is a diagnostic, not data, and its scores are not used.

Not done:
- Human revision of the anchors and checks, and ratings from 3 outside experts. Then freeze v1.2.
- Running the database searches, second screener on 20%, citation chaining.
- Blind human scoring of the 20 validation sources (Tani and Gabe) and the two AI runs.
- OSF pre-registration, before any validation scores exist.

## Plan

1. Human rewrite of anchors and checks; expert content-validity ratings; freeze rubric v1.2 and prompt AI-P1.1.
2. Pre-register on OSF.
3. Two AI models and two blind human raters score the 20 validation sources. `agreement.py` decides whether the AI is acceptable, using a non-inferiority margin of 0.15 on weighted kappa with a paper-level bootstrap.
4. Main corpus: factual-check scores are auto-accepted only when both models agree and validation supports that item; every other score is verified by a person. A blind human audit of 15-20% checks the result.
5. Report item profiles, not single totals.

## Files

- `oi-review/OI_Critical_Review_Scoring_Sheet.xlsx`: snapshot of the live workbook (protocol, search log, screening, checks, validation, agreement, scoring, analysis). Contains no AI or rater scores
- `oi-review/UPDATE_NOTES.md`: full notes on the November 2026 changes (method, rubric, validation, audit fixes, limits, next steps)
- `oi-review/method_v1_2.md`: method, validation design, acceptance and routing rules, known limits
- `oi-review/rubric_v1_2_checks.md`: rubric v1.2 draft (factual checks and scoring rules)
- `oi-review/analysis/run_ai.py`: scripted, logged AI scoring runs
- `oi-review/search/`: search scripts, run log and string test
- `oi-review/analysis/agreement.py`: agreement statistics and the acceptance decision; `test_data/` is synthetic
- `oi-review/search_protocol.md`: question, searches, include and exclude rules
- `oi-review/rubric_scoring_anchors_v1.md`: what 0, 1 and 2 mean for each item
- `oi-review/review_sources.md`: papers in the screening log, with links
- `oi-review/rubric_v1_1.md`: rubric v1 with the pilot changes built in (draft, not frozen)
- `oi-review/rubric_v1_1_evaluation.md`, `oi-review/rubric_critique_v1_1.md`: which changes are worth keeping, and a layer-by-layer critique against review standards
- `oi-review/pilot/`: first AI pilot run of the rubric on four papers (findings and per-item scores). Not human scores; used to find unclear anchors
- `PONG_REPLICATION.md`, `DEVIATIONS.md`, `pong_env.py`, `dqn.py`, `analyze.py`: the Pong replication
