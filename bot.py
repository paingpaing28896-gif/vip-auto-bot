```python
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================
# BOT SETTINGS
# =========================

BOT_TOKEN = "8884700528:AAFC3ReuEta_V7iSqcT9t8cZsmPP4WOe_So"
ADMIN_CHAT_ID = 8710007891   # မင်းရဲ့ Telegram User ID

# Payment information
PAYMENT_TEXT = (
    "💳 KPay / WavePay\n"
    "(5000) Ks\n\n"
    "Name - Aung Naing Oo\n"
    "09761936714\n\n"
    "ငွေလွှဲပြေစာလေး ပို့ပေးပါ။ 📷"
)

# Admin က User ကို reply ပြန်နိုင်အောင်
# Admin ဆီပို့ထားတဲ့ message_id -> User ID
admin_messages = {}


# =========================
# START MENU
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [
            InlineKeyboardButton("1️⃣ VIP ဝင်ရန်", callback_data="vip_join")
        ],
        [
            InlineKeyboardButton(
                "2️⃣ VIP အကြောင်းကြည့်ရန်",
                callback_data="vip_info"
            )
        ],
    ]

    await update.message.reply_text(
        "မင်္ဂလာပါ 👋\n\n"
        "အောက်မှ ရွေးချယ်ပေးပါ။",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================
# VIP JOIN
# =========================

async def vip_join(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton(
                "1️⃣ VIP ဝင်ရန်",
                callback_data="payment"
            )
        ],
        [
            InlineKeyboardButton(
                "2️⃣ နောက်ပြန်ရန်",
                callback_data="back"
            )
        ],
    ]

    await query.edit_message_text(
        "VIP ရာသက်ပန် (5000) ကျပ် 💰\n\n"
        "နောက်လာမည့် Channel များကိုပါ အကုန် "
        "ရာသက်ပန် ဝင်ရောက်ခွင့်ရှိမှာဖြစ်ပါသည်။ ✅\n\n"
        "🎁 Gift အနေနဲ့ကတော့ ခ၄ ကား အရှည် "
        "(8) ကားပါရပါမယ်ခင်ဗျာ့။\n\n"
        "အောက်မှ ရွေးချယ်ပေးပါ။",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================
# VIP INFORMATION
# =========================

async def vip_info(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton(
                "1️⃣ VIP ဝင်ရန်",
                callback_data="payment"
            )
        ],
        [
            InlineKeyboardButton(
                "2️⃣ နောက်ပြန်ရန်",
                callback_data="back"
            )
        ],
    ]

    await query.edit_message_text(
        "📋 VIP Channel စာရင်း\n\n"
        "1 - Thin Zar Win Kyaw\n"
        "2 - Tha Zin Oo\n"
        "3 - Nilli Na Na\n"
        "4 - Arlene Lee\n"
        "5 - Zuyi\n"
        "6 - မြဖူး\n"
        "8 - Chan Chan\n"
        "9 - Violet\n"
        "10 - PPG Vip Girl Vip\n\n"
        "Channel အကုန်လုံးနှင့် နောက်အသစ်ထွက် "
        "Channel အားလုံး ရာသက်ပန် (5000) ကျပ်။",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================
# PAYMENT INFORMATION
# =========================

async def payment(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        PAYMENT_TEXT
        + "\n\n📷 ငွေလွှဲပြေစာ Screenshot ကို ဒီ Chat ထဲ ပို့ပေးပါ။"
    )


# =========================
# BACK
# =========================

async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton(
                "1️⃣ VIP ဝင်ရန်",
                callback_data="vip_join"
            )
        ],
        [
            InlineKeyboardButton(
                "2️⃣ VIP အကြောင်းကြည့်ရန်",
                callback_data="vip_info"
            )
        ],
    ]

    await query.edit_message_text(
        "မင်္ဂလာပါ 👋\n\n"
        "အောက်မှ ရွေးချယ်ပေးပါ။",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# =========================
# PAYMENT PHOTO
# =========================

async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user
    photo = update.message.photo[-1]

    username = (
        f"@{user.username}"
        if user.username
        else user.full_name
    )

    # User ကို ပြန်ပြော
    await update.message.reply_text(
        "ငွေလွှဲပြေစာ ရရှိပါပြီ။ ✅\n\n"
        "Admin တက်တာနဲ့ လင့်ပြန်ပို့ပေးပါမယ်။\n"
        "ခဏစောင့်ပေးပါ။ 🙏"
    )

    # Admin ဆီပို့
    admin_caption = (
        "📩 VIP ငွေလွှဲပြေစာ အသစ်\n\n"
        f"👤 User: {username}\n"
        f"🆔 User ID: {user.id}\n\n"
        "👇 ဒီ Photo message ကို Reply လုပ်ပြီး\n"
        "VIP Channel Link ပို့နိုင်ပါတယ်။"
    )

    sent_message = await context.bot.send_photo(
        chat_id=ADMIN_CHAT_ID,
        photo=photo.file_id,
        caption=admin_caption
    )

    # Admin message ID နဲ့ User ID ချိတ်ထား
    admin_messages[sent_message.message_id] = user.id


# =========================
# ADMIN REPLY
# =========================

async def admin_reply_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    message = update.message

    # Admin မဟုတ်ရင် မလုပ်
    if message.chat_id != ADMIN_CHAT_ID:
        return

    # Reply မဟုတ်ရင် မလုပ်
    if not message.reply_to_message:
        return

    replied_message_id = message.reply_to_message.message_id

    # အဲ့ဒီ Admin message ကို ဘယ် User ပို့ခဲ့လဲ ရှာ
    user_id = admin_messages.get(replied_message_id)

    if not user_id:
        return

    # Admin က စာပို့ရင် User ဆီ စာပြန်ပို့
    if message.text:
        await context.bot.send_message(
            chat_id=user_id,
            text=message.text
        )

        await message.reply_text(
            "✅ User ဆီ ပို့ပြီးပါပြီ။"
        )

    # Admin က Photo ပို့ရင် User ဆီ Photo ပို့
    elif message.photo:

        await context.bot.send_photo(
            chat_id=user_id,
            photo=message.photo[-1].file_id,
            caption=message.caption or ""
        )

        await message.reply_text(
            "✅ User ဆီ Photo ပို့ပြီးပါပြီ။"
        )


# =========================
# CALLBACK ROUTER
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    data = query.data

    if data == "vip_join":
        await vip_join(update, context)

    elif data == "vip_info":
        await vip_info(update, context)

    elif data == "payment":
        await payment(update, context)

    elif data == "back":
        await back(update, context)


# =========================
# MAIN
# =========================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    # /start
    app.add_handler(
        CommandHandler("start", start)
    )

    # Buttons
    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    # User Photo
    app.add_handler(
        MessageHandler(
            filters.PHOTO & ~filters.COMMAND,
            photo_handler
        )
    )

    # Admin Reply
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            admin_reply_handler
        )
    )

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()
```
