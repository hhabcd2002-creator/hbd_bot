import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime

# ၁။ Bot Token
TOKEN = '8600398871:AAHLCYV37fQ-5lOqahmCoj0RivaZhNDNxX4'

# ၂။ Start Command (မြန်မာလို ရေးထားပါတယ်)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ခလုတ်ပေါ်ကစာကို မြန်မာလို ရေးလို့ရပါတယ်
    keyboard = [[InlineKeyboardButton("အချိန်ဘယ်လောက်လိုသေးလဲ ကြည့်မယ် ⏳", callback_data='check')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"မင်္ဂလာပါ {user_name}! ✨\nဒီ Bot လေးကတော့ မွေးနေ့အတွက် Countdown ကြည့်ဖို့ ဖြစ်ပါတယ်။",
        reply_markup=reply_markup
    )

# ၃။ ခလုတ်နှိပ်တဲ့အခါ ထွက်လာမယ့်စာ
async def check_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # မွေးနေ့ရက်စွဲ (၂၀၂၆၊ ဇွန်လ၊ ၁ ရက်)
    target_date = datetime(2026, 6, 1, 0, 0) 
    now = datetime.now()
    diff = target_date - now

    if diff.total_seconds() > 0:
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        # တွက်ချက်ပြီး ထွက်လာမယ့်စာကို မြန်မာလို ပြင်ထားပါတယ်
        text = (
            f"🎂 မွေးနေ့ရောက်ဖို့ လိုအပ်တဲ့အချိန် -\n\n"
            f"📅 {days} ရက်၊ {hours} နာရီ၊ {minutes} မိနစ်!\n\n"
            f"စိတ်လှုပ်ရှားနေပြီလား? ✨"
        )
    else:
        text = "🎉 Happy Birthday!!! 🎂✨\n\nဒီနေ့ကစပြီး ပျော်ရွှင်စရာတွေပဲ ကြုံပါစေ။ မွေးနေ့လက်ဆောင်လေး ရောက်ရှိလို့လာပါပြီ!"

    await query.edit_message_text(text)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_time))
    
    print("Bot is running...")
    app.run_polling()