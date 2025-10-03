import os, requests, html
from django.conf import settings

BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
CHAT_ID = settings.TELEGRAM_CHAT_ID
API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def send_message(text: str) -> None:
    if not BOT_TOKEN or not CHAT_ID:
        return
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    try:
        # timeout=(connect, read)
        r = requests.post(API, data=payload, timeout=(3, 5))
        r.raise_for_status()
    except requests.RequestException:
        # не роняем поток. логируем на stderr
        import logging
        logging.exception("Telegram send failed")
