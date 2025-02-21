import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Dispatcher, CommandHandler, CallbackContext

# Create a Flask app
app = Flask(__name__)

# Get configuration from environment variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PORT = int(os.environ.get("PORT", 8000))

# Set up the Telegram Bot and Dispatcher
bot = Bot(BOT_TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)

# Define a command handler function
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I'm running on Koyeb 🚀")

# Add the command handler to the dispatcher
dispatcher.add_handler(CommandHandler("start", start))

# Endpoint to receive webhook updates from Telegram
@app.route("/", methods=["POST"])
def webhook():
    # Parse the incoming update from Telegram
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

# A simple health-check endpoint
@app.route("/", methods=["GET"])
def index():
    return "Bot is running", 200

if __name__ == '__main__':
    # Optionally, if you want to set the webhook automatically, uncomment and adjust the line below:
    # bot.set_webhook("https://your-koyeb-app-url/")
    app.run(host="0.0.0.0", port=PORT)
