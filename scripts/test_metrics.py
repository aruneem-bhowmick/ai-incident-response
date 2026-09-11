"""Unit tests for scripts/metrics.py.

Runs against a self-contained, hand-constructed 5-row fixture -- NOT the real
`/ledger/claims.csv`, which will most likely not exist yet or be incomplete at
the time these tests are run. The fixture is written out to a temporary CSV so
the tests also exercise the real CSV-reading path (`read_claims`), not just
the in-memory metric functions.

Run with either:
    python scripts/test_metrics.py
    pytest scripts/
"""

from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

import metrics

FIELDNAMES = [
    "claim_id",
    "source_org",
    "source_url",
    "retrieval_date",
    "source_revision",
    "claim_text_paraphrased",
    "claim_type",
    "primary_channel",
    "corroborating_channels",
    "verifiability",
    "d1_verdict",
    "d1_note",
    "d2_verdict",
    "d2_note",
    "d3_verdict",
    "d3_note",
    "excerpt_available",
    "coder",
    "coding_date",
]


def _dummy_row(**overrides) -> dict:
    """A row with every column filled with an innocuous placeholder value,
    overridden by whatever the caller cares about for a given test case."""
    row = {
        "claim_id": "C000",
        "source_org": "TestOrg",
        "source_url": "https://example.invalid/source",
        "retrieval_date": "2026-09-10",
        "source_revision": "original",
        "claim_text_paraphrased": "Dummy paraphrased claim for unit test.",
        "claim_type": "T1",
        "primary_channel": "C4",
        "corroborating_channels": "",
        "verifiability": "V1",
        "d1_verdict": "SURVIVES",
        "d1_note": "",
        "d2_verdict": "SURVIVES",
        "d2_note": "",
        "d3_verdict": "SURVIVES",
        "d3_note": "",
        "excerpt_available": "FALSE",
        "coder": "test-fixture",
        "coding_date": "2026-09-10",
    }
    row.update(overrides)
    return row


# Five hand-constructed dummy rows covering (at least once each):
#   1. a T3 claim whose sole channel is C1              -> counts toward M1
#   2. a claim that SURVIVES D1
#   3. a claim that COLLAPSES under D1
#   4. a claim on an agent-writable-only channel         -> counts toward M3
#   5. a T5 claim at V3                                  -> counts toward M4
#
# Expected metrics on this fixture (worked by hand, asserted below):
#   M1 (T3, sole channel C1)            = 1/2 = 0.5   (C001 yes, C002 no -- corroborated)
#   M2 overall (SURVIVES under D1)      = 3/5 = 0.6   (C001, C003, C005 survive)
#   M2 by claim_type                    = {T1: 1.0, T3: 0.5, T5: 0.5}
#   M3 (sole substrate agent-writable)  = 2/5 = 0.4   (C001 via C1, C004 via C3)
#   M4 (T5 claims at V3)                = 1/2 = 0.5   (C004 no, C005 yes)
FIXTURE_ROWS = [
    _dummy_row(
        claim_id="C001",
        claim_type="T3",
        primary_channel="C1",
        corroborating_channels="",
        verifiability="V1",
        d1_verdict="SURVIVES",
    ),
    _dummy_row(
        claim_id="C002",
        claim_type="T3",
        primary_channel="C2",
        corroborating_channels="C1",
        verifiability="V2",
        d1_verdict="COLLAPSES",
    ),
    _dummy_row(
        claim_id="C003",
        claim_type="T1",
        primary_channel="C4",
        corroborating_channels="",
        verifiability="V1",
        d1_verdict="SURVIVES",
    ),
    _dummy_row(
        claim_id="C004",
        claim_type="T5",
        primary_channel="C3",
        corroborating_channels="",
        verifiability="V2",
        d1_verdict="COLLAPSES",
    ),
    _dummy_row(
        claim_id="C005",
        claim_type="T5",
        primary_channel="C4",
        corroborating_channels="C2",
        verifiability="V3",
        d1_verdict="SURVIVES",
    ),
]


def _write_fixture_csv(path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(FIXTURE_ROWS)


class MetricsFixtureTests(unittest.TestCase):
    """Tests that go through the real CSV file path (read_claims + compute_*)."""

    @classmethod
    def setUpClass(cls) -> None:
        cls._tmpdir = tempfile.TemporaryDirectory()
        cls.fixture_path = Path(cls._tmpdir.name) / "claims.csv"
        _write_fixture_csv(cls.fixture_path)
        cls.rows = metrics.read_claims(cls.fixture_path)

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmpdir.cleanup()

    def test_fixture_loads_all_five_rows(self) -> None:
        self.assertEqual(len(self.rows), 5)

    def test_m1_cot_monopoly(self) -> None:
        self.assertAlmostEqual(metrics.compute_m1_cot_monopoly(self.rows), 0.5)

    def test_m2_record_survival_overall(self) -> None:
        overall, _ = metrics.compute_m2_record_survival(self.rows)
        self.assertAlmostEqual(overall, 0.6)

    def test_m2_record_survival_by_claim_type(self) -> None:
        _, by_type = metrics.compute_m2_record_survival(self.rows)
        self.assertAlmostEqual(by_type["T1"], 1.0)
        self.assertAlmostEqual(by_type["T3"], 0.5)
        self.assertAlmostEqual(by_type["T5"], 0.5)
        self.assertEqual(set(by_type.keys()), {"T1", "T3", "T5"})

    def test_m3_forgery_exposure(self) -> None:
        self.assertAlmostEqual(metrics.compute_m3_forgery_exposure(self.rows), 0.4)

    def test_m4_assurance_gap(self) -> None:
        self.assertAlmostEqual(metrics.compute_m4_assurance_gap(self.rows), 0.5)

    def test_compute_all_matches_individual_metrics(self) -> None:
        result = metrics.compute_all(self.rows)
        self.assertEqual(result["n_claims"], 5)
        self.assertAlmostEqual(result["M1_cot_monopoly"], 0.5)
        self.assertAlmostEqual(result["M2_record_survival_overall"], 0.6)
        self.assertAlmostEqual(result["M3_forgery_exposure"], 0.4)
        self.assertAlmostEqual(result["M4_assurance_gap"], 0.5)


class ChannelParsingTests(unittest.TestCase):
    """Tests for the corroborating-channels parsing helpers in isolation."""

    def test_empty_string_means_no_corroboration(self) -> None:
        self.assertTrue(metrics.has_no_corroboration({"corroborating_channels": ""}))

    def test_none_token_means_no_corroboration(self) -> None:
        for token in ("NONE", "none", "N/A", "n/a", "NA"):
            with self.subTest(token=token):
                self.assertTrue(
                    metrics.has_no_corroboration({"corroborating_channels": token})
                )

    def test_missing_key_means_no_corroboration(self) -> None:
        self.assertTrue(metrics.has_no_corroboration({}))

    def test_semicolon_separated_channels_are_corroboration(self) -> None:
        self.assertFalse(
            metrics.has_no_corroboration({"corroborating_channels": "C4;C6"})
        )

    def test_comma_separated_channels_are_corroboration(self) -> None:
        self.assertFalse(
            metrics.has_no_corroboration({"corroborating_channels": "C4,C6"})
        )


class EmptyLedgerTests(unittest.TestCase):
    """The script must degrade gracefully when the real ledger is missing/empty,
    since /ledger/claims.csv will most likely not exist yet or be incomplete."""

    def test_read_claims_on_missing_file_returns_empty_list(self) -> None:
        missing_path = Path(tempfile.gettempdir()) / "does-not-exist-claims.csv"
        self.assertFalse(missing_path.exists())
        self.assertEqual(metrics.read_claims(missing_path), [])

    def test_metrics_on_empty_rows_are_none_not_crashes(self) -> None:
        empty_rows: list[dict] = []
        self.assertIsNone(metrics.compute_m1_cot_monopoly(empty_rows))
        overall, by_type = metrics.compute_m2_record_survival(empty_rows)
        self.assertIsNone(overall)
        self.assertEqual(by_type, {})
        self.assertIsNone(metrics.compute_m3_forgery_exposure(empty_rows))
        self.assertIsNone(metrics.compute_m4_assurance_gap(empty_rows))


if __name__ == "__main__":
    unittest.main()
