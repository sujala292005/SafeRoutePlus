from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from app.models import SafetyScore, SafetyFactors
from app.config import settings
from app.telegram import TelegramClient

app = FastAPI(title=settings.APP_NAME)


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.APP_NAME, "env": settings.ENV}


@app.get("/safety-score", response_model=SafetyScore)
def get_safety_score():
    return SafetyScore(
        score=75,
        band="safe",
        factors=SafetyFactors(crime=40, lighting=20)
    )


# ------- Telegram ping & SOS ---------
@app.get("/telegram/ping")
async def telegram_ping():
    if not settings.TELEGRAM_BOT_TOKEN:
        raise HTTPException(status_code=500, detail="Telegram bot token missing. Put it in Key Vault as TELEGRAM-BOT-TOKEN.")
    tg = TelegramClient(settings.TELEGRAM_BOT_TOKEN)
    return {"ok": True}


class SosPayload(BaseModel):
    name: str
    phone: Optional[str] = None
    lat: float = Field(..., description="Latitude")
    lon: float = Field(..., description="Longitude")
    address: Optional[str] = None
    extra: Optional[str] = None


@app.post("/sos")
async def sos(payload: SosPayload):
    """
    Sends an SOS to your Telegram chat with location & details.
    """
    if not settings.TELEGRAM_BOT_TOKEN:
        raise HTTPException(status_code=500, detail="Telegram bot token missing in Key Vault.")
    if not settings.TELEGRAM_CHAT_ID:
        raise HTTPException(status_code=500, detail="TELEGRAM-CHAT-ID missing. Set it after you fetch it in step 4.")

    tg = TelegramClient(settings.TELEGRAM_BOT_TOKEN)
    message = (
        f"🚨 SOS from {payload.name}\n"
        f"Phone: {payload.phone or '-'}\n"
        f"Location: {payload.lat}, {payload.lon}\n"
        f"Address: {payload.address or '-'}\n"
        f"Extra: {payload.extra or '-'}\n"
        f"Maps: https://maps.google.com/?q={payload.lat},{payload.lon}"
    )
    result = await tg.send_message(settings.TELEGRAM_CHAT_ID, message)
    return {"sent": True, "telegram_response": result}
