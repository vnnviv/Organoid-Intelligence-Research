# Searches

Scripts for the database searches on the Search_Log tab. Standard-library Python; run from this folder in Windows CMD.

- `run_searches.py`: PubMed S1 as planned. Writes `S1_pubmed.csv` (not committed: it holds publisher abstracts) and `run_log.json`.
- `run_arxiv.py`: arXiv S5. Writes `S5_arxiv.csv` and adds to `run_log.json`.
- `test_strings.py`, `compare.py`: compare the planned PubMed string with revised versions by record count and by how many known Includes they find.
- `S1_string_test.md`: results of that comparison on 12 Nov 2026.

First run: 12 Nov 2026, before OSF registration, so it counts as a pilot run. Record counts: S1 1,723 (1,669 new), S5 23 (16 new). Which string is registered is a team decision; re-run on the registration date.
