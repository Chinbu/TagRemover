import os
import logging
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiogram.utils.executor import start_webhook

# Load environment variables
TOKEN = os.getenv("BOT_TOKEN")  # Bot Token from BotFather
CHANNEL_ID = os.getenv("-1002135826586")  # Channel ID (with -100 prefix)
WEBHOOK_URL = os.getenv("https://app.koyeb.com/")  # Koyeb webhook URL

# Initialize bot and dispatcher
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# Flask app for webhook
app = Flask(__name__)

# Logging
logging.basicConfig(level=logging.INFO)

# Webhook settings
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_URL_FULL = f"{WEBHOOK_URL}{WEBHOOK_PATH}"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 8080))  # Koyeb default port

@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    """Handle incoming webhook updates"""
    update = Update(**request.get_json())
    await dp.process_update(update)
    return "OK", 200

@dp.message_handler(content_types=types.ContentType.ANY)
async def forward_without_tag(message: types.Message):
    """Forwards messages to the channel without forward tag"""
    try:
        # Handle different content types
        if message.text:
            await bot.send_message(CHANNEL_ID, message.text)
        elif message.photo:
            await bot.send_photo(CHANNEL_ID, message.photo[-1].file_id, caption=message.caption)
        elif message.video:
            await bot.send_video(CHANNEL_ID, message.video.file_id, caption=message.caption)
        elif message.document:
            await bot.send_document(CHANNEL_ID, message.document.file_id, caption=message.caption)
        elif message.audio:
            await bot.send_audio(CHANNEL_ID, message.audio.file_id, caption=message.caption)
        elif message.voice:
            await bot.send_voice(CHANNEL_ID, message.voice.file_id, caption=message.caption)
        elif message.sticker:
            await bot.send_sticker(CHANNEL_ID, message.sticker.file_id)
        
        await message.reply("✅ Forwarded to channel without tag!")
    except Exception as e:
        logging.error(f"Error forwarding message: {e}")
        await message.reply("❌ Error forwarding message!")

async def on_startup(dp):
    """Set webhook on bot startup"""
    await bot.set_webhook(WEBHOOK_URL_FULL)
    logging.info(f"Webhook set: {WEBHOOK_URL_FULL}")

async def on_shutdown(dp):
    """Delete webhook on shutdown"""
    await bot.delete_webhook()

if __name__ == "__main__":
    from aiogram import executor
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
