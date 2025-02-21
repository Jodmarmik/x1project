import os
from fastapi import FastAPI, Request
import uvicorn
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Retrieve required environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT token is missing. Set BOT_TOKEN in environment variables.")

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
if not WEBHOOK_URL:
    raise ValueError("Webhook URL is missing. Set WEBHOOK_URL in environment variables.")

# Define the path on which Telegram will send updates
WEBHOOK_PATH = "/webhook"

# Create a FastAPI instance
app = FastAPI()

# Define command handlers for Telegram
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I'm your spam bot. Use /spam <count> <message>.")

async def spam(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /spam <count> <message>")
        return
    try:
        count = int(context.args[0])
    except ValueError:
        await update.message.reply_text("The first argument must be an integer for count.")
        return
    if count > 50:  # Limit to 50 times
        count = 50
    message_text = " ".join(context.args[1:])
    for _ in range(count):
        await update.message.reply_text(message_text)

# Build the Telegram Application
application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("spam", spam))

# FastAPI route to receive webhook updates from Telegram
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    update_data = await request.json()
    update = Update.de_json(update_data, application.bot)
    await application.process_update(update)
    return {"ok": True}

# A simple health check route
@app.get("/")
def read_root():
    return {"message": "Bot is running"}

# On startup, set the webhook for Telegram to send updates to
@app.on_event("startup")
async def on_startup():
    # Construct the full webhook URL (e.g., https://your-app.koyeb.app/webhook)
    full_webhook_url = WEBHOOK_URL.rstrip("/") + WEBHOOK_PATH
    await application.bot.set_webhook(full_webhook_url)
    print("Webhook set to:", full_webhook_url)

# On shutdown, remove the webhook (optional)
@app.on_event("shutdown")
async def on_shutdown():
    await application.bot.delete_webhook()
    print("Webhook removed")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    # Run the FastAPI server with uvicorn
    uvicorn.run("bot:app", host="0.0.0.0", port=port, reload=False)
