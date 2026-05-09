# DataMind

DataMind is an intelligent predictive analytics platform designed to bridge data gaps and enable real-time decision-making.

## Features

- Data ingestion for CSV, Excel, and JSON files
- Preprocessing and normalization utilities
- Missing-data imputation pipeline
- Predictive analytics (linear regression and random forest)
- Anomaly detection (z-score and isolation forest)
- Real-time stream processing and recommendation engine
- FastAPI REST endpoints with interactive docs

## Project Structure

```text
.
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   └── requirements.txt
├── datamind/
│   ├── analytics/
│   │   ├── anomaly_detector.py
│   │   ├── metrics.py
│   │   └── predictive_model.py
│   ├── data/
│   │   ├── gap_handler.py
│   │   ├── loader.py
│   │   └── preprocessor.py
│   ├── realtime/
│   │   ├── decision_engine.py
│   │   └── stream_processor.py
│   └── utils/
│       └── logger.py
├── sample_data/
│   └── dataset.csv
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Requirements

- Python 3.9+

Install dependencies:

```bash
pip install -r app/requirements.txt
```

## Run the application

```bash
python app/main.py
```

API base URL: `http://localhost:8000`

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Data

- `POST /api/data/upload` (multipart upload)
- `POST /api/data/impute` (JSON records + imputation method)

### Analytics

- `POST /api/analytics/summary`
- `POST /api/analytics/predict/train`
- `POST /api/analytics/predict`

### Real-time

- `POST /api/realtime/recommendation`

## Quick cURL Examples

```bash
curl -X POST http://localhost:8000/api/analytics/summary \
  -H "Content-Type: application/json" \
  -d '{"records":[{"sales":120,"inventory":50},{"sales":140,"inventory":40}]}'

curl -X POST http://localhost:8000/api/realtime/recommendation \
  -H "Content-Type: application/json" \
  -d '{"signal":{"anomaly_score":0.2,"prediction_confidence":0.9,"missing_ratio":0.05}}'
```

## Docker

Build and run with Docker Compose:

```bash
docker compose up --build
```

## Notes

- The app is pip-install and runtime ready via `python app/main.py`.
- `sample_data/dataset.csv` is included for quick tests.
