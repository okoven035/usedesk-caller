import asyncio
from flask import Flask, request
from telethon import TelegramClient
from pytgcalls import PyTgCalls
from pytgcalls.types.input_phone_call import InputPhoneCall

app = Flask(__name__)

api_id = 123456      # <-- Вставьте свой api_id
api_hash = "ABCDEF"  # <-- Ваш api_hash
your_user_id = 123456789  # <-- Ваш Telegram user_id

client = TelegramClient("session/session", api_id, api_hash)
call_client = PyTgCalls(client)

@app.before_first_request
def init_telegram():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.start())
    loop.run_until_complete(call_client.start())

@app.post("/usedesk")
def usedesk_webhook():
    data = request.json

    subject = data["ticket"]["subject"]
    ticket_id = data["ticket"]["id"]

    text = f"Новая заявка #{ticket_id}\nТема: {subject}"

    asyncio.get_event_loop().create_task(notify_and_call(text))

    return "ok"

async def notify_and_call(text):
    await client.send_message(your_user_id, text)
    await call_client.join(InputPhoneCall(your_user_id))

if name == "__main__":
    app.run(host="0.0.0.0", port=10000)
