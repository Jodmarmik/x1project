from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import os

# Environment variable se bot token lena
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Bot token is missing. Set BOT_TOKEN in environment variables.")

# Naya method use karein
app = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! I am your bot.")

app.add_handler(CommandHandler("start", start))

# Bot ko run karne ke liye
if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
