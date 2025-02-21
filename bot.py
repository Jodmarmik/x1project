import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Get bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Bot token is missing. Set BOT_TOKEN in environment variables.")

# /start command: Just a welcome message.
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "Hello! I'm your spam bot. Use /spam <count> <message> to spam a message."
    )

# /spam command: Expects at least 2 arguments. First is count, rest is message.
async def spam(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /spam <count> <message>")
        return

    try:
        count = int(context.args[0])
    except ValueError:
        await update.message.reply_text("The first argument must be an integer for count.")
        return

    # Optionally, limit the count to prevent abuse (here maximum 50)
    if count > 50:
        count = 50

    message_text = " ".join(context.args[1:])

    # Send the message count times
    for i in range(count):
        await update.message.reply_text(message_text)

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("spam", spam))
    
    # Start the bot using polling
    application.run_polling()

if __name__ == "__main__":
    main()
