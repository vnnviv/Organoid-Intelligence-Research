# Rubric: scoring anchors v1

Score each item 2, 1, 0 or NA. NA only when the item truly does not apply. If an item applies but the information is missing, score 0.


## Empirical papers (9 items)

| Item | Asks | 2 | 1 | 0 | NA when |
|---|---|---|---|---|---|
| SM System match | Does the claim concern the system that was actually tested? | Claim is about the substrate tested (organoid claims from organoid data) | Mixed or 2D/organoid gap exists and the paper acknowledges it | Claim extrapolated beyond the system tested with no acknowledgment (e.g., 2D culture result presented as organoid or brain evidence) | Never for empirical papers. For reviews, score the evidence they cite for their headline claims |
| UA Unit of analysis | Are statistics done at the level of independent biological units? | Stats at culture/organoid level, or a model that accounts for repeated sessions | n reported but independence unclear | n missing, or repeated sessions/recordings treated as independent samples | No quantitative result or statistics reported (reviews, grey literature) |
| CT Controls | Could the result arise from artifact rather than neural activity or learning? | Two or more appropriate negative controls (e.g., no-cell, inactive cells, no stimulation, no feedback) | One control | No controls | Reviews and grey literature |
| CF Comparator fairness | If compared with AI/silicon, is the comparison like-for-like? | Same task and metric, matched inputs and budget, baseline tuned or tuning documented, no cap that favors one side | Partial matching, limitations stated | Comparator unmatched, untuned, or unspecified | No comparison to AI or silicon is made |
| EA Energy accounting | If an energy-efficiency claim is made, was energy measured for the full system? | Measured full-system energy including life support (incubation, pumps, cooling), against a stated comparator | Partial measurement (e.g., electrode or neuron level only) | Energy appears only as motivation or as brain-level figures | No energy claim. Sample- or data-efficiency claims are scored under CF, not here |
| RB Robustness | Does the result hold across days, batches, lines, or labs? | Shown across days/batches/lines (or replicated within the paper) | Single condition, limitation honestly stated | Not examined, or contradicted by the paper's own data | Reviews and grey literature |
| TR Transparency | Could another lab reproduce the work? | Methods sufficient (organoid/culture protocol, stimulation and recording parameters) and data or code available | Methods sufficient but no data/code, or data on request only | Insufficient methods and no data/code | Grey literature (score as 0 if no methods given) |
| CC Claim calibration | Do title, abstract, and headline claims match the evidence and the paper's own limitations? | Headline claims match results and limitations | Mild overreach (stronger wording in title/abstract than in results) | Headline contradicted by the paper's own hedges or limitations | Never |
| RP Replication | Has the result been reproduced by anyone other than the original team? | Independently reproduced by a lab with no author overlap (or an independent reanalysis of shared data reaches the same result) | Repeated only by the same group or company, or in a follow-up by overlapping authors | No replication attempt known | Never. Expect mostly 0 in this field; the point is to see where the exceptions are |

## Reviews, roadmaps, company pages (4 items)

| Item | Asks | 2 | 1 | 0 | NA when |
|---|---|---|---|---|---|
| PS Primary sourcing | Do the headline numbers trace to primary measurements? | Each headline number is cited to the primary study that measured it | Some traced, some cited second-hand or to other reviews | Key numbers uncited, or only cited to reviews or press | Never |
| HR Hedge retention | Does it carry forward the original authors' caveats? | Caveats preserved (e.g., 2D not organoid, whole-brain not organoid, capped comparison) | Some caveats dropped | Caveated results stated as established | Never |
| MP Measured vs projected | Does it separate what was measured from what is projected or hoped for? | Labels measured, projected and aspirational claims clearly | Partly separated | Blends them (e.g., brain-level efficiency presented as organoid-level) | Never |
| CC Claim calibration | Do title, abstract and headline match the evidence it presents? | Headline matches the evidence and the stated limits | Mild overreach | Headline contradicted by its own hedges or by the evidence it cites | Never |
