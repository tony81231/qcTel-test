import time
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7800921682:AAHZESvnObcLLFIIMgdwpEK4FTK5ZutLYVs"
QC_SERVER_URL = "https://qctel-test.onrender.com"  # Replace after deployment

# Dummy whitelist
AUTHORIZED_USERS = {"testuser"}
active_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please enter your username:")

async def handle_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.text.strip().lower()
    if username in AUTHORIZED_USERS:
        token = str(uuid.uuid4())
        expires_at = time.time() + 600
        active_sessions[token] = expires_at
        link = f"{QC_SERVER_URL}/qc/session/{token}"
        await update.message.reply_text(f"✅ Here’s your upload link (valid 10 min):\n{link}")
    else:
        await update.message.reply_text("❌ Not authorized.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_username))
    app.run_polling()
