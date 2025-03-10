import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Get the bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi")

# Main function to start the bot
async def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    await application.initialize()
    await application.start()
    await application.bot.delete_webhook(drop_pending_updates=True)
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
