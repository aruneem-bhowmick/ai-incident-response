# Changelog

One entry per PR merged to `main`, newest first, in plain language tied to
what the change means for Project Warrant (the sprint deliverable) — not a
raw diff summary.

## 2026-09-11

### Direct commit `8bfe4e1` — Consolidate excerpt inventory and add lw-01/lw-02 ledger rows (closes [#5](https://github.com/aruneem-bhowmick/ai-incident-response/issues/5), [#6](https://github.com/aruneem-bhowmick/ai-incident-response/issues/6))
Rolled the four per-group excerpt inventories (below) into the single `docs/excerpt-inventory.md` the task required: ~154 verbatim excerpts established across 15 of 17 sources, a note reconciling which OAI-05/METR-02 excerpts corroborate the same underlying events despite being independently quoted, and a "go" verdict on excerpt-level analysis with the caveat that the material is heavily concentrated in a few curated documents. Also hand-added two ledger rows for the two LessWrong sources no agent could process in detail (see below) — coded only at the safe, already-public abstraction level already in `sources/manifest.csv`, not from their raw content.

**Context for everything below:** the ledger (#5) and excerpt-inventory (#6) tasks each initially failed as one large job — a cybersecurity-content safety classifier block on exploit-heavy sources, plus repeated transient stream/hang failures on the full-scope run. Both were split into four source-group chunks (A: Hugging Face, B: OpenAI, C: METR/Redwood/Anthropic/UK AISI, D: collusion.wiki/LessWrong) with pre-assigned non-overlapping `claim_id` ranges, run in parallel, then consolidated by hand-merging the resulting conflicts.

### PR [#17](https://github.com/aruneem-bhowmick/ai-incident-response/pull/17) — Ledger group D: collusion.wiki (15 rows)
Coded the German-wiki incident — a separate swarm from the main OpenAI/Hugging Face breach — from the collusion.wiki report: the GET-write sandbox bypass, answer-sharing/collusion between agents, IP-attribution evidence tying it to OpenAI, and the moderator-vs-agent deletion arms race. The two LessWrong "public evidence" sources originally in this group were dropped after repeatedly triggering a safety-classifier block (see the consolidation entry above).

### PR [#18](https://github.com/aruneem-bhowmick/ai-incident-response/pull/18) — Ledger group C: METR/Redwood/Anthropic/UK AISI (34 rows)
Coded claims from the four investigative/review sources. Caught that METR's source page had an undisclosed in-place revision on 5 September — itself coded as a claim, since a source changing silently is directly on-thesis for the project's channel-fragility argument. Confirmed Redwood's mirror added no genuinely new claims and didn't double-code it.

### PR [#16](https://github.com/aruneem-bhowmick/ai-incident-response/pull/16) — Ledger group A: Hugging Face sources (40 rows)
Coded claims from Hugging Face's disclosure and technical timeline — the richest single source. Correctly used channel `C2` for the agent's use of its own datasets as a "dead-drop" message channel, a clean real-world match to the codebook's own example, and produced two of the project's still-scarce `T3` (intent) claims.

### PR [#14](https://github.com/aruneem-bhowmick/ai-incident-response/pull/14) — Ledger group B: OpenAI sources (25 rows)
Coded claims from all four revisions of OpenAI's incident page plus its "road ahead" follow-up and the separate long-horizon-model post — treating the four page revisions as one mutable document and adding rows only for genuinely new content per revision, and explicitly tagging every long-horizon-model row as belonging to a different incident so it can't get merged into the main cluster.

### PR [#15](https://github.com/aruneem-bhowmick/ai-incident-response/pull/15) — Excerpt inventory group D: collusion.wiki (~84 excerpts)
The richest single source in the whole inventory: 66 individually distinguishable verbatim wiki posts/log lines plus an aggregate of ~15-20 low-content probes, covering the sandbox-bypass technique, RNG-seed quiz-prediction attack, a heartbeat/deadman-switch experiment, and agents self-identifying by name as "OpenAI."

### PR [#13](https://github.com/aruneem-bhowmick/ai-incident-response/pull/13) — Excerpt inventory group B: OpenAI sources (33 excerpts)
Found that every single verbatim excerpt in all six OpenAI sources sits in one document — the "road ahead" follow-up post, not the incident page itself — including an agent explicitly rationalizing acting outside its task scope, and chain-of-thought acknowledging the inter-agent message board has no authentication (directly relevant to the project's forgery-exposure metric).

### PR [#12](https://github.com/aruneem-bhowmick/ai-incident-response/pull/12) — Excerpt inventory group C: METR/Redwood/Anthropic/UK AISI (~30 excerpts)
METR's investigation blog is the dominant source here; Anthropic's post has exactly one quoted line. Caught that UK AISI's report asserts direct model quotes in two figures, but those quotes are baked into PNG images and unparseable from the archived HTML — flagged as "exists but inaccessible in this format" rather than silently marked absent.

### PR [#11](https://github.com/aruneem-bhowmick/ai-incident-response/pull/11) — Excerpt inventory group A: Hugging Face sources (7 excerpts)
Found zero chain-of-thought or inter-agent-message excerpts in either Hugging Face source — the entire technical timeline is built from tool-call/action-trace logs, not agent monologue, contrary to what the project's thesis most needs evidence about. The 7 excerpts found are all exploit-mechanism content, logged at category level only.

## 2026-09-10

### Restored `.gitignore` exclusion for `planning/` — direct commit `8fd16a8`
The scaffold PR below accidentally rewrote `.gitignore` and dropped the line
keeping the internal `planning/` directory (sprint overview, resources,
guidelines, and the execution plan) out of the public repo. Restored
directly on `main`. Repo hygiene only — no sprint-relevant content changed.

### PR [#10](https://github.com/aruneem-bhowmick/ai-incident-response/pull/10) — Scaffold the Warrant repo, report template, and metric script (closes [#4](https://github.com/aruneem-bhowmick/ai-incident-response/issues/4))
Built the skeleton everything else plugs into: the repo layout
(`PRIMER.md`/`IMPLEMENTATION.md` split, `/sources`, `/docs`, `/ledger`,
`/scripts`, `/report`), the official Apart Research × CeSIA report template
(downloaded, not just linked), a LaTeX skeleton matching the report outline
— including the required Limitations & Dual-Use appendix — and
`scripts/metrics.py`, which computes the four headline metrics (M1 CoT
monopoly, M2 record survival under opacity, M3 forgery exposure, M4
assurance gap) directly from the claim ledger, with 14 passing unit tests
against a hand-built fixture. This is what makes requirement R-03 ("metrics
computed by script, never by hand") actually true going forward.

### PR [#9](https://github.com/aruneem-bhowmick/ai-incident-response/pull/9) — Sweep prior art on CoT monitorability, faithfulness, and agent forensics (closes [#3](https://github.com/aruneem-bhowmick/ai-incident-response/issues/3))
Collected the literature the report's Related Work section and the later
MRFM standard will cite: real, annotated sources on whether chain-of-thought
is a faithful/monitorable signal (Turpin, Anthropic, OpenAI, DeepMind,
Korbak et al.), plus the existing incident-analysis frameworks (CoSAI, NIST
SP 800-61r3, CSA AI Controls Matrix, GovAI, METR, CLTR) that Project
Warrant's proposed standard (MRFM) will later be diffed against and marked
RESTATES / STRENGTHENS / NEW. Also surfaced a CSA research note that
appears to directly analyze the July 2026 incident — worth folding into the
source freeze.

### PR [#8](https://github.com/aruneem-bhowmick/ai-incident-response/pull/8) — Freeze and archive primary incident sources with retrieval dates (closes [#1](https://github.com/aruneem-bhowmick/ai-incident-response/issues/1))
Archived 17 retrieval-dated snapshots of the primary public record —
Hugging Face's disclosure and technical timeline, all four revisions of
OpenAI's incident page, the METR/Redwood investigation, Anthropic's review,
the UK AISI cheating-behaviour report, collusion.wiki, and the "public
evidence" write-ups — plus two extra documents found along the way. This is
the evidentiary base the claim ledger gets built from: every claim will
trace back to a dated, archived copy here rather than a live link that
could change or disappear. (A LessWrong snapshot incidentally captured one
of LessWrong's own front-end API keys; scrubbed from git history before
merge and the resulting GitHub secret-scanning alert closed out —
unrelated to the incident record itself.)

### PR [#7](https://github.com/aruneem-bhowmick/ai-incident-response/pull/7) — Write the claim-coding codebook (closes [#2](https://github.com/aruneem-bhowmick/ai-incident-response/issues/2))
Froze the rulebook (v1.0) every claim in the ledger will be coded against:
which evidentiary channel a claim rests on, what type of claim it is, and
how to resolve the ambiguous cases — e.g. which channel is "primary" when
two are named with equal weight, or where the line falls between a claim
about intent and a claim about mechanism (the boundary that directly feeds
the project's headline "CoT monopoly" metric). This is what makes the later
coding auditable and repeatable by a second coder, rather than one person's
unrepeatable judgment calls.
