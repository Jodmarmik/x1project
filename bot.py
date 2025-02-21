from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import os

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I'm running on Koyeb 🚀")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

if __name__ == "__main__":
    app.run_polling()
