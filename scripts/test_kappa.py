"""Unit tests for scripts/kappa.py.

Runs against self-contained, hand-constructed fixtures -- NOT the real
`/ledger/claims.csv` or any actual blind-recode CSV, which don't exist yet at
this phase (this task has no dependency on the ledger's content; see
`kappa.py`'s docstring). The CSV-fixture tests below write two small CSVs to
a temp directory so they also exercise the real file-reading path
(`read_claims` + `matched_label_pairs`), not just the in-memory formula.

Run with either:
    python scripts/test_kappa.py
    pytest scripts/
"""

from __future__ import annotations

import csv
import math
import tempfile
import unittest
from pathlib import Path

import kappa

FIELDNAMES = ["claim_id", "d1_verdict", "d2_verdict", "d3_verdict"]
# Only claim_id + the three verdict columns are needed to exercise kappa.py
# (unlike the full ledger schema that scripts/metrics.py's fixture uses) --
# kappa.py never reads any other column.


# ---------------------------------------------------------------------------
# Twelve-row hand-built fixture, one row per claim_id, independently
# patterned per condition so each condition demonstrates a different, fully
# hand-worked kappa value from the *same* pair of CSVs:
#
#   D1 -- perfect agreement across all 12 rows, split 4/4/4 across the three
#         verdict categories (SURVIVES/DEGRADED/COLLAPSES). Because rater1
#         and rater2 agree on every row, p_o = 1. Because the categories are
#         NOT all identical (there's real variation, so p_e < 1), kappa
#         reduces to (1 - p_e) / (1 - p_e) = 1.0 exactly. (A trap worth
#         naming: perfect agreement alone doesn't guarantee kappa == 1 --
#         if every row were the *same* single category on both sides, p_e
#         would also be 1 and kappa would be undefined; see D1_ALL_SAME
#         below for that degenerate case tested directly against the
#         formula.)
#
#   D2 -- confusion matrix (rater1 rows x rater2 columns), using only
#         SURVIVES/DEGRADED:
#                        rater2=SURVIVES   rater2=DEGRADED
#           rater1=SURVIVES     6                 1
#           rater1=DEGRADED     2                 3
#         n = 6+1+2+3 = 12.
#         Observed agreement:  p_o = (6+3)/12 = 9/12 = 3/4.
#         Rater1 marginals:    SURVIVES=7, DEGRADED=5   (7+5=12)
#         Rater2 marginals:    SURVIVES=8, DEGRADED=4   (8+4=12)
#         Chance agreement:    p_e = (7/12)*(8/12) + (5/12)*(4/12)
#                                   = 56/144 + 20/144 = 76/144 = 19/36
#         kappa = (p_o - p_e) / (1 - p_e)
#               = (3/4 - 19/36) / (1 - 19/36)
#               = (27/36 - 19/36) / (17/36)
#               = (8/36) / (17/36)
#               = 8/17
#               ~= 0.4705882352941176
#
#   D3 -- confusion matrix, again SURVIVES/DEGRADED only, but symmetric
#         chance-level agreement:
#                        rater2=SURVIVES   rater2=DEGRADED
#           rater1=SURVIVES     3                 3
#           rater1=DEGRADED     3                 3
#         n = 12. p_o = (3+3)/12 = 6/12 = 1/2.
#         Rater1 marginals: SURVIVES=6, DEGRADED=6. Rater2 marginals: SURVIVES=6, DEGRADED=6.
#         p_e = (6/12)*(6/12) + (6/12)*(6/12) = 1/4 + 1/4 = 1/2.
#         kappa = (1/2 - 1/2) / (1 - 1/2) = 0 / (1/2) = 0.0 exactly --
#         agreement is exactly what chance alone would predict.
# ---------------------------------------------------------------------------

# claim_id -> (d1_rater1, d1_rater2, d2_rater1, d2_rater2, d3_rater1, d3_rater2)
_ROWS = {
    "C001": ("SURVIVES", "SURVIVES", "SURVIVES", "SURVIVES", "SURVIVES", "SURVIVES"),
    "C002": ("SURVIVES", "SURVIVES", "SURVIVES", "SURVIVES", "SURVIVES", "SURVIVES"),
    "C003": ("SURVIVES", "SURVIVES", "SURVIVES", "SURVIVES", "SURVIVES", "SURVIVES"),
    "C004": ("SURVIVES", "SURVIVES", "SURVIVES", "SURVIVES", "SURVIVES", "DEGRADED"),
    "C005": ("DEGRADED", "DEGRADED", "SURVIVES", "SURVIVES", "SURVIVES", "DEGRADED"),
    "C006": ("DEGRADED", "DEGRADED", "SURVIVES", "SURVIVES", "SURVIVES", "DEGRADED"),
    "C007": ("DEGRADED", "DEGRADED", "SURVIVES", "DEGRADED", "DEGRADED", "SURVIVES"),
    "C008": ("DEGRADED", "DEGRADED", "DEGRADED", "SURVIVES", "DEGRADED", "SURVIVES"),
    "C009": ("COLLAPSES", "COLLAPSES", "DEGRADED", "SURVIVES", "DEGRADED", "SURVIVES"),
    "C010": ("COLLAPSES", "COLLAPSES", "DEGRADED", "DEGRADED", "DEGRADED", "DEGRADED"),
    "C011": ("COLLAPSES", "COLLAPSES", "DEGRADED", "DEGRADED", "DEGRADED", "DEGRADED"),
    "C012": ("COLLAPSES", "COLLAPSES", "DEGRADED", "DEGRADED", "DEGRADED", "DEGRADED"),
}

EXPECTED_D1_KAPPA = 1.0
EXPECTED_D2_KAPPA = 8 / 17
EXPECTED_D3_KAPPA = 0.0


def _original_rows() -> list[dict]:
    return [
        {
            "claim_id": claim_id,
            "d1_verdict": values[0],
            "d2_verdict": values[2],
            "d3_verdict": values[4],
        }
        for claim_id, values in _ROWS.items()
    ]


def _recoded_rows() -> list[dict]:
    return [
        {
            "claim_id": claim_id,
            "d1_verdict": values[1],
            "d2_verdict": values[3],
            "d3_verdict": values[5],
        }
        for claim_id, values in _ROWS.items()
    ]


def _write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


class KappaCsvFixtureTests(unittest.TestCase):
    """Tests that go through the real CSV file path (read_claims + compute_kappa)."""

    @classmethod
    def setUpClass(cls) -> None:
        cls._tmpdir = tempfile.TemporaryDirectory()
        tmpdir = Path(cls._tmpdir.name)
        cls.original_path = tmpdir / "original.csv"
        cls.recoded_path = tmpdir / "recoded.csv"
        _write_csv(cls.original_path, _original_rows())
        _write_csv(cls.recoded_path, _recoded_rows())
        cls.result = kappa.compute_kappa(cls.original_path, cls.recoded_path)

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmpdir.cleanup()

    def test_returns_all_three_conditions(self) -> None:
        self.assertEqual(set(self.result.keys()), {"d1", "d2", "d3"})

    def test_d1_perfect_agreement_is_exactly_one(self) -> None:
        self.assertEqual(self.result["d1"], EXPECTED_D1_KAPPA)

    def test_d2_partial_disagreement_matches_hand_worked_fraction(self) -> None:
        self.assertAlmostEqual(self.result["d2"], EXPECTED_D2_KAPPA, places=9)

    def test_d3_chance_level_agreement_is_exactly_zero(self) -> None:
        self.assertAlmostEqual(self.result["d3"], EXPECTED_D3_KAPPA, places=9)


class CohensKappaFormulaTests(unittest.TestCase):
    """Tests against the formula directly, isolated from CSV I/O."""

    def test_perfect_agreement_with_category_variation_is_one(self) -> None:
        pairs = (
            [("SURVIVES", "SURVIVES")] * 4
            + [("DEGRADED", "DEGRADED")] * 4
            + [("COLLAPSES", "COLLAPSES")] * 4
        )
        self.assertEqual(kappa.cohens_kappa(pairs), 1.0)

    def test_partial_disagreement_matches_hand_worked_fraction(self) -> None:
        pairs = (
            [("SURVIVES", "SURVIVES")] * 6
            + [("SURVIVES", "DEGRADED")] * 1
            + [("DEGRADED", "SURVIVES")] * 2
            + [("DEGRADED", "DEGRADED")] * 3
        )
        self.assertAlmostEqual(kappa.cohens_kappa(pairs), 8 / 17, places=9)

    def test_chance_level_agreement_is_zero(self) -> None:
        pairs = (
            [("SURVIVES", "SURVIVES")] * 3
            + [("SURVIVES", "DEGRADED")] * 3
            + [("DEGRADED", "SURVIVES")] * 3
            + [("DEGRADED", "DEGRADED")] * 3
        )
        self.assertAlmostEqual(kappa.cohens_kappa(pairs), 0.0, places=9)

    def test_all_pairs_same_single_category_is_nan_not_one_or_zero(self) -> None:
        # Every row is SURVIVES for both raters: p_o = 1 and p_e = 1 (a
        # single category with 100% share on both sides), so (1 - p_e) is
        # zero and kappa is genuinely undefined -- not the same thing as
        # "perfect agreement" in the D1 sense above, because there's no
        # variation for the coefficient to measure.
        pairs = [("SURVIVES", "SURVIVES")] * 5
        result = kappa.cohens_kappa(pairs)
        self.assertTrue(math.isnan(result))

    def test_no_pairs_is_nan(self) -> None:
        result = kappa.cohens_kappa([])
        self.assertTrue(math.isnan(result))


class MatchedLabelPairsTests(unittest.TestCase):
    """Tests for the claim_id-matching / blank-skipping helper in isolation."""

    def test_only_shared_claim_ids_are_paired(self) -> None:
        original = [
            {"claim_id": "C001", "d1_verdict": "SURVIVES"},
            {"claim_id": "C002", "d1_verdict": "DEGRADED"},
        ]
        recoded = [
            {"claim_id": "C001", "d1_verdict": "SURVIVES"},
            {"claim_id": "C999", "d1_verdict": "COLLAPSES"},
        ]
        pairs = kappa.matched_label_pairs(original, recoded, "d1_verdict")
        self.assertEqual(pairs, [("SURVIVES", "SURVIVES")])

    def test_blank_verdict_on_either_side_is_skipped(self) -> None:
        original = [
            {"claim_id": "C001", "d1_verdict": "SURVIVES"},
            {"claim_id": "C002", "d1_verdict": ""},
            {"claim_id": "C003", "d1_verdict": "DEGRADED"},
        ]
        recoded = [
            {"claim_id": "C001", "d1_verdict": "SURVIVES"},
            {"claim_id": "C002", "d1_verdict": "DEGRADED"},
            {"claim_id": "C003", "d1_verdict": ""},
        ]
        pairs = kappa.matched_label_pairs(original, recoded, "d1_verdict")
        self.assertEqual(pairs, [("SURVIVES", "SURVIVES")])


class EmptyInputTests(unittest.TestCase):
    """The script must degrade gracefully -- report NaN, not crash -- when
    an input CSV is missing, mirroring scripts/metrics.py's handling of a
    missing ledger."""

    def test_read_claims_on_missing_file_returns_empty_list(self) -> None:
        missing_path = Path(tempfile.gettempdir()) / "does-not-exist-recode.csv"
        self.assertFalse(missing_path.exists())
        self.assertEqual(kappa.read_claims(missing_path), [])

    def test_compute_kappa_on_missing_files_is_nan_for_all_conditions(self) -> None:
        missing_original = Path(tempfile.gettempdir()) / "does-not-exist-original.csv"
        missing_recoded = Path(tempfile.gettempdir()) / "does-not-exist-recoded.csv"
        result = kappa.compute_kappa(missing_original, missing_recoded)
        self.assertEqual(set(result.keys()), {"d1", "d2", "d3"})
        for value in result.values():
            self.assertTrue(math.isnan(value))


if __name__ == "__main__":
    unittest.main()
