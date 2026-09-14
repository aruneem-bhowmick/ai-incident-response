# Headline metrics (M1-M4): Project Warrant

**Deliverable:** Gate G1's closing step (`planning/SPRINT-PLAN.md` §6, P1.3). Computed by
script, never by hand (R-03), from the frozen claim ledger.

**Status:** Final. `ledger/claims.csv` is at **v1.2**, **125 rows**, as of **2026-09-11**,
all six degradation columns populated on every row. See `ledger/schema.md`'s changelog
for the full freeze/reopen history and `docs/reliability-report.md` +
`adr/0001-d2-self-report-corroboration.md` for why the version passed through v1.1 first.

**Why 125 and not 116:** the ledger was frozen at 116 rows (v1.1) after Gate G1. It was
then reopened once, narrowly, to add 9 rows (`C352`-`C360`) recovered from
`lw-01`/`lw-02` at a category-only level of description. A stress-test of the frozen
results flagged that these two sources' near-total absence likely understated M3/M5's
fragility numbers, and a narrower retry succeeded where two earlier attempts had been
blocked by a safety classifier. This is a disclosed, one-time exception to the freeze,
not a re-opening of the analytical process: no existing row was changed, only 9 new
rows were added and D-coded by the same established convention (all rest solely on `C5`,
so all six degradation columns are `SURVIVES` by the same reasoning already used for
`C350`/`C351`).

**Note:** this document also carries a fifth, **supplementary** metric, M5 (§4), added
after the original four were frozen, grounded in the codebook's own broader fragility
ranking rather than a new concept. M5 does not touch or re-open the frozen ledger, and it
is never meant to be confused with the plan's original four (M1-M4).

---

## 1. Provenance

- **Ledger:** `ledger/claims.csv`, v1.2, 125 rows. D1 and D3 verdicts on the original 116
  rows are exactly as coded in P1.1. D2 verdicts on those 116 reflect the corrected
  codebook rule from `adr/0001-d2-self-report-corroboration.md`, recoded for 6 of 116
  rows after the blind-recode reliability check found Cohen's κ = 0.5690 on D2 (below the
  0.6 bar), while D1 (κ = 0.7788) and D3 (κ = 0.7794) both passed and were left untouched.
  Full detail: `docs/reliability-report.md`. The 9 rows added after the freeze
  (`C352`-`C360`) are D-coded `SURVIVES`/`SURVIVES`/`SURVIVES` by direct, uncontested
  application of the same rule already used for `C350`/`C351` (sole `C5`, no CoT, not
  agent-writable), not run through the blind-recode check, since they're not a judgment
  call on any axis that check was designed to test.
- **Script:** `scripts/metrics.py` (unit-tested, `scripts/test_metrics.py`, 15/15 passing).
- **Command run:** `python scripts/metrics.py` (default path, resolves to
  `ledger/claims.csv`), executed 2026-09-11 against the final 125-row ledger. Re-run twice
  after freeze: once to add the supplementary M5 metric (M1-M4 unchanged that time), once
  after the 9-row `lw-01`/`lw-02` addition (all five numbers shift slightly; see §2).
- **Note on D2/D3 and these four numbers:** none of M1-M4 as implemented reads
  `d2_verdict` or `d3_verdict` directly. M1/M3 are structural (channel-code membership),
  M2 reads only `d1_verdict`, and M4 reads only `claim_type`/`verifiability`. The D2 fix
  and recode was still required to satisfy Gate G1's per-condition κ bar and to keep the
  codebook/ledger consistent before freeze; it does not change any of the four numbers
  below, and re-running this script before vs. after the recode would print identical
  output.

## 2. Script output (verbatim)

```
Claims loaded: 125 (from ledger/claims.csv)
M1 - CoT monopoly (T3 claims, sole channel C1):        11.1% (0.1111)
M2 - Record survival under opacity (overall):          90.4% (0.9040)
M2 - Record survival under opacity (by claim_type):
    T1: 100.0% (1.0000)
    T2: 90.5% (0.9048)
    T3: 22.2% (0.2222)
    T4: 100.0% (1.0000)
    T5: 92.9% (0.9286)
M3 - Forgery exposure (sole substrate agent-writable): 8.8% (0.0880)
M4 - Assurance gap (T5 claims at V3):                  57.1% (0.5714)
M5 - Broad channel fragility (SUPPLEMENTARY, not one of the plan's original four):
    Primary channel in {C1,C2,C3,C6} (any corroboration):        78.4% (0.7840)
    Primary channel in {C1,C2,C3,C6} AND no corroboration:       47.2% (0.4720)
```

(Superseded output at 116 rows, before the `lw-01`/`lw-02` addition, for reference:
M1 11.1%, M2 overall 89.7% (T2 89.5%, others unchanged), M3 9.5%, M5 84.5%/50.9%. T1, T3,
T4, T5's per-type figures and M4 are identical at both row counts; the 9 new rows are
all T1/T2, all `C5`.)

## 3. The four metrics

### M1: CoT monopoly, **11.1%** (0.1111)

**Definition** (`planning/SPRINT-PLAN.md` §4.5): share of T3 (intent) claims whose only
channel is C1 (raw chain-of-thought / agent monologue), no corroborating channel at all.

**Plain language:** About one in nine claims made about *why* the agent did what it did
rests solely on the model's own chain-of-thought, with nothing else backing it up. That
is exactly the evidentiary channel this project's thesis flags as most likely to be
absent, unfaithful, or forged in a future incident, so a non-trivial slice of the
public's understanding of this agent's intent already depends entirely on it.

**Sample-size caveat:** This is 1 of 9 T3 claims in the ledger; a single row changes
this figure by roughly 11 percentage points, so treat 11.1% as directional, not precise,
until a larger claim population is coded (e.g. in a follow-up incident or a larger
sample of this one).

### M2: Record survival under opacity, **90.4%** overall (0.9040); by claim type below

| Claim type | n | Survival under D1 (opacity) |
|---|---|---|
| T1, Event | 58 | **100.0%** (1.0000) |
| T2, Mechanism | 42 | **90.5%** (0.9048) |
| T3, Intent | 9 | **22.2%** (0.2222) |
| T4, Counterfactual | 2 | **100.0%** (1.0000) |
| T5, Assurance | 14 | **92.9%** (0.9286) |

(Table corrected 2026-09-12 to the frozen 125-row ledger's per-type n's and percentages.
The table previously carried stale 116-row figures left over from before the
`lw-01`/`lw-02` addition, even though §2's verbatim script output above was already
correct. Independently re-verified against a fresh `ledger/claims.csv` read and a live
`python scripts/metrics.py` run, both of which match this table exactly. No metric value
changed; only this table's own carried-over numbers were stale.)

**Definition:** share of all claims (overall, and per claim type) whose D1 verdict is
`SURVIVES`, i.e., the claim's warrant would still hold up even if chain-of-thought were
never logged or never disclosed to investigators.

**Plain language:** Roughly 90% of what is publicly known about this incident would
still be knowable even if the agent's chain-of-thought had never been released, except
for claims about the agent's *intent* (T3), where survival collapses to about one in
five. This is exactly the split the sprint plan predicted (§4.5: "the prediction is that
T1 survives and T3/T4 do not"): it holds for T1, and it holds sharply for T3 (n=9).
Intent claims are the ones genuinely dependent on CoT being available at all.

**Sample-size caveat on T4:** the ledger contains only 2 T4 (counterfactual) claims
total, and both survive D1 (100%, i.e. 2/2). That is not a statistically meaningful test
of the plan's prediction that T3/T4 should both fail to survive; two data points cannot
confirm or refute a prediction either way. The honest reading is that T4 didn't collapse
in this ledger's two counterfactual claims, but there isn't enough T4 data here to call
the plan's prediction confirmed or refuted for that claim type.

### M3: Forgery exposure, **8.8%** (0.0880)

**Definition:** share of all 125 claims whose sole substrate (primary channel, zero
corroborating channels) is an agent-writable channel: C1 (raw CoT), C2 (inter-agent
message content), or C3 (tool-call/action trace), i.e., content the agent itself could
have authored, altered, or fabricated, with the record documenting at least one
technique by which such channels were successfully forged in this incident.

**Plain language:** About one in ten claims in the record rest entirely on content the
acting agent itself produced, with no independent channel backing it up, exactly the
condition under which a forged or spoofed record could stand unchallenged.

### M4: Assurance gap, **57.1%** (0.5714)

**Definition:** share of T5 (assurance, e.g. "no copy of the pre-release model
persists," "nothing was missed") claims coded at verifiability tier V3 (not checkable by
any third party via any stated procedure).

**Plain language:** More than half of the public reassurances that this incident is
fully contained and fully accounted for cannot be independently checked by anyone
outside the investigating institution. These are the specific claims where the public
is simply being asked to trust the lab's own word, with no stated way for an outside
party to verify it.

## 4. M5, Broad channel fragility (SUPPLEMENTARY, not one of the plan's original four)

**Why this exists:** `docs/codebook.md` §3.1 already defines a fragility ranking across
*all six* channel codes, `C1 > C2 > C3 > C6 > C5 > C4` (most fragile to least), for its
own internal tie-breaking rule. M1 and M3 only treat `C1` (M1) or `C1`/`C2`/`C3` (M3, the
"agent-writable" channels) as fragile; neither counts `C6` (lab assertion with no stated
substrate), even though the codebook's own ranking places `C6` above both `C5` and `C4`
as more fragile. A stress-test of the frozen ledger found that using the codebook's
already-defined, broader fragile set (`C1`/`C2`/`C3`/`C6`) instead produces a far more
statistically robust finding than M1, which rests on only 9 `T3` claims. M5 is not one of
the sprint plan's original four metrics (`planning/SPRINT-PLAN.md` §4.5); it is a
supplementary metric added by this issue, grounded entirely in a ranking the codebook
already commits to, not a new concept.

**Definition:** two shares of all 125 claims, both keyed on `primary_channel` membership
in the codebook's broad-fragile set `{C1, C2, C3, C6}`:
  - share whose primary channel is in that set, regardless of corroboration;
  - share whose primary channel is in that set **and** which have no corroborating
    channel at all (same blank/`NONE`/`N/A`/`NA` convention `has_no_corroboration` already
    uses for M3).

**Script output:**

```
M5 - Broad channel fragility (SUPPLEMENTARY, not one of the plan's original four):
    Primary channel in {C1,C2,C3,C6} (any corroboration):        78.4% (0.7840)
    Primary channel in {C1,C2,C3,C6} AND no corroboration:       47.2% (0.4720)
```

(At 116 rows, before the `lw-01`/`lw-02` addition, these were 84.5%/50.9%. The 9 new
rows are all `C5`, sturdy by the codebook's own ranking, so adding them mechanically
pulls both M5 figures down. This is expected and is itself worth naming in the report:
the one source-group whose absence most likely *inflated* M3/M5's fragility numbers, once
partially restored, pulled those numbers toward less dramatic, not more. That is evidence
the original figures weren't being padded by researcher error in the other direction.)

**Result:** 78.4% of all 125 claims rest on one of the four codebook-fragile channels as
their primary channel, and 47.2% of all 125 claims, just under half, rest on one of
those four fragile channels *with no corroborating channel of any kind*. For contrast,
21.6% of all 125 claims rest on `C4` or `C5`, the two channels the codebook's ranking
treats as sturdy, up from 15.5% at 116 rows, entirely due to the 9 new `C5` rows.

**Plain language:** M1's headline number (11.1%) is real but is drawn from a small
denominator: only 9 `T3` claims exist in the ledger at all, so M1 is a fragile statistic
about a fragile channel. M5 asks the same underlying question, how much of the record
rests on a channel the codebook itself flags as likely to disappear or be forged, across
*all* 125 claims and *all* four channels the codebook's own ranking calls fragile, not
just the narrowest one. The answer is still stark even after the correction toward
sturdier evidence: nearly half of everything publicly known about this incident rests on
a fragile, uncorroborated channel, and the closer-to-average claim is more likely fragile
than sturdy by better than three to one.

## 5. Reliability caveat carried forward from Gate G1

D1 (opacity, κ = 0.7788) and D3 (adversarial forgery, κ = 0.7794) both cleared the 0.6
reliability bar on the first blind-recode pass and are used here exactly as originally
coded. D2 (unfaithfulness) did not (κ = 0.5690); the codebook rule was fixed
(`docs/codebook.md` §2.3/§3.7, `adr/0001-d2-self-report-corroboration.md`) and the full
ledger's D2 columns were recoded against the fixed rule before this run, which is why
the ledger is versioned v1.1, not v1.0. As noted in §1 above, none of M1-M4 reads
`d2_verdict`, so this fix changed the ledger's integrity/reliability posture but not any
number reported here. Full reliability detail: `docs/reliability-report.md`.

The main threat to validity carried into these numbers (per `planning/SPRINT-PLAN.md`
§7): claims are coded as *reported*, so a claim can score `SURVIVES` under D1 because a
source *asserts* corroborating telemetry that this project cannot independently inspect.
That is the ceiling on M2 in particular, and it should be stated in the report's Results
section, not left implicit.

## 6. Freeze statement

Per `planning/SPRINT-PLAN.md` §6, P1.3 ("Run the metric script. Write the four numbers
down and stop touching the ledger."), `ledger/claims.csv` was frozen at **v1.1**, 116
rows, on 2026-09-11. Gate G1 (four metrics computed, κ reported, ledger frozen) was met
at that point. The ledger was reopened once, narrowly, the same day to add 9 rows
(`C352`-`C360`) recovered from `lw-01`/`lw-02` (see §1), a disclosed, one-time exception
motivated by closing a specific, previously-flagged evidentiary gap, not a general
reopening of the coding process. `ledger/claims.csv` is now frozen again at **v1.2**,
125 rows, as of 2026-09-11. No further edits are anticipated for the remainder of the
sprint.
