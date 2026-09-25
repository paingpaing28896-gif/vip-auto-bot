import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "မင်္ဂလာပါ 👋\n"
        "VIP / Membership အကြောင်း သိလိုတာ မေးနိုင်ပါတယ်။"
    )

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""

    await update.message.reply_text(
        f"သင့်မေးခွန်းကို လက်ခံရရှိပါတယ်။\n\n"
        f"မေးထားတာ — {text}\n\n"
        "AI Auto Reply ကို မကြာခင် ချိတ်ဆက်ပေးပါမယ်။"
    )

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is not configured")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)
    )

    print("Bot is running...")
    app.run_polling()

if name == "main":
    main()
