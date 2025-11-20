import asyncio
from flask import Flask, request
from pyrogram import Client
from pytgcalls import PyTgCalls

api_id = 123456       # ТВОИ данные!
api_hash = "ABCDEFG"  # ТВОИ данные!
your_user_id = 123456789  # Твой Telegram ID

app = Flask(__name__)

# Pyrogram
client = Client(
    "session",
    api_id=api_id,
    api_hash=api_hash
)

# TGCALLS
call = PyTgCalls(client)


@app.before_first_request
def init_telegram():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_bot())


async def start_bot():
    await client.start()
    await call.start()


@app.post("/usedesk")
def usedesk_webhook():
    data = request.json

    subject = data["ticket"]["subject"]
    ticket_id = data["ticket"]["id"]

    text = f"Новая заявка #{ticket_id}\nТема: {subject}"

    asyncio.get_event_loop().create_task(notify_and_call(text))

    return "ok"


async def notify_and_call(text):

    # Отправить сообщение
    await client.send_message(your_user_id, text)

    # Сделать звонок
    await call.join_group_call(
        chat_id=your_user_id,
        input_stream=None  # значит просто звонок без аудио
    )


if name == "__main__":
    app.run(host="0.0.0.0", port=10000)
