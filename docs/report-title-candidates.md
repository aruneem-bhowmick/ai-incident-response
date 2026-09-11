# Report title candidates

**Status:** draft, awaiting a pick. Not a P1 deliverable — this exists because
`planning/SPRINT-PLAN.md` §10's working title says to replace it "once M1 and M2 are in
hand," and a stress-test of the frozen P1 results found the placeholder would overclaim
if kept ("Warranted by One Channel: How Much of the July 2026 Incident Record Survives
Chain-of-Thought Opacity?" — the record survives opacity at 89.7% overall, so a title
implying broad collapse doesn't match the data).

Per `planning/GUIDELINES.md`'s publishing notes: "Pick a title that states the finding
rather than the topic" and, for LessWrong specifically, "state the number in the title."
All candidates below try to honor that.

## The three findings a title could anchor on

1. **The narrow, sharp finding (M2 by type):** intent-attribution claims (`T3`)
   specifically depend on chain-of-thought — nothing else in the ledger does, in any
   comparable way. Two ways to state the number: strict survival is 22.2% (2/9), or
   "any degradation" (`DEGRADED` + `COLLAPSES`) is 77.8% (7/9). **Caveat: n=9.** Small,
   should be stated as directional in the report itself (see `docs/headline-metrics.md`
   after issue #41 lands).
2. **The broad, well-powered finding (M5, supplementary):** 78.4% of all 125 claims
   rest on a channel the codebook's own fragility ranking treats as fragile (C1/C2/C3/C6),
   and 47.2% of all claims have no corroboration at all on top of that. This is the
   strongest, most statistically robust number in the whole ledger (n=125, not n=9).
   (Updated from 84.5%/50.9% at n=116 after a later, disclosed 9-row addition from
   lw-01/lw-02 — see `docs/headline-metrics.md` §4.)
3. **The regulator-facing finding (M4):** 57.1% of the incident's "we've got this
   contained" assurance claims cannot be independently verified by anyone outside the
   lab.

## Candidates

**A — anchored on the narrow finding, most faithful to the original working title's
intent:**
> "Intent Claims Collapse Without Chain-of-Thought — Almost Everything Else Survives"

or, with the number stated per the LessWrong convention:
> "78% of Claims About *Why* the July 2026 AI Agent Attacked Depend on Its Own
> Chain-of-Thought"

*Pro:* directly answers the sprint's own working-title question. *Con:* n=9 — needs the
caveat stated prominently right where the title's claim is made, or a sharp reader will
ask "out of how many?" immediately.

**B — anchored on the broad finding, strongest statistics, recommended:**
> "78% of the July 2026 AI Incident Record Rests on a Channel This Project's Own
> Framework Calls Fragile"

or shorter:
> "Most of What We Know About the July 2026 AI Incident Rests on Fragile Evidence — and
> That's Measurable"

*Pro:* n=125, the best-powered number in the ledger; matches the original one-sentence
thesis ("the public understanding... is disproportionately warranted by the single
evidentiary channel most likely to disappear or be forged") more literally than the
narrow finding does, once "fragile channel" is read broadly rather than as CoT alone.
*Con:* less viscerally specific than naming chain-of-thought by name; "fragile" needs one
clause of definition even in the title's own context (a subtitle or first line can carry
that).

**C — combines both, two-part title:**
> "Most of the July 2026 AI Incident Record Rests on Fragile Evidence — and the Part
> About *Why* the Agent Did It Is the Most Fragile of All"

*Pro:* carries both findings, gives the reader the general claim and the sharpest
specific instance of it in one sentence. *Con:* longer; two numbers competing for
attention if both get stated.

## Recommendation

**B**, with **A's finding stated prominently in the abstract/intro** rather than the
title — B's number is the one that survives scrutiny at n=125, and it's the more literal
match to the project's own one-sentence thesis. A's finding is real and worth leading
with in the body (it's more emotionally legible — "the record can't tell you *why*"),
but shouldn't carry the weight of a title on 9 data points.

Final pick is a judgment call for whoever drafts the report in P3 — this file exists so
that decision isn't made from memory of the numbers, and so the tradeoff between "more
dramatic, less powered" (A) and "less viscerally specific, better powered" (B) is
explicit rather than accidental.
