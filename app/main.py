import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

load_dotenv()

app_name = os.getenv("APP_NAME", "DataMind")
app = FastAPI(title=app_name)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": f"{app_name} is running"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    project_root = str(Path(__file__).resolve().parent.parent)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    uvicorn.run(
        "app.main:app",
        host=os.getenv("HOST", "127.0.0.1"),
        port=int(os.getenv("PORT", "8000")),
        reload=os.getenv("RELOAD", "false").lower() == "true",
    )
