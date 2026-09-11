# `claims.csv` schema

Column definitions for `/ledger/claims.csv`, the claim ledger (DL-1). This file
documents column **shape and purpose only**. The controlled vocabularies for
coded columns (`claim_type`, `primary_channel`, `corroborating_channels`,
`verifiability`, and the `d*_verdict` values) are defined authoritatively in
`/docs/codebook.md` (DL-2) — that document is the source of truth for what
counts as, e.g., a `T3` claim or a `C1` channel. This schema only states what
each column *is for* and what a few values mean where those values are
referenced directly by the metric definitions in `/scripts/metrics.py`, so the
metric script has a fixed contract to code against before the codebook is
frozen.

| Column | Type | Description |
|---|---|---|
| `claim_id` | string | Unique identifier for the row (e.g. `C001`). |
| `source_org` | string | Organization that published the source this claim was extracted from (e.g. `OpenAI`, `Hugging Face`, a news outlet, an independent researcher). |
| `source_url` | string (URL) | URL of the specific source document/page the claim was extracted from. Should also have a corresponding row in `/sources/manifest.csv`. |
| `retrieval_date` | ISO date (`YYYY-MM-DD`) | Date this specific source was retrieved/archived. |
| `source_revision` | string | Revision/version marker for the source if it has been edited since first publication (e.g. an updated blog post) — free text, e.g. `"v2, edited 2026-07-14"` or `"original, no known revisions"`. |
| `claim_text_paraphrased` | string | A **paraphrase** of the claim, not a verbatim quotation (paraphrase discipline, SPRINT-PLAN §5 — copyright and R-06 reasons). |
| `claim_type` | code | Controlled-vocabulary code classifying what kind of claim this is (`T1`-`T5` per the codebook). `T3` and `T5` are referenced directly by metrics M1 and M4 respectively; see `/docs/codebook.md` for what distinguishes all five. |
| `primary_channel` | code | The single evidentiary channel this claim most directly rests on (`C1`, `C2`, `C3`, ... per the codebook). `C1` is the channel implicated in the "CoT monopoly" metric (M1); `C1`/`C2`/`C3` collectively are the channels treated as **agent-writable** (i.e. content an agent could itself have authored or altered) for the forgery-exposure metric (M3). |
| `corroborating_channels` | code list | Zero or more additional channel codes that independently corroborate the claim, **semicolon-separated** (e.g. `C4;C6`), empty string if none. `scripts/metrics.py` also accepts comma-separated values defensively. A claim with an empty `corroborating_channels` value rests solely on its `primary_channel` — this is the "sole substrate" condition used by M1 and M3. |
| `verifiability` | code | Ordinal verifiability tier (`V1` strongest/most independently verifiable, down to `V3` weakest/least verifiable per the codebook). `V3` is referenced directly by metric M4 (assurance gap). |
| `d1_verdict` | code | Verdict of stress-testing this claim against degradation condition **D1 — opacity** (does the claim's warrant survive if the primary channel becomes unavailable/opaque?). Observed values include at least `SURVIVES` and `COLLAPSES`; see the codebook for the full verdict vocabulary. |
| `d1_note` | string | Paraphrased justification for the `d1_verdict` call. Subject to the same paraphrase discipline as `claim_text_paraphrased`. |
| `d2_verdict` | code | Verdict of stress-testing against degradation condition **D2 — unfaithfulness** (does the claim's warrant survive if the channel's content is an unfaithful representation of the underlying process?). Same vocabulary as `d1_verdict`. |
| `d2_note` | string | Paraphrased justification for the `d2_verdict` call. |
| `d3_verdict` | code | Verdict of stress-testing against degradation condition **D3 — adversarial forgery** (does the claim's warrant survive if the channel's content could have been forged/spoofed?). Same vocabulary as `d1_verdict`. |
| `d3_note` | string | Paraphrased justification for the `d3_verdict` call. Per **R-06**, this must never include the actual tamper/forgery technique, even at quotation level — describe at the level of "what class of technique, roughly" only. |
| `excerpt_available` | boolean-like (`TRUE`/`FALSE`) | Whether a verbatim agent-authored excerpt underlying this claim is catalogued in `/docs/excerpt-inventory.md`. |
| `coder` | string | Identifier of whoever coded this row. |
| `coding_date` | ISO date (`YYYY-MM-DD`) | Date this row was coded. |

## Notes for `/scripts/metrics.py`

- Blank/whitespace-only `corroborating_channels` (and the literal values
  `NONE`, `N/A`, `NA`, case-insensitive) are all treated as "no corroborating
  channels."
- Channel-code comparisons are case-sensitive on the codes as coded (`C1`, not
  `c1`); the metric script does not normalize case, so coders should code
  channel values consistently.
- If `/ledger/claims.csv` doesn't exist yet, or is missing rows for a given
  `claim_type`/`verifiability` slice, `scripts/metrics.py` reports the
  corresponding metric as unavailable for that slice rather than dividing by
  zero.

## Changelog

- **v1.1 frozen, 2026-09-11.** `/ledger/claims.csv` is frozen at v1.1 (116 rows, all
  six degradation columns populated) — see `/docs/reliability-report.md` for the κ
  reliability gate (D1 0.7788, D2 0.5690 pre-fix, D3 0.7794) and
  `/docs/headline-metrics.md` for the final M1-M4 numbers computed from this frozen
  ledger. Versioned v1.1, not v1.0, because D2 (unfaithfulness)'s κ fell below the 0.6
  bar, triggering a codebook rule fix and a full recode of the ledger's
  `d2_verdict`/`d2_note` columns against the corrected rule — see
  `/adr/0001-d2-self-report-corroboration.md` and `/docs/codebook.md`'s own changelog
  for the rule change itself. Per `planning/SPRINT-PLAN.md` §6 P1.3, no further edits
  to `/ledger/claims.csv` are made after this point.
