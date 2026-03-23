import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import asyncio
import tempfile
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi_mail import FastMail, MessageSchema, MessageType
from telegram import Bot
from telegram.error import TelegramError
from config import mail_config, settings

# ─── Хранилище chat_id (in-memory, для прода замени на Redis/DB) ──────────────
subscribed_users: set[str] = set()
polling_task: asyncio.Task | None = None


# ─── Polling loop ─────────────────────────────────────────────────────────────
async def poll_telegram():
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    offset = None
    while True:
        try:
            updates = await bot.get_updates(offset=offset, timeout=10)
            for update in updates:
                offset = update.update_id + 1
                if update.message:
                    chat_id = str(update.message.chat.id)
                    username = update.message.chat.username or "unknown"
                    subscribed_users.add(chat_id)
                    # Приветствие при первом /start
                    if update.message.text == "/start":
                        await bot.send_message(
                            chat_id=chat_id,
                            text=f"👋 Привет, @{username}! Ты подписан на уведомления от e-shop.",
                        )
        except Exception as e:
            print(f"[polling error] {e}")
        await asyncio.sleep(2)


# ─── Lifespan: запуск polling при старте приложения ───────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    global polling_task
    polling_task = asyncio.create_task(poll_telegram())
    yield
    polling_task.cancel()


app = FastAPI(title="Notification Service", lifespan=lifespan)
bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)


# ─── EMAIL ────────────────────────────────────────────────────────────────────

@app.post("/notify/email", summary="Send email with optional image")
async def send_email(
    recipient: str = Form(..., example="user@example.com"),
    subject: str = Form(..., example="Hello from e-shop"),
    body: str = Form(..., example="Your order is confirmed!"),
    image: UploadFile | None = File(default=None),
):
    attachments = [image] if image else []
    message = MessageSchema(
        subject=subject,
        recipients=[recipient],
        body=body,
        subtype=MessageType.html,
        attachments=attachments,
    )
    try:
        await FastMail(mail_config).send_message(message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Email error: {e}")
    return {"status": "sent", "recipient": recipient}


# ─── TELEGRAM: конкретный chat_id ─────────────────────────────────────────────

@app.post("/notify/telegram", summary="Send Telegram message to specific chat_id")
async def send_telegram(
    chat_id: str = Form(..., example="123456789"),
    text: str = Form(..., example="New order placed!"),
    image: UploadFile | None = File(default=None),
):
    try:
        if image:
            contents = await image.read()
            suffix = os.path.splitext(image.filename)[1]
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(contents)
                tmp_path = tmp.name
            with open(tmp_path, "rb") as photo:
                await bot.send_photo(chat_id=chat_id, photo=photo, caption=text)
            os.unlink(tmp_path)
        else:
            await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
    except TelegramError as e:
        raise HTTPException(status_code=500, detail=f"Telegram error: {e}")
    return {"status": "sent", "chat_id": chat_id}


# ─── TELEGRAM: рассылка всем подписчикам ──────────────────────────────────────

@app.post("/notify/telegram/broadcast", summary="Broadcast to all subscribed users")
async def broadcast_telegram(
    text: str = Form(..., example="🔥 Sale! 50% off today only"),
    image: UploadFile | None = File(default=None),
):
    if not subscribed_users:
        raise HTTPException(status_code=404, detail="No subscribed users yet")

    image_bytes = await image.read() if image else None
    results = {"sent": [], "failed": []}

    for chat_id in subscribed_users:
        try:
            if image_bytes:
                suffix = os.path.splitext(image.filename)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(image_bytes)
                    tmp_path = tmp.name
                with open(tmp_path, "rb") as photo:
                    await bot.send_photo(chat_id=chat_id, photo=photo, caption=text)
                os.unlink(tmp_path)
            else:
                await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
            results["sent"].append(chat_id)
        except TelegramError as e:
            results["failed"].append({"chat_id": chat_id, "error": str(e)})

    return {"status": "done", "total": len(subscribed_users), **results}


# ─── Посмотреть кто подписан ──────────────────────────────────────────────────

@app.get("/notify/telegram/subscribers", summary="List all subscribed chat_ids")
async def get_subscribers():
    return {"count": len(subscribed_users), "chat_ids": list(subscribed_users)}


@app.head("/health")
async def health_check():
    return {"status": "healthy"}