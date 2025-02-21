import os
import asyncio
import logging
from fastapi import FastAPI
import uvicorn
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Retrieve the bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Bot token is missing. Set BOT_TOKEN in environment variables.")

# Create a FastAPI instance for a simple health-check endpoint
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bot is running"}

# /start command: Sends a welcome message.
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Hello! I'm your spam bot. Use /spam <count> <message> to spam a message."
    )

# /spam command: Spams the specified message 'count' times.
async def spam(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /spam <count> <message>")
        return

    try:
        count = int(context.args[0])
    except ValueError:
        await update.message.reply_text("The first argument must be an integer for count.")
        return

    if count > 50:  # Limit spam to a maximum of 50 times to prevent abuse.
        count = 50

    message_text = " ".join(context.args[1:])
    logger.info("Spamming '%s' %d times", message_text, count)
    for i in range(count):
        await update.message.reply_text(message_text)
        # Optional: you can add a slight delay between messages:
        # await asyncio.sleep(0.5)

async def main():
    # Build the Telegram Application
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("spam", spam))

    # Initialize and start the Telegram bot
    await application.initialize()
    await application.start()
    logger.info("Bot is starting with PTB v20 ...")
    
    # Start polling in an asyncio Task (non-blocking)
    polling_task = asyncio.create_task(application.updater.start_polling())
    
    # Configure and start the FastAPI server with uvicorn asynchronously
    port = int(os.environ.get("PORT", 8000))
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info", loop="asyncio")
    server = uvicorn.Server(config)
    uvicorn_task = asyncio.create_task(server.serve())
    
    # Run both tasks concurrently. They should run forever.
    await asyncio.gather(polling_task, uvicorn_task)

if __name__ == "__main__":
    asyncio.run(main())
