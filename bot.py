import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackContext,
    CallbackQueryHandler
)

# Admin Telegram ID (သင့် Telegram ID ထည့်ပါ)
ADMIN_ID = 7155245576

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "💰 Member ဝင်ကြေး – 5,000 MMK\n\n"
        "📲 ပေးပို့ရန်နည်းလမ်းများ:\n\n"
        "✅ WavePay / 09891947437 / A Mee Htun\n"
        "✅ KBZPay / 09894396106 / U Chit San Mg\n"
        "✅ MPT Pay / ATOM Pay\n"
        "📌 Phone Bill Payment\n"
        "📸 Screenshot နဲ့ နံပါတ် (Phone Number) ကိုတစ်ခါတည်းရေးပြီး ပေးပို့ပေးပါ။\n\n"
        "⚠️ ပေးပြီးပါက Screenshot ပေးပို့ပါ။ Admin စစ်ဆေးပြီး access ပေးပါမယ်။"
    )

async def handle_photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    photo_file_id = update.message.photo[-1].file_id
    caption = f"📥 Screenshot from @{user.username or user.id} (ID: {user.id})"

    keyboard = [
        [InlineKeyboardButton("✅ Approve", callback_data=f"approve_{user.id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Admin ထံပို့မယ်
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo_file_id,
        caption=caption,
        reply_markup=reply_markup
    )

    await update.message.reply_text("📤 Screenshot ပေးပြီးပါပြီ – Admin စစ်ဆေးနေပါတယ်။")

async def approve(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    user_id = int(query.data.split('_')[1])

    await context.bot.send_message(
        chat_id=user_id,
        text="✅ မင်္ဂလာပါ – သင်သည် Member ဖြစ်ပြီး အသုံးပြုနိုင်ပါပြီ။"
    )

    await query.edit_message_caption(caption="✅ Approved by Admin")

def main():
    token = os.getenv("8143240744:AAHOfq7OecMTw2WvWJhvqDp-VOnO_cuHHQk")
    if not token:
        print("❌ BOT_TOKEN မတွေ့ပါ၊ Railway Variables ထဲထည့်ထားပါ။")
        return

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(CallbackQueryHandler(approve, pattern="^approve_"))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
