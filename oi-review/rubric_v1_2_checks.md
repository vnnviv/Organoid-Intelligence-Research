# Rubric v1.2 draft: fact checks and judgment items

Status: draft, 2026-11-08. Not frozen. A human rewrite of the checks and the expert content-validity ratings (Expert_Review tab) come before the freeze. The checks were drafted with AI help, so they need that human revision.

Rule items are answered as factual checks; a fixed rule turns the answers into the 0/1/2 score, so nobody makes the 0/1/2 call directly. The same rule is in the workbook (Checks tab) and in `analysis/agreement.py --score`, and the two were checked against each other on edge cases. Judgment items keep the anchors in `rubric_v1_1.md`. `U` means not reported or cannot tell, and counts as not-Y.

| Item | Track | Type | Check | Question | Answers | Rule |
|---|---|---|---|---|---|---|
| SM | Empirical | Rule | SM1 | What system produced the data? (2D culture, organoid, slice, in vivo, in silico, mixed) | 2D / organoid / slice / in vivo / in silico / mixed | 2 if SM1 = SM2. Otherwise 1 if SM3 = Y, else 0. |
| SM | Empirical | Rule | SM2 | What system is the headline claim (title or abstract) about? Use 'brain' for claims about brains or intelligence in general. | 2D / organoid / slice / in vivo / in silico / mixed / brain |  |
| SM | Empirical | Rule | SM3 | Does the paper say in words that its result may not carry over from the tested system to the system in the claim? | Y / N / U |  |
| UA | Empirical | Rule | UA1 | Is the number of independent biological units (cultures, organoids, chips) reported? Answer NA only if the paper reports no quantitative result or statistics at all. | Y / N / U / NA | NA if UA1 = NA. 0 if UA1 is N or U. Otherwise 0 if UA2 = Y, 2 if UA2 = N, 1 if UA2 = U. |
| UA | Empirical | Rule | UA2 | Do the statistics treat repeated sessions, recordings or electrodes from the same culture as independent samples? | Y / N / U |  |
| CT | Empirical | Rule | CT1 | How many of these negative controls were run: no cells, inactive or dead cells, no stimulation, no feedback, random or sham feedback? (other controls go in Notes and are not counted) | Whole number 0-5 | min(CT1, 2) |
| CF | Empirical | Rule | CF1 | Does the paper claim anywhere (including the introduction) that the biological system compares well with AI, silicon or another computer? | Y / N | NA if CF1 = N. 0 if CF2 is not Y. 2 if CF3 = Y and CF4 = Y. 1 if one of CF3/CF4 = Y and CF5 = Y. Otherwise 0. |
| CF | Empirical | Rule | CF2 | Was the comparator actually run in this paper (not only cited)? | Y / N / U |  |
| CF | Empirical | Rule | CF3 | Same task and same performance metric for both sides? | Y / N / U |  |
| CF | Empirical | Rule | CF4 | Is the comparator's tuning, training budget or input matching documented? | Y / N / U |  |
| CF | Empirical | Rule | CF5 | Are limitations of the comparison stated? | Y / N / U |  |
| EA | Empirical | Rule | EA1 | Does the paper claim anywhere that the system is energy- or power-efficient? | Y / N | NA if EA1 = N. 0 if EA2 = none, 1 if partial, 2 if full and EA3 = Y (full without a comparator = 1). |
| EA | Empirical | Rule | EA2 | What energy was measured? none = no measurement or brain-level figures only; partial = electrode, chip or neuron level only; full = whole system including incubation, pumps and cooling | none / partial / full |  |
| EA | Empirical | Rule | EA3 | Is the measured energy compared against a stated comparator? | Y / N / U |  |
| RB | Empirical | Rule | RB1 | Is the main result shown in more than one independent day, batch, cell line or lab? | Y / N / U | 2 if RB1 = Y. Otherwise 1 if RB2 = Y, else 0. |
| RB | Empirical | Rule | RB2 | If not, does the paper state the single-condition limitation? | Y / N / U |  |
| TR | Empirical | Rule | TR1 | Is the culture or organoid protocol reported or cited to a specific protocol? | Y / N / U | 2 if TR1 = Y, TR2 = Y and (TR3 = Y or TR4 = Y). 1 if methods (TR1 and TR2) are complete, or data or code is public. Otherwise 0. |
| TR | Empirical | Rule | TR2 | Are stimulation and recording parameters reported (e.g. amplitude, frequency, sampling rate)? | Y / N / U |  |
| TR | Empirical | Rule | TR3 | Is the data publicly available (repository, accession or supplement)? 'request' = on request only | Y / N / request |  |
| TR | Empirical | Rule | TR4 | Is the code publicly available? 'request' = on request only | Y / N / request |  |
| CC | Empirical | Judgment | - | Use the CC anchors on Rubric_Anchors, after logging claims on Claims. | 0 / 1 / 2 | Scored directly. Two AI models; disagreements go to a human. |
| SR | Review | Rule | SR1 | Are the databases or sources searched named? | Y / N / U | 2 if all three = Y, 1 if one or two = Y, 0 if none. |
| SR | Review | Rule | SR2 | Are search terms reported? | Y / N / U |  |
| SR | Review | Rule | SR3 | Are inclusion or selection criteria reported? | Y / N / U | Scored directly by two AI models; a human verifies every CC score at its cited location (CC is never auto-accepted). Model disagreements are marked for closer reading. |
| PS | Review | Judgment | - | Use the PS anchors (needs checking the cited primary source). | 0 / 1 / 2 / NA | Scored directly. AI assists; a human checks every score (6 review sources is too few to validate). |
| HR | Review | Judgment | - | Use the HR anchors. | 0 / 1 / 2 / NA | As PS. |
| MP | Review | Judgment | - | Use the MP anchors. | 0 / 1 / 2 / NA | As PS. |
| CC | Review | Judgment | - | Use the review-track CC anchors. | 0 / 1 / 2 | As PS. |

## What changed from v1.1 and why

1.0. Operationalising the anchors as checks follows the evidence that LLM accuracy depends more on how a variable is described than on which model is used, and that factual reporting indicators can be automated with measured sensitivity and specificity (Serghiou 2021; SciScore).
2.0. Two edge cases the old anchors left open now have a rule: TR with data shared but thin methods = 1; EA full measurement without a comparator = 1. The 'no cap that favors one side' part of CF anchor 2 is folded into CF4. Experts should confirm or reject these on Expert_Review.
3.0. CT now counts only the five listed control types. A paper with a good control not on the list will be under-scored; record it in Notes so the effect can be checked.
