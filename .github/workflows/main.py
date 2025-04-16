import logging
import requests
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Token bot Telegram
TELEGRAM_TOKEN = '6367532329:AAFzGAqQZ_f4VQqX7VbwAoQ7iqbFO07Hzqk'

# Cấu hình logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Chào bạn! Tôi là bot hỗ trợ lấy dữ liệu từ API.\n"
        "Dùng lệnh: /fl <username> (VD: /fl ducthng8)"
    )

# Lệnh /fl <username>
async def fl_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Vui lòng nhập username. Ví dụ: /fl baohuydz158")
        return

    username_input = context.args[0].lstrip("@")
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    url = f"http://ngocanfreekey.x10.mx/ftik.php?username=@{username_input}&key=ngocanvip"

    try:
        response = requests.get(url, timeout=15)
        response.encoding = 'utf-8'

        if response.status_code == 200:
            result = response.text.strip()
            if not result or "null" in result.lower():
                result = "Không tìm thấy dữ liệu cho người dùng này."
        else:
            result = f"Lỗi API. Mã trạng thái: {response.status_code}"
    except requests.exceptions.Timeout:
        result = "Lỗi: API không phản hồi (timeout)."
    except Exception as e:
        logging.exception("Lỗi khi gọi API")
        result = f"Đã xảy ra lỗi: {e}"

    await update.message.reply_text(result)

# Khởi động bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("fl", fl_command))

    print("Bot đang chạy...")
    app.run_polling()

if __name__ == "__main__":
    main()
