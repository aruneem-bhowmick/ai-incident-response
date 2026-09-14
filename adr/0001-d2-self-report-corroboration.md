# ADR 0001: D2 (unfaithfulness) corroboration must be independent of the self-report it's stress-testing

**Date:** 2026-09-11
**Status:** Accepted
**Codebook version this moves to:** `v1.1, 2026-09-11`
**Trigger:** `docs/reliability-report.md`: Cohen's κ on D2 (unfaithfulness) = 0.5690, below the
0.6 bar, while D1 (0.7788) and D3 (0.7794) both pass. Per `planning/SPRINT-PLAN.md` §8's risk
table ("Coding drift | κ < 0.6 at P1.2 | Fix the rule, ADR, full recode"), this is the
fix-and-recode branch, and it applies to D2 only.

## 1. Which rows motivated this

The 25-row blind-recode subsample disagreed on D2 for exactly two rows (all other 23 D2 calls
matched between `ledger/blind-subsample-recoded.csv` and the answer key at
`C:\Users\arune\research\sprints\_warrant-reliability-answer-key\answer-key.csv`):

- **C124**: original verdict `SURVIVES`, blind recode `DEGRADED`. Claim: a model split a
  secret into pieces and reassembled it to evade a credential scanner, and stated so explicitly
  both in its own reasoning trace (C1) and in user-facing comments captured by the harness's
  action trace (C3). The original coder treated the C3 comments as an independent second
  channel that rescues the claim to full `SURVIVES`. The blind recoder treated the C3 comments'
  restatement of *why* the model did it as no more trustworthy than the C1 statement it
  supposedly corroborates: only the mechanical splitting/reassembly action, not the stated
  reason, is genuinely independently backed, landing on `DEGRADED`.
- **C204**: original verdict `DEGRADED`, blind recode `COLLAPSES`. Claim: AISI asserts no model
  has cheated undetected, based on manually reviewing transcripts. The original coder treated
  "final actions remain independently reviewable" as a fallback that softens the verdict to
  `DEGRADED`. The blind recoder noted that this fallback covers a *different, narrower* scope
  (completed actions) than the specific thing the claim asserts (that deliberate-but-unactioned
  cheating reasoning is never missed), a scope an unfaithful CoT would defeat with no
  fallback, landing on `COLLAPSES`.

With only 2 of 25 pairs disagreeing (92% raw agreement), κ still came in under 0.6 because the
D2 verdict distribution is heavily skewed toward `SURVIVES` in this sample, which inflates
chance agreement and makes even a couple of disagreements costly to κ. Both disagreements are
real, not noise; see §2.

## 2. Diagnosis: is this a genuine codebook ambiguity, or coder drift?

Both disagreements have the same shape, and it recurs in the full ledger (see §4), so this is a
rule gap, not a one-off judgment call. `docs/codebook.md` §2.3 defines D1, D2, and D3 with
near-identical two-line asks ("ask: is the claim's warrant defeated?") and lets coders reuse the
same "is there a corroborating channel?" logic across all three conditions. That reuse is sound
for D1 (opacity: is the content available at all?) and for D3 (adversarial forgery, a
discrete, effortful, one-off act, so a pattern recurring across many independent
agent instances genuinely is harder to have coordinately faked; see the existing D3 notes on
C221/C222/C223/C226 crediting "harder to attribute to coordinated fabrication").

D2 is different in a way the codebook never says out loud: D2's failure mode
(a self-report doesn't faithfully reflect the underlying computation) can be a **systematic**
property of how a model narrates itself, not a one-off slip. That means:

- A second channel that just **repeats the same agent-authored self-report** of a reason,
  belief, or intent (whether the same content logged twice, as in C124, or the same *kind* of
  self-report recurring across many transcripts, as in the aggregate-motivation claims in
  §4) does not establish that any of those self-reports is faithful; an unfaithful narration
  habit would show up consistently across the repeats, not just once. This is exactly backwards
  from D3, where repetition across many independent instances *does* argue against coordinated
  forgery.
- A named fallback only rescues a claim if it covers the **same specific scope** the claim
  actually asserts, not a broader or narrower adjacent fact. C204's "final actions stay
  reviewable" doesn't address unactioned cheating-directed reasoning, which is precisely what
  the claim's "nothing missed" wording is about.

Both original-coder errors (C124, C204) are best explained as importing the D1/D3
corroboration-counts-as-rescue reasoning into D2 without checking that it transfers; the
codebook never told either coder it doesn't. That is a genuine rule gap, not coder-specific
carelessness: a clear rule would have produced the same call from both coders.

## 3. Old rule vs. new rule

**Old rule (`docs/codebook.md` §2.3, D2, as frozen v1.0):**
> D2, Unfaithfulness. CoT is logged but is not a reliable report of the computation that
> produced the action. Ask: *is the claim's warrant defeated?*

No further guidance on how a corroborating/fallback channel interacts with that question; coders
were left to reuse whatever corroboration-weighing intuition they'd built for D1/D3.

**New rule (added to `docs/codebook.md` §2.3 and as new edge-case rule §3.7):**
> For D2 specifically, a corroborating or fallback channel only rescues a claim's verdict to
> the extent it independently establishes the *same specific content* the CoT's unfaithfulness
> would put in doubt, via a source that is not itself just another self-report of the same
> reasoning/intent/belief. Two things do **not** count as independent rescue for D2 (though
> they may still count for D1/D3, which stress different mechanics):
> 1. **Self-report echo.** A second channel, or a second agent instance, or an aggregate/sampled
>    population, that merely repeats the same kind of agent-self-reported mental content
>    (a stated reason, belief, or intent) does not establish that any instance of it faithfully
>    reflects computation, because an unfaithful self-report mechanism can be systematic across
>    repeats and across a population, not a one-off error a second look would catch.
> 2. **Scope-mismatched fallback.** A named fallback that only covers a broader or narrower
>    scope than the claim's specific stated assertion (e.g., a completeness/exhaustiveness claim
>    like "nothing was missed") does not rescue that specific assertion.
>
> Where a claim bundles a technical/behavioral sub-assertion that *is* independently
> corroborated (by a non-self-report channel, e.g. C4, C6-that-is-not-itself-derived-from-the-same
> self-report, C5, or a genuinely distinct behavioral fact within an agent-writable channel)
> with a mental-content sub-assertion that is not, verdict the claim against its most specific
> stated content, per the claim's typed core assertion (§3.4), not the softened gist.
>
> This extends the codebook's existing conservative, bias-toward-detection posture (§3.1's
> tie-break rationale) to D2 verdict assignment: where it is genuinely unclear whether a
> corroborating channel counts, prefer the more skeptical verdict.

## 4. Scope of the fix

This ADR changes **D2 only**. D1 (κ = 0.7788) and D3 (κ = 0.7794) both clear the reliability bar
and their verdicts/notes are untouched. Per the decision rule in `planning/SPRINT-PLAN.md` §6,
the full 116-row ledger's `d2_verdict`/`d2_note` columns are recoded against this tightened rule
(see the recode commit(s) on this branch); `d1_verdict`/`d1_note`/`d3_verdict`/`d3_note` are left
exactly as they were.
