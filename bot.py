import os
import threading
import asyncio
from fastapi import FastAPI
import uvicorn
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Retrieve the bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Bot token is missing. Set BOT_TOKEN in environment variables.")

# Create a FastAPI instance for a simple health-check endpoint
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Bot is running"}

# Define an asynchronous command handler for /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I'm running on Koyeb.")

# Function to run the Telegram bot (polling mode)
def run_bot():
    # Create and set a new event loop for this thread.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    print("Bot is starting with PTB v20 ...")
    # Disable signal handlers by setting allowed_signals to an empty tuple.
    application.run_polling(allowed_signals=())

if __name__ == "__main__":
    # Run the bot in a separate thread so that uvicorn can serve HTTP requests concurrently
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Get the port from environment variables, defaulting to 8000
    port = int(os.environ.get("PORT", 8000))
    # Pass the FastAPI application as an import string to uvicorn
    uvicorn.run("bot:app", host="0.0.0.0", port=port, reload=False)
