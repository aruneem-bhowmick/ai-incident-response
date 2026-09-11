# Official sprint report template

**`apart-cesia-report-template.pdf`** is a static export of the official Apart
Research x CeSIA AI Incident Response Sprint report template, retrieved
directly (see provenance below) rather than guessed. Per this task's
instructions, the live sprint page's "Guidelines" content supersedes anything
in an acceptance email, so this was located from the live sprint page itself.

## Provenance

- **Found via:** [AI Incident Response Sprint | Apart Research](https://apartresearch.com/sprints/ai-incident-response-sprint-2026-09-11-to-2026-09-13),
  under the page's "Submission Requirements" heading, linked as
  **"Submission Template =>"**.
- **Canonical link (Google Doc, editable):**
  <https://docs.google.com/document/d/1PQBlhI3tM5vb51x7jBWXBQMYg6hkiU_x8RaCws4kjl4/copy?usp=sharing>
  — this is a "make a copy" link; opening it creates your own editable Google
  Doc copy of the blank template. This is the authoritative, live version --
  if it and the archived PDF here ever disagree, the live doc wins.
- **What's in this directory:** `apart-cesia-report-template.pdf` is a direct
  export of that Google Doc (`.../export?format=pdf`) taken at retrieval time,
  archived here as a snapshot for offline reference (same practice as
  `/sources/manifest.csv` snapshots). It is the blank template with its own
  guidance/instructional text still in place (delete that text when actually
  drafting a submission from a copy of the live doc).
- **Retrieval date:** 2026-09-10.
- **Confirmed page count:** 4 pages, consistent with the template's own stated
  "Recommended length: 4 pages excluding references and appendix."

## Why the project's actual LaTeX skeleton differs from this template's outline

The generic template above uses a generic outline (Introduction; Related Work;
Methods; Results; Discussion and Limitations; Conclusion; Code and Data;
Author Contributions; References; Appendix; LLM Usage Statement) and says
explicitly: *"The section structure is strong guidance but not rigid. If your
project requires a different organization, feel free to adapt."*

Project Warrant's actual submission is built from `/report/report.tex`, which
follows this project's own outline (Introduction, Related Work, Method,
Results, MRFM v0.1, Discussion, then appendices) instead of reproducing this
generic template section-for-section, because the project has a
project-specific section (MRFM v0.1) that the generic template has no slot
for. The generic template's *required* elements not already covered by
`report.tex`'s own structure -- author/affiliation block, an LLM Usage
Statement, and a Code and Data section -- should be folded in when the report
is actually drafted (P2/P3), not deferred indefinitely.

`report.tex` additionally includes a stubbed **Limitations and Dual-Use
Considerations** appendix, which this generic template does not name as such
(it only has a generic "Discussion and Limitations" section and an optional
"Appendix" for supplementary material) -- that appendix is required in every
submission regardless of track per the sprint's Guidelines page, which is a
different document from this template.
