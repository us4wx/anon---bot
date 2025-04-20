from telegram import Update, MessageEntity
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
import random
import string

TOKEN = '7826319545:AAGHUD7mRS78F2x5evn74vrRlunJJ_pkxI0'
ADMIN_CHAT_ID = 7512329165

user_code_map = {}  # برای نگهداری کدهای یکتا

# ساخت کد یکتا
def generate_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

# خوش آمدگویی
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! پیام ناشناست رو بفرست. من به مدیر منتقل می‌کنم.")

# پیام کاربران
async def forward_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    code = generate_code()
    user_code_map[code] = user.id

    msg_type = update.message.effective_attachment
    if msg_type:
        forwarded = await update.message.copy(chat_id=ADMIN_CHAT_ID)
    else:
        await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=f"◜письмо ⊹◞:پیام جدید از کاربر {code}:\n{update.message.text}")

    username = f"@{user.username}" if user.username else "ندارد"
    info = f"اطلاعات کاربر:\nنام: {user.full_name}\nیوزرنیم: {username}\nکد کاربر: {code}"
    await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=info)

    await update.message.reply_text("پیامت با موفقیت ناشناس ارسال شد!")

# پاسخ مدیر به کاربران
async def reply_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("فرمت صحیح: /reply کد_کاربر پیام")
        return

    code = args[0]
    reply_text = ' '.join(args[1:])
    user_id = user_code_map.get(code)

    if user_id:
        await context.bot.send_message(chat_id=user_id, text=f"پاسخ ناشناس:\n{reply_text}")
        await update.message.reply_text("پاسخ ارسال شد.")
    else:
        await update.message.reply_text("کد نامعتبر است یا کاربر ناشناس نیست.")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("reply", reply_handler))
app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, forward_all))

app.run_polling()
