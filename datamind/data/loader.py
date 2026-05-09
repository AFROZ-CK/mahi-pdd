"""Data loading helpers for DataMind."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import BinaryIO

import pandas as pd


class DataLoader:
    """Load tabular data from filesystem paths or in-memory uploads."""

    @staticmethod
    def load_file(file_path: str) -> pd.DataFrame:
        """Load a supported file format from disk."""
        path = Path(file_path)
        suffix = path.suffix.lower()
        if suffix == ".csv":
            return pd.read_csv(path)
        if suffix in {".xlsx", ".xls"}:
            return pd.read_excel(path)
        if suffix == ".json":
            return pd.read_json(path)
        raise ValueError(f"Unsupported file extension: {suffix}")

    @staticmethod
    def load_upload(filename: str, content: bytes | BinaryIO) -> pd.DataFrame:
        """Load a supported file format from uploaded bytes."""
        raw = content.read() if hasattr(content, "read") else content
        suffix = Path(filename).suffix.lower()
        if suffix == ".csv":
            return pd.read_csv(BytesIO(raw))
        if suffix in {".xlsx", ".xls"}:
            return pd.read_excel(BytesIO(raw))
        if suffix == ".json":
            return pd.read_json(BytesIO(raw))
        raise ValueError(f"Unsupported uploaded file extension: {suffix}")

    @staticmethod
    def info(df: pd.DataFrame) -> dict:
        """Return standard information used by API responses."""
        return {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "column_names": [str(col) for col in df.columns.tolist()],
            "missing_values": {str(k): int(v) for k, v in df.isna().sum().to_dict().items()},
        }
