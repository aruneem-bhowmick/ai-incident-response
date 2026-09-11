"""Compute Project Warrant's four headline metrics (M1-M4), plus the
supplementary M5 metric, from the claim ledger.

Per R-03, headline metrics must be computed by script, never by hand. This
module is that script. It reads `/ledger/claims.csv` (schema documented in
`/ledger/schema.md`) and computes:

    M1 - CoT monopoly.
        Share of T3 claims whose only channel (primary channel, no
        corroborating channels) is C1.

    M2 - Record survival under opacity.
        Share of all claims scoring SURVIVES under d1_verdict, reported
        overall and split by claim_type.

    M3 - Forgery exposure.
        Share of claims whose sole substrate (primary channel, no
        corroborating channels) is an agent-writable channel (C1/C2/C3).

    M4 - Assurance gap.
        Share of T5 claims at verifiability == V3.

    M5 - Broad channel fragility (SUPPLEMENTARY, not one of the plan's
    original four metrics).
        Uses the codebook's own broader fragility ranking from
        `/docs/codebook.md` §3.1 (C1 > C2 > C3 > C6 > C5 > C4, most fragile
        to least) rather than the narrower agent-writable-only set M1/M3
        use. Reports two shares of all 116 claims:
          (a) primary_channel in {C1, C2, C3, C6}, regardless of
              corroboration;
          (b) primary_channel in {C1, C2, C3, C6} AND no corroborating
              channel at all.

The controlled vocabularies for `claim_type`, channel codes, and `verifiability`
are defined authoritatively in `/docs/codebook.md`; this script only needs to
know the specific codes referenced directly in the metric definitions above
(T3, T5, C1, C2, C3, C6, V3), which are given in the sprint plan and codebook
and reproduced here as constants.

Usage:
    python scripts/metrics.py [path/to/claims.csv]

If no path is given, defaults to `ledger/claims.csv` resolved relative to the
repository root (i.e. the parent of this script's directory). If the file is
missing or empty, this prints a clear message and each metric is reported as
unavailable rather than crashing -- the real ledger is populated by a separate
task and may not exist yet.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path
from typing import Iterable, Optional

# Channel codes treated as "agent-writable" for the forgery-exposure metric
# (M3). C1 is additionally the specific channel checked by the CoT-monopoly
# metric (M1).
AGENT_WRITABLE_CHANNELS = {"C1", "C2", "C3"}

# Channel codes treated as "fragile" under the codebook's own broader
# fragility ranking (`docs/codebook.md` §3.1: C1 > C2 > C3 > C6 > C5 > C4,
# most fragile to least). This is the set used by the supplementary M5
# metric -- it additionally includes C6 (lab assertion with no stated
# substrate), which M1/M3 as originally scoped do not count.
BROAD_FRAGILE_CHANNELS = {"C1", "C2", "C3", "C6"}

COT_CHANNEL = "C1"
COT_MONOPOLY_CLAIM_TYPE = "T3"
ASSURANCE_GAP_CLAIM_TYPE = "T5"
ASSURANCE_GAP_VERIFIABILITY = "V3"
SURVIVES = "SURVIVES"

# Values in `corroborating_channels` (after stripping) that mean "none",
# beyond an outright empty string.
_NO_CORROBORATION_TOKENS = {"", "NONE", "N/A", "NA"}

_SPLIT_RE = re.compile(r"[;,]")


def _split_channels(raw: Optional[str]) -> list[str]:
    """Split a corroborating-channels cell into a list of channel codes.

    Accepts semicolon- or comma-separated values defensively (schema.md
    specifies semicolons); blank cells and common "none" spellings yield an
    empty list.
    """
    if raw is None:
        return []
    stripped = raw.strip()
    if stripped.upper() in _NO_CORROBORATION_TOKENS:
        return []
    return [part.strip() for part in _SPLIT_RE.split(stripped) if part.strip()]


def has_no_corroboration(row: dict) -> bool:
    """True if a row's primary channel is its sole substrate (no corroborating channels)."""
    return len(_split_channels(row.get("corroborating_channels"))) == 0


def read_claims(path: Path) -> list[dict]:
    """Read the claim ledger CSV into a list of dict rows.

    Returns an empty list if the file does not exist or has no data rows.
    Raises nothing on a missing file -- callers should check for an empty
    result and report accordingly, since a missing/incomplete ledger is an
    expected state early in the project.
    """
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def _safe_ratio(numerator: int, denominator: int) -> Optional[float]:
    if denominator == 0:
        return None
    return numerator / denominator


def compute_m1_cot_monopoly(rows: Iterable[dict]) -> Optional[float]:
    """M1 - CoT monopoly: share of T3 claims whose sole channel is C1."""
    t3_rows = [r for r in rows if r.get("claim_type") == COT_MONOPOLY_CLAIM_TYPE]
    numerator = sum(
        1
        for r in t3_rows
        if r.get("primary_channel") == COT_CHANNEL and has_no_corroboration(r)
    )
    return _safe_ratio(numerator, len(t3_rows))


def compute_m2_record_survival(
    rows: Iterable[dict],
) -> tuple[Optional[float], dict[str, Optional[float]]]:
    """M2 - Record survival under opacity: overall share and share by claim_type."""
    rows = list(rows)
    overall_numerator = sum(1 for r in rows if r.get("d1_verdict") == SURVIVES)
    overall = _safe_ratio(overall_numerator, len(rows))

    by_type: dict[str, Optional[float]] = {}
    claim_types = sorted({r.get("claim_type", "") for r in rows if r.get("claim_type")})
    for claim_type in claim_types:
        type_rows = [r for r in rows if r.get("claim_type") == claim_type]
        type_numerator = sum(1 for r in type_rows if r.get("d1_verdict") == SURVIVES)
        by_type[claim_type] = _safe_ratio(type_numerator, len(type_rows))

    return overall, by_type


def compute_m3_forgery_exposure(rows: Iterable[dict]) -> Optional[float]:
    """M3 - Forgery exposure: share of all claims whose sole substrate is agent-writable."""
    rows = list(rows)
    numerator = sum(
        1
        for r in rows
        if has_no_corroboration(r) and r.get("primary_channel") in AGENT_WRITABLE_CHANNELS
    )
    return _safe_ratio(numerator, len(rows))


def compute_m4_assurance_gap(rows: Iterable[dict]) -> Optional[float]:
    """M4 - Assurance gap: share of T5 claims at verifiability == V3."""
    t5_rows = [r for r in rows if r.get("claim_type") == ASSURANCE_GAP_CLAIM_TYPE]
    numerator = sum(
        1 for r in t5_rows if r.get("verifiability") == ASSURANCE_GAP_VERIFIABILITY
    )
    return _safe_ratio(numerator, len(t5_rows))


def compute_m5_broad_fragility(
    rows: Iterable[dict],
) -> tuple[Optional[float], Optional[float]]:
    """M5 - Broad channel fragility (SUPPLEMENTARY, not one of the plan's
    original four metrics).

    Uses the codebook's own broader fragility ranking (`docs/codebook.md`
    §3.1: C1 > C2 > C3 > C6 > C5 > C4) rather than the narrower
    agent-writable-only set M1/M3 use (C1/C2/C3). Returns a pair:

        (share_fragile, share_fragile_and_uncorroborated)

    where `share_fragile` is the share of all claims whose primary_channel
    is in {C1, C2, C3, C6} regardless of corroboration, and
    `share_fragile_and_uncorroborated` is the share of all claims whose
    primary_channel is in {C1, C2, C3, C6} AND has no corroborating channel
    at all.
    """
    rows = list(rows)
    fragile_numerator = sum(
        1 for r in rows if r.get("primary_channel") in BROAD_FRAGILE_CHANNELS
    )
    fragile_uncorroborated_numerator = sum(
        1
        for r in rows
        if r.get("primary_channel") in BROAD_FRAGILE_CHANNELS and has_no_corroboration(r)
    )
    denominator = len(rows)
    return (
        _safe_ratio(fragile_numerator, denominator),
        _safe_ratio(fragile_uncorroborated_numerator, denominator),
    )


def compute_all(rows: Iterable[dict]) -> dict:
    """Compute all four headline metrics and the supplementary M5 metric,
    returning them all in one dict."""
    rows = list(rows)
    m2_overall, m2_by_type = compute_m2_record_survival(rows)
    m5_fragile, m5_fragile_uncorroborated = compute_m5_broad_fragility(rows)
    return {
        "n_claims": len(rows),
        "M1_cot_monopoly": compute_m1_cot_monopoly(rows),
        "M2_record_survival_overall": m2_overall,
        "M2_record_survival_by_claim_type": m2_by_type,
        "M3_forgery_exposure": compute_m3_forgery_exposure(rows),
        "M4_assurance_gap": compute_m4_assurance_gap(rows),
        "M5_broad_fragility": m5_fragile,
        "M5_broad_fragility_uncorroborated": m5_fragile_uncorroborated,
    }


def _fmt(value: Optional[float]) -> str:
    if value is None:
        return "N/A (no claims in denominator)"
    return f"{value:.1%} ({value:.4f})"


def _default_ledger_path() -> Path:
    repo_root = Path(__file__).resolve().parent.parent
    return repo_root / "ledger" / "claims.csv"


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else _default_ledger_path()
    rows = read_claims(path)

    if not rows:
        print(f"No claim rows found at {path}.")
        print(
            "The real ledger may not exist yet or may be empty -- this is "
            "expected before the ledger-building task (DL-1) completes. "
            "Run `python scripts/test_metrics.py` to verify metric logic "
            "against the unit-test fixture instead."
        )
        return 0

    metrics = compute_all(rows)
    print(f"Claims loaded: {metrics['n_claims']} (from {path})")
    print(f"M1 - CoT monopoly (T3 claims, sole channel C1):        {_fmt(metrics['M1_cot_monopoly'])}")
    print(f"M2 - Record survival under opacity (overall):          {_fmt(metrics['M2_record_survival_overall'])}")
    print("M2 - Record survival under opacity (by claim_type):")
    for claim_type, value in metrics["M2_record_survival_by_claim_type"].items():
        print(f"    {claim_type}: {_fmt(value)}")
    print(f"M3 - Forgery exposure (sole substrate agent-writable): {_fmt(metrics['M3_forgery_exposure'])}")
    print(f"M4 - Assurance gap (T5 claims at V3):                  {_fmt(metrics['M4_assurance_gap'])}")
    print("M5 - Broad channel fragility (SUPPLEMENTARY, not one of the plan's original four):")
    print(f"    Primary channel in {{C1,C2,C3,C6}} (any corroboration):        {_fmt(metrics['M5_broad_fragility'])}")
    print(f"    Primary channel in {{C1,C2,C3,C6}} AND no corroboration:       {_fmt(metrics['M5_broad_fragility_uncorroborated'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
