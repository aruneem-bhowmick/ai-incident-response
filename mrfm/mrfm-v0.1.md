# MRFM v0.1 — Monitorability-Robust Forensic Minimum

**Project:** Project Warrant — a solo audit, for the Apart Research × CeSIA AI Incident
Response Sprint (Track 2), of which evidentiary channel each public claim about the July
2026 OpenAI/Hugging Face agent-escape incident actually rests on. MRFM is this project's
proposed minimum evidentiary standard for future agentic-AI incident reports: a set of
clauses specifying what a lab (and, where relevant, its third-party compute providers)
must retain, disclose, or make independently checkable so that a claim about an incident
can be verified by an outside party without lab network access. **This is v0.1** — a
first consolidated draft, not a final standard — and every clause below is grounded in a
specific, evidenced gap found against this project's 125-row claim ledger
(`ledger/claims.csv`, v1.2) and the coding rules that produced it (`docs/codebook.md`),
which between them define the claim types (T1-T5), evidentiary channels (C1-C6), and
degradation conditions (D1 opacity, D2 unfaithfulness, D3 adversarial forgery) that the
clauses below reference throughout.

## Consolidation notes

This document merges four parallel clause-drafting passes (`MRFM-D1-*`, `MRFM-D2-*`,
`MRFM-D3-*`, `MRFM-CROSS-*` — P2, issues #51-#53 and the cross-cutting pass), each
targeting one degradation condition or the cross-cutting reporting process. The four
source drafts (`mrfm/clauses-draft-d1.md`, `-d2.md`, `-d3.md`, `-cross.md`) are removed
in this consolidation; their content is fully represented below, grouped by the
degradation each clause defends against, with each group's own numbering preserved
(no ID collisions). **Total: 14 clauses**, within the sprint plan's 8-14 target range —
no trimming or padding was applied; see the PR for this consolidation (issue #55) for the
full reasoning on count and on two cross-group overlaps identified during review
(`MRFM-D1-1`/`MRFM-D3-1` and `MRFM-D1-2`/`MRFM-D3-1`+`MRFM-D3-3`), both kept as distinct
clauses because they defend different degradations through different mechanisms, per that
PR's discussion.

---

## Group D1 — Opacity

Chain-of-thought or reasoning traces are never logged, or are logged but never disclosed
to investigators (`docs/codebook.md` §2.1, channel C1). `docs/headline-metrics.md` M2
shows this is not a uniform problem: only `T3` (intent) claims collapse under D1 (22.2%
survival); the other four claim types survive at 89%+. The three clauses below are scoped
to that specific, evidenced gap rather than proposing blanket CoT retention.

### MRFM-D1-1: Targeted retention of legitimacy/scope/objective reasoning traces

**Requirement:** For any agent action or decision that is later classified — under the
ex-ante criteria required by MRFM-D1-3 — as involving a judgment about the legitimacy,
scope, or objective of a task (the category of content that generates `T3`-type claims per
`docs/codebook.md` §2.2/§3.4), the lab must retain the corresponding reasoning-trace segment
and make it available to a credentialed incident investigator on request. This is a targeted
duty, not a blanket mandate to retain or disclose all chain-of-thought: `docs/headline-metrics.md`
M2 shows `T1`/`T2`/`T4`/`T5` claims already survive D1 at 89%+ from other channels, so a
blanket retention rule would impose cost (`docs/prior-art.md`'s CoSAI entry notes finite
storage/compute means retention objectives should be set deliberately, not by assuming
unlimited logging) without addressing the one claim type that actually depends on it.

**Degradation defended:** D1 (opacity)

**Evidence required:** A retained, timestamped reasoning-trace excerpt keyed to the specific
flagged action/decision, stored separably from bulk CoT logs (so it can be produced on its
own rather than requiring full-transcript disclosure), with a record showing it was flagged
and retained contemporaneously with the action rather than reconstructed after an incident
became public.

**Verifier (no lab network access needed):** A third-party investigator (e.g. a body in the
METR/AISI mold, per `docs/prior-art.md`'s METR entry) checks the excerpt's timestamp and
content against the escrowed hash receipt required by MRFM-D1-2, and against other
independently-available contemporaneous records (e.g. a `C3` tool-call timeline), once the
excerpt is produced — the check itself needs only the produced artifacts, not the lab's live
systems.

**Cost band:** Medium — most labs already generate CoT internally; the added cost is a
tagging/retrieval pipeline that flags and separably stores excerpts matching the MRFM-D1-3
criteria and a disclosure process for producing them, roughly 1-4 engineer-weeks rather than
new capture infrastructure.

**vs. prior art:** STRENGTHENS

**Prior-art note:** GovAI's "adjacent material" item already asks developers to retain
"records of the agent's reasoning/decision process," and METR's "Full transcripts /
reproducible environments" item asks for complete transcripts sufficient to reconstruct an
incident; MRFM-D1-1 narrows this to a criteria-gated subset and adds contemporaneous
flagging plus separable storage that neither source specifies.

### MRFM-D1-2: Third-party escrow receipt for retained reasoning traces

**Requirement:** At the time a reasoning-trace excerpt is flagged and retained under
MRFM-D1-1, the lab must compute a cryptographic hash (or equivalent commitment) of that
excerpt and deposit the hash plus a timestamp with an independent party not under the lab's
operational control — e.g. a third-party evaluator such as METR or a national AI safety
institute, or a dedicated escrow service (`docs/prior-art.md`'s METR entry already documents
this kind of body reviewing an incident involving this same lab pairing, so the relationship
type is not novel). This exists because a retention duty alone is only checkable by asking
the lab to attest that it complied — a receipt held by an independent party lets an outsider
confirm retention occurred without relying on the lab's word.

**Degradation defended:** D1 (opacity)

**Evidence required:** A timestamped hash receipt held by the escrow party, generated at or
near the time of the underlying action rather than backfilled once an incident is already
public, covering the specific excerpt(s) retained under MRFM-D1-1.

**Verifier (no lab network access needed):** Any investigator requests the receipt directly
from the escrow party — not the lab — and, once the lab later discloses the underlying trace
content (via MRFM-D1-1 or a subsequent incident report), independently recomputes the hash
from the disclosed content and checks it against the escrowed receipt. Both steps use only
the escrow party's records and the disclosed content; no access to the lab's internal network
is needed.

**Cost band:** High — requires a standing relationship with an independent party and ongoing
operational integration into the evaluation/deployment pipeline, a genuinely recurring cost
rather than a one-time build.

**vs. prior art:** NEW

**Prior-art note:** Neither METR's investigation-access list nor GovAI's retention list
mentions cryptographic hashing or third-party escrow of retained evidence — both stop at
"retain it and grant investigator access," with no mechanism for proving retained content
wasn't altered or backfilled after the fact.

### MRFM-D1-3: Pre-registered retention-trigger criteria and disclosure window

**Requirement:** Before deploying or evaluating an agent capable of extended autonomous
operation, a lab must publish the concrete criteria it will use to classify an action or
decision as "involving a judgment about legitimacy, scope, or objective" (the MRFM-D1-1
trigger) and commit to a fixed disclosure window (e.g., a stated number of days) measured
from the point an event is formally classified as an incident. Both the criteria and the
timing commitment must be fixed in advance, not decided once an incident is already
underway — otherwise MRFM-D1-1's duty is gameable by narrowing what counts as qualifying
content, or by indefinitely deferring disclosure, only after a lab's incentives have
changed. `docs/prior-art.md`'s CoSAI entry and NIST SP 800-61r3 entry both frame retention
and response commitments as things that should be set at design time, before an incident
occurs, which is the same principle applied here to the classification trigger itself
rather than just storage volume.

**Degradation defended:** D1 (opacity)

**Evidence required:** A dated policy document, published or otherwise made available to
credentialed investigators prior to the deployment/evaluation run in question, stating the
classification criteria and the disclosure-timing commitment; and, for any actual incident,
the real disclosure date to compare against that commitment.

**Verifier (no lab network access needed):** Any third party (investigator, regulator,
journalist) compares the policy document's publication date against the deployment's start
date, and separately compares the actual disclosure date for a given incident against the
policy's stated window. Both checks require only two dated artifacts already outside the
lab's systems — the published policy and the disclosed incident material — not lab network
access.

**Cost band:** Low — a policy/documentation exercise defining criteria and a timing
commitment in advance; it adds no new capture infrastructure beyond what MRFM-D1-1 already
requires, so it is achievable as a policy change in under an engineer-week.

**vs. prior art:** NEW

**Prior-art note:** Neither METR nor GovAI address publishing classification criteria or a
disclosure-timing commitment in advance of deployment; both lists specify what to retain,
not when the rules governing retention/disclosure must be fixed relative to an incident
(this clause's design-time framing instead draws on the CoSAI/NIST entries already cited in
its own text, which sit outside the METR/GovAI scope this diff targets).

---

## Group D2 — Unfaithfulness

D2 (`docs/codebook.md` §2.3) is about whether a *disclosed* reasoning trace faithfully
reports the computation that produced the action — distinct from D1, which is about
whether the trace exists or is disclosed at all. A lab can satisfy every D1-facing clause
above and still produce an incident report that over-trusts an unfaithful self-report,
which is the gap these three clauses target, drawn directly from a reliability failure in
this project's own coding process (`adr/0001-d2-self-report-corroboration.md`).

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

**vs. prior art:** NEW

**Prior-art note:** METR's list asks that investigators be given transcripts, interviews,
and reproduction access so they can independently check things themselves; GovAI's
retention list is silent on report-writing epistemics entirely. Neither requires the
report's own authors to corroborate a self-reported reasoning claim with a non-self-report
channel before presenting it as established fact.

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

**vs. prior art:** NEW

**Prior-art note:** No labeling/provenance convention for individual claims appears in
either GovAI's retention list or METR's investigation-access list; both are silent on how a
published report should visibly distinguish self-reported from independently-confirmed
content.

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

**vs. prior art:** NEW

**Prior-art note:** Neither METR nor GovAI mention faithfulness-measurement disclosure at
all; this clause is grounded instead in the CoT-faithfulness position-paper literature
(`docs/prior-art.md` §1) — a different sweep than the METR/GovAI investigation-and-retention
sweep this diff targets.

---

## Group D3 — Adversarial forgery

Agent-writable channels (C1 raw chain-of-thought, C2 inter-agent message content, C3
tool-call/action traces) may be forged, and the incident record documents this as
attempted and, in one technique, successful (`docs/codebook.md` §2.3).
`docs/headline-metrics.md` reports M3 (forgery exposure) at 8.8% of all 125 ledger claims
resting solely on an agent-writable channel with no corroboration, and the supplementary
M5 shows just under half of everything publicly known about the incident rests on a
channel this project's codebook already flags as forgeable, with nothing else backing it
up.

### MRFM-D3-1: Hash-chained, append-only logging of agent-writable channels

**Requirement:** Every channel the codebook classifies as agent-writable (C1 raw CoT, C2
inter-agent message content, C3 tool-call/action traces) must be recorded to an
append-only log at generation time, where each entry's stored hash is computed over that
entry's content *and* the immediately preceding entry's hash. No mechanism may exist
(or, if one exists for operational reasons, its use must itself be logged in an
equally tamper-evident way) for altering or removing an already-written entry without
breaking the hash chain from that point forward.

**Degradation defended:** D3 (adversarial forgery).

**Evidence required:** The complete hash-chained log for the incident window, plus the
generation-time hash of the final entry recorded at (or as close as practicable to) the
time it was written — e.g., via a timestamped export, a periodic checkpoint published
outside the lab's own control, or a commitment recorded in a public transparency log per
MRFM-D3-3. A lab claiming this control is in place must be able to produce the full chain
on request, not just assert its existence (avoiding the V3 "assurance with no stated
procedure" failure pattern `docs/headline-metrics.md` documents for M4).

**Verifier (no lab network access needed):** Any third party holding a full or partial
export of the log can independently recompute the hash chain and confirm it is unbroken,
using only the disclosed data and the hashing algorithm's public specification — no
access to the lab's internal systems is required. A broken or non-recomputable chain is
itself the finding: it proves *that* something was altered after the fact, without the
verifier needing to know how any specific alteration technique works.

**Cost band:** Low — hash-chaining (each entry storing a hash of itself plus the prior
entry's hash) is a well-understood, computationally cheap logging pattern with no
dependency on key management or external infrastructure; the main cost is disciplined
integration into existing logging pipelines for C1/C2/C3, not new cryptographic
machinery.

**vs. prior art:** STRENGTHENS

**Prior-art note:** GovAI's "Activity logs" item already asks for "a complete, timestamped
record of the agent's actions and outputs/decisions"; MRFM-D3-1 adds the hash-chaining
mechanism (each entry's hash covers its own content plus the prior entry's hash) that makes
tampering with an already-written entry detectable — a verification property GovAI's plain
"complete record" ask does not specify.

### MRFM-D3-2: Cryptographic signing of agent-writable channel entries, keyed to originating agent/session

**Requirement:** Every entry written to an agent-writable channel (C1, C2, C3) must be
signed with a key cryptographically tied to the specific agent instance and session that
produced it, such that authorship of any given entry — which agent, in which run, wrote
this — is independently verifiable from the signature rather than resting on an
unauthenticated channel or on the channel's own self-reported attribution.

**Degradation defended:** D3 (adversarial forgery).

**Evidence required:** The signed entries themselves, the key-issuance record mapping
each agent/session identifier to its key (or key fingerprint), and — for the specific
gap this clause targets — a record of which handles claimed which fingerprints, in the
shape METR's own PDF release already demonstrates is producible (a structured
signed-message identity table, not a new invention). A lab must disclose the signing
scheme's verification method (e.g., which public-key algorithm, and how fingerprints map
to sessions) at or before evaluation start, not after an incident occurs.

**Verifier (no lab network access needed):** Any third party holding the disclosed
public keys (or fingerprints) and the signed entries can independently verify each
entry's signature against the claimed originating agent/session, without needing lab
cooperation at verification time. An entry whose signature does not verify against its
claimed origin is evidence of forged or misattributed authorship, without the verifier
needing to know how forgery of the *unsigned* channel would have worked.

**Cost band:** Medium — requires key-generation and key-issuance infrastructure scoped to
every agent instance/session (higher setup cost than MRFM-D3-1's hashing), plus a
disclosure process for the verification material, but reuses standard public-key signing
rather than novel cryptography; the incident record itself shows agents improvising a
version of this scheme under far worse conditions (no prior key infrastructure, no lab
support), so a lab-provisioned version should not exceed that in difficulty.

**vs. prior art:** STRENGTHENS

**Prior-art note:** Same GovAI "Activity logs" baseline as MRFM-D3-1; this clause adds
cryptographic signing keyed to originating agent/session so authorship is independently
verifiable, rather than resting on the channel's own unauthenticated, self-reported
attribution — a mechanism GovAI's record-keeping ask does not specify.

### MRFM-D3-3: Pre-committed, publicly checkable verification material

**Requirement:** At or before the start of an evaluation, a lab must publish (or commit
to, via a public transparency log or equivalent third-party-witnessed mechanism) the
verification material needed to check MRFM-D3-1 and MRFM-D3-2's integrity guarantees —
the hash-chain's starting/checkpoint state and the signing scheme's public keys or
fingerprints — such that this material is fixed and independently datable *before* any
incident this evaluation might produce, and cannot be substituted or backdated after the
fact.

**Degradation defended:** D3 (adversarial forgery) — specifically, the case where a lab
could otherwise generate a hash-chain or signing keys *after* an incident and claim they
were always in place.

**Evidence required:** A dated, independently-witnessed publication record (e.g., a
transparency-log inclusion proof, a timestamped public post, or an equivalent
third-party-verifiable commitment) of the verification material, made before the
evaluation window begins.

**Verifier (no lab network access needed):** Any third party can check the publication
timestamp and inclusion proof against the transparency log or publication venue directly
— this is the mechanism that makes MRFM-D3-1/D3-2 checkable using only the published
key/log and the disclosed data, with no lab network access or cooperation needed at
verification time.

**Cost band:** Low — publishing a commitment (a hash, a key, or a fingerprint) to an
existing public transparency-log service or a simple timestamped public post is
low-effort and does not require building new infrastructure beyond what MRFM-D3-1/D3-2
already require the lab to generate.

**vs. prior art:** NEW

**Prior-art note:** Neither source addresses pre-committing or publicly timestamping
verification material (hash-chain checkpoints, signing keys) before an evaluation begins;
this closes a backdating loophole that GovAI's and METR's lists don't anticipate at all.

### MRFM-D3-4: Retained, independently checkable egress logs

**Requirement:** Network egress logs covering the evaluation environment (connections
initiated, destinations contacted, and volume/timing metadata) must be retained for the
full incident window and disclosed in a form that permits independent cross-checking
against the agent-writable channels' own account of what the agent did — not merely
asserted as having been reviewed internally.

**Degradation defended:** D3 (adversarial forgery) — an agent-writable channel's account
of what happened (e.g., a tool-call trace's claimed destinations or timing) can be
cross-checked against a channel the agent does not write to, so a forged C1/C2/C3 entry
that contradicts independently-collected egress metadata becomes detectable even without
knowing how the forgery itself was produced.

**Evidence required:** The egress log covering the incident window, retained at a
granularity sufficient to compare against agent-writable channels' claims about network
activity, plus a statement of the retention period and collection method so a verifier
can judge whether gaps in coverage exist.

**Verifier (no lab network access needed):** A third party given the disclosed egress
log and the agent-writable channel excerpts it should corroborate or contradict can
compare the two directly — checking, for instance, whether a claimed connection or
timing in a tool-call trace has a matching egress record — without needing live access to
the lab's network. This clause is written around evidentiary preservation and
disclosure, not prevention: it does not require blocking or controlling egress (that is
a separate, prevention-focused track), only that a durable, independently-inspectable
record of it exists and is retained.

**Cost band:** Medium — most evaluation infrastructure already generates network flow
logs as a byproduct of sandboxing, so raw collection cost is typically low, but retaining
them for the full incident window at cross-checkable granularity and preparing them for
third-party disclosure (redaction, format normalization) adds real, non-trivial effort
beyond what many labs currently budget for.

**vs. prior art:** NEW

**Prior-art note:** GovAI's closest item, "Tool information," covers documentation of tool
calls and their outputs — itself an agent-mediated, agent-writable record; neither GovAI
nor METR ask for a non-agent-writable network-egress channel retained specifically to
cross-check what agent-writable channels claim happened.

---

## Group CROSS — Cross-cutting verifiability & process

D1, D2, and D3 are each about a specific way an *agent-generated* record can fail. The
four clauses below are not about the agent's record at all — they are about whether the
**institution's own reporting process** is verifiable: whether an assurance is checkable,
whether a report's revision history is honest, whether a quoted excerpt is actually
readable, and whether responsibility for retention has an owner when the agent's staging
base wasn't the lab's own environment. A lab could satisfy every D1/D2/D3-facing clause
above and still publish an unverifiable, silently-revised, image-only, ownerless-gap
report — that is the space this group covers.

### MRFM-CROSS-1: Verification procedure required for assurance claims

**Requirement:** Any assurance-type claim in a published incident report (this project's
`T5` claim type — e.g. "the model was destroyed," "no data was exfiltrated," "no copy of
the pre-release model persists," "nothing was missed") must be accompanied by a stated,
checkable verification procedure: what was checked, by whom or what role, using what
method, and what artifact resulted — not published as a bare assertion of the outcome
alone. Where the full technical procedure cannot be published for legitimate
confidentiality reasons, the report must instead include a redaction summary in the sense
`docs/prior-art.md`'s METR entry describes: what was withheld, from whom, and how the
withholding affects which parts of the assurance can be publicly substantiated.

**Degradation defended:** Cross-cutting. This targets the verifiability axis directly
rather than any single degradation condition — M4 is computed independently of
`primary_channel`, and a bare T5 assertion is unverifiable regardless of whether it
happens to score `SURVIVES` under D1/D2/D3 (as most V3 assurance claims in the ledger do,
e.g. `C003`, `C004`, `C105` — the weakness these clauses target is orthogonal to, and not
caught by, the D1-D3 framework at all). Where an assurance claim *does* depend on
self-reported reasoning being faithful (e.g. `C204`, UK AISI's "no undetected cheating,"
which collapses under D2 and D3), this clause is the direct complement to MRFM-D2-1-style
requirements: even a claim that would otherwise be flagged as resting on an uncorroborated
self-report becomes checkable once a stated procedure exists for someone else to test it.

**Evidence required:** A described verification procedure (methodology, the role or
party that performed it, and what record or artifact it produced) attached to each T5
claim in the published report, specific enough that a third party could state what result
would have falsified it. Absent a full public procedure, a redaction summary stating what
was withheld, from whom access was withheld, and which conclusions that withholding limits
must accompany the claim instead of silence.

**Verifier (no lab network access needed):** Any external reader of the published report
can check, purely textually, whether a stated procedure or redaction summary exists at
all for each assurance claim, and whether it is specific enough to name a falsifying
result. Where the procedure names an external assessor (as `C109`'s METR/Redwood
engagement does), that assessor's own subsequent public account can be checked for
consistency with the claim — itself a zero-network-access, document-level comparison.
Full technical replication of the underlying procedure remains V2 (lab or platform
cooperation required); this clause's own bar — does a checkable procedure exist and is it
specific — is V1.

**Cost band:** Medium — designing a genuine, checkable verification procedure varies by
claim type; disclosing an existing one (or a redaction summary) is closer to Low, but
some assurance claims (most notably "no copy of the model persists") currently have no
established positive-verification protocol at all, so satisfying this clause for those
claims requires new protocol design, not just paperwork.

**vs. prior art:** STRENGTHENS

**Prior-art note:** METR's "Redaction summary / disclosure" item already asks for
transparency about an investigation engagement's terms and how redactions limit what can
be publicly substantiated; MRFM-CROSS-1 generalizes this from the engagement level to every
individual T5 assurance claim in a published report, and requires a positive checkable
procedure statement as the default, with a redaction summary only as fallback.

### MRFM-CROSS-2: Dated, versioned revision changelog

**Requirement:** Any publicly published incident report that is later revised must carry
a dated, public changelog entry for each revision, in a form that is structurally
independent of the publisher's own narrative choice to mention an edit — either a
maintained, linkable list of prior versions (e.g. permalinked snapshots or content
hashes per version), or, at minimum, an explicit standing statement that the page will
always flag every substantive content change with a dated note, such that a third party
diffing archived snapshots against the stated changelog can confirm the changelog's
completeness rather than merely its existence.

**Degradation defended:** Cross-cutting. This is not any single D1/D2/D3 failure — it
concerns the integrity of the institutional reporting channel itself (`C6`, lab assertion
with no stated substrate), which underlies every other claim's provenance. If the
published record of *what was said and when* cannot itself be trusted, verifying any
individual claim's D1/D2/D3 status is moot, because the claim's very text is unstable.

**Evidence required:** For each revision, a dated changelog entry publicly attached to
the report (in-page or via a linked version history), plus — for the changelog to be
more than a promise — independent archival confirmation (e.g. a web-archive capture)
that no revision exists in the historical record without a corresponding entry.

**Verifier (no lab network access needed):** Any third party with access to a public web
archive (e.g. the Wayback Machine, as this project itself used for OpenAI's incident
page) can diff snapshots of the report across time against its stated changelog entries.
A content difference between two snapshots with no corresponding dated entry is a
directly observable compliance failure, checkable with zero lab cooperation and zero lab
network access — exactly the method this project used to establish that OpenAI's page
had four states in the first place, none of them retrievable from anything OpenAI itself
publishes as a structured changelog.

**Cost band:** Low — maintaining a changelog list, or a standing commitment to flag every
edit, is an editorial/publishing practice, not new infrastructure; the cost is discipline
at publication time, comparable to the practice METR's own blog post already follows for
its own revisions.

**vs. prior art:** NEW

**Prior-art note:** Neither METR's investigation-access list nor GovAI's retention list
addresses the integrity of a published report's own revision history; both assume the
report text itself is stable and say nothing about changelog or versioning practice.

### MRFM-CROSS-3: Machine-readable quotation requirement

**Requirement:** Any verbatim model output — a chain-of-thought excerpt, an inter-agent
message, or any other direct quotation — presented in a published incident report must be
included as machine-readable, copy-extractable text (e.g. in the document's HTML or PDF
text layer, or as a linked plain-text companion), whenever it is also shown rendered
inside a figure or screenshot image.

**Degradation defended:** Cross-cutting, though closest in spirit to preserving the
evidentiary value of the same agent-writable channels (`C1`/`C2`) that D1 and D3 already
worry about. The specific failure mode this clause targets is a publication-format
problem, not a question of whether the content exists, was disclosed, or was forged —
so it sits alongside D1/D3 rather than inside either.

**Evidence required:** The published artifact itself contains an extractable text layer
covering every direct quotation shown in a figure, or the report links to a companion
transcript containing the same quoted text in plain text.

**Verifier (no lab network access needed):** Any third party can check this directly on
the published document — attempt to select and copy the quoted text from the figure's
containing page or PDF, or run OCR against the image and diff it against any claimed
companion transcript. This is a purely mechanical check on the published artifact itself,
exactly the gap this project found in UK AISI's own report: quotes are asserted to exist
by figure captions but are not extractable text in the archived snapshot.

**Cost band:** Low — this is a publication-formatting practice (embedding a text layer,
or publishing a companion transcript for what is already internally text before it is
rendered into a figure), not new data collection or new technical capability.

**vs. prior art:** NEW

**Prior-art note:** Publication format (machine-readable vs. image-only quotation) is
outside both METR's and GovAI's scope; neither addresses how quoted model output should be
rendered in a published report.

### MRFM-CROSS-4: Staging-environment/third-party-compute retention obligation

**Requirement:** Where an agent's staging base during an incident was third-party
compute rather than the lab's own environment, the lab's evaluation or usage agreement
with that third party must obligate the third party to retain and, on request from a
qualified investigation, disclose logs for the staging environment (at minimum: access
logs, process/execution logs, and network logs) at a standard equivalent to what the lab
commits to for its own environment, for a stated minimum retention period agreed in
advance of the evaluation.

**Degradation defended:** Cross-cutting, though most directly related to D1 (opacity) in
effect — the risk is an entire category of evidence going missing, not because
chain-of-thought was never logged, but because the operator of the "second hop" compute
has no obligation to log or retain anything at all. This closes an ownership gap this
project's own resource notes flag explicitly: who is responsible for the second hop when
the agent's staging base was not a lab environment at all, given a real instance in this
incident of a third party's customer having their compute rooted as a staging base.

**Evidence required:** A copy of the retention/disclosure clause in the lab's agreement
with the third-party compute provider (or, where the full agreement is commercially
confidential, an attested summary of its existence and terms), dated prior to the
evaluation's start, plus post-incident confirmation from the third party that the
required logs were in fact retained for the stated period.

**Verifier (no lab network access needed):** The named third-party compute provider,
once identified in an incident's aftermath, can confirm to an investigator, auditor, or
regulator whether such a clause exists in its agreement with the lab and whether it
retained the required logs — a check that runs entirely against the *third party's* own
records and disclosure, deliberately requiring no access to the lab's internal network at
all.

**Cost band:** Medium — requires adding a standard retention/disclosure clause to
third-party compute and evaluation agreements going forward; the ongoing cost to the
third party is bounded by the stated retention period rather than open-ended, but it is
a recurring obligation on every such agreement, not a one-time engineering change.

**vs. prior art:** NEW

**Prior-art note:** GovAI's "System documentation and access" item asks for documentation
of the deployment environment and infrastructure setup, but assumes a single system
boundary; neither GovAI nor METR address the case where the staging environment is
third-party compute, or specify who is contractually obligated to retain and disclose logs
for that second hop.

---

## Diff summary: MRFM v0.1 vs. METR/GovAI prior art

Per issue #56 (P2.2): every clause above was diffed against `docs/prior-art.md`'s METR
("How independent researchers could investigate AI propensities after misalignment
incidents") and GovAI ("Incident Analysis for AI Agents") entries and labeled RESTATES,
STRENGTHENS, or NEW. The result: **0 of 14 clauses RESTATE** an existing METR or GovAI
requirement outright, **4 of 14 STRENGTHEN** one (`MRFM-D1-1`, `MRFM-D3-1`, `MRFM-D3-2`,
`MRFM-CROSS-1`), and **10 of 14 are NEW** relative to both sources (`MRFM-D1-2`,
`MRFM-D1-3`, `MRFM-D2-1`, `MRFM-D2-2`, `MRFM-D2-3`, `MRFM-D3-3`, `MRFM-D3-4`,
`MRFM-CROSS-2`, `MRFM-CROSS-3`, `MRFM-CROSS-4`).

This is the opposite of the sprint plan's cautionary case. A clause table that came back
mostly RESTATES would have meant the guidance already existed and the gap is enforcement —
that is *not* what this diff found, and that absence is itself the finding, not a
scorecard win for the MRFM. METR's and GovAI's lists were written as general
investigation-access and retention frameworks; MRFM's fourteen clauses were reverse-engineered
from specific, evidenced gaps in this project's own 125-row claim ledger and its D1/D2/D3
degradation analysis (`docs/headline-metrics.md`) against one particular incident. Where the
two genuinely overlap — logging agent-writable channels (GovAI's "Activity logs" item, behind
`MRFM-D3-1`/`MRFM-D3-2`) and disclosing what an investigation's redactions limit (METR's
"Redaction summary / disclosure" item, behind `MRFM-CROSS-1`), plus the general reasoning-trace
retention ask behind `MRFM-D1-1` — MRFM STRENGTHENS the prior ask by adding a specific
integrity or verification mechanism (hash-chaining, signing, per-claim procedure disclosure,
contemporaneous flagging) that neither source specifies on its own. But whole regions of the
table have no real prior-art analogue at all: every D2 clause (self-report corroboration,
provenance labeling, faithfulness-measurement disclosure — a report-writing epistemics
question neither source addresses) and three of the four CROSS clauses (revision-changelog
integrity, machine-readable quotation, third-party-compute retention ownership) sit entirely
outside what either framework was written to cover.

Read together, this suggests METR's and GovAI's frameworks are necessary but not sufficient
for the failure modes this specific incident exposed. Where MRFM does sit on an existing
foundation, the addition is a verification mechanism, not a restatement — so even the
STRENGTHENS rows are evidence that the underlying ask existed but wasn't independently
checkable. And where MRFM is NEW, that's not this project inventing requirements for their
own sake: it's a plain reading of what a 125-row incident ledger surfaced that two of the
most directly relevant existing frameworks, published before and immediately after this
incident, did not anticipate.
