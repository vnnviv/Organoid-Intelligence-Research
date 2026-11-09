# Method v1.2: LLM-assisted appraisal with human validation

Copied from the Protocol tab of the workbook (2026-11-09). The workbook is the source of truth; if the two differ, the workbook wins.

## Method (revised 2026-11-08 after rigor audit)

LLM-assisted appraisal, validated before use. 1) A human revises the rubric anchors (Anchor_Revision) and outside experts rate item relevance (Expert_Review); rubric frozen as v1.2. 2) Prompt frozen as AI-P1.1. 3) Two different LLMs score the 20 validation sources from full text with fixed settings; scores stored outside the shared sheet. 4) Tani and Gabe score the same sources blind; consensus agreed. 5) AI scores pasted in; agreement.py gives the decision. 6) If accepted, AI scores the remaining sources and a person verifies every score at its cited location; a random 15-20% are also scored blind by a human (audit columns). Vivian runs the AI and is not a rater.

## Validation set (revised 2026-11-08)

All 41 Includes were put in random order (Python random.Random(202611082), stratified so about two empirical sources per review/grey source). Sources 1-20 form the validation set (14 empirical, 6 review/grey). No source was hand-picked; three of them (Khajehnejad, Liu Braille, Jordan FinalSpark) had an earlier exploratory AI pass, which is disclosed. The 9-source set from earlier the same day is withdrawn.

## Acceptance rule (revised 2026-11-08, set before any validation scores exist)

Primary: delta = mean(weighted kappa of Tani vs AI, Gabe vs AI) minus weighted kappa of Tani vs Gabe, with a 95% CI from 2,000 bootstrap resamples of papers (agreement.py). AI non-inferior if the lower bound is above -0.15; inferior if the upper bound is below -0.15; otherwise inconclusive, in which case the AI result is reported as exploratory and humans score the main corpus. Sensitivity: same test with Gwet's AC2. Per item: AI-assisted only if consensus-vs-AI exact agreement is at least 70% and off-by-2 occurs on at most 10% of sources; other items are human-scored. Margin 0.15 chosen because published LLM risk-of-bias studies report AI-human weighted kappa of about 0.3-0.5, so a smaller margin would be unrealistic and a larger one would not be meaningful.

## AI scoring paused (2026-11-08)

Audit issue C2: anchors and prompt AI-P1.0 were drafted with AI help. No further AI scoring until the anchors are human-revised and frozen and AI-P1.1 is written. The two papers scored under AI-P1.0 (locked file) are exploratory only and will be re-scored.

## Registration timing (honest statement for OSF)

Searching and title/abstract screening were done before registration; two sources had an exploratory AI scoring pass. Registration happens before any validation or main-corpus appraisal scores exist.

## Search (revised 2026-11-08, audit issue C4)

The paper-index queries Q1-Q8 are kept as a pilot search but are not reproducible (proprietary index, top-N cut-offs). The reported search is Search_Log S1-S8: full Boolean strings in PubMed plus Scopus or Web of Science, preprint servers, citation chaining and archived grey literature, all from 2020-01-01, with no relevance cut-off. Second screener: random 20% of title/abstract decisions plus all Maybes, with kappa reported; if kappa is below 0.6, dual-screen everything.

## Rubric content validation (audit issue C3)

Item_Evidence lists the failure each item targets and supporting literature (each reference to be checked before citing). Expert_Review collects relevance and clarity ratings from 3 outside experts; items need I-CVI = 1.0 to stay unchanged, scale S-CVI/Ave >= 0.90. Anchor_Revision records the human rewrite of every anchor. Rubric frozen as v1.2 only after both are complete.

## Rubric v1.2 draft and reduced human workload (2026-11-08)

Rule items (SM, UA, CT, CF, EA, RB, TR, SR) are now answered as factual checks (Check_Items) and scored by a fixed rule, identically in the sheet (Checks tab) and in agreement.py (--score); the two were checked against each other on edge cases. Judgment items (CC; PS, HR, MP for reviews) keep anchors. Validation stays at 20 sources with two blind humans: this human calibration set cannot be removed, because AI error can only be measured against independent human labels. What is removed is most of the human scoring of the main corpus.

## Main-corpus routing (pre-set)

Two different AI models answer every source. A rule-item score is accepted without human verification only if (a) both models give the same score, (b) the item passed the per-item rule on Validation, (c) when both models agreed on Validation they matched the human consensus on at least 90% of sources, and (d) that 90% rests on at least 10 sources. Everything else, including every judgment-item score and every review-track score (only 6 review sources, too few to validate), is verified by a person at the cited location. The random 15-20% blind human audit covers auto-accepted scores too and is reported with a 95% CI; if audit agreement on auto-accepted scores falls below 85%, auto-accept is withdrawn and those scores are verified.

## Check-level reporting

agreement.py --checks reports per check: human-human agreement (exact, Gwet AC1), AI sensitivity and specificity against the consensus with Wilson 95% CIs, AI1-AI2 agreement and accuracy when they agree, and the rate of U answers. Checks with fewer than 5 consensus-Y sources are flagged as not estimable rather than reported as accurate. A check with U on more than 20% of answers is reworded before the freeze.

## Known limits of this design

1) The reference standard is two student raters, not domain experts; disputed 0-vs-2 items should be adjudicated by Margaret or an outside expert if available, and the paper should say who the raters were. 2) The checks were drafted with AI help (same issue as audit C2), so Anchor_Revision and Expert_Review must cover Check_Items before the freeze. 3) With 14 empirical sources, per-item accuracy CIs are wide (13/14 correct gives a lower bound of about 0.69); the audit, not the validation set, is the main evidence for auto-accepted scores. 4) AI runs must be scripted (fixed model version, temperature, prompt version, date) so they can be re-run.

## Running the analysis

Standard-library Python 3, no installs. In Windows CMD, from `oi-review\analysis`:

```
python agreement.py Validation.csv
python agreement.py --checks Checks.csv
python agreement.py --score AI_checks.csv > AI_item_scores.csv
```

Download the Validation and Checks tabs as CSV first (File > Download > Comma-separated values). `test_data/` holds synthetic files (made-up answers with known error rates) to check the script runs; they are not study data.
