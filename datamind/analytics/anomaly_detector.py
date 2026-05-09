"""Anomaly detection module."""

from __future__ import annotations

import pandas as pd
from sklearn.ensemble import IsolationForest


class AnomalyDetector:
    """Detect anomalies using either z-score heuristic or isolation forest."""

    @staticmethod
    def zscore_anomalies(df: pd.DataFrame, threshold: float = 3.0) -> dict:
        """Flag records whose max absolute z-score exceeds threshold."""
        numeric = df.select_dtypes(include=["number"])
        if numeric.empty:
            return {"anomaly_indices": [], "count": 0}

        mean = numeric.mean()
        std = numeric.std().replace(0, 1)
        zscores = ((numeric - mean) / std).abs()
        mask = zscores.max(axis=1) > threshold
        indices = [int(i) for i in df.index[mask]]
        return {"anomaly_indices": indices, "count": len(indices)}

    @staticmethod
    def isolation_forest_anomalies(df: pd.DataFrame, contamination: float = 0.05) -> dict:
        """Run isolation forest and return anomaly indices."""
        numeric = df.select_dtypes(include=["number"])
        if numeric.empty:
            return {"anomaly_indices": [], "count": 0}

        model = IsolationForest(contamination=contamination, random_state=42)
        labels = model.fit_predict(numeric)
        anomalies = [int(i) for i, label in zip(df.index, labels) if label == -1]
        return {"anomaly_indices": anomalies, "count": len(anomalies)}
