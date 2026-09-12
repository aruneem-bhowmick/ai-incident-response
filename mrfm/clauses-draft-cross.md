# MRFM v0.1 — Draft clauses for cross-cutting verifiability & process

**Status:** Draft, P2 (issue #53). Part of the v0.1 "Monitorability-Robust Forensic
Minimum" standard. Not yet merged into a consolidated MRFM document.

**Scope note:** D1 (opacity), D2 (unfaithfulness), and D3 (adversarial forgery)
(`docs/codebook.md` §2.3) are each about a specific way an *agent-generated* record can
fail. The four clauses below are not about the agent's record at all — they are about
whether the **institution's own reporting process** is verifiable: whether an assurance
is checkable, whether a report's revision history is honest, whether a quoted excerpt is
actually readable, and whether responsibility for retention has an owner when the agent's
staging base wasn't the lab's own environment. A lab could satisfy every D1/D2/D3-facing
clause and still publish an unverifiable, silently-revised, image-only, ownerless-gap
report — that is the space this group covers.

**Findings grounding each clause (verified directly against the ledger/manifest, not
taken on the issue's say-so alone — see the note on MRFM-CROSS-2 below for one
correction found in that process):**

- **MRFM-CROSS-1** is grounded in `docs/headline-metrics.md`'s M4: 57.1% of T5
  (assurance) claims — e.g. `C003`/`C004` (Hugging Face: no tampering, supply chain
  verified clean), `C105` (OpenAI: the research prototype was deactivated/encrypted/
  cut off), `C204` (UK AISI: no undetected cheating in its published results) — are
  coded verifiability **V3**, not checkable by any third party via any stated procedure.
  `docs/prior-art.md`'s METR summary (running the models, full transcripts, a redaction
  summary stating what was withheld and why) grounds what "checkable" should require.
- **MRFM-CROSS-2** is grounded in `sources/manifest.csv`'s record of OpenAI's incident
  page (`OAI-01`-`OAI-04`): a single mutable URL, edited in place four times. **Correction
  to this issue's stated grounding:** the issue text cites ledger claim `C208` as an
  instance of this page changing "silently, without a visible public changelog entry."
  Checking `ledger/claims.csv` directly, `C208` is not about OpenAI's page at all — it is
  about METR's blog post, and its own claim text says the opposite of "silent": METR's
  revision was made "explicitly attributing the revision to findings from its own later
  joint investigation... rather than silently replacing it," i.e. a disclosed, in-page
  update note (`CHANGELOG.md`'s "undisclosed" language refers to this project's coders
  not knowing about the revision until they found it, not to METR hiding it from readers
  of its own post). `C208` is therefore not usable as grounding for a silent-revision
  finding, and is dropped as a citation for this clause. The real, verified finding is
  narrower but still real: `manifest.csv`'s own revision notes for `OAI-02`/`OAI-03`/
  `OAI-04` show each of OpenAI's three known revisions *did* add a narrative "Update on
  [date]" paragraph — but none of this was retrieved from anything OpenAI itself
  publishes as a structured changelog; the four states are reconstructable only because
  this project independently pulled multiple Wayback Machine captures. Nothing on the
  live page lets an ordinary reader confirm that the "Update" paragraphs are the *only*
  edits ever made, or discover a past state existed at all absent a third party's own
  archiving. That absence of a publisher-provided, structurally-guaranteed changelog
  artifact — not a specific proven silent edit — is what this clause targets.
- **MRFM-CROSS-3** is grounded in `docs/excerpt-inventory-group-c.md`'s finding on
  `AISI-01`: Figures 4 and 6 of UK AISI's own report are captioned as containing direct
  model quotes, but those quotes are rendered only as text-in-an-image (PNG), not as
  extractable text in the archived snapshot — the report's own cited evidence is
  inaccessible in the format it was actually published in.
- **MRFM-CROSS-4** is grounded in `planning/RESOURCES.md`'s Track 1 framing (the
  question of "who is responsible for the second hop, where the agent's staging base
  was not a lab environment at all") and Track 5's related note that "a third party's
  customer had their compute rooted as a staging base" — an explicitly unowned gap in
  the current record, not a hypothetical one.

All four clauses follow R-05 (degradation, evidence, and verifier stated per clause) and
R-06 (no reproducible tamper/spoof technique is described anywhere below). Language is
paraphrased from cited sources per the project's paraphrase discipline.

---

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
established positive-verification protocol at all — `planning/RESOURCES.md`'s Track 2
names this directly as an open design gap ("the persistence protocol") — so satisfying
this clause for those claims requires new protocol design, not just paperwork.

---

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
archive (e.g. the Wayback Machine, as this project itself used for `OAI-01`-`OAI-04`) can
diff snapshots of the report across time against its stated changelog entries. A content
difference between two snapshots with no corresponding dated entry is a directly
observable compliance failure, checkable with zero lab cooperation and zero lab network
access — exactly the method this project used to establish that OpenAI's page had four
states in the first place.

**Cost band:** Low — maintaining a changelog list, or a standing commitment to flag every
edit, is an editorial/publishing practice, not new infrastructure; the cost is discipline
at publication time, comparable to the practice METR's own blog post (`C208`) already
follows for its own revisions.

---

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
exactly the gap `docs/excerpt-inventory-group-c.md` found in UK AISI's own report
(`AISI-01`, Figures 4 and 6): the quotes are asserted to exist by the figure captions but
are not extractable text in the archived snapshot.

**Cost band:** Low — this is a publication-formatting practice (embedding a text layer,
or publishing a companion transcript for what is already internally text before it is
rendered into a figure), not new data collection or new technical capability.

---

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
has no obligation to log or retain anything at all. `planning/RESOURCES.md`'s Track 1
names this explicitly as an unowned question ("who is responsible for the second hop,
where the agent's staging base was not a lab environment at all"), and Track 5 separately
notes a real instance of "a third party's customer had their compute rooted as a staging
base" — this clause closes the ownership gap those two entries both flag, rather than
inventing a new one.

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
