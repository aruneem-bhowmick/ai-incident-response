# Project Warrant: Primer

Project Warrant is a solo audit of the July 2026 OpenAI/Hugging Face agent-escape
incident, built for the Apart Research × CeSIA AI Incident Response Sprint
(Track 2, "What happened, and what breaks next"). Rather than re-litigating what
happened, it asks a narrower and checkable question: **which evidentiary channel
does each public claim about the incident actually rest on**, and how many of
those claims would survive if that channel went dark, lied, or was forged. Every
claim made about the incident in the public record is logged in a claim ledger,
tagged with its primary and corroborating evidence channels, and stress-tested
against three degradation conditions (opacity, unfaithfulness, and adversarial
forgery) to produce five headline metrics and a draft v0.1 minimum forensic
standard (MRFM) for what future incident reports should be required to preserve.

**One-sentence thesis:** the public understanding of this incident is
disproportionately warranted by the single evidentiary channel most likely to
disappear or be forged next time, and that dependency is measurable.

**Where to start:** a judge skimming this in under 15 minutes should read
`/report/report.pdf` (or its LaTeX source, `/report/report.tex`) for the full
writeup; it is the primary deliverable. For the underlying instrument, see
`/ledger/claims.csv` (the claim ledger itself) and `/docs/codebook.md` (the
coding rules that produced it). `/IMPLEMENTATION.md` explains how the pieces fit
together and how to reproduce the headline metrics from the raw ledger.
