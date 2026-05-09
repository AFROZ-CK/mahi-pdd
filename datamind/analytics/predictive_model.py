"""Predictive modeling module for training and inference."""

from __future__ import annotations

from dataclasses import dataclass
import math

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


@dataclass
class ModelMetrics:
    """Basic training metrics for quick model quality checks."""

    mae: float
    mse: float
    r2: float


class PredictiveModel:
    """Wrapper around common regression models used by DataMind."""

    def __init__(self) -> None:
        self._model = None
        self._feature_columns: list[str] = []

    def train(self, df: pd.DataFrame, target_column: str, algorithm: str = "linear_regression") -> dict:
        """Train a model and return summary metrics."""
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' not found")

        model_df = df.copy()
        model_df = pd.get_dummies(model_df, drop_first=True)
        encoded_target = [col for col in model_df.columns if col == target_column or col.startswith(f"{target_column}_")]
        if encoded_target and target_column not in model_df.columns:
            raise ValueError("Target column must be numeric for this baseline API")

        X = model_df.drop(columns=[target_column])
        y = model_df[target_column]
        if X.empty:
            raise ValueError("At least one feature column is required")

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        if algorithm == "random_forest":
            self._model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            self._model = LinearRegression()

        self._model.fit(X_train, y_train)
        predictions = self._model.predict(X_test)
        self._feature_columns = list(X.columns)

        r2_value = float(r2_score(y_test, predictions))
        if not math.isfinite(r2_value):
            r2_value = 0.0

        metrics = ModelMetrics(
            mae=float(mean_absolute_error(y_test, predictions)),
            mse=float(mean_squared_error(y_test, predictions)),
            r2=r2_value,
        )
        return {
            "algorithm": algorithm,
            "target_column": target_column,
            "feature_count": len(self._feature_columns),
            "metrics": metrics.__dict__,
        }

    def predict(self, records: list[dict]) -> list[float]:
        """Generate predictions for a list of feature records."""
        if self._model is None:
            raise ValueError("Model has not been trained")

        input_df = pd.DataFrame(records)
        input_df = pd.get_dummies(input_df, drop_first=True)
        input_df = input_df.reindex(columns=self._feature_columns, fill_value=0)
        values = self._model.predict(input_df)
        return [float(v) for v in values]
