"""Preprocessing utilities for tabular data."""

from __future__ import annotations

import pandas as pd


class Preprocessor:
    """Run basic cleaning and feature preparation steps."""

    @staticmethod
    def clean(df: pd.DataFrame) -> pd.DataFrame:
        """Drop duplicates and normalize column names."""
        clean_df = df.copy()
        clean_df.columns = [str(col).strip().lower().replace(" ", "_") for col in clean_df.columns]
        clean_df = clean_df.drop_duplicates().reset_index(drop=True)
        return clean_df

    @staticmethod
    def normalize_numeric(df: pd.DataFrame) -> pd.DataFrame:
        """Min-max normalize numeric columns to [0, 1]."""
        normalized = df.copy()
        numeric_cols = normalized.select_dtypes(include=["number"]).columns
        for col in numeric_cols:
            min_val = normalized[col].min()
            max_val = normalized[col].max()
            if pd.isna(min_val) or pd.isna(max_val) or min_val == max_val:
                normalized[col] = 0.0
            else:
                normalized[col] = (normalized[col] - min_val) / (max_val - min_val)
        return normalized
