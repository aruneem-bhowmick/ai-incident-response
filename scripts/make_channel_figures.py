"""Generate two additional Results-section figures for Project Warrant's report (DL-6).

Figure A (channel-fragility-class.png): claim count by primary_channel (C1-C6),
colored by fragility class -- agent-writable (C1-C3), lab-assertion (C6), and
sturdy (C4-C5) -- the same three-way split the report's Results section uses
to decompose M5. The point of the figure is visual: C6 should read as visibly
taller than every other bar, showing why M5's 78.4% headline is driven mainly
by unsubstantiated lab assertion rather than agent-writable content.

Figure B (verifiability-tiers.png): claim count by verifiability tier (V1-V3),
status-colored the same way D1 verdicts are (V1 good/green, V2 caution/amber,
V3 critical/red), tying directly to M4 (assurance gap, computed over T5 claims
at V3).

Both figures read /ledger/claims.csv via metrics.read_claims, matching every
other figure/metric script in this project. Neither recomputes a headline
metric (R-03); both only tally counts for the chart.

Usage:
    python scripts/make_channel_figures.py [path/to/claims.csv] [path/to/figures/dir]
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from metrics import read_claims

# Fixed channel order, matching the codebook's fragility ranking
# (docs/codebook.md Sec 3.1): C1 > C2 > C3 > C6 > C5 > C4, most fragile first.
CHANNEL_ORDER = ["C1", "C2", "C3", "C6", "C5", "C4"]
CHANNEL_LABELS = {
    "C1": "C1\nRaw CoT",
    "C2": "C2\nInter-agent\nmessages",
    "C3": "C3\nTool-call\ntrace",
    "C6": "C6\nLab\nassertion",
    "C5": "C5\nHuman\ntestimony",
    "C4": "C4\nDefender\ntelemetry",
}

AGENT_WRITABLE = {"C1", "C2", "C3"}
LAB_ASSERTION = {"C6"}

# Status palette steps (docs/dataviz reference palette, fixed and never
# themed): good/critical for the two-way fragile/sturdy split already used in
# Figure 1's D1-verdict coloring; a third, distinct status step (serious,
# amber-orange) marks C6 as fragile for a different reason than agent-writable
# content, matching the report's own three-way M5 decomposition.
COLOR_AGENT_WRITABLE = "#d03b3b"  # critical -- agent-writable, forgery-relevant
COLOR_LAB_ASSERTION = "#ec835a"  # serious -- unsubstantiated assertion, distinct mechanism
COLOR_STURDY = "#0ca30c"  # good -- independent of the acting agent

VERIFIABILITY_ORDER = ["V1", "V2", "V3"]
VERIFIABILITY_LABELS = {
    "V1": "V1\nPublic\nartifacts",
    "V2": "V2\nLab/platform\ncooperation",
    "V3": "V3\nNot\ncheckable",
}
VERIFIABILITY_COLORS = {
    "V1": "#0ca30c",
    "V2": "#fab219",
    "V3": "#d03b3b",
}


def _style_axes(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#c3c2b7")
    ax.spines["bottom"].set_color("#c3c2b7")
    ax.yaxis.grid(True, color="#e1e0d9", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)


def make_channel_figure(rows: list[dict], output_path: Path) -> None:
    counts = Counter(row.get("primary_channel", "") for row in rows)

    x_labels = [CHANNEL_LABELS.get(c, c) for c in CHANNEL_ORDER]
    x_positions = range(len(CHANNEL_ORDER))
    values = [counts.get(c, 0) for c in CHANNEL_ORDER]

    def color_for(channel: str) -> str:
        if channel in AGENT_WRITABLE:
            return COLOR_AGENT_WRITABLE
        if channel in LAB_ASSERTION:
            return COLOR_LAB_ASSERTION
        return COLOR_STURDY

    colors = [color_for(c) for c in CHANNEL_ORDER]

    fig, ax = plt.subplots(figsize=(5.0, 3.5), dpi=300)
    bars = ax.bar(x_positions, values, width=0.62, color=colors, edgecolor="#fcfcfb", linewidth=1.2)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1.2,
            str(value),
            ha="center",
            va="bottom",
            fontsize=8,
            color="#0b0b0b",
        )

    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(x_labels, fontsize=7.5)
    ax.set_ylabel("Claim count (primary channel)", fontsize=9)
    ax.set_ylim(0, max(values) * 1.18)
    ax.tick_params(axis="y", labelsize=8)
    _style_axes(ax)

    handles = [
        plt.Rectangle((0, 0), 1, 1, color=COLOR_AGENT_WRITABLE),
        plt.Rectangle((0, 0), 1, 1, color=COLOR_LAB_ASSERTION),
        plt.Rectangle((0, 0), 1, 1, color=COLOR_STURDY),
    ]
    ax.legend(
        handles,
        ["Agent-writable (C1-C3)", "Lab assertion (C6)", "Sturdy (C4-C5)"],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.22),
        ncol=1,
        frameon=False,
        fontsize=8,
        handlelength=1.2,
    )

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def make_verifiability_figure(rows: list[dict], output_path: Path) -> None:
    counts = Counter(row.get("verifiability", "") for row in rows)

    x_labels = [VERIFIABILITY_LABELS.get(v, v) for v in VERIFIABILITY_ORDER]
    x_positions = range(len(VERIFIABILITY_ORDER))
    values = [counts.get(v, 0) for v in VERIFIABILITY_ORDER]
    colors = [VERIFIABILITY_COLORS[v] for v in VERIFIABILITY_ORDER]

    fig, ax = plt.subplots(figsize=(3.6, 3.5), dpi=300)
    bars = ax.bar(x_positions, values, width=0.55, color=colors, edgecolor="#fcfcfb", linewidth=1.2)
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 1.2,
            str(value),
            ha="center",
            va="bottom",
            fontsize=8,
            color="#0b0b0b",
        )

    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(x_labels, fontsize=7.5)
    ax.set_ylabel("Claim count", fontsize=9)
    ax.set_ylim(0, max(values) * 1.2)
    ax.tick_params(axis="y", labelsize=8)
    _style_axes(ax)

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def _default_paths() -> tuple[Path, Path]:
    repo_root = Path(__file__).resolve().parent.parent
    claims_path = repo_root / "ledger" / "claims.csv"
    figures_dir = repo_root / "report" / "figures"
    return claims_path, figures_dir


def main(argv: list[str]) -> int:
    default_claims_path, default_figures_dir = _default_paths()
    claims_path = Path(argv[1]) if len(argv) > 1 else default_claims_path
    figures_dir = Path(argv[2]) if len(argv) > 2 else default_figures_dir

    rows = read_claims(claims_path)
    if not rows:
        print(f"No claim rows found at {claims_path}; cannot build the figures.")
        return 1

    make_channel_figure(rows, figures_dir / "channel-fragility-class.png")
    make_verifiability_figure(rows, figures_dir / "verifiability-tiers.png")
    print(f"Wrote 2 figures to {figures_dir} from {len(rows)} claims in {claims_path}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
