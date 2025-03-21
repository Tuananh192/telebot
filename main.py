import os
import asyncio
import logging
import nest_asyncio
from flask import Flask
from threading import Thread
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, MessageHandler, CommandHandler, filters, CallbackContext

# ✅ Sửa lỗi thư viện "telegram" bị sai phiên bản
try:
    import telegram
    if not hasattr(telegram, 'Update'):
        raise ImportError
except ImportError:
    print("⚠️ Phát hiện thư viện lỗi, đang sửa lỗi...")
    os.system("pip uninstall -y telegram python-telegram-bot")
    os.system("pip install python-telegram-bot --upgrade")
    print("✅ Đã sửa lỗi, vui lòng chạy lại bot!")
    exit()

# ✅ Fix lỗi "RuntimeError: This event loop is already running" trên Replit
nest_asyncio.apply()

# ✅ Token bot Telegram (THAY BẰNG TOKEN CỦA BẠN)
TOKEN = "7965174674:AAEWfcmry3cuNsaMYKqPNYLzVnVaMriJaz0"

# ✅ Cấu hình logging để debug dễ hơn
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# ✅ Hàm xử lý lệnh /start
async def start(update: Update, context: CallbackContext):
    keyboard = [[KeyboardButton("🎲 Tung xúc xắc")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    await update.message.reply_text("🎲 Nhấn vào nút dưới để tung xúc xắc!", reply_markup=reply_markup)

# ✅ Hàm xử lý khi người dùng bấm "🎲 Tung xúc xắc"
async def roll_dice(update: Update, context: CallbackContext):
    message = await update.message.reply_dice(emoji="🎲")
    await asyncio.sleep(3)  # Chờ xúc xắc dừng lại

    dice_value = message.dice.value  # Lấy kết quả tung xúc xắc (1-6)
    result = "Tài" if dice_value % 2 == 0 else "Xỉu"  # Số chẵn là Tài, số lẻ là Xỉu

    await update.message.reply_text(f"🎲 Kết quả: {dice_value} → *{result}*", parse_mode="Markdown")

# ✅ Tạo Flask để giữ bot online trên Replit
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# ✅ Hàm khởi động bot Telegram
async def main():
    bot_app = Application.builder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & filters.Regex("🎲 Tung xúc xắc"), roll_dice))

    print("✅ Bot is running...")
    await bot_app.run_polling()

if __name__ == "__main__":
    # 🔹 Chạy Flask trên luồng riêng để giữ bot online trên Replit
    Thread(target=run_flask, daemon=True).start()

    # 🔹 Chạy bot Telegram
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
