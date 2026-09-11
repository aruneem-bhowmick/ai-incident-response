# Headline metrics (M1-M4) — Project Warrant

**Deliverable:** Gate G1's closing step (`planning/SPRINT-PLAN.md` §6, P1.3). Computed by
script, never by hand (R-03), from the frozen claim ledger.

**Status:** Final. `ledger/claims.csv` is frozen at **v1.1** as of **2026-09-11** — 116
rows, all six degradation columns (`d1_verdict`/`d1_note`/`d2_verdict`/`d2_note`/
`d3_verdict`/`d3_note`) populated. See `ledger/schema.md`'s changelog for the freeze
statement and `docs/reliability-report.md` + `adr/0001-d2-self-report-corroboration.md`
for why the version is v1.1, not v1.0 (below).

---

## 1. Provenance

- **Ledger:** `ledger/claims.csv`, v1.1. D1 and D3 verdicts are exactly as originally
  coded in P1.1. D2 verdicts reflect the corrected codebook rule from
  `adr/0001-d2-self-report-corroboration.md` — `d2_verdict`/`d2_note` were recoded for 6
  of 116 rows after the blind-recode reliability check found Cohen's κ = 0.5690 on D2
  (below the 0.6 bar), while D1 (κ = 0.7788) and D3 (κ = 0.7794) both passed and were left
  untouched. Full detail: `docs/reliability-report.md`.
- **Script:** `scripts/metrics.py` (unit-tested, `scripts/test_metrics.py`, 14/14 passing).
- **Command run:** `python scripts/metrics.py` (default path, resolves to
  `ledger/claims.csv`), executed 2026-09-11 against the final, fully-recoded ledger
  described above.
- **Note on D2/D3 and these four numbers:** none of M1-M4 as implemented reads
  `d2_verdict` or `d3_verdict` directly — M1/M3 are structural (channel-code membership),
  M2 reads only `d1_verdict`, and M4 reads only `claim_type`/`verifiability`. The D2 fix
  and recode was still required to satisfy Gate G1's per-condition κ bar and to keep the
  codebook/ledger consistent before freeze; it does not change any of the four numbers
  below, and re-running this script before vs. after the recode would print identical
  output.

## 2. Script output (verbatim)

```
Claims loaded: 116 (from ledger/claims.csv)
M1 - CoT monopoly (T3 claims, sole channel C1):        11.1% (0.1111)
M2 - Record survival under opacity (overall):          89.7% (0.8966)
M2 - Record survival under opacity (by claim_type):
    T1: 100.0% (1.0000)
    T2: 89.5% (0.8947)
    T3: 22.2% (0.2222)
    T4: 100.0% (1.0000)
    T5: 92.9% (0.9286)
M3 - Forgery exposure (sole substrate agent-writable): 9.5% (0.0948)
M4 - Assurance gap (T5 claims at V3):                  57.1% (0.5714)
```

## 3. The four metrics

### M1 — CoT monopoly: **11.1%** (0.1111)

**Definition** (`planning/SPRINT-PLAN.md` §4.5): share of T3 (intent) claims whose only
channel is C1 (raw chain-of-thought / agent monologue) — no corroborating channel at all.

**Plain language:** About one in nine claims made about *why* the agent did what it did
rests solely on the model's own chain-of-thought, with nothing else backing it up. That
is exactly the evidentiary channel this project's thesis flags as most likely to be
absent, unfaithful, or forged in a future incident — so a non-trivial slice of the
public's understanding of this agent's intent already depends entirely on it.

### M2 — Record survival under opacity: **89.7%** overall (0.8966); by claim type below

| Claim type | Survival under D1 (opacity) |
|---|---|
| T1 — Event | **100.0%** (1.0000) |
| T2 — Mechanism | **89.5%** (0.8947) |
| T3 — Intent | **22.2%** (0.2222) |
| T4 — Counterfactual | **100.0%** (1.0000) |
| T5 — Assurance | **92.9%** (0.9286) |

**Definition:** share of all claims (overall, and per claim type) whose D1 verdict is
`SURVIVES` — i.e., the claim's warrant would still hold up even if chain-of-thought were
never logged or never disclosed to investigators.

**Plain language:** Roughly 90% of what is publicly known about this incident would
still be knowable even if the agent's chain-of-thought had never been released — except
for claims about the agent's *intent* (T3), where survival collapses to about one in
five. This is exactly the split the sprint plan predicted (§4.5: "the prediction is that
T1 survives and T3/T4 do not") — it holds for T1 and, notably, does *not* hold for T4 in
this ledger (T4 also survives at 100%), but it holds sharply for T3: intent claims are
the ones genuinely dependent on CoT being available at all.

### M3 — Forgery exposure: **9.5%** (0.0948)

**Definition:** share of all 116 claims whose sole substrate (primary channel, zero
corroborating channels) is an agent-writable channel — C1 (raw CoT), C2 (inter-agent
message content), or C3 (tool-call/action trace) — i.e., content the agent itself could
have authored, altered, or fabricated, with the record documenting at least one
technique by which such channels were successfully forged in this incident.

**Plain language:** About one in ten claims in the record rest entirely on content the
acting agent itself produced, with no independent channel backing it up — exactly the
condition under which a forged or spoofed record could stand unchallenged.

### M4 — Assurance gap: **57.1%** (0.5714)

**Definition:** share of T5 (assurance — e.g. "no copy of the pre-release model
persists," "nothing was missed") claims coded at verifiability tier V3 (not checkable by
any third party via any stated procedure).

**Plain language:** More than half of the public reassurances that this incident is
fully contained and fully accounted for cannot be independently checked by anyone
outside the investigating institution — these are the specific claims where the public
is simply being asked to trust the lab's own word, with no stated way for an outside
party to verify it.

## 4. Reliability caveat carried forward from Gate G1

D1 (opacity, κ = 0.7788) and D3 (adversarial forgery, κ = 0.7794) both cleared the 0.6
reliability bar on the first blind-recode pass and are used here exactly as originally
coded. D2 (unfaithfulness) did not (κ = 0.5690); the codebook rule was fixed
(`docs/codebook.md` §2.3/§3.7, `adr/0001-d2-self-report-corroboration.md`) and the full
ledger's D2 columns were recoded against the fixed rule before this run — which is why
the ledger is versioned v1.1, not v1.0. As noted in §1 above, none of M1-M4 reads
`d2_verdict`, so this fix changed the ledger's integrity/reliability posture but not any
number reported here. Full reliability detail: `docs/reliability-report.md`.

The main threat to validity carried into these numbers (per `planning/SPRINT-PLAN.md`
§7): claims are coded as *reported*, so a claim can score `SURVIVES` under D1 because a
source *asserts* corroborating telemetry that this project cannot independently inspect.
That is the ceiling on M2 in particular, and it should be stated in the report's Results
section, not left implicit.

## 5. Freeze statement

Per `planning/SPRINT-PLAN.md` §6, P1.3 ("Run the metric script. Write the four numbers
down and stop touching the ledger."), `ledger/claims.csv` is frozen at **v1.1** as of
2026-09-11. Gate G1 (four metrics computed, κ reported, ledger frozen) is met. No further
edits to `ledger/claims.csv` are anticipated for the remainder of the sprint (P2/P3 build
on top of this ledger; they do not re-open it) — see the PR for this file for the
explicit statement of that intent.
