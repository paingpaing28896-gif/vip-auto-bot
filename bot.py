import os
from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")  # သင့်ရဲ့ Telegram User ID (မထည့်လည်း ရပါသည်)

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not configured")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is not configured")

client = OpenAI(api_key=OPENAI_API_KEY)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "မင်္ဂလာပါ 👋\n"
        "VIP Channel ဝင်ရောက်လိုပါက သို့မဟုတ် သိလိုသည်များရှိပါက မေးမြန်းနိုင်ပါတယ်။\n\n"
        "💎 VIP ဝင်ကြေး - ၅,၀၀၀ ကျပ်"
    )


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly customer service AI bot for a Telegram VIP Channel.\n\n"
                        "Rules & Information:\n"
                        "- VIP Entry Fee: 5,000 MMK (၅,၀၀၀ ကျပ်).\n"
                        "- Payment Account Details: KBZPay / WavePay 09XXXXXXXXX (Name: U XX).\n"
                        "- Instructions for User:\n"
                        "  1. Transfer 5,000 Kyats to the given account.\n"
                        "  2. Send the payment receipt (screenshot) directly into this chat.\n"
                        "  3. Inform them that once the screenshot is received, the Admin will check it when online and send them the VIP Channel Link.\n\n"
                        "- Response Style:\n"
                        "  - Friendly, clear, and polite in Burmese language.\n"
                        "  - Answer any questions naturally and guide them step-by-step if they want to join VIP."
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
            "AI နဲ့ ချိတ်ဆက်ရာမှာ အခက်အခဲရှိနေပါတယ်။ ခဏနေပြီး ပြန်စမ်းကြည့်ပါ။"
        )


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    သုံးစွဲသူမှ ငွေလွှဲပြေစာ (Photo) ပို့လိုက်သည့်အခါ အလုပ်လုပ်မည့် စနစ်
    """
    user = update.message.from_user
    username = f"@{user.username}" if user.username else user.full_name

    # ၁။ သုံးစွဲသူဆီ အလိုအလျောက် ပြန်စာ ပို့မည်
    await update.message.reply_text(
        "ငွေလွှဲပြေစာ ရရှိပါပြီ ကျေးဇူးတင်ပါတယ်။ 🙏\n"
        "Admin လိုင်းတက်လာပါက ပြေစာကို စစ်ဆေးပြီး VIP Channel Link ပေးပို့ပေးပါမည်။ ခဏစောင့်ဆိုင်းပေးပါ။"
    )

    # ၂။ Admin ဆီသို့ ငွေလွှဲပြေစာပုံ နှင့် သုံးစွဲသူအချက်အလက် တိုက်ရိုက် ပို့ပေးမည် (ADMIN_CHAT_ID ရှိပါက)
    if ADMIN_CHAT_ID:
        try:
            caption_text = (
                f"📩 **VIP ငွေလွှဲပြေစာ အသစ် ရရှိပါသည်။**\n\n"
                f"👤 သုံးစွဲသူ: {username}\n"
                f"🆔 User ID: `{user.id}`"
            )
            await context.bot.send_photo(
                chat_id=ADMIN_CHAT_ID,
                photo=update.message.photo[-1].file_id,
                caption=caption_text,
                parse_mode="Markdown"
            )
        except Exception as e:
            print("Failed to send photo to admin:", e)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    # စာလာပို့ပါက AI အကြောင်းပြန်ရန်
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    # ငွေလွှဲပြေစာ (ပုံ) လာပို့ပါက အကြောင်းပြန်ရန်
    app.add_handler(MessageHandler(filters.PHOTO, photo_handler))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
