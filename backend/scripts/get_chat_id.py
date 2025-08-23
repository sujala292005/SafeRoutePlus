import asyncio
from app.config import settings
from app.telegram import TelegramClient

async def main():
    if not settings.TELEGRAM_BOT_TOKEN:
        print("Missing TELEGRAM-BOT-TOKEN in Key Vault.")
        return
    tg = TelegramClient(settings.TELEGRAM_BOT_TOKEN)
    updates = await tg.get_updates()
    # Find a chat id from the latest messages
    chats = []
    for item in updates.get("result", []):
        msg = item.get("message") or item.get("edited_message") or {}
        chat = msg.get("chat", {})
        if chat.get("id"):
            chats.append((chat.get("type"), chat.get("title") or chat.get("username") or chat.get("first_name"), chat.get("id")))
    if not chats:
        print("No chats found. Send a message to your bot in Telegram, then run again.")
    else:
        print("Candidate chat IDs:")
        for c in chats:
            print(c)

asyncio.run(main())
