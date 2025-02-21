import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# 1. Retrieve the bot token from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Bot token is missing. Set BOT_TOKEN in environment variables.")

# 2. Define a simple start command handler
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hello! I'm running on the new PTB v20.")

def main():
    # 3. Create the Application (replaces Updater)
    app = Application.builder().token(BOT_TOKEN).build()

    # 4. Add a command handler
    app.add_handler(CommandHandler("start", start))

    # 5. Run the bot in polling mode
    print("Bot is starting with PTB v20 ...")
    app.run_polling()

# 6. Entry point
if __name__ == "__main__":
    main()
