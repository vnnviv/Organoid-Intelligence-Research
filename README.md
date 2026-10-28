# Rigor Review of Organoid Intelligence Research

Working files for a critical review of how rigorous organoid intelligence (OI) and biocomputing research is. A separate Pong replication tests one paper's claim directly: see [PONG_REPLICATION.md](PONG_REPLICATION.md).

## Overview

OI claims that living neurons can compute or learn, sometimes more efficiently than AI. Our group first planned an argumentative paper. About a month ago we changed it to a metascience review: instead of arguing for or against OI, we check how well the field's claims are supported. The questions are:

- Does each claim match the system that was actually tested (2D cultures vs organoids, whole brain vs organoid)?
- Are the controls, statistics and comparisons to AI fair?
- Do reviews and company pages keep the original authors' caveats, or drop them?
- Has anyone outside the original team reproduced the result?

## Where it stands

- Rubric v1 and the workbook are built. The protocol, screening log and source list are done for the first search pass.
- Screening was title and abstract only, by one screener. A second screener still needs to check a random 20% and the full text of every Include and Maybe.
- The workbook has almost no scores yet. Nothing here is a finding.
- Citation chaining from the seed papers is not done.
- The tier cut-offs and the "determining factor" are still open. Tiers use the same scores as the factor, so I will re-tier with each item left out and call the result exploratory.

## Files

- `oi-review/OI_Critical_Review_Scoring_Sheet.xlsx`: screening log, scoring sheets, tiers, claims, analysis
- `oi-review/search_protocol.md`: question, searches, include and exclude rules
- `oi-review/rubric_scoring_anchors_v1.md`: what 0, 1 and 2 mean for each item
- `oi-review/review_sources.md`: papers in the screening log, with links
- `PONG_REPLICATION.md`, `DEVIATIONS.md`, `pong_env.py`, `dqn.py`, `analyze.py`: the Pong replication
