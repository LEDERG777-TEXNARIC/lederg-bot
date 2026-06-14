import asyncio
import os
import re
from urllib.parse import urlparse, parse_qs
import aiohttp
from flask import Flask
from threading import Thread

TOKEN = "8939573062:AAHknUKGdCbDAuFeff_778rEuFru4n6iXbU"
PROXY_LIST_URL = "https://raw.githubusercontent.com/SoliSpirit/mtproto/master/all_proxies.txt"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/"

# --- Flask app for keeping the bot alive ---
web_app = Flask(__name__)

@web_app.route('/')
def index():
    return "Bot is running!"

@web_app.route('/health')
def health_check():
    return "OK", 200

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    web_app.run(host="0.0.0.0", port=port)

# --- Telegram bot logic ---
async def fetch_proxies() -> list:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(PROXY_LIST_URL, timeout=10) as resp:
                if resp.status != 200:
                    return []
                text = await resp.text()
                return [line.strip() for line in text.split("\n") if line.strip()]
        except Exception:
            return []

async def send_message(chat_id: int, text: str) -> None:
    async with aiohttp.ClientSession() as session:
        payload = {"chat_id": chat_id, "text": text}
        try:
            await session.post(TELEGRAM_API_URL + "sendMessage", json=payload)
        except Exception:
            pass

async def handle_update(update: dict) -> None:
    if "message" not in update:
        return
    message = update["message"]
    chat_id = message.get("chat", {}).get("id")
    if not chat_id:
        return

    proxies = await fetch_proxies()
    if not proxies:
        await send_message(chat_id, "❌ Не удалось получить список прокси. Попробуйте позже.")
        return

    valid_proxies = []
    for raw_link in proxies[:10]:
        match = re.search(r"tg://proxy\?(.+)", raw_link)
        if match:
            params = parse_qs(match.group(1))
            server = params.get("server", [None])[0]
            port = params.get("port", [None])[0]
            secret = params.get("secret", [None])[0]
            if server and port and secret:
                valid_proxies.append(raw_link)

    if not valid_proxies:
        await send_message(chat_id, "⚠️ В списке нет корректных ссылок на прокси.")
        return

    message_text = (
        "✅ *Актуальные MTProto прокси (первые 5):*\n\n" +
        "\n\n".join(valid_proxies[:5]) +
        "\n\n💡 *Использование:* скопируйте ссылку целиком и откройте её в браузере."
    )
    await send_message(chat_id, message_text)

async def poll_updates() -> None:
    offset = 0
    print("Бот запущен и ждёт команды...")
    while True:
        async with aiohttp.ClientSession() as session:
            params = {"offset": offset, "timeout": 30}
            try:
                async with session.get(TELEGRAM_API_URL + "getUpdates", params=params) as resp:
                    if resp.status != 200:
                        await asyncio.sleep(3)
                        continue
                    data = await resp.json()
                    if not data.get("ok"):
                        await asyncio.sleep(3)
                        continue
                    updates = data.get("result", [])
                    for update in updates:
                        await handle_update(update)
                        offset = update["update_id"] + 1
            except Exception:
                await asyncio.sleep(3)

if __name__ == "__main__":
    # Запускаем Flask в отдельном потоке
    Thread(target=run_flask).start()
    # Запускаем основную логику бота
    asyncio.run(poll_updates())
