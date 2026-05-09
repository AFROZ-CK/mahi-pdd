"""Basic smoke tests for DataMind modules."""

import unittest

import pandas as pd

from datamind.data.gap_handler import GapHandler
from datamind.data.preprocessor import Preprocessor
from datamind.realtime.decision_engine import DecisionEngine


class DataMindModuleTests(unittest.TestCase):
    """Smoke tests to validate core module behavior."""

    def test_gap_handler_mean_imputation(self) -> None:
        df = pd.DataFrame({"value": [1.0, None, 3.0]})
        imputed = GapHandler.impute(df, method="mean")
        self.assertFalse(imputed["value"].isna().any())


    def test_gap_handler_invalid_method_raises(self) -> None:
        df = pd.DataFrame({"value": [1.0, None]})
        with self.assertRaises(ValueError):
            GapHandler.impute(df, method="unsupported")

    def test_preprocessor_cleans_columns(self) -> None:
        df = pd.DataFrame({" Sales Value ": [1, 2]})
        cleaned = Preprocessor.clean(df)
        self.assertIn("sales_value", cleaned.columns)

    def test_decision_engine_high_priority(self) -> None:
        decision = DecisionEngine.recommend({"anomaly_score": 0.95})
        self.assertEqual(decision["priority"], "high")


if __name__ == "__main__":
    unittest.main()
