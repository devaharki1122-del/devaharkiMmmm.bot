from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)
from telegram.constants import ChatMemberStatus
import json
import os

# ================== ⚙️ زانیاری تۆ ==================
BOT_TOKEN = "8526442713:AAHlr_7Gwg-NUY4rWPA09fwSHyffANCO5dY"

CHANNELS = [
    "@chanaly_boot",
    "@team_988",
    "@my_d4ily"
]

ADMIN_ID = 8186735286
DATA_FILE = "data.json"
# ===================================================


# ================== 📦 داتا ==================
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"vvip": []}, f)

def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)
# =============================================


# ================== 🔒 Forci Join ==================
async def is_member(bot, user_id):
    for ch in CHANNELS:
        try:
            m = await bot.get_chat_member(ch, user_id)
            if m.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
                return False
        except:
            return False
    return True
# ================================================


# ================== 🚀 START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if not await is_member(context.bot, user.id):
        buttons = [
            [InlineKeyboardButton("📢 جەنال 1", url=f"https://t.me/{CHANNELS[0][1:]}")],
            [InlineKeyboardButton("📢 جەنال 2", url=f"https://t.me/{CHANNELS[1][1:]}")],
            [InlineKeyboardButton("📢 جەنال 3", url=f"https://t.me/{CHANNELS[2][1:]}")],
            [InlineKeyboardButton("✅ پشکنین بکە", callback_data="check")]
        ]
        await update.message.reply_text(
            "🚫 تکایە سەرەتا جەنالەکان Join بکە 👇",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    keyboard = [
        [InlineKeyboardButton("🆓 بەشی فری", callback_data="free")],
        [InlineKeyboardButton("👑 کرینی VVIP", callback_data="buy")],
    ]

    await update.message.reply_text(
        "👋 بەخێربێیت بۆ بوتی زێرەک\n\n"
        "🆓 فری: ڕۆژانە 5 ڤیدیۆ\n"
        "👑 VVIP: بێ سنوور + AI MAX\n\n"
        "دووگمە هەڵبژێرە 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
# =============================================


# ================== 🔘 CALLBACK ==================
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = load_data()

    if query.data == "check":
        if await is_member(context.bot, user_id):
            await query.edit_message_text("✅ سپاس! ئێستا دەتوانیت بوت بەکاربهێنیت 👑")
        else:
            await query.answer("🚫 هێشتا Join نەکراوە!", show_alert=True)

    elif query.data == "free":
        await query.edit_message_text(
            "🆓 بەشی فری\n\n"
            "🎥 ڕۆژانە 5 ڤیدیۆ\n"
            "⛔ زیاتر ناتوانیت\n\n"
            "👑 بۆ بێ سنوور → VVIP بکڕە"
        )

    elif query.data == "buy":
        keyboard = [
            [InlineKeyboardButton("💎 بۆ کرین کلیک بکە", url="https://t.me/Deva_harki")]
        ]
        await query.edit_message_text(
            "👑 ChatGPT-MAX (VVIP)\n\n"
            "💵 5$ / مانگ\n"
            "🤖 AI قویترین\n"
            "♾ بێ سنوور\n"
            "⚡ زۆر خێرا\n"
            "🧠 تێگەیشتنی قووڵ\n\n"
            "بۆ کرین 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
# =============================================


# ================== 👑 ADMIN PANEL ==================
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        "👑 ئەدمین پانێل\n\n"
        "/add ID → زیادکردنی VVIP\n"
        "/del ID → لابردنی VVIP\n"
        "/list → لیستی VVIP"
    )

async def add_vvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        uid = int(context.args[0])
        data = load_data()
        if uid not in data["vvip"]:
            data["vvip"].append(uid)
            save_data(data)
            await update.message.reply_text("✅ بەکارهێنەر VVIP کرا")
    except:
        await update.message.reply_text("❌ هەڵە")

async def del_vvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    try:
        uid = int(context.args[0])
        data = load_data()
        if uid in data["vvip"]:
            data["vvip"].remove(uid)
            save_data(data)
            await update.message.reply_text("🗑️ لابرا")
    except:
        await update.message.reply_text("❌ هەڵە")

async def list_vvip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    data = load_data()
    await update.message.reply_text("👑 VVIP IDs:\n" + "\n".join(map(str, data["vvip"])))
# =============================================


# ================== 🤖 AI CHAT ==================
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_data()

    if user_id not in data["vvip"]:
        await update.message.reply_text(
            "🆓 تۆ لە فرییت\n"
            "⛔ تەنها 5 جار ڕۆژانە\n"
            "👑 بۆ بێ سنوور → VVIP"
        )
        return

    await update.message.reply_text("🤖 (AI MAX) وەڵامت لێرە دەدەمەوە...")
# =============================================


# ================== ▶️ RUN ==================
app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(CommandHandler("admin", admin))
app.add_handler(CommandHandler("add", add_vvip))
app.add_handler(CommandHandler("del", del_vvip))
app.add_handler(CommandHandler("list", list_vvip))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

app.run_polling()
# =============================================