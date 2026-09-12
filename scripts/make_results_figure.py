"""Generate the Results-section figure for Project Warrant's report (DL-6).

Per the report's own TODO comment (`report/report.tex`, Results section), this
produces a stacked bar chart of claim count by `claim_type` (T1-T5), with each
bar segmented by `d1_verdict` (SURVIVES / DEGRADED / COLLAPSES) -- the same
opacity-condition verdict `docs/headline-metrics.md`'s M2 metric is built on.
The point of the figure is visual: T3 (intent) claims should read as
compositionally different from T1/T2/T4/T5 -- mostly DEGRADED/COLLAPSES rather
than mostly SURVIVES -- which is the same finding M2's by-claim-type table
reports as numbers.

This reads `/ledger/claims.csv` with Python's `csv` module, matching
`scripts/metrics.py`'s own reading path (`metrics.read_claims`, which handles
the `utf-8-sig` BOM and empty/missing-file cases) rather than re-implementing
CSV parsing. Nothing here recomputes a headline metric (R-03) -- this script
only tallies claim counts per (claim_type, d1_verdict) cell for the chart; the
percentages that appear in the report's prose and tables come from
`docs/headline-metrics.md` / `scripts/metrics.py` directly, not from here.

Colors follow the project's own stoplight-severity reading of the three D1
verdicts (SURVIVES is safe/green, DEGRADED is a caution/amber, COLLAPSES is a
failure/red) and use the fixed, non-thematic "status" hex steps validated for
this purpose: good `#0ca30c`, warning `#fab219`, critical `#d03b3b`.

Usage:
    python scripts/make_results_figure.py [path/to/claims.csv] [path/to/output.png]

If no arguments are given, defaults to `ledger/claims.csv` and
`report/figures/claims-by-type-d1-verdict.png`, both resolved relative to the
repository root (the parent of this script's directory).
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path
from typing import Optional

import matplotlib

matplotlib.use("Agg")  # headless-safe backend; no display needed to save a PNG.
import matplotlib.pyplot as plt

from metrics import read_claims

# Fixed claim-type order, matching every other table/figure in this project
# (docs/headline-metrics.md, docs/codebook.md): T1 Event, T2 Mechanism,
# T3 Intent, T4 Counterfactual, T5 Assurance.
CLAIM_TYPE_ORDER = ["T1", "T2", "T3", "T4", "T5"]
CLAIM_TYPE_LABELS = {
    "T1": "T1\nEvent",
    "T2": "T2\nMechanism",
    "T3": "T3\nIntent",
    "T4": "T4\nCounterfactual",
    "T5": "T5\nAssurance",
}

# D1 verdict stacking order (bottom to top) and stoplight-severity colors.
# Hex values are this project's fixed "status" palette steps (good / warning /
# critical), reserved for state encoding and never reused as a categorical
# series color.
VERDICT_ORDER = ["SURVIVES", "DEGRADED", "COLLAPSES"]
VERDICT_COLORS = {
    "SURVIVES": "#0ca30c",   # good -- green
    "DEGRADED": "#fab219",   # warning -- amber
    "COLLAPSES": "#d03b3b",  # critical -- red/rose
}


def tally_by_type_and_verdict(rows: list[dict]) -> dict[str, Counter]:
    """Count rows per (claim_type, d1_verdict) cell.

    Returns a dict keyed by claim_type -> Counter over d1_verdict values.
    Claim types or verdicts outside the fixed vocabularies are counted too
    (so a coding error would show up as an unexpected bar/segment rather than
    being silently dropped), but the chart only draws the fixed, documented
    categories in a fixed order.
    """
    by_type: dict[str, Counter] = {}
    for row in rows:
        claim_type = row.get("claim_type", "")
        verdict = row.get("d1_verdict", "")
        by_type.setdefault(claim_type, Counter())[verdict] += 1
    return by_type


def make_figure(rows: list[dict], output_path: Path) -> None:
    """Build and save the stacked bar chart to `output_path`."""
    by_type = tally_by_type_and_verdict(rows)

    x_labels = [CLAIM_TYPE_LABELS.get(ct, ct) for ct in CLAIM_TYPE_ORDER]
    x_positions = range(len(CLAIM_TYPE_ORDER))

    fig, ax = plt.subplots(figsize=(4.6, 3.5), dpi=300)

    bottoms = [0] * len(CLAIM_TYPE_ORDER)
    for verdict in VERDICT_ORDER:
        counts = [by_type.get(ct, Counter()).get(verdict, 0) for ct in CLAIM_TYPE_ORDER]
        bars = ax.bar(
            x_positions,
            counts,
            bottom=bottoms,
            width=0.62,
            color=VERDICT_COLORS[verdict],
            edgecolor="#fcfcfb",  # 2px-equivalent surface gap between segments
            linewidth=1.2,
            label=verdict.title(),
        )
        # Selective direct labels: only label segments large enough to hold
        # a legible number, so the chart isn't cluttered with near-zero labels.
        for bar, count in zip(bars, counts):
            if count >= 2:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + bar.get_height() / 2,
                    str(count),
                    ha="center",
                    va="center",
                    fontsize=8,
                    color="#0b0b0b" if verdict == "DEGRADED" else "#ffffff",
                )
        bottoms = [b + c for b, c in zip(bottoms, counts)]

    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(x_labels, fontsize=8)
    ax.set_ylabel("Claim count", fontsize=9)
    ax.set_xlabel("Claim type", fontsize=9)
    ax.tick_params(axis="y", labelsize=8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#c3c2b7")
    ax.spines["bottom"].set_color("#c3c2b7")
    ax.yaxis.grid(True, color="#e1e0d9", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, -0.16),
        ncol=3,
        frameon=False,
        fontsize=8,
        columnspacing=1.2,
        handlelength=1.4,
    )

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _default_paths() -> tuple[Path, Path]:
    repo_root = Path(__file__).resolve().parent.parent
    claims_path = repo_root / "ledger" / "claims.csv"
    output_path = repo_root / "report" / "figures" / "claims-by-type-d1-verdict.png"
    return claims_path, output_path


def main(argv: list[str]) -> int:
    default_claims_path, default_output_path = _default_paths()
    claims_path = Path(argv[1]) if len(argv) > 1 else default_claims_path
    output_path = Path(argv[2]) if len(argv) > 2 else default_output_path

    rows = read_claims(claims_path)
    if not rows:
        print(f"No claim rows found at {claims_path}; cannot build the figure.")
        return 1

    make_figure(rows, output_path)
    print(f"Wrote {output_path} from {len(rows)} claims in {claims_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
