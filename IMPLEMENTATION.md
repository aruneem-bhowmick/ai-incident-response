# Implementation

How Project Warrant's pieces fit together, and how to reproduce the headline
metrics. This file describes what exists in the repo as of this scaffold task
(P0.6) — it will grow as later phases land.

## Pieces

- **`/sources/manifest.csv`** — one row per primary source used anywhere in the
  project: `source_id, source_org, title, url, retrieval_date, revision_note,
  local_path`. Populated by the source-freeze task; archived snapshots of the
  sources themselves live alongside it under `/sources/`.
- **`/docs/codebook.md`** — the claim-coding codebook (DL-2): the controlled
  vocabulary for `claim_type` (T-codes), evidentiary `channel` codes (C-codes),
  `verifiability` tiers (V-codes), and the verdict rules for the three
  degradation conditions (D1 opacity, D2 unfaithfulness, D3 adversarial
  forgery). This is the authoritative definition of every coded column in the
  ledger; `/ledger/schema.md` only documents column *shape*, not the vocabulary
  itself, and defers to the codebook for that.
- **`/ledger/claims.csv`** — the claim ledger (DL-1): one row per public claim
  about the incident, coded against the codebook. Target size is 80-150 rows
  (Gate G0). Column definitions are in `/ledger/schema.md`.
- **`/scripts/metrics.py`** — computes the four headline metrics (M1-M4) from
  `/ledger/claims.csv`. Per R-03, metrics are never computed by hand — this
  script is the only sanctioned way to produce them for the report.
- **`/scripts/test_metrics.py`** — unit tests for `metrics.py` against a
  self-contained 5-row fixture (not the real ledger, which may not exist yet or
  be incomplete). Run with `python scripts/test_metrics.py` or `pytest
  scripts/`.
- **`/report/template/`** — the official sprint report template (downloaded
  from the Apart Research sprint page's Guidelines section).
- **`/report/report.tex`** — the LaTeX skeleton for the actual submission,
  structured per the project's own report outline (Introduction, Related Work,
  Method, Results, MRFM v0.1, Discussion, Appendices), not the generic template
  outline. Sections are stubbed with placeholder comments only; content is
  written in a later phase.

## Reproducing the headline metrics

```
python scripts/metrics.py
```

By default this reads `ledger/claims.csv` relative to the repo root and prints
M1-M4 to stdout. Pass an explicit path as the first argument
(`python scripts/metrics.py path/to/claims.csv`) to point it at a different
ledger snapshot. If the ledger file does not exist yet or is empty, the script
reports that explicitly rather than crashing.

To verify the metric logic itself (independent of whether the real ledger is
populated), run the test suite:

```
python scripts/test_metrics.py
```

## Changelog

`CHANGELOG.md` at the repo root has a plain-language, sprint-framed entry
for every PR merged to `main` — what to read if you want "what changed and
why it matters for Project Warrant" without reading diffs.

## What is not built yet

The **MRFM v0.1** — the project's draft minimum forensic standard that Results
feeds into — and the **full report** (compiled PDF from `report.tex` with real Results and Discussion
content) are both later-phase deliverables (P2/P3 in the sprint plan), not part
of this scaffold task. `report/report.tex` currently contains only a stubbed
section skeleton for both; there is no MRFM clause table or report content yet.
Similarly, `/docs/codebook.md`, `/docs/prior-art.md`,
`/docs/excerpt-inventory.md`, and `/ledger/claims.csv` are the outputs of other
P0 tasks and may not exist or may be incomplete at the time this file is read —
`scripts/metrics.py` is written to degrade gracefully (not crash) if the ledger
isn't there yet.
