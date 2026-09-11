# Changelog

One entry per PR merged to `main`, newest first, in plain language tied to
what the change means for Project Warrant (the sprint deliverable) — not a
raw diff summary.

## 2026-09-11

### Direct commit `16ece7a` and PR [#40](https://github.com/aruneem-bhowmick/ai-incident-response/pull/40) — Freeze the ledger at v1.1 and record headline metrics (closes [#30](https://github.com/aruneem-bhowmick/ai-incident-response/issues/30), [#19](https://github.com/aruneem-bhowmick/ai-incident-response/issues/19))
Gate G1 met. Final M1-M4 recorded in `docs/headline-metrics.md`: M1 (CoT monopoly) 11.1%, M2 (record survival under opacity) 89.7% overall — but split by claim type, T1 and T4 survive at 100% while T3 (intent) collapses to 22.2%, confirming half of the plan's own prediction and contradicting the other half (T4 was predicted not to survive). M3 (forgery exposure) 9.5%, M4 (assurance gap) 57.1%. Per the plan's own instruction, no further edits to the ledger from here — this closes out the whole P1 phase.

### PR [#39](https://github.com/aruneem-bhowmick/ai-incident-response/pull/39) — Fix codebook D2 rule and recode the ledger (closes [#29](https://github.com/aruneem-bhowmick/ai-incident-response/issues/29))
The reliability check below failed on D2 specifically. Diagnosed the cause precisely: the codebook let D2 reuse the same "does a corroborating channel rescue this?" logic as D1/D3, but D2 needs a stricter test since an unfaithful self-report can be systematic rather than a one-off — a corroborating channel only counts if it's independent of the self-report being tested and matches the claim's actual scope. Logged as ADR 0001, codebook bumped to v1.1, then recoded all 116 rows' D2 verdicts against the fixed rule — only 6 actually changed, confirming the fix was surgical rather than a wholesale rewrite.

### PR [#38](https://github.com/aruneem-bhowmick/ai-incident-response/pull/38) — Compute Cohen's kappa and write the reliability report (closes [#28](https://github.com/aruneem-bhowmick/ai-incident-response/issues/28))
The actual reliability numbers: D1 (opacity) κ=0.7788, D2 (unfaithfulness) κ=0.5690, D3 (forgery) κ=0.7794. D2 fails the project's own 0.6 bar — the one number in P1 that determined whether the codebook needed a real fix, and it did.

### PR [#37](https://github.com/aruneem-bhowmick/ai-incident-response/pull/37) — Blind re-code the 25-row reliability subsample (closes [#27](https://github.com/aruneem-bhowmick/ai-incident-response/issues/27))
A fresh agent coded all three degradation conditions on the 25-row subsample from scratch, using only the stripped ledger rows and the codebook — no access to the original verdicts, which were kept on a path entirely outside the git repository for exactly this reason.

### PR [#36](https://github.com/aruneem-bhowmick/ai-incident-response/pull/36) — Prepare the blind re-code subsample and answer key (closes [#26](https://github.com/aruneem-bhowmick/ai-incident-response/issues/26))
Sampled 25 rows (seed 42) for the reliability check, naturally drawing 6 T5 (assurance) rows — well above the minimum needed to actually stress-test the rarest, highest-stakes claim type. Split the sample into a stripped version (committed, degradation columns removed) and an answer key written to a sibling directory outside the repo entirely, verified invisible to `git status` from inside it.

### Direct commit `c1f4f1c` — Consolidate group A-D degradation verdicts into the ledger (closes [#25](https://github.com/aruneem-bhowmick/ai-incident-response/issues/25))
Merged the four parallel D-coding passes below into `ledger/claims.csv` by `claim_id` (verified 116/116 exact match, no gaps or duplicates). M2 became real for the first time here: 89.7% overall opacity-survival, with the T1/T4-vs-T3 split noted above already visible at this stage.

### PRs [#31](https://github.com/aruneem-bhowmick/ai-incident-response/pull/31)-[#35](https://github.com/aruneem-bhowmick/ai-incident-response/pull/35) — D1/D2/D3 coding for ledger groups A-D, and the Cohen's kappa script (closes [#20](https://github.com/aruneem-bhowmick/ai-incident-response/issues/20)-[#24](https://github.com/aruneem-bhowmick/ai-incident-response/issues/24))
The start of P1: five independent, unblocked tasks run in parallel. The four D-coding passes (PR #34 group A, #33 group B, #35 group C, #32 group D) each wrote to their own narrow file rather than editing the shared ledger directly, avoiding the conflict risk P0 hit; several surfaced genuinely hard judgment calls worth remembering — group A deliberately favored the codebook's spirit over strict channel-literalism on its two T3 rows, group C flagged a self-referential problem in METR's own forgery-detection claims (a successful forgery would, by construction, never appear as a "confirmed case"), and group B explicitly noted a case where the channel-based test doesn't capture a claim's real weakness. PR #31 (kappa script) validated Cohen's kappa against three hand-worked cases before anything downstream depended on it.

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
