"""FastAPI entry point for the DataMind predictive analytics platform."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pandas as pd
import uvicorn
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config import settings
from datamind.analytics.anomaly_detector import AnomalyDetector
from datamind.analytics.metrics import Metrics
from datamind.analytics.predictive_model import PredictiveModel
from datamind.data.gap_handler import GapHandler
from datamind.data.loader import DataLoader
from datamind.data.preprocessor import Preprocessor
from datamind.realtime.decision_engine import DecisionEngine
from datamind.realtime.stream_processor import StreamProcessor
from datamind.utils.logger import configure_logging

configure_logging(settings.log_level)

app = FastAPI(
    title="DataMind",
    description="Intelligent predictive analytics platform for bridging data gaps and real-time decisions.",
    version="1.0.0",
)

model_service = PredictiveModel()
stream_processor = StreamProcessor()


class RecordsPayload(BaseModel):
    """Payload containing records and optional processing parameters."""

    records: list[dict[str, Any]] = Field(default_factory=list)


class ImputePayload(RecordsPayload):
    """Payload for imputation requests."""

    method: str = "mean"


class TrainPayload(RecordsPayload):
    """Payload for model training requests."""

    target_column: str
    algorithm: str = "linear_regression"


class RecommendationPayload(BaseModel):
    """Payload for recommendation engine requests."""

    signal: dict[str, Any] = Field(default_factory=dict)


@app.get("/")
def root() -> dict:
    """Root endpoint with service description."""
    return {
        "application": "DataMind",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "upload": "/api/data/upload",
            "impute": "/api/data/impute",
            "analytics": "/api/analytics/summary",
            "train": "/api/analytics/predict/train",
            "predict": "/api/analytics/predict",
            "realtime": "/api/realtime/recommendation",
        },
    }


@app.get("/health")
def health() -> dict:
    """Health check endpoint."""
    return {"status": "ok", "environment": settings.env}


@app.post("/api/data/upload")
async def upload_data(file: UploadFile = File(...)) -> dict:
    """Upload a dataset and return profile metadata."""
    content = await file.read()
    try:
        df = DataLoader.load_upload(file.filename or "dataset.csv", content)
        df = Preprocessor.clean(df)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"message": "Data uploaded", "profile": DataLoader.info(df)}


@app.post("/api/data/impute")
def impute_data(payload: ImputePayload) -> dict:
    """Impute missing values for posted records."""
    df = pd.DataFrame(payload.records)
    if df.empty:
        raise HTTPException(status_code=400, detail="No records provided")
    try:
        imputed = GapHandler.impute(df, method=payload.method)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "method": payload.method,
        "missing_report": GapHandler.missing_report(df),
        "records": imputed.to_dict(orient="records"),
    }


@app.post("/api/analytics/summary")
def analytics_summary(payload: RecordsPayload) -> dict:
    """Return descriptive analytics and anomaly summaries."""
    df = pd.DataFrame(payload.records)
    if df.empty:
        raise HTTPException(status_code=400, detail="No records provided")

    return {
        "metrics": Metrics.summary(df),
        "anomalies": {
            "zscore": AnomalyDetector.zscore_anomalies(df),
            "isolation_forest": AnomalyDetector.isolation_forest_anomalies(df),
        },
    }


@app.post("/api/analytics/predict/train")
def train_model(payload: TrainPayload) -> dict:
    """Train predictive model from records and target column."""
    df = pd.DataFrame(payload.records)
    if df.empty:
        raise HTTPException(status_code=400, detail="No records provided")

    try:
        train_result = model_service.train(df, target_column=payload.target_column, algorithm=payload.algorithm)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {"message": "Model trained", "result": train_result}


@app.post("/api/analytics/predict")
def predict(payload: RecordsPayload) -> dict:
    """Generate predictions from trained model."""
    if not payload.records:
        raise HTTPException(status_code=400, detail="No records provided")
    try:
        predictions = model_service.predict(payload.records)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"predictions": predictions}


@app.post("/api/realtime/recommendation")
def realtime_recommendation(payload: RecommendationPayload) -> dict:
    """Process stream signal and return decision recommendation."""
    stream_stats = stream_processor.ingest(payload.signal)
    recommendation = DecisionEngine.recommend(payload.signal)
    return {"stream": stream_stats, "decision": recommendation}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=False)
