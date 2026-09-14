# Project Warrant

Project Warrant is a solo audit, submitted to the Apart Research × CeSIA AI Incident
Response Sprint (Track 2, "What happened, and what breaks next"), of which evidentiary
channel each public claim about the July 2026 OpenAI/Hugging Face agent-escape incident
actually rests on. Its thesis: public understanding of the incident is disproportionately
warranted by the single evidentiary channel most likely to disappear or be forged next
time, and that dependency is measurable. To test that, every public claim about the
incident was extracted, coded against a fixed codebook, and stress-tested against three
degradation conditions: D1 opacity (the channel disappears or is withheld), D2
unfaithfulness (the channel's content misrepresents the underlying process), and D3
adversarial forgery (the channel's content could have been tampered with). That produced
a frozen 125-row claim ledger, five headline metrics summarizing how much of the public
record survives each stress test, a proposed v0.1 forensic-minimum evidentiary standard
(MRFM) for future agentic-AI incident reports, and a set of draft RFI questions a
regulator could send to probe exactly where the ledger shows the public record is
weakest.

## Key artifacts

- **Claim ledger**: [`ledger/claims.csv`](ledger/claims.csv) (125 rows, frozen v1.2),
  documented by [`ledger/schema.md`](ledger/schema.md).
- **Codebook**: [`docs/codebook.md`](docs/codebook.md), the controlled-vocabulary coding
  standard (claim types, evidentiary channels, degradation verdicts, verifiability tiers)
  the ledger is coded against.
- **Headline metrics**: [`docs/headline-metrics.md`](docs/headline-metrics.md), five
  metrics (M1-M5) computed by script from the frozen ledger, quantifying CoT monopoly,
  record survival under opacity, forgery exposure, the assurance gap, and overall claim
  fragility.
- **MRFM v0.1**: [`mrfm/mrfm-v0.1.md`](mrfm/mrfm-v0.1.md), the Monitorability-Robust
  Forensic Minimum: 14 clauses specifying what a lab (and its third-party compute
  providers) should retain, disclose, or make independently checkable so incident claims
  can be verified without lab network access.
- **RFI questions**: [`docs/rfi-questions.md`](docs/rfi-questions.md), draft
  request-for-information questions derived directly from the ledger rows where the
  public record is weakest (`verifiability == V3` or any degradation-verdict
  `COLLAPSES`).
- **Report**: [`report/report.pdf`](report/report.pdf), the final compiled submission
  ("Project Warrant: On Evidentiary Channel Dependency in a Frontier AI Incident
  Record," 12 pages total, 8 pages of core content plus references and appendix).
  LaTeX source at [`report/report.tex`](report/report.tex); build instructions in
  [`report/BUILD.md`](report/BUILD.md).

Supporting materials: the source manifest and archived primary sources
([`sources/`](sources/)), the metrics/reliability scripts and their unit tests
([`scripts/`](scripts/)), and one architecture decision record documenting a coding-rule
fix found during reliability testing ([`adr/`](adr/)).

## Disclosure: what was built during the sprint vs. prior art

Per this project's sprint plan (§6, P3.3) and the sprint's own guidelines on disclosing
prior work: **all content in `ledger/`, `docs/`, `mrfm/`, `adr/`, and the report itself
was created during the sprint window (10-13 September 2026).** None of the claim coding,
the codebook, the metrics, the MRFM clauses, the RFI questions, or the report text
existed before the sprint began.

The **only** thing that predates the sprint is the execution *method* used to produce
this repo: a spec-driven workflow, run with Claude Code, that scaffolds a repo layout up
front and then dispatches parallel work to one isolated git worktree per subagent per
task. That is the author's standing, habitual way of working on any project, not
sprint-specific prior art, and not an undisclosed pre-built instrument. No
incident-specific analysis, ledger content, codebook rules, or MRFM clauses were carried
in from outside the sprint window; only the general-purpose execution scaffolding
predates it.

## License

MIT. See [`LICENSE`](LICENSE).
