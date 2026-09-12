# MRFM v0.1 — Draft clauses defending against D2 (unfaithfulness)

**Status:** Draft, P2 (issue #51). Part of the v0.1 "Monitorability-Robust Forensic
Minimum" standard. Not yet merged into a consolidated MRFM document.

**Scope note:** D2 (`docs/codebook.md` §2.3) is about whether a *disclosed* reasoning
trace faithfully reports the computation that produced the action — distinct from D1
(opacity), which is about whether the trace exists or is disclosed at all. A lab can
satisfy every D1-facing disclosure clause and still produce an incident report that
over-trusts an unfaithful self-report, which is exactly the gap these clauses target.

**Direct source:** `adr/0001-d2-self-report-corroboration.md` documents a reliability
failure in this project's own coding process — a blind re-coder disagreed with the
original coder on D2 specifically (Cohen's κ = 0.5690, below the project's 0.6 bar)
because the codebook let D2 reuse D1/D3's "does a corroborating channel rescue this?"
logic. The diagnosis (§2 of the ADR, codified as codebook §3.7): a corroborating channel
only rescues a D2 verdict if it is *independent* of the self-report being tested — not a
second instance of the same kind of self-report, whether that repetition is a second
transcript, a second agent instance, or an aggregate/sampled population — and if it
actually matches the claim's specific asserted scope rather than an adjacent broader or
narrower one. That fix, made to keep this project's own claim-coding internally
consistent, generalizes directly into a requirement a lab's incident report should be
held to: MRFM-D2-1 below restates it as a lab-facing obligation. MRFM-D2-2 and MRFM-D2-3
extend the same underlying concern — that self-reported reasoning can be systematically,
not just occasionally, unfaithful — into a labeling convention and a disclosure
obligation, respectively, drawing on the broader CoT-faithfulness literature surveyed in
`docs/prior-art.md` §1.

All three clauses follow R-05 (degradation, evidence, and verifier stated per clause) and
R-06 (no reproducible tamper/spoof technique is described anywhere below, including in
the defenses proposed). Language is paraphrased from cited sources per the project's
paraphrase discipline; no prior-art text is quoted verbatim.

---

### MRFM-D2-1: Independent-corroboration requirement for self-reported reasoning

**Requirement:** Before an incident report presents a claim about the acting agent's
stated reasoning, belief, or intent as established fact, the report must corroborate that
claim with at least one channel that (a) is not itself another instance of the same kind
of agent self-report — not a second transcript, a second agent instance, or an
aggregate/sampled population restating the same kind of self-narrated content — and
(b) independently establishes the *same specific scope* the claim asserts, not merely an
adjacent broader or narrower fact. Where a claim bundles a self-report sub-assertion
(a stated reason, belief, or intent) together with a technical/behavioral sub-assertion
that genuinely is independently corroborated, the report must state its conclusion
against the claim's most specific stated content, not a softened composite that borrows
credibility from the corroborated half to cover the uncorroborated half.

**Degradation defended:** D2 (unfaithfulness) — directly generalizes the finding in
`adr/0001-d2-self-report-corroboration.md` and `docs/codebook.md` §3.7: an unfaithful
self-report can be a systematic property of how a model narrates itself, so a second
self-report-type channel does not test for faithfulness the way it would test for mere
availability (D1) or one-off forgery (D3).

**Evidence required:** For each reasoning/intent claim the report makes, a stated mapping
to the specific non-self-report channel that corroborates it (e.g., defender-side
telemetry, a raw tool-call/action-log entry distinct from the agent's own narrated reason
for that action, human testimony, or an investigator-verified record) and confirmation
that the channel's content matches the claim's specific asserted scope. Where no such
channel exists, the report must say so explicitly rather than let the self-report stand
uncontested as fact.

**Verifier (no lab network access needed):** Any external reader of the published
report — a journalist, academic auditor, or affected third party — by checking the
report's own text: does each reasoning/intent claim cite a channel other than a second
self-report, and does the cited channel's described content actually cover the claim's
specific scope rather than an adjacent one? This is a document-literacy check against the
report as published; it requires no transcript access, no technical infrastructure, and
no lab cooperation.

**Cost band:** Low — under an engineer-week. The corroborating evidence, where it exists,
is typically already collected during the lab's own investigation; the cost is the
report-writing discipline of mapping each reasoning/intent claim to its specific
corroborating channel (or explicitly flagging its absence) rather than generating new
evidence.

---

### MRFM-D2-2: Self-report vs. independently-confirmed labeling requirement

**Requirement:** Every sentence or claim in an incident report that asserts a
reasoning-, intent-, or belief-type fact about the agent must be visibly labeled, in the
report's own text or an accompanying claim table, as either "self-reported" (its sole
basis is the agent's own narrated output, however many times repeated) or "independently
confirmed" (it satisfies MRFM-D2-1's corroboration test). A claim that bundles a
self-reported sub-assertion with an independently-confirmed sub-assertion must be split
into its components for labeling purposes rather than given one blended label that
implies more confirmation than the self-reported portion actually has.

**Degradation defended:** D2 (unfaithfulness) — makes the self-report/corroboration
distinction that MRFM-D2-1 requires labs to *apply* internally also visible externally, so
a reader is not left to infer from prose tone alone whether "the agent explained that it
acted because..." is a confirmed fact or an unverified self-narration.

**Evidence required:** The published incident report itself, containing per-claim or
per-paragraph provenance labels, or a claim-provenance table attached to or embedded in
the report, consistent with the corroboration mapping required by MRFM-D2-1.

**Verifier (no lab network access needed):** Any member of the public reading the
released report. The check is purely textual: are the labels present, and are they
internally consistent with the evidence the report itself cites for each claim? No
special technical background, transcript access, or lab cooperation is required — this is
the same zero-network-access bar as MRFM-D2-1's verification.

**Cost band:** Low — under an engineer-week. This is a drafting/formatting convention
applied at report-writing time, comparable in effort to standard citation formatting, not
a new technical capability.

---

### MRFM-D2-3: Faithfulness-measurement disclosure requirement

**Requirement:** If an incident report's narrative relies on any disclosed reasoning
trace (channel C1) from a given model or model version, the report must state whether
that model has been subject to an established faithfulness-measurement procedure of the
kind documented in the public CoT-faithfulness literature (e.g., perturbation- or
hint-based tests that check whether a model's stated reasoning changes consistently with
its behavior) and, if so, disclose the measured faithfulness/verbalization rate and the
conditions under which it was measured. If no such measurement exists for the model in
question, the report must say so explicitly rather than let the narrative implicitly
assume the disclosed CoT is a reliable report of the computation that produced the
action.

**Degradation defended:** D2 (unfaithfulness) — generalizes the same ADR 0001 insight one
level up from individual claims: because an unfaithful narration habit can be a
systematic property of a model (not a one-off slip a single corroborating channel would
catch), a reader needs to know the model's *baseline* measured faithfulness rate, not just
whether any one claim happens to have a corroborating channel. This is grounded in the
published finding that verbalization/faithfulness rates in reasoning models have been
measured well below 50% in some evaluated settings, with a documented trend toward less
faithful reasoning as models scale on some tasks (see `docs/prior-art.md` §1, citing the
Anthropic and Turpin et al. faithfulness literature) — monitorability of this kind is an
emergent property that a report should not silently assume persists, per the position
paper on CoT monitorability's fragility also cited there.

**Evidence required:** A cited faithfulness-measurement result for the implicated model —
methodology used and date measured — or, absent one, an explicit disclosed statement that
no such measurement has been performed for that model.

**Verifier (no lab network access needed):** Any external reviewer with public familiarity
with the CoT-faithfulness literature (an academic reviewer, an AI-safety-focused
journalist, or a third-party auditor) can check whether the report cites a specific, dated
faithfulness measurement, and — where the model family has been studied in published
faithfulness research — can check the cited figure for plausibility against that public
literature. No lab-internal access is needed to perform this check; it only requires the
published report and publicly available faithfulness studies.

**Cost band:** Medium — 1-4 engineer-weeks for a lab with no existing faithfulness-testing
pipeline to run and report a baseline measurement using established methodology adapted to
the implicated model. Labs with an existing internal faithfulness-testing practice incur
only the low cost of disclosure; the band is set at Medium because the requirement must
still be satisfiable by a lab starting from zero.
