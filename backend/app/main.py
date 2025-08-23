from fastapi import FastAPI
from app.models import SafetyScore, SafetyFactors
from app.config import settings

app = FastAPI(title=settings.APP_NAME)

@app.get("/health")
def health():
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.ENV}

@app.get("/safety-score", response_model=SafetyScore)
def get_safety_score():
    # dummy data for smoke test
    return SafetyScore(
        score=75,
        band="safe",
        factors=SafetyFactors(crime=40, lighting=20)
    )
