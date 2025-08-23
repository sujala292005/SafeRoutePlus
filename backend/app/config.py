import os
from pydantic_settings import BaseSettings
from typing import Optional

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


class Settings(BaseSettings):
    APP_NAME: str = "SafeRoute+"
    ENV: str = "dev"

    # Fallbacks if Key Vault not available
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None

    class Config:
        env_file = ".env"


def _try_load_from_key_vault() -> dict:
    """
    Loads secrets from Key Vault 'saferoutepluskvci' if available.
    Works locally with 'az login' via DefaultAzureCredential.
    """
    kv_name = "saferoutepluskvci"
    url = f"https://{kv_name}.vault.azure.net/"
    secrets = {}

    try:
        cred = DefaultAzureCredential(exclude_interactive_browser_credential=False)
        client = SecretClient(vault_url=url, credential=cred)
        for key in ["TELEGRAM-BOT-TOKEN", "TELEGRAM-CHAT-ID"]:
            try:
                secret = client.get_secret(key)
                if key == "TELEGRAM-BOT-TOKEN":
                    secrets["TELEGRAM_BOT_TOKEN"] = secret.value
                elif key == "TELEGRAM-CHAT-ID":
                    secrets["TELEGRAM_CHAT_ID"] = secret.value
            except Exception:
                # secret might not exist yet, that's okay
                pass
    except Exception:
        # No Key Vault / no permission / offline — just skip
        pass

    return secrets


kv_overrides = _try_load_from_key_vault()
settings = Settings(**kv_overrides)

