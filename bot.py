import os
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

async def main():
    # Build the Telegram Application
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    # Initialize and start the bot without blocking the event loop
    await application.initialize()
    await application.start()
    
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
