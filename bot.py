import os
import asyncio
import logging
from fastapi import FastAPI
import uvicorn
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configure logging for debugging
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
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your raid/spam bot. Use /spam and /raid commands!")

# /spam command: Spams the specified message count times.
async def spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = update.message.text.split()[1:]  # Extract command arguments
    if len(args) < 2:
        await update.message.reply_text("Usage: /spam <count> <message>")
        return

    try:
        count = int(args[0])
    except ValueError:
        await update.message.reply_text("The first argument must be an integer for count.")
        return

    count = min(count, 50)  # Limit to 50 times to prevent abuse
    message_text = " ".join(args[1:])
    
    for _ in range(count):
        await update.message.reply_text(message_text)
        await asyncio.sleep(0.5)

# /raid command: When used in reply to a user's message,
# the bot sends a series of raid messages addressing that user by their first name.
async def raid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a user's message to raid them.")
        return

    args = update.message.text.split()[1:]  # Extract command arguments
    if len(args) < 1:
        await update.message.reply_text("Usage: /raid <count> (used as a reply)")
        return

    try:
        count = int(args[0])
    except ValueError:
        await update.message.reply_text("The count must be an integer.")
        return

    count = min(count, 10)  # Limit to 10 messages
    target_user = update.message.reply_to_message.from_user
    first_name = target_user.first_name if target_user.first_name else "there"

    raid_messages = [
        f"{first_name}, brace yourself! The raid is coming!",
        f"Raid alert! {first_name}, prepare for action!",
        f"{first_name}, you're being raided! Get ready!",
        f"{first_name}, the raid has begun!",
        f"Hold on, {first_name}! Here comes the raid!"
    ]

    for i in range(count):
        await update.message.reply_text(raid_messages[i % len(raid_messages)])
        await asyncio.sleep(0.5)

# Main function to start bot and FastAPI server
async def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("spam", spam))
    application.add_handler(CommandHandler("raid", raid))

    await application.initialize()
    await application.start()
    logger.info("Bot is running...")

    # Delete any existing webhook to prevent conflicts if using polling.
    await application.bot.delete_webhook(drop_pending_updates=True)

    # Start polling in a separate task
    polling_task = asyncio.create_task(application.run_polling())

    # Start FastAPI server in another task
    port = int(os.environ.get("PORT", 8000))
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info", loop="asyncio")
    server = uvicorn.Server(config)
    uvicorn_task = asyncio.create_task(server.serve())

    await asyncio.gather(polling_task, uvicorn_task)

if __name__ == "__main__":
    asyncio.run(main())
