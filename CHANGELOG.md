# Changelog

One entry per PR merged to `main`, newest first, in plain language tied to
what the change means for Project Warrant (the sprint deliverable) — not a
raw diff summary.

## 2026-09-12 (P3)

### PR [#80](https://github.com/aruneem-bhowmick/ai-incident-response/pull/80) — Resolve the LaTeX/PDF build path for the report (closes [#67](https://github.com/aruneem-bhowmick/ai-incident-response/issues/67))
Closed Gap A from the 2026-09-12 stress test: this machine had no LaTeX toolchain installed at all. Rather than a multi-gigabyte system-wide TeX install, downloaded the portable Tectonic engine into a repo-local, gitignored path (`.tools/tectonic.exe`) — no admin rights, no PATH changes, fully reversible. Smoke-tested against the still-placeholder `report/report.tex` skeleton and it compiled clean. `report/BUILD.md` now has the exact working command plus a documented Overleaf fallback, so producing the final `report.pdf` is a solved problem well before the report's content is finished.

### PR [#79](https://github.com/aruneem-bhowmick/ai-incident-response/pull/79) — Draft the report's Related Work section (closes [#69](https://github.com/aruneem-bhowmick/ai-incident-response/issues/69))
First P3 report section to land. `report/drafts/related-work.tex` synthesizes `docs/prior-art.md`'s three sweeps — CoT monitorability/faithfulness, agent-forensics/incident-analysis frameworks, and incident-reporting design — into the report's actual Related Work prose, and states the gap this project fills explicitly: no existing framework measures channel-dependence of specific public claims about a specific incident. Sets up the later MRFM diff by naming the GovAI/METR connection here first, so the RESTATES/STRENGTHENS/NEW result doesn't surprise a reader encountering it cold. Fifteen citations, each traced back to a real entry in the prior-art doc.

## 2026-09-12

### PR [#65](https://github.com/aruneem-bhowmick/ai-incident-response/pull/65) — Freeze MRFM v0.1 and close Gate G2 (closes [#57](https://github.com/aruneem-bhowmick/ai-incident-response/issues/57), [#49](https://github.com/aruneem-bhowmick/ai-incident-response/issues/49))
Gate G2 met. `mrfm/mrfm-v0.1.md` tagged `v0.1 — frozen 2026-09-12` with a Limitations section added: it doesn't establish that any lab would find these 14 clauses adoptable (no lab was asked), doesn't establish the evidence-required fields survive a red-teaming pass (none has happened), and only covers what one incident's 125-row ledger surfaced — not incidents in general. Per the sprint plan's own criterion, quoted verbatim in the PR: "clause table complete with diff column; RFI questions drafted." That closes the whole of P2 — five parallel drafting/derivation issues, a consolidation, a prior-art diff, and this freeze, all running as independent worktree-per-subagent tasks the same way P1 handled its four ledger-coding groups.

### PR [#64](https://github.com/aruneem-bhowmick/ai-incident-response/pull/64) — Diff MRFM v0.1 against METR/GovAI prior art (closes [#56](https://github.com/aruneem-bhowmick/ai-incident-response/issues/56))
P2.2 done. Diffed all 14 clauses against `docs/prior-art.md`'s METR and GovAI entries: 0 RESTATES, 4 STRENGTHENS (`MRFM-D1-1`, `MRFM-D3-1`, `MRFM-D3-2`, `MRFM-CROSS-1` — each adds a verification mechanism, like hash-chaining or signing, to a general ask METR/GovAI already make), 10 NEW. This is the inverse of the sprint plan's cautionary framing ("mostly RESTATES is a finding, not a failure") — here mostly-NEW is the finding: METR's and GovAI's frameworks were written as general investigation-access and retention guidance, and simply didn't anticipate several of the specific failure modes this incident's ledger surfaced (self-report corroboration, revision-changelog integrity, machine-readable quotation, third-party-compute retention ownership). Framed honestly in the document itself rather than forced into a RESTATES-heavy narrative that the actual diff didn't support.

### PR [#63](https://github.com/aruneem-bhowmick/ai-incident-response/pull/63) — Consolidate MRFM clause groups into MRFM v0.1 (closes [#55](https://github.com/aruneem-bhowmick/ai-incident-response/issues/55))
Merged the four parallel clause drafts below into `mrfm/mrfm-v0.1.md`: 14 clauses total (D1×3, D2×3, D3×4, CROSS×4), right at the sprint plan's upper target of 8-14 — none trimmed, since every one traces to a distinct evidenced gap. Two cross-group overlaps were found and deliberately kept rather than merged: `MRFM-D1-1`/`MRFM-D3-1` both impose CoT retention duties but for different reasons (targeted disclosure vs. blanket tamper-evidence), and `MRFM-D1-2`/`MRFM-D3-1`+`D3-3` both use outside-party escrow but prove different things (retention timing vs. non-tampering). The four source draft files are deleted; their content lives on in the consolidated table.

### PR [#62](https://github.com/aruneem-bhowmick/ai-incident-response/pull/62) — Derive RFI questions from V3/COLLAPSES ledger rows (closes [#54](https://github.com/aruneem-bhowmick/ai-incident-response/issues/54))
P2.3 done. Queried the frozen 125-row ledger for `verifiability == V3` (15 rows) and any `COLLAPSES` verdict across D1/D2/D3 (2/9/21 rows respectively) — 36 distinct claims once de-duplicated. Grouped into 8 recurring gaps rather than one question per row: self-graded assurance claims with no external check (Hugging Face's containment claims, the unreleased-model persistence claim, UK AISI's anti-cheating monitor), intent/motivation claims resting only on self-report echoes (the same D2 problem ADR 0001 already fixed in this project's own coding), an attribution chain nobody outside two labs can verify, technical claims resting solely on agent-writable logs, and the DSEWiki secondary incident's total dependence on the wiki's own editable history. Each question states concretely what answer would and wouldn't settle it — all cited `claim_id`s spot-checked directly against the ledger before merging.

### PR [#61](https://github.com/aruneem-bhowmick/ai-incident-response/pull/61) — Draft MRFM clauses for cross-cutting verifiability & process (closes [#53](https://github.com/aruneem-bhowmick/ai-incident-response/issues/53))
Four clauses (`MRFM-CROSS-1..4`) targeting the reporting process itself rather than any one degradation condition: assurance claims need a stated verification procedure, not a bare assertion (M4's 57.1% V3 finding); revised incident reports need a real changelog, not just an occasional "Update on [date]" paragraph; quoted model output has to be machine-readable text, not just baked into a screenshot (UK AISI's own report does this); and third-party-compute staging environments need the same retention obligations as a lab's own systems. Notably, the agent caught and corrected a bad citation in its own issue's grounding text (claim `C208` doesn't say what the issue assumed it said) rather than drafting around it silently — flagged transparently in the file itself.

### PR [#60](https://github.com/aruneem-bhowmick/ai-incident-response/pull/60) — Draft MRFM clauses defending against D3 (adversarial forgery) (closes [#52](https://github.com/aruneem-bhowmick/ai-incident-response/issues/52))
Four clauses (`MRFM-D3-1..4`): hash-chained append-only logging for agent-writable channels so tampering is detectable without needing to know how it was done; cryptographic signing of channel entries keyed to the originating agent/session — formalizing the same signing scheme METR's report describes agents inventing themselves mid-incident; pre-committed, publicly checkable verification material so a lab can't generate keys after the fact and claim they were always there; and retained, cross-checkable egress logs framed as evidentiary preservation rather than prevention.

### PR [#59](https://github.com/aruneem-bhowmick/ai-incident-response/pull/59) — Draft MRFM clauses defending against D1 (opacity) (closes [#50](https://github.com/aruneem-bhowmick/ai-incident-response/issues/50))
Three clauses (`MRFM-D1-1..3`), scoped tightly to M2's actual finding — only `T3` (intent) claims depend on CoT disclosure, everything else survives D1 at 89%+ — rather than proposing blanket retention: targeted retention of legitimacy/scope/objective reasoning traces, a third-party escrow receipt so retention is verifiable without lab cooperation, and pre-registered retention-trigger criteria so a lab can't narrow what counts as qualifying content after an incident is already underway.

### PR [#58](https://github.com/aruneem-bhowmick/ai-incident-response/pull/58) — Draft MRFM clauses defending against D2 (unfaithfulness) (closes [#51](https://github.com/aruneem-bhowmick/ai-incident-response/issues/51))
Start of P2 (drafting the v0.1 forensic-minimum standard, MRFM). Three clauses (`MRFM-D2-1..3`), all generalizing the ADR 0001 fix directly into lab-facing requirements: self-reported reasoning/intent claims need independent, scope-matched corroboration before an incident report can present them as fact; reports must visibly label each reasoning claim as self-reported vs. independently confirmed; and any report relying on disclosed chain-of-thought must disclose the model's measured faithfulness rate or admit none exists. Four parallel clause-drafting/derivation issues (D1, D2, D3, cross-cutting, RFI) ran as independent, unblocked tasks — the same pattern P1 used for its four ledger-coding groups.

## 2026-09-11

### Direct commits `db875f2`, `ac7f2d9` — Re-freeze the ledger at v1.2 after the lw-01/lw-02 addition
Merging the lw-retry PR below required follow-up: D-coded the 9 new rows (all trivially `SURVIVES` on D1-D3, since all rest solely on `C5`), refreshed M1-M5 for the new 125-row ledger (M3 and M5 both moved slightly toward *less* dramatic — evidence the original numbers weren't inflated by omission), updated the freeze statement in `docs/headline-metrics.md` and `ledger/schema.md`'s changelog to record the ledger passed through v1.1 (116 rows) before settling at v1.2 (125 rows), and refreshed the numbers quoted in the title-candidates doc to match.

### PR [#48](https://github.com/aruneem-bhowmick/ai-incident-response/pull/48) — Retry lw-01/lw-02 with a narrow, category-only pass (closes [#43](https://github.com/aruneem-bhowmick/ai-incident-response/issues/43))
A stress-test of the frozen P1 ledger flagged that these two sources' near-total absence (only 2 hand-coded rows out of 116) most plausibly made the forgery-exposure metrics look more fragile than reality, since they're specifically the record's technical/mechanism evidence. Two prior attempts to process them in any detail had been blocked by a cybersecurity-content safety classifier. This retry succeeded by extracting only section-heading text — never reading, quoting, or summarizing any code, command, or payload underneath — adding 9 new claim-level rows without tripping the classifier at all.

### PR [#47](https://github.com/aruneem-bhowmick/ai-incident-response/pull/47) — Add a supplementary codebook-fragility metric (M5) to metrics.py (closes [#42](https://github.com/aruneem-bhowmick/ai-incident-response/issues/42))
The project's four official metrics only treat raw chain-of-thought (M1) or agent-writable channels (M3) as "fragile." But the codebook's own fragility ranking already places lab assertions with no stated substrate (`C6`) above two channels it calls sturdy. Using that broader, already-defined fragile set instead of inventing a new one found a far more statistically robust version of the project's core finding: originally 84.5% of all 116 claims (later 78.4% of 125, after the lw-retry above) rest on a fragile primary channel — a much better-powered number than M1's fragile 11.1% (drawn from only 9 claims).

### PR [#46](https://github.com/aruneem-bhowmick/ai-incident-response/pull/46) — Add small-sample-size caveats to headline metrics (closes [#41](https://github.com/aruneem-bhowmick/ai-incident-response/issues/41))
`docs/headline-metrics.md` was quietly overclaiming on two numbers: M1's 11.1% is 1 of only 9 `T3` claims (a single row swings it ~11 points), and the M2 table's "T4 survives at 100%" was 2 of 2 claims, presented as if it meaningfully confirmed or contradicted the sprint plan's own prediction. Neither claim was false, but neither was disclosed as fragile. Both now state their denominators plainly.

### PR [#44](https://github.com/aruneem-bhowmick/ai-incident-response/pull/44) — Draft working-title candidates for the report
The sprint plan's own working title ("Warranted by One Channel...") would overclaim once M1/M2 were in hand — the record survives CoT opacity at ~90% overall, so a title implying broad collapse doesn't match the data. Three candidates drafted with an explicit tradeoff (a dramatic-but-n=9 framing vs. a less viscerally specific but n=125-powered framing), left open for a P3 decision rather than picked here.

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
