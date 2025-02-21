import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Get token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Bot token is missing. Set BOT_TOKEN in environment variables.")

# Create Updater
updater = Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Sample start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I am your bot.")

dispatcher.add_handler(CommandHandler("start", start))

# Start polling
updater.start_polling()
updater.idle()
