# Building `report.pdf`

Status: **local compile path confirmed working** in this environment (no
system-wide LaTeX install existed or was required). Use the Tectonic path
below unless you have a reason to prefer Overleaf (see fallback at the
bottom).

## Why Tectonic

This machine (and, per the 2026-09-12 stress test that opened this issue,
Aruneem's usual machine too) has no LaTeX toolchain at all: `pdflatex`,
`xelatex`, and `lualatex` are all absent from `PATH`, and there is no MiKTeX
or TeX Live install anywhere on it.

[Tectonic](https://tectonic-typesetting.github.io/) is a single self-contained
LaTeX engine binary. It needs no separate TeX Live/MiKTeX install: on first
compile it fetches only the specific packages/fonts a given document actually
uses from a CTAN-mirroring bundle server, and caches them locally for reuse.
That makes it the least invasive option available — no multi-gigabyte
system-wide install, nothing added to `PATH`, nothing outside this repo.

## One-time setup

1. Download the Windows x86\_64 build of Tectonic **0.17.0** (or newer) from
   the [tectonic-typesetting/tectonic releases
   page](https://github.com/tectonic-typesetting/tectonic/releases):
   asset `tectonic-<version>-x86_64-pc-windows-msvc.zip`.
2. Unzip it and place `tectonic.exe` at `.tools/tectonic.exe` (repo root).
   This path is gitignored (see `.gitignore`, "Portable build tooling")
   precisely so it's never committed — every contributor fetches their own
   copy.
3. Verify it runs:

   ```sh
   .tools/tectonic.exe --version
   # Tectonic 0.17.0
   ```

No PATH changes, no admin rights, and no other system changes are needed.

## Compile command

From a clean checkout of this repo, with the working directory at the repo
root:

```sh
.tools/tectonic.exe -X compile report/report.tex --outdir report
```

This produces `report/report.pdf`. On the very first run, Tectonic needs
network access to fetch the LaTeX packages/fonts the document uses
(`article` class, `geometry`, `hyperref`, `booktabs`, `graphicx`,
`enumitem`, plus their dependencies and Latin Modern fonts) — expect it to
print a long list of `note: downloading ...` lines. Those are cached
afterwards (Tectonic's bundle cache, outside the repo), so subsequent
compiles are fast and offline-capable.

`report/*.pdf` is gitignored, matching the rest of the LaTeX build artifacts
already ignored in `.gitignore` — the compiled PDF is a build output, not a
tracked file. Regenerate it with the command above whenever you need it
(e.g. right before submission).

### Confirmed smoke test (2026-09-12)

Ran the exact command above against the then-current `report/report.tex`
(P0.6 skeleton, placeholder content throughout, unmodified by this check).
Result: **pass**. Tectonic downloaded its package bundle, ran the TeX engine
(one rerun triggered automatically because `report.out` changed, which is
normal `hyperref`/TOC behavior, not an error), and wrote a valid
`report/report.pdf` (~36 KB, PDF 1.5). Only warning emitted was a single
harmless `Overfull \hbox (1.45482pt too wide)` at report.tex:133-134 — not
fatal, and expected to change once real content replaces the placeholder
text. No errors.

## Fallback: Overleaf (no local compile possible)

Not needed in this environment — the Tectonic path above worked — but
documented here in case a future environment can't run a downloaded binary
(no internet egress, execution restricted, etc.):

1. Go to [overleaf.com](https://www.overleaf.com) and create a new blank
   project.
2. Upload `report/report.tex` plus everything under `report/template/`
   (keep the same relative layout, i.e. a `template/` subfolder next to
   `report.tex`, if `report.tex` ever references those assets directly).
3. Set the project's compiler to **pdfLaTeX** (Menu -> Compiler -> pdfLaTeX).
   `report.tex` only uses the standard `article` class plus `geometry`,
   `hyperref`, `booktabs`, `graphicx`, and `enumitem`, all of which are
   available by default in Overleaf's TeX Live install — no extra package
   setup needed.
4. Compile (Overleaf compiles automatically on save, or click "Recompile").
5. Download the resulting PDF (Menu -> Download PDF, or the download icon
   above the preview pane).

## Summary for whoever builds the final PDF (P3 assembly / Aruneem)

Run this from the repo root once `report/report.tex` has real content:

```sh
.tools/tectonic.exe -X compile report/report.tex --outdir report
```

If `.tools/tectonic.exe` isn't present, re-fetch it per "One-time setup"
above (takes under a minute; the binary is ~50 MB). If for any reason a
local compile can't be made to work, use the Overleaf fallback above — it is
a real, actionable path, not a dead end.
