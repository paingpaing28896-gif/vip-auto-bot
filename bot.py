import os
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("8884700528:AAFC3ReuEta_V7iSqcT9t8cZsmPP4WOe_So")
OPENAI_API_KEY = os.getenv("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")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not configured")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not configured")

client = OpenAI(api_key=OPENAI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "မင်္ဂလာပါ 👋\n"
        "VIP / Membership အကြောင်း သိလိုတာ မေးနိုင်ပါတယ်။"
    )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""

    try:
        response = client.responses.create(
            model="gpt-5.6-luna",
            instructions=(
                "You are a helpful Telegram bot. "
                "Answer the user's questions clearly and naturally in Burmese. "
                "If the user asks about VIP or Membership, answer helpfully."
            ),
            input=text
        )

        reply = response.output_text

        await update.message.reply_text(reply)

    except Exception as e:
        print("OpenAI Error:", e)

        await update.message.reply_text(
            "AI နဲ့ ချိတ်ဆက်ရာမှာ အခက်အခဲရှိနေပါတယ်။ "
            "ခဏနေပြီး ပြန်စမ်းကြည့်ပါ။"
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)
    )

    print("Bot is running...")
    app.run_polling()


if name == "main":
    main()
