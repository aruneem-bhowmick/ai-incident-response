# Implementation

How Project Warrant's pieces fit together, and how to reproduce the headline
metrics.

## Pieces

- **`/sources/manifest.csv`**: one row per primary source used anywhere in the
  project: `source_id, source_org, title, url, retrieval_date, revision_note,
  local_path`. Archived snapshots of the sources themselves live alongside it
  under `/sources/`.
- **`/docs/codebook.md`**: the claim-coding codebook (DL-2), the controlled
  vocabulary for `claim_type` (T-codes), evidentiary `channel` codes (C-codes),
  `verifiability` tiers (V-codes), and the verdict rules for the three
  degradation conditions (D1 opacity, D2 unfaithfulness, D3 adversarial
  forgery). This is the authoritative definition of every coded column in the
  ledger; `/ledger/schema.md` only documents column *shape*, not the vocabulary
  itself, and defers to the codebook for that.
- **`/ledger/claims.csv`**: the claim ledger (DL-1), 125 rows, frozen at
  schema/content version v1.2, one row per public claim about the incident,
  coded against the codebook. Column definitions are in `/ledger/schema.md`.
- **`/scripts/metrics.py`**: computes the five headline metrics (M1-M5) from
  `/ledger/claims.csv`. Per R-03, metrics are never computed by hand; this
  script is the only sanctioned way to produce them for the report.
- **`/scripts/test_metrics.py`**: unit tests for `metrics.py` against a
  self-contained 5-row fixture. Run with `python scripts/test_metrics.py` or
  `pytest scripts/`.
- **`/scripts/kappa.py`**, with its own test suite in `/scripts/test_kappa.py`:
  computes Cohen's kappa per degradation condition for the blind-recode
  reliability check documented in `/docs/reliability-report.md`.
- **`/scripts/make_results_figure.py`** and
  **`/scripts/make_channel_figures.py`**: generate the report's three
  Results figures directly from `/ledger/claims.csv`.
- **`/mrfm/mrfm-v0.1.md`**: the Monitorability-Robust Forensic Minimum
  (DL-5), 14 clauses specifying what a lab should retain, disclose, or make
  independently checkable, each grounded in a specific gap the ledger
  surfaced and diffed against METR's and GovAI's existing frameworks.
- **`/docs/rfi-questions.md`**: eight request-for-information questions
  derived from the ledger's weakest rows (`verifiability == V3` or any
  degradation-verdict `COLLAPSES`).
- **`/report/template/`**: the official sprint report template (downloaded
  from the Apart Research sprint page's Guidelines section).
- **`/report/report.tex`**: the LaTeX source for the final report,
  structured as Introduction, Related Work, Methods, Results, Discussion and
  Limitations, References, and an Appendix. Compiles to
  `/report/report.pdf` per `/report/BUILD.md`'s instructions.

## Reproducing the headline metrics

```
python scripts/metrics.py
```

By default this reads `ledger/claims.csv` relative to the repo root and prints
M1-M5 to stdout. Pass an explicit path as the first argument
(`python scripts/metrics.py path/to/claims.csv`) to point it at a different
ledger snapshot.

To verify the metric logic itself, run the test suite:

```
python scripts/test_metrics.py
```

## Changelog

`CHANGELOG.md` at the repo root has a plain-language, sprint-framed entry
for every PR merged to `main`: what to read if you want "what changed and
why it matters for Project Warrant" without reading diffs.
