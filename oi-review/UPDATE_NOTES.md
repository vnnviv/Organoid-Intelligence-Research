# OI Review: Update Notes (Nov 2026)

9 Nov 2026 · Vivian Chan

## 12 Nov 2026 update

- Merged pull request #1 (rubric v1.2, method notes, agreement.py, update notes) into main.
- Ran PubMed S1 and arXiv S5 as planned: 1,723 and 23 records, 1,685 new after de-duplication against Screening_Log. Logged on Search_Log; records to screen are in the Drive sheet "OI_search_S1_S5_new_records_to_screen (2026-11-12)".
- Search check: S1 finds 17 of the 19 known Includes that PubMed indexes. A revised string (Search_Log row 15, `search/S1_string_test.md`) finds 19 of 19 with 1,246 records; this is optimistic because two terms were added after seeing the misses. Cai 2023 and Smirnova 2023 are not in PubMed, so Scopus or Web of Science is required.
- Added `analysis/run_ai.py`: builds the AI prompt from the Check_Items and Rubric_Anchors tabs, logs every call (model, settings, prompt SHA-256, date, raw reply), validates replies, and writes files that paste into the Checks and Validation tabs. Tested with a mock model only.
- Drafted expert-review requests (not sent) and a Friday agenda with an RM 7 draft.
- Open decision: Khajehnejad and Liu are validation sources and are also on the group reading list; discussing them before blind scoring would inflate rater agreement. Proposal: swap them for reserve sources 21 and 22.

## Summary

The review now uses LLM-assisted rigor appraisal, validated against two blind human raters on 20 random sources. Rubric v1.2 (draft) turns eight items into factual checks scored by a fixed rule, which cuts most human scoring of the main corpus. Everything is built and tested with dummy data; nothing has been scored yet.

The work is in the Google Sheets workbook (OI_Critical_Review_Scoring_Sheet), the `agreement.py` script, and this repo. The next blocker is human: anchors and checks must be revised by a person and rated by 3 outside experts before the rubric is frozen.

## Method change

The method is now "LLM-assisted rigor appraisal, validated against human raters". This is a methods contribution on top of the OI findings.

Humans cannot be removed entirely. Every published LLM-as-judge or automated-appraisal approach measures AI error against an independent human-labelled set, and RAISE and the 2025 Cochrane/Campbell/JBI/CEE position statement require human oversight. What can be removed is most of the human scoring of the main corpus.

Why the design looks the way it does:

- LLM agreement with humans on judgment-type appraisal is weak: published weighted kappa is about 0.3 to 0.5, against about 0.65 between two humans.
- A Psychological Bulletin study of 8 LLMs found accuracy varied most between variables and least between models, and was higher when variables were described in detail. So rewriting items as precise questions matters more than which model is used.
- Large metascience audits (Serghiou 2021 on 2.75 million PMC articles; SciScore on 1.58 million) automate factual reporting indicators, validated once against human labels with sensitivity and specificity.

Roles: Tani and Gabe are the blind raters. Vivian runs the AI and is not a rater.

## Rubric changes

v1.1 added a review track and tightened the scoring rules; v1.2 (draft, not frozen) splits items into factual checks and judgment items.

**v1.1 (8 Nov)**

- Reviews, roadmaps and grey literature are scored on their own sheet with five items: PS primary sourcing, HR hedge retention, MP measured vs projected, SR search and selection transparency (new, from PRISMA 2020 items 5-7 and AMSTAR 2 item 4), CC claim calibration.
- NA only when a claim never appears. An untested motivation claim (for example "more energy-efficient than AI" with no measurement) scores 0, not NA.
- Independent replication is a recorded descriptor, not a scored item, so papers are not marked down for the field's age.
- Claims are logged on the Claims tab before CC is scored.

**v1.2 draft (8 Nov)** — full checks in [rubric_v1_2_checks.md](rubric_v1_2_checks.md)

| Type | Items | How scored | Who checks |
| --- | --- | --- | --- |
| Rule items (empirical) | SM, UA, CT, CF, EA, RB, TR | Raters answer 2-5 factual checks each; a fixed rule gives 0/1/2/NA | Auto-accepted only when both AIs agree and validation supports it |
| Rule item (review) | SR | Three Y/N checks | Always human-verified (only 6 review sources) |
| Judgment items | CC; PS, HR, MP, CC for reviews | Anchors, 0/1/2/NA | Always human-verified |

- The same rule runs in the sheet (Checks tab) and in `agreement.py --score`; both gave identical results on 35 edge-case scores.
- Two old gaps now have a rule: TR with data shared but thin methods = 1; EA with full measurement but no comparator = 1.
- CT counts only five control types (no cells, inactive cells, no stimulation, no feedback, sham feedback). Other controls go in Notes.
- UA keeps NA for papers with no quantitative result (this was dropped by mistake and restored).

## Validation, acceptance and routing

The AI is used on the main corpus only if it is non-inferior to a human rater on 20 random sources, and every rule was set before any scores exist. Full text in [method_v1_2.md](method_v1_2.md).

**Validation set.** All 41 Includes were randomly ordered (seed 202611082, stratified about 2 empirical per review). Sources 1-20 are the validation set: 14 empirical, 6 review/grey. Sources 21-30 are a reserve list (Protocol row 26). The earlier hand-picked 9-source set is withdrawn.

**Order of work**

1. A person revises anchors and checks; 3 experts rate them; rubric frozen as v1.2 and prompt as AI-P1.1.
2. Two different AI models answer the 20 sources; answers stored outside the shared sheet.
3. Tani and Gabe fill the Checks tab and the judgment items blind, then agree a consensus.
4. AI answers are pasted in last; Validation and Checks are downloaded as CSV and `agreement.py` gives the decision.

**Acceptance rule (primary).** delta = mean(kappa Tani-AI, kappa Gabe-AI) minus kappa Tani-Gabe, linear-weighted, with a 95% CI from 2,000 bootstrap resamples of papers. Lower bound above -0.15 = non-inferior; upper bound below -0.15 = inferior; otherwise inconclusive, and humans score the corpus. Gwet's AC2 is the sensitivity analysis. The margin 0.15 reflects published AI-human kappa of about 0.3-0.5.

**Per item.** AI-assisted only if consensus-vs-AI exact agreement is at least 70% and off-by-2 happens on at most 10% of sources.

**Main-corpus routing.** A score skips human checking only if all four hold:

- both AI models give the same score;
- it is a rule item that passed the per-item rule;
- when both AIs agreed on Validation, they matched the consensus on at least 90% of sources;
- that 90% rests on at least 10 sources.

Everything else is verified by a person at the cited location (AI_Scoring column U says auto-accept or verify). A random 15-20% blind human audit covers auto-accepted scores too; if audit agreement on them drops below 85%, auto-accept is withdrawn.

## Rigor audit fixes

All four critical audit issues have a fix in the workbook; three still need human work to close.

| Issue | Fix made | Still needed |
| --- | --- | --- |
| C1 Validation set too small and hand-picked (9 sources gave a kappa CI about 0.25 wide) | Random, stratified 20-source set (CI about 0.17 wide); pre-set non-inferiority rule; paper-level bootstrap | Tani and Gabe score the 20 sources |
| C2 Anchors and prompt drafted with AI help (circularity) | AI scoring paused; prompt AI-P1.0 retired; Anchor_Revision tab for a human rewrite; the two AI-scored papers marked exploratory | A person rewrites anchors and checks; write AI-P1.1 |
| C3 No content validation of the rubric | Item_Evidence tab; Expert_Review tab with I-CVI (must be 1.0 with 3 experts) and S-CVI/Ave at least 0.90; experts now rate the checks too | Recruit 3 experts and collect ratings |
| C4 Search not reproducible (proprietary index, top-N cut-offs) | Search_Log S1-S8: full Boolean strings for PubMed, Scopus or Web of Science, preprint servers, citation chaining, archived grey literature, from 2020-01-01 | Tani runs the searches; second screener on 20% plus all Maybes |

Other fixes:

- Score dropdown values were stored as text, so formulas would have ignored them; converted to numbers.
- Validation flags now say "compare check answers" for a 0-vs-2 split on a rule item, and "fix anchor" only for judgment items.
- Registration-timing statement added for OSF: searching and screening came before registration; validation and appraisal scores will not.

## Workbook and script

The workbook has 21 tabs; the ones that changed this week are below.

| Tab | What it holds | Who fills it |
| --- | --- | --- |
| Protocol | Criteria, change log, PRISMA mapping, method, acceptance and routing rules, known limits (rows 21-34) | Fixed |
| Search_Log | Search strings S1-S8 | Tani runs them |
| Check_Items | The v1.2 checks and scoring rules | Human rewrite, then frozen |
| Anchor_Revision | Current anchors next to a human rewrite | Margaret or an instructor |
| Item_Evidence, Expert_Review | Why each item exists; expert relevance and clarity ratings | 3 outside experts |
| Checks | One row per source and rater (Tani, Gabe, Consensus, AI 1, AI 2); scores computed by rule | Tani and Gabe blind, AI last |
| Validation | 20 sources by item; judgment items scored here, rule items pulled from Checks | Tani and Gabe blind, AI last |
| Agreement | Point estimates and per-item routing (the decision comes from the script) | Formulas |
| AI_Scoring | Main corpus: two AI scores, agree flag, route, human verdict, verified score | Vivian pastes; humans verify |
| Scoring, Scoring_Reviews | Scores used in the analysis, plus blind audit columns | Formulas plus audit |

`analysis/agreement.py` needs only standard Python. Download the tab as CSV first, then in Windows CMD:

```
python agreement.py Validation.csv
python agreement.py --checks Checks.csv
python agreement.py --score AI_checks.csv > AI_item_scores.csv
```

The first gives pair kappas, AC2, bootstrap CIs and the primary decision. The second gives per-check sensitivity and specificity with Wilson 95% CIs, AI1-AI2 agreement and "can't tell" rates. The third turns AI check answers into item scores. Each was tested on synthetic data and on empty and wrong files.

## GitHub updates

| Date | File | Change |
| --- | --- | --- |
| 9 Nov | `oi-review/UPDATE_NOTES.md` | These notes |
| 9 Nov | `oi-review/rubric_v1_2_checks.md` | Rubric v1.2 draft: checks and scoring rules |
| 9 Nov | `oi-review/method_v1_2.md` | Method, validation, acceptance and routing rules, known limits, how to run the script |
| 9 Nov | `oi-review/analysis/agreement.py` | Analysis script, plus synthetic test files in `test_data/` |
| 9 Nov | `oi-review/OI_Critical_Review_Scoring_Sheet.xlsx` | Fresh export of the live workbook; checked to contain no AI or rater scores |
| 9 Nov | `README.md` | Current status, plan and file list |

Left out on purpose: scratch build files, and the private locked file with exploratory AI scores (the repo is public).

Already public before this week: `oi-review/pilot/pilot_scores_ai.csv` holds AI scores for Khajehnejad, Liu and Jordan, three of the 20 validation sources. Raters must not open it before scoring, and the OSF registration should disclose it.

## Known limits and risks

1. **The reference standard is two student raters.** A reviewer can ask why their consensus counts as truth. Have Margaret or an outside expert settle 0-vs-2 disputes, and state who the raters were.
2. **The checks were drafted with AI help.** Same circularity as audit issue C2; the human rewrite and expert ratings must cover Check_Items before the freeze.
3. **14 empirical sources is a small validation set.** Even 13 of 14 correct gives a lower 95% bound of about 0.69, so the blind audit is the main evidence for auto-accepted scores.
4. **AI runs are not reproducible yet.** A script must record the model version, temperature, prompt version and date. This is the biggest open gap.
5. **Rare "yes" answers.** Checks such as public code or full-system energy measurement may have too few positives to estimate sensitivity; the script flags these and the paper should say so.
6. **Workload is still real.** Each rater fills about 23 quick checks plus the judgment items for 20 sources. The time saved comes from the main corpus, not from validation.
7. **The agreement test may fail.** Given published AI-human kappa of 0.3-0.5, an inconclusive result is possible; then the AI part is reported as exploratory and humans score the corpus.

## Next steps

The rubric freeze is the blocker: nothing downstream can start until the first two items are done.

- [ ] Rewrite anchors and checks (Anchor_Revision, Check_Items): Margaret or an instructor
- [ ] Recruit 3 outside experts and collect Expert_Review ratings: Vivian
- [ ] Write and freeze prompt AI-P1.1; set up a scripted AI run that logs model, settings and date: Vivian
- [ ] Run Search_Log S1-S8; second screener on 20% plus Maybes: Tani
- [ ] Register Protocol, rubric v1.2 and analysis plan on OSF, disclosing the public pilot file: team
- [ ] Blind scoring of the 20 validation sources: Tani and Gabe
- [ ] Two AI runs, paste last, run agreement.py: Vivian
- [ ] Change workbook sharing from "anyone with link" to named editors: Vivian
- [ ] Merge pull request #1; tell Tani about the method change and file RM 7: Vivian

## Sources

- [Serghiou et al. 2021, PLOS Biology: transparency indicators across the biomedical literature](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3001107)
- [rtransparency package and validation](https://rdrr.io/cran/rtransparency/f/README.md)
- [Menke et al., SciScore rigor criteria at scale](https://pmc.ncbi.nlm.nih.gov/articles/PMC7644557)
- [Gartlehner et al. 2025, AI-assisted data extraction study within reviews](https://www.rti.org/publication/artificial-intelligence-assisted-data-extraction-with-a-large-lan)
- [Psychological Bulletin 2025, determinants of genAI extraction accuracy](https://ifp.nyu.edu/2025/journal-article-abstracts/bul0000501/)
- [GMDS 2025, LLMs for data extraction in a systematic review](https://conferences.publisso.de/en/conferences/gmds2025/25gmds060)
- [How to Correctly Report LLM-as-a-Judge Evaluations (ICML 2026)](https://icml.cc/media/icml-2026/Slides/63607.pdf)
