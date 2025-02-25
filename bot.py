import os
import logging
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.types import Update
from aiogram.utils.executor import start_webhook

# Load environment variables
TOKEN = os.getenv("BOT_TOKEN")  # Get bot token from environment
TARGET_CHAT_ID = os.getenv("4732667353")  # Get target chat ID
WEBHOOK_URL = os.getenv("https://app.koyeb.com/")  # Set your webhook URL (e.g., Koyeb domain)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

# Flask app for webhook
app = Flask(__name__)

# Logging
logging.basicConfig(level=logging.INFO)

# Webhook settings
WEBHOOK_PATH = f"/{TOKEN}"
WEBHOOK_HOST = WEBHOOK_URL
WEBHOOK_URL_FULL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 8080))  # Set to 8080 for Koyeb

@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    """Handle incoming webhook updates"""
    update = Update(**request.get_json())
    await dp.process_update(update)
    return "OK", 200

@dp.message_handler(content_types=types.ContentType.ANY)
async def forward_without_tag(message: types.Message):
    """Removes forward tags and forwards messages."""
    if message.forward_from or message.forward_from_chat:
        await message.copy_to(chat_id=TARGET_CHAT_ID)  # Copies without forward tag
        await message.reply("✅ Forwarded without tag!")
    else:
        await message.reply("❌ This message has no forward tag.")

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
