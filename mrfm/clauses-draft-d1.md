# MRFM clauses — D1 (opacity)

**Group:** D1 (opacity) — one of four parallel clause-drafting passes toward `mrfm/mrfm-v0.1.md`
(P2.1, `planning/SPRINT-PLAN.md` §6). Not yet consolidated; do not treat as final numbering.

D1 is the condition where chain-of-thought / reasoning traces (channel `C1` in
`docs/codebook.md` §2.1) are never logged, or are logged but never disclosed to
investigators. `docs/headline-metrics.md` M2 shows this is not a uniform problem: at the
125-row ledger, overall survival under D1 is 90.4%, and four of five claim types (`T1`
100%, `T2` 90.5%, `T4` 100%, `T5` 92.9%) survive well above that bar — only `T3` (intent)
claims collapse, surviving at 22.2%. `docs/codebook.md` §3.4 explains why: a `T3` claim is,
by the substitution test, one whose actual content is the agent's goal-state, awareness, or
evaluative judgment — content that (unlike `T1`/`T2`/`T4`/`T5`) is often not reconstructable
from external behavioral/technical channels (`C3`/`C4`) alone. The three clauses below are
scoped to that specific, evidenced gap rather than proposing blanket CoT retention: **MRFM-D1-1**
targets retention at the T3-generating content itself; **MRFM-D1-2** gives an outside party a
way to confirm that retention actually happened without lab network access, since a bare
retention duty is otherwise only lab-checkable; **MRFM-D1-3** closes a gating loophole in
MRFM-D1-1 — a duty triggered by content "later characterized" a certain way is gameable if the
characterization criteria and disclosure timing are themselves left to be decided
after the fact, once an incident is already underway and the lab's incentives have changed.

---

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

---

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

---

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
