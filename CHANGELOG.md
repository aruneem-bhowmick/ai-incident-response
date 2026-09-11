# Changelog

One entry per PR merged to `main`, newest first, in plain language tied to
what the change means for Project Warrant (the sprint deliverable) — not a
raw diff summary.

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
