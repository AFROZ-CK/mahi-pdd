"""Decision engine that converts analytics results into recommendations."""

from __future__ import annotations


class DecisionEngine:
    """Produce action-oriented recommendations based on incoming signals."""

    @staticmethod
    def recommend(signal: dict) -> dict:
        """Generate recommendation and priority from numeric health signals."""
        anomaly_score = float(signal.get("anomaly_score", 0.0))
        prediction_confidence = float(signal.get("prediction_confidence", 0.0))
        missing_ratio = float(signal.get("missing_ratio", 0.0))

        if anomaly_score > 0.8:
            return {"priority": "high", "recommendation": "Investigate anomalies immediately and trigger alert."}
        if missing_ratio > 0.2:
            return {"priority": "medium", "recommendation": "Improve source data completeness before critical decisions."}
        if prediction_confidence < 0.6:
            return {"priority": "medium", "recommendation": "Retrain model with additional representative data."}
        return {"priority": "normal", "recommendation": "System stable; continue monitoring in real time."}
