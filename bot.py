import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Replace with your bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me any forwarded message, and I will remove the forward tag.")

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

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.FORWARDED, remove_forward_tag))

    # Start the bot
    app.run_polling()
