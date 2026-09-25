import os
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# Railway Variables ထဲကနေ Key တွေကို ယူပါမယ်
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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
        # OpenAI chat completion API
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # သုံးစွဲစရိတ် သက်သာပြီး အဆင်ပြေသည့် Model
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful Telegram bot. "
                        "Answer the user's questions clearly and naturally in Burmese. "
                        "If the user asks about VIP or Membership, answer helpfully."
                    )
                },
                {"role": "user", "content": text}
            ]
        )

        reply = response.choices[0].message.content
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


if __name__ == "__main__":
    main()
