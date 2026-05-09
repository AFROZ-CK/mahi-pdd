"""Missing data detection and imputation helpers."""

from __future__ import annotations

import pandas as pd


class GapHandler:
    """Handle missing values with simple deterministic strategies."""

    SUPPORTED_METHODS = {"mean", "median", "ffill", "bfill", "interpolate"}

    @staticmethod
    def missing_report(df: pd.DataFrame) -> dict:
        """Report missing-value counts and percentage."""
        total = len(df) or 1
        missing = df.isna().sum()
        return {
            "count": {str(k): int(v) for k, v in missing.to_dict().items()},
            "percent": {str(k): float((v / total) * 100) for k, v in missing.to_dict().items()},
        }

    @staticmethod
    def impute(df: pd.DataFrame, method: str = "mean") -> pd.DataFrame:
        """Impute missing values using the requested method."""
        if method not in GapHandler.SUPPORTED_METHODS:
            raise ValueError(f"Unsupported imputation method: {method}")

        result = df.copy()
        if method == "mean":
            numeric_cols = result.select_dtypes(include=["number"]).columns
            for col in numeric_cols:
                result[col] = result[col].fillna(result[col].mean())
            return result.fillna("unknown")

        if method == "median":
            numeric_cols = result.select_dtypes(include=["number"]).columns
            for col in numeric_cols:
                result[col] = result[col].fillna(result[col].median())
            return result.fillna("unknown")

        if method == "ffill":
            return result.ffill().fillna("unknown")
        if method == "bfill":
            return result.bfill().fillna("unknown")
        return result.interpolate(method="linear", limit_direction="both").fillna("unknown")
