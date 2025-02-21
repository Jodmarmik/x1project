import os
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Configure logging to help with debugging.
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get the bot token from the environment variable.
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Bot token is missing. Set BOT_TOKEN in environment variables.")

# /start command: Sends a welcome message.
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I'm your spam bot. Use /spam <count> <message>.")

# /spam command: Spams the specified message a given number of times.
async def spam(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /spam <count> <message>")
        return

    try:
        count = int(context.args[0])
    except ValueError:
        await update.message.reply_text("The count must be an integer.")
        return

    # Optionally, limit the count to prevent abuse.
    if count > 50:
        count = 50

    message_text = " ".join(context.args[1:])
    logger.info("Spamming message '%s' %d times", message_text, count)

    for i in range(count):
        await update.message.reply_text(message_text)
        # Add a slight delay between messages to avoid rate limits.
        await asyncio.sleep(0.5)

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Register command handlers.
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("spam", spam))

    # Start the bot using polling.
    application.run_polling()

if __name__ == "__main__":
    main()
