import os
from typing import Optional
import httpx

class TelegramClient:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.base = f"https://api.telegram.org/bot{self.bot_token}"

    async def send_message(self, chat_id: str, text: str) -> dict:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.post(f"{self.base}/sendMessage", json={"chat_id": chat_id, "text": text})
            r.raise_for_status()
            return r.json()

    async def get_updates(self) -> dict:
        async with httpx.AsyncClient(timeout=15) as client:
            r = await client.get(f"{self.base}/getUpdates")
            r.raise_for_status()
            return r.json()
