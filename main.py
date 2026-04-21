import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from datetime import datetime

# ၁။ Bot Token နဲ့ Admin ID
TOKEN = '8143960100:AAESLdYpD-W797uV3p5C-P_MivL77899X7o'
ADMIN_ID = 1658151455 
PARTNER_ID = None 
START_DATE = datetime(2025, 7, 14) 

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- Calculator Keyboard Helper ---
def get_calc_keyboard(current_val="0"):
    keys = [
        ['7', '8', '9', '/'],
        ['4', '5', '6', '*'],
        ['1', '2', '3', '-'],
        ['0', '.', '=', '+'],
        ['Clear', 'Back']
    ]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(k, callback_data=f"calc_{k}") for k in row]
        for row in keys
    ] + [[InlineKeyboardButton("🔙 Menu သို့ပြန်သွားရန်", callback_data='main_menu')]])

# --- Tic-Tac-Toe Logic ---
def get_ttt_keyboard(board):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(board[i], callback_data=f"ttt_{i}") for i in range(j, j+3)]
        for j in range(0, 9, 3)
    ])

def check_winner(board):
    win_pos = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for p in win_pos:
        if board[p[0]] == board[p[1]] == board[p[2]] != " ":
            return board[p[0]]
    return "Draw" if " " not in board else None

# --- Main Interface ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    keyboard = [
        [InlineKeyboardButton("မွေးနေ့ Countdown 🎂", callback_data='check_time')],
        [InlineKeyboardButton("တို့တွဲလာတဲ့ သက်တမ်း ❤️", callback_data='rel_days')],
        [InlineKeyboardButton("Calculator 🔢", callback_data='start_calc')],
        [InlineKeyboardButton("Tic-Tac-Toe ❌⭕️", callback_data='start_ttt')],
        [InlineKeyboardButton("စကားလုံးဂိမ်း 🐾", callback_data='start_word_game')],
        [InlineKeyboardButton("အားပေးစကား 💌", callback_data='get_quote')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if user_id == ADMIN_ID:
        msg = "🤴 မင်္ဂလာပါ သခင်ကြီး!"
    else:
        global PARTNER_ID
        PARTNER_ID = user_id
        msg = f"မင်္ဂလာပါ {update.effective_user.first_name}! ✨"
    
    await update.message.reply_text(msg, reply_markup=reply_markup)

# --- Handling All Clicks ---
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    now = datetime.now()

    # --- Main Menu Logic ---
    if query.data == 'main_menu':
        keyboard = [
            [InlineKeyboardButton("မွေးနေ့ Countdown 🎂", callback_data='check_time')],
            [InlineKeyboardButton("တို့တွဲလာတဲ့ သက်တမ်း ❤️", callback_data='rel_days')],
            [InlineKeyboardButton("Calculator 🔢", callback_data='start_calc')],
            [InlineKeyboardButton("Tic-Tac-Toe ❌⭕️", callback_data='start_ttt')],
            [InlineKeyboardButton("စကားလုံးဂိမ်း 🐾", callback_data='start_word_game')]
        ]
        await query.edit_message_text("Menu ရွေးချယ်ပေးပါရှင် -", reply_markup=InlineKeyboardMarkup(keyboard))

    # --- Calculator Logic ---
    elif query.data == 'start_calc':
        context.user_data['calc_val'] = ""
        await query.edit_message_text("🔢 Calculator\nအဖြေ: 0", reply_markup=get_calc_keyboard())

    elif query.data.startswith('calc_'):
        val = query.data.split('_')[1]
        current = context.user_data.get('calc_val', "")

        if val == "=":
            try:
                res = str(eval(current))
                context.user_data['calc_val'] = res
                await query.edit_message_text(f"🔢 Calculator\nအဖြေ: {res}", reply_markup=get_calc_keyboard())
            except:
                await query.edit_message_text("🔢 Calculator\nError ပြနေပါတယ်!", reply_markup=get_calc_keyboard())
                context.user_data['calc_val'] = ""
        elif val == "Clear":
            context.user_data['calc_val'] = ""
            await query.edit_message_text("🔢 Calculator\nအဖြေ: 0", reply_markup=get_calc_keyboard())
        elif val == "Back":
            context.user_data['calc_val'] = current[:-1]
            display = context.user_data['calc_val'] if context.user_data['calc_val'] else "0"
            await query.edit_message_text(f"🔢 Calculator\nအဖြေ: {display}", reply_markup=get_calc_keyboard())
        else:
            context.user_data['calc_val'] += val
            await query.edit_message_text(f"🔢 Calculator\nအဖြေ: {context.user_data['calc_val']}", reply_markup=get_calc_keyboard())

    # --- Other Features (Countdown, Rel Days, Games) ---
    elif query.data == 'check_time':
        target = datetime(2026, 4, 25)
        diff = target - now
        res = f"🎂 မွေးနေ့အထိ - {diff.days} ရက် နှင့် {diff.seconds // 3600} နာရီ လိုပါတယ်!"
        await query.edit_message_text(res, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Menu", callback_data='main_menu')]]))

    elif query.data == 'rel_days':
        diff = now - START_DATE
        res = f"👩‍❤️‍👨 တို့တွဲလာတာ ရက်ပေါင်း {diff.days} ရှိပြီ။ ❤️"
        await query.edit_message_text(res, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Menu", callback_data='main_menu')]]))

    elif query.data == 'start_ttt':
        context.user_data['ttt_board'] = [" "] * 9
        await query.edit_message_text("❌ မင်းအလှည့် (X)", reply_markup=get_ttt_keyboard(context.user_data['ttt_board']))

    elif query.data.startswith('ttt_'):
        idx = int(query.data.split('_')[1])
        board = context.user_data.get('ttt_board')
        if board and board[idx] == " ":
            board[idx] = "X"
            winner = check_winner(board)
            if not winner:
                empty = [i for i, v in enumerate(board) if v == " "]
                board[random.choice(empty)] = "O"
                winner = check_winner(board)
            if winner:
                res_msg = "🎉 မင်းနိုင်ပြီ!" if winner == "X" else "🤖 Bot နိုင်ပြီ!" if winner == "O" else "🤝 သရေ!"
                await query.edit_message_text(f"{res_msg}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ပြန်ဆော့မယ်", callback_data='start_ttt')], [InlineKeyboardButton("🔙 Menu", callback_data='main_menu')]]))
            else:
                await query.edit_message_text("❌ မင်းအလှည့်", reply_markup=get_ttt_keyboard(board))

# --- Messaging & Forwarding ---
async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID and PARTNER_ID:
        if update.message.photo: await context.bot.send_photo(PARTNER_ID, update.message.photo[-1].file_id)
        else: await context.bot.send_message(PARTNER_ID, f"💬 ကိုကို: {update.message.text}")
    elif user_id != ADMIN_ID:
        if update.message.photo: await context.bot.send_photo(ADMIN_ID, update.message.photo[-1].file_id, caption=f"📩 {update.effective_user.first_name}")
        else: await context.bot.send_message(ADMIN_ID, f"📩 {update.effective_user.first_name}: {update.message.text}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_click))
    application.add_handler(MessageHandler(filters.TEXT | filters.PHOTO, handle_msg))
    application.run_polling()
