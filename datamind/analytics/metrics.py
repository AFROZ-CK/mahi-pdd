"""Analytics metrics for descriptive and quality insights."""

from __future__ import annotations

import pandas as pd


class Metrics:
    """Compute common analytics and data-quality metrics."""

    @staticmethod
    def summary(df: pd.DataFrame) -> dict:
        """Return high-level statistical summary for API responses."""
        numeric = df.select_dtypes(include=["number"])
        correlation = numeric.corr().fillna(0).to_dict() if not numeric.empty else {}
        return {
            "shape": {"rows": int(df.shape[0]), "columns": int(df.shape[1])},
            "missing_ratio": float(df.isna().sum().sum() / (df.size if df.size else 1)),
            "numeric_columns": list(numeric.columns),
            "describe": numeric.describe().fillna(0).to_dict() if not numeric.empty else {},
            "correlation": correlation,
        }
