"""Compute Cohen's kappa for Project Warrant's blind-recode reliability check.

Per Gate G1 / R-04, inter-rater reliability on the degradation-coding pass
(D1/D2/D3) must be reported as a computed coefficient, not asserted. This
module is that computation. It takes two CSVs describing the *same* set of
ledger rows (matched by `claim_id`) -- an original coding pass and an
independent blind-recode pass -- each with columns `d1_verdict`, `d2_verdict`,
`d3_verdict` drawn from the controlled vocabulary `{SURVIVES, DEGRADED,
COLLAPSES}` (`docs/codebook.md` §2.3), and computes Cohen's kappa
independently for each of the three conditions.

Cohen's kappa is implemented directly rather than pulling in a dependency
(e.g. scikit-learn) for one formula:

    kappa = (p_o - p_e) / (1 - p_e)

where `p_o` is observed agreement (fraction of matched rows where both
raters gave the same verdict) and `p_e` is the agreement expected by chance
given each rater's marginal distribution over verdicts. See `cohens_kappa`
below for the derivation of `p_e`.

Usage:
    python scripts/kappa.py path/to/original.csv path/to/recoded.csv

If a condition's kappa is mathematically undefined (every matched row falls
into a single, identical category for both raters, so agreement-by-chance is
already 1.0 and the denominator is zero), this is reported explicitly as
NaN rather than crashing or silently returning 0 -- see `cohens_kappa`.
"""

from __future__ import annotations

import csv
import math
import sys
from pathlib import Path
from typing import Iterable

# The three degradation conditions this project stress-tests claims against
# (docs/codebook.md §2.3). Column names follow ledger/schema.md.
CONDITIONS = ("d1", "d2", "d3")
VERDICT_COLUMNS = {condition: f"{condition}_verdict" for condition in CONDITIONS}


def read_claims(path: Path) -> list[dict]:
    """Read a coded ledger CSV into a list of dict rows.

    Mirrors `scripts/metrics.py`'s `read_claims`: returns an empty list if
    the file does not exist rather than raising, so callers can report a
    missing input file as an unavailable/N-A result instead of crashing.
    """
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def _index_by_claim_id(rows: Iterable[dict]) -> dict[str, dict]:
    """Index rows by `claim_id`. On a duplicate id, the last row wins."""
    return {row["claim_id"]: row for row in rows if row.get("claim_id")}


def matched_label_pairs(
    original_rows: Iterable[dict],
    recoded_rows: Iterable[dict],
    verdict_column: str,
) -> list[tuple[str, str]]:
    """Pair up (original_label, recoded_label) for one verdict column.

    Only `claim_id`s present in *both* row sets are considered -- a row that
    exists in one coding pass but not the other can't contribute to an
    agreement count. Rows where either side's value for `verdict_column` is
    blank/missing are also skipped (an uncoded row hasn't been rated yet).
    """
    original_by_id = _index_by_claim_id(original_rows)
    recoded_by_id = _index_by_claim_id(recoded_rows)
    shared_ids = sorted(set(original_by_id) & set(recoded_by_id))

    pairs: list[tuple[str, str]] = []
    for claim_id in shared_ids:
        label1 = (original_by_id[claim_id].get(verdict_column) or "").strip()
        label2 = (recoded_by_id[claim_id].get(verdict_column) or "").strip()
        if not label1 or not label2:
            continue
        pairs.append((label1, label2))
    return pairs


def cohens_kappa(pairs: Iterable[tuple[str, str]]) -> float:
    """Compute Cohen's kappa for a sequence of (rater1_label, rater2_label) pairs.

        kappa = (p_o - p_e) / (1 - p_e)

    `p_o` (observed agreement) is the fraction of pairs where both raters
    gave the same label.

    `p_e` (chance agreement) is computed from each rater's marginal label
    distribution over the `n` pairs:

        p_e = sum over categories c of (count_rater1[c] / n) * (count_rater2[c] / n)

    i.e. the probability the two raters would land on the same category by
    chance, if each rater independently drew from their own observed
    distribution of labels.

    Returns `float('nan')` -- not 0, not a crash -- if kappa is undefined:
    either there are no pairs at all (`n == 0`), or every pair falls into a
    single, identical category for both raters (`p_e == 1`, so `1 - p_e`,
    the denominator, is zero). The second case is a real degenerate case,
    not an error: when there's no variation across categories, there's
    nothing for kappa to distinguish from chance.
    """
    pairs = list(pairs)
    n = len(pairs)
    if n == 0:
        return float("nan")

    rater1_counts: dict[str, int] = {}
    rater2_counts: dict[str, int] = {}
    agreements = 0
    for label1, label2 in pairs:
        rater1_counts[label1] = rater1_counts.get(label1, 0) + 1
        rater2_counts[label2] = rater2_counts.get(label2, 0) + 1
        if label1 == label2:
            agreements += 1

    p_o = agreements / n

    categories = set(rater1_counts) | set(rater2_counts)
    p_e = sum(
        (rater1_counts.get(category, 0) / n) * (rater2_counts.get(category, 0) / n)
        for category in categories
    )

    denominator = 1 - p_e
    if denominator == 0:
        return float("nan")

    return (p_o - p_e) / denominator


def compute_kappa(original_csv_path: Path | str, recoded_csv_path: Path | str) -> dict[str, float]:
    """Compute Cohen's kappa for each of D1/D2/D3 between two coded CSVs.

    `original_csv_path` and `recoded_csv_path` point to two CSVs describing
    the same set of ledger rows (matched by `claim_id`), each carrying
    `d1_verdict`/`d2_verdict`/`d3_verdict` columns per `ledger/schema.md`.

    Returns `{"d1": float, "d2": float, "d3": float}`. Any value may be
    `float('nan')` if that condition's kappa is undefined for the given
    inputs (see `cohens_kappa`) -- callers should check with `math.isnan`
    rather than assume a numeric result.
    """
    original_rows = read_claims(Path(original_csv_path))
    recoded_rows = read_claims(Path(recoded_csv_path))

    result: dict[str, float] = {}
    for condition, column in VERDICT_COLUMNS.items():
        pairs = matched_label_pairs(original_rows, recoded_rows, column)
        result[condition] = cohens_kappa(pairs)
    return result


def _fmt(value: float) -> str:
    if math.isnan(value):
        return "undefined (NaN) -- no rated pairs, or no variation across raters/categories to measure"
    return f"{value:.4f}"


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: python scripts/kappa.py <original_csv> <recoded_csv>")
        return 1

    original_path = Path(argv[1])
    recoded_path = Path(argv[2])

    if not original_path.exists():
        print(f"Original CSV not found: {original_path}")
        return 1
    if not recoded_path.exists():
        print(f"Recoded CSV not found: {recoded_path}")
        return 1

    kappas = compute_kappa(original_path, recoded_path)

    print(f"Cohen's kappa -- original: {original_path}, recoded: {recoded_path}")
    print(f"D1 (opacity) kappa:             {_fmt(kappas['d1'])}")
    print(f"D2 (unfaithfulness) kappa:      {_fmt(kappas['d2'])}")
    print(f"D3 (adversarial forgery) kappa: {_fmt(kappas['d3'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
