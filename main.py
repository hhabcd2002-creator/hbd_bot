import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
from datetime import datetime

# ၁။ Bot Token (ဒီတိုင်းပဲထားပါ)
TOKEN = '8143960100:AAESLdYpD-W797uV3p5C-P_MivL77899X7o'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ၂။ Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    keyboard = [[InlineKeyboardButton("မွေးနေ့အထိ အချိန်ဘယ်လောက်လိုလဲ ကြည့်မယ် ✨", callback_data='check_time')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"မင်္ဂလာပါ {user_name}! ✨\n\nဧပြီလ ၂၅ ရက်နေ့မှာ ကျရောက်မယ့် သင့်ရဲ့ ၂၃ နှစ်ပြည့် မွေးနေ့အတွက် Countdown Bot လေး ဖြစ်ပါတယ်။",
        reply_markup=reply_markup
    )

# ၃။ ခလုတ်နှိပ်တဲ့အခါ တွက်ချက်ပေးမယ့်အပိုင်း
async def check_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # မွေးနေ့ရက်စွဲ (၂၀၂၆၊ ဧပြီ၊ ၂၅)
    target_date = datetime(2026, 4, 25, 0, 0, 0)
    now = datetime.now()
    diff = target_date - now

    days = diff.days
    seconds = diff.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60

    result_text = f"🎂 မွေးနေ့အထိ လိုအပ်သောအချိန် -\n\n🗓 {days} ရက်\n⏰ {hours} နာရီ\n⏳ {minutes} မိနစ် ဖြစ်ပါတယ်!"
    
    await query.edit_message_text(text=result_text)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(check_time))
    
    print("Bot is running...")
    application.run_polling()