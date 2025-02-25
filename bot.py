import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from aiohttp import web

# Replace with your bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello {mention}! Send me any forwarded message, and I will remove the forward tag.")

async def remove_forward_tag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.forward_from or update.message.forward_from_chat:
        # Copy the forwarded message text
        text = update.message.text or update.message.caption
        if text:
            await update.message.reply_text(text)
        else:
            await update.message.reply_text("The forwarded message has no text content.")
    else:
        await update.message.reply_text("This message is not forwarded.")

async def health_check(request):
    return web.Response(text="Bot is running!")

if __name__ == "__main__":
    # Start the Telegram bot
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.FORWARDED, remove_forward_tag))

    # Start the bot in polling mode
    app.run_polling()

    # Start a simple HTTP server on port 8080
    http_app = web.Application()
    http_app.router.add_get("/", health_check)
    web.run_app(http_app, port=8080)
