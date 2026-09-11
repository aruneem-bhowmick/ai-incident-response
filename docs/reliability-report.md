# Reliability Report — Cohen's κ on the Blind-Recode Subsample (DL-4)

**Project:** Project Warrant
**Deliverable:** DL-4 — inter-rater reliability for the D1/D2/D3 degradation coding, per Gate G1.
**Status:** computed from script output below; not asserted, not hand-estimated (R-03, R-04).

---

## 1. What was compared

- **Rater A ("answer key"):** `C:\Users\arune\research\sprints\_warrant-reliability-answer-key\answer-key.csv`
  — the original P1.1 verdicts for the 25-row reliability subsample, built by an earlier
  P1 task and held outside this repo so the blind re-coder could not see it.
- **Rater B ("blind recode"):** `ledger/blind-subsample-recoded.csv` — the same 25 rows,
  independently re-coded cold (verdicts stripped, re-coded without reference to the
  original), per `p1.2-blind-recode`.
- **Instrument:** `scripts/kappa.py`, which implements Cohen's κ directly (`kappa = (p_o
  - p_e) / (1 - p_e)`) with no external dependency, matching each row by `claim_id` and
  computing one κ per condition (D1, D2, D3) over the `d1_verdict` / `d2_verdict` /
  `d3_verdict` columns, drawn from the controlled vocabulary `{SURVIVES, DEGRADED,
  COLLAPSES}` (`docs/codebook.md` §2.3).

## 2. Command and actual output

```
python scripts/kappa.py "C:\Users\arune\research\sprints\_warrant-reliability-answer-key\answer-key.csv" ledger\blind-subsample-recoded.csv
```

```
Cohen's kappa -- original: C:\Users\arune\research\sprints\_warrant-reliability-answer-key\answer-key.csv, recoded: ledger\blind-subsample-recoded.csv
D1 (opacity) kappa:             0.7788
D2 (unfaithfulness) kappa:      0.5690
D3 (adversarial forgery) kappa: 0.7794
```

This command was re-run a second time (once via a POSIX-style path under Bash, once via
the literal Windows path under PowerShell, both against the same two files) and produced
identical values both times. Both raters supplied verdicts for all 25 shared `claim_id`s
on all three conditions — 25 matched, non-blank pairs per condition — so none of the
three κ values is a degenerate/undefined case (no `NaN`s were returned; see
`scripts/kappa.py`'s `cohens_kappa` for when that would occur — either zero matched pairs,
or every matched pair identical in category for both raters, making chance agreement 1.0
and the denominator zero). All three results here are genuine, non-degenerate
computations.

| Condition | κ (computed) | ≥ 0.6? |
|---|---|---|
| D1 — opacity | **0.7788** | Yes |
| D2 — unfaithfulness | **0.5690** | **No** |
| D3 — adversarial forgery | **0.7794** | Yes |

## 3. Decision rule (restated verbatim from `planning/SPRINT-PLAN.md` §6, P1.2)

> P1.2 Blind a 25-row subsample (strip your verdicts), re-code it cold, compute Cohen's κ
> per condition. **If κ < 0.6 on any condition, the codebook rule for that condition is
> underspecified: fix the rule, log an ADR, recode the whole ledger against the fixed
> rule.**

## 4. Verdict, given the actual numbers above

**κ < 0.6 on D2 (unfaithfulness) — the codebook-fix-and-recode issue should be executed
before freezing.**

D1 (opacity, κ = 0.7788) and D3 (adversarial forgery, κ = 0.7794) both clear the 0.6 bar
comfortably and would, on their own, support proceeding to freeze. But the decision rule
is stated per-condition and triggers on *any* condition falling short — it does not
average across conditions or let strong conditions offset a weak one. D2's κ of 0.5690
is below 0.6, so the rule's fix-and-recode branch applies specifically to **D2
(unfaithfulness)**: the D2 codebook rule (`docs/codebook.md` §2.3) is underspecified
enough that two independent, blinded coders disagreed more than the 0.6 threshold
tolerates. D1 and D3 do not require a codebook fix or a full recode on their own basis.

Gate G1's reliability bar is **not** met as-is (one of three conditions fails). Per the
decision rule, the next step is: fix the D2 rule in `docs/codebook.md`, log the change as
a dated ADR (R-07: "codebook changes after coding begins are recorded as dated ADR
entries; no silent recoding"), and recode the whole ledger's D2 verdicts against the
fixed rule — before the ledger is frozen at v1.0.

## 5. Degenerate-case check

None of the three conditions is degenerate. All three κ values are ordinary, finite
numbers computed from 25 non-blank, matched pairs per condition; none relies on a
`NaN`/undefined result being reported as if it were a clean pass.
