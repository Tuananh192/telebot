import telebot
import json
import sqlite3
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from flask import Flask
from threading import Thread
import time
import telebot.util
import dropbox
from telebot.formatting import escape_markdown  # Import hàm escape_markdown

# ✅ Cấu hình bot
TOKEN = "7815604030:AAELtDIikq3XylIwzwITArq-kjrFP6EFwsM"
ADMIN_ID = 6283529520  # Thay bằng Telegram ID của admin

bot = telebot.TeleBot(TOKEN)


# Thay thế bằng token mới của bạn
DROPBOX_ACCESS_TOKEN = "sl.u.AFlUfZINWzm_g2qzc10DYw5MVJE0-UYbZfUBH_puua_gsYGbct5HDNlu3WEkiK0njDIauMLpGfOCzlSoie3N9sHGByKo13yECMlWJBBFPEdMkTvJT5kfSWVEkdRNud5hpVNmtxXBr4TRvJNVW1pZo-Fk1zkJtkkaWsYUvP2203M9KZZdPpx9H4tyUie0Msxmv3PSZPPTPxGktcRoCOUr5BT5C8TTkR-K_nxQ1cSQQAU7VOW79KfLWkhahIJiWXLf9hmEEBT4PScUXaI3jYmFmB359kombx3DTjbeTfu8X5ApAfqWRaurVRov70C0j3rfg3MVmvnQt8gRxo0deVGwWWXRLbxEOgEoZTrSkiIR_1fcQqwTc9k7I9jhnv9jhUE15qaJHz-g6UzSyDfZaf5mVUFHI6e4WpJ2ptP5UsODrq2vSbkfu02PWCotFPZSrg86Uz6thqdd0Cm9tju15CTekAt-OX5NyW3ODfxxqDQmmQeEjqh8zraY-sppDHaMIVwrgUII1w1C2s41tbT21nEg609HtHwx74smjT0hJCBKEOKfMWCt2wfPTo5BaaLaWyhBxxuMhc7r94ZYSNErS8XWenSgxoVVYvt_ydVT0bmPOu7P-bIw24KvPKDvpSyohnElXPNEXv-Sv4NBVpcGhSR8MUo0UVVb0yDB61529xYhHjslB2d8k8sPiCrxMoFJ8pa6bJ0LP7u73d4Gvw55Ha6m43VgzFQWwgWjYz4Q36Dt3Czvy-CjR8U33vrVI6mVx4t8Jve8Zu7Eapfw8o1DNNUd5wT5otE6qpzUAabNxugPRY3y7ySfc3z0HWWLPdOL6nvgdNSogC7J5uisskZzmyWmki7efXL9YGix737-Hv-Mjkj7L2DsfpDh9Ikbx1imzl1ESjvFYUioWYVk62PHjOfTHg98uyhtusgfRMZYm-FFWleN1hFDxxv9mogdROehtJWnlF7qUXkWl9QKHFwijuG5TIn0aPOY9aZ5r44ylqJvfW7cXx9sQN2uv3hZzpJ-_zePfjYr6q7B_ktoKqtC2Zjcc03eRNLv4mkXllqcTSruw5XXuif7kt_KJbVfFctRzXjqwAaZqdh_fREwxUJL103VHqlO5XmBHwKjxkUjrfJGZE97vzkTfHU3ZJ0kgzH_A8UJ6KN01wSNvFvPlvWgKj_a_iN_-Dk65HNmdsWEEv7W1b2HDLHI1GJy-gPnz3yzrpevIUuuS99_CbGT3Huc2OS86ak6IoJ7y6_5sHin9FEIwnQlBilqZ9z6jLt045P8_BbloOJmlm6Xf14OYbtg50xOA_KwSR0BItSVFiCeehKjUXyc9Z-Og_wAnI32xbuyDOQXlfA1sGTqTf9QA-jhvK9oLojuAVvHcFHUF3-fVw_VLVVJ0gCFEZdOwTcCihZrsA572naeO6BmimfF2z4w-v0kX4vvyLVkRN363tdYM7A4CWnrTQ"

from functools import wraps
import time
from dropbox.exceptions import ApiError
from requests.exceptions import RequestException

def rate_limit(max_per_second):
    min_interval = 1.0 / max_per_second
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            elapsed = now - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator

def retry_with_timeout(max_retries=3, timeout=30):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (ApiError, RequestException) as e:
                    if attempt == max_retries - 1:
                        print(f"❌ Lỗi sau {max_retries} lần thử: {str(e)}")
                        raise
                    print(f"⚠️ Lần thử {attempt + 1} thất bại, đang thử lại...")
                    time.sleep(2 ** attempt)  # Exponential backoff
            return None
        return wrapper
    return decorator

@rate_limit(max_per_second=2)
@retry_with_timeout(max_retries=3, timeout=30)
def upload_to_dropbox(local_file_path, dropbox_file_path):
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN, timeout=30)

    with open(local_file_path, "rb") as f:
        dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))

    print(f"✅ Đã upload {local_file_path} lên Dropbox tại {dropbox_file_path}")

# Kiểm tra và tải database từ Dropbox nếu chưa có
import os
if not os.path.exists("database.db"):
    try:
        print("⏳ Đang tải database từ Dropbox...")
        download_from_dropbox("/database.db", "database.db")
        print("✅ Đã tải database từ Dropbox")
    except Exception as e:
        print(f"❌ Lỗi khi tải database: {str(e)}")
        # Tạo database mới nếu không tải được
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                balance REAL DEFAULT 0,
                last_bill TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bypass_link TEXT UNIQUE,
                original_link TEXT,
                price REAL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                type TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        print("✅ Đã tạo database mới")


@rate_limit(max_per_second=2)
@retry_with_timeout(max_retries=3, timeout=30)
def download_from_dropbox(dropbox_file_path, local_file_path):
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN, timeout=30)

    with open(local_file_path, "wb") as f:
        metadata, res = dbx.files_download(dropbox_file_path)
        f.write(res.content)

    print(f"✅ Đã tải {dropbox_file_path} từ Dropbox về {local_file_path}")

# Ví dụ: Tải về database.db
download_from_dropbox("/database.db", "database.db")


# Kết nối database
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Tạo bảng nếu chưa có
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        balance REAL DEFAULT 0,
        last_bill TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS links (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        bypass_link TEXT UNIQUE,
        original_link TEXT,
        price REAL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL,
        type TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()


# Hàm lấy số dư
def get_balance(user_id):
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id, ))
    result = cursor.fetchone()
    return result[0] if result else 0


# Hàm cập nhật số dư
def update_balance(user_id, amount):
    try:
        cursor.execute(
            "INSERT INTO users (user_id, balance) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET balance = balance + ?",
            (user_id, amount, amount))
        cursor.execute(
            "INSERT INTO transactions (user_id, amount, type) VALUES (?, ?, ?)",
            (user_id, amount, "deposit" if amount > 0 else "purchase"))
        conn.commit()

        # Upload to Dropbox after successful database update
        upload_to_dropbox("database.db", "/database.db")

        # Download the latest version to ensure consistency
        download_from_dropbox("/database.db", "database.db")

        print("✅ Đã cập nhật số dư và đồng bộ với Dropbox")
    except Exception as e:
        print(f"❌ Lỗi khi cập nhật/đồng bộ: {str(e)}")
        conn.rollback()


# Hàm thêm link vào DB (Admin)
def add_link(bypass_link, original_link, price):
    try:
        cursor.execute(
            "INSERT INTO links (bypass_link, original_link, price) VALUES (?, ?, ?)",
            (bypass_link, original_link, price))
        conn.commit()
        # Auto upload after changes
        upload_to_dropbox("database.db", "/database.db")
        return "✅ Link đã được thêm!"
    except sqlite3.IntegrityError:
        return "⚠️ Link này đã tồn tại!"


# Hàm lấy giá và link gốc
def get_link(bypass_link):
    cursor.execute(
        "SELECT original_link, price FROM links WHERE bypass_link = ?",
        (bypass_link, ))
    return cursor.fetchone()


# Định dạng số tiền
def format_currency(amount):
    return "{:,}".format(int(float(amount))).replace(",", ".")


# Database helper functions
def get_user_balance(telegram_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE telegram_id = ?",
                   (telegram_id, ))
    result = cursor.fetchone()
    conn.close()
    if result:
        return f"{int(result[0]):,} VNĐ".replace(",", ".")
    return None


def set_user_balance(user_id, balance):
    cursor.execute(
        "INSERT OR REPLACE INTO users (user_id, balance) VALUES (?, ?)",
        (user_id, balance))
    conn.commit()


def get_link_info(bypass_link):
    cursor.execute(
        "SELECT original_link, price FROM links WHERE bypass_link = ?",
        (bypass_link, ))
    result = cursor.fetchone()
    return {"url": result[0], "price": result[1]} if result else None


def save_link(bypass_link, original_link, price):
    cursor.execute(
        "INSERT OR REPLACE INTO links (bypass_link, original_link, price) VALUES (?, ?, ?)",
        (bypass_link, original_link, price))
    conn.commit()
    # Auto upload after changes
    upload_to_dropbox("database.db", "/database.db")


#Thêm TB
@bot.message_handler(commands=["thong_bao"])
def send_announcement(message):
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id,
                         "❌ Bạn không có quyền sử dụng lệnh này.")
        return

    msg = bot.send_message(ADMIN_ID, "📢 Nhập nội dung thông báo:")
    bot.register_next_step_handler(msg, process_announcement)


def process_announcement(message):
    content = message.text
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()

    if not users:
        bot.send_message(ADMIN_ID,
                         "❌ Không có người dùng nào để gửi thông báo.")
        return

    success_count = 0
    for (user_id, ) in users:
        try:
            bot.send_message(user_id,
                             f"📢 *Thông báo từ Admin:*\n{content}",
                             parse_mode="Markdown")
            success_count += 1
        except:
            pass  # Tránh lỗi khi user chặn bot hoặc không nhận tin nhắn

    bot.send_message(ADMIN_ID,
                     f"✅ Đã gửi thông báo đến {success_count} người dùng.")


# ✅ /start - Chào mừng khách hàng
@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.chat.id
    # Create new connection and cursor for this operation
    local_conn = sqlite3.connect("database.db")
    local_cursor = local_conn.cursor()

    try:
        local_cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, balance) VALUES (?, 0)",
            (user_id, ))
        local_conn.commit()

        bot.send_message(
            message.chat.id, "🤖 Chào mừng đến BOT mua link! Bạn có thể:\n"
            "💰 /nap_tien - Nạp tiền\n"
            "🔍 /so_du - Kiểm tra số dư\n"
            "🛒 /mua_link - Mua link")
    finally:
        local_cursor.close()
        local_conn.close()


# ✅ /so_du - Kiểm tra số dư
@bot.message_handler(commands=["so_du"])
def check_balance(message):
    user_id = message.chat.id
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id, ))
    result = cursor.fetchone()
    balance = int(result[0]) if result else 0
    formatted_balance = "{:,}".format(balance).replace(",", ".")

    bot.send_message(message.chat.id,
                     f"💰 Số dư của bạn: {formatted_balance} VND")


# ✅ /nap_tien - Hướng dẫn nạp tiền
@bot.message_handler(commands=["nap_tien"])
def deposit_money(message):
    user_id = message.chat.id
    amount = 100000  # Có thể cho người dùng nhập số tiền nạp
    content = f"NAP{user_id}"  # Nội dung giao dịch

    qr_code_url = f"https://img.vietqr.io/image/ICB-109878256183-compact.png?amount={amount}&addInfo={content}"

    msg_text = ("💵 Để nạp tiền, vui lòng chuyển khoản:\n"
                "🏦 *VIETTINBANK*\n"
                "📌 STK: `109878256183`\n"
                "👤 TTK: *CAO DINH TUAN ANH*\n"
                f"💬Nội dung: `{content}`\n\n"
                "✅ 👉 NẠP TỐI THIỂU 10k\n"
                "✅ GỬI BILL ĐỂ ĐƯỢC XÁC NHẬN")

    bot.send_message(message.chat.id, msg_text, parse_mode="MarkdownV2")
    bot.send_photo(
        message.chat.id,
        qr_code_url,
        caption=
        "📌 Mã QR đã tự động điền thông tin để thanh toán nhanh hơn!\n✅ GỬI BILL ĐỂ ĐƯỢC XÁC NHẬN"
    )


# ✅ Lưu ảnh bill khi khách hàng gửi
@bot.message_handler(content_types=["photo"])
def handle_bill_photo(message):
    user_id = message.chat.id
    file_id = message.photo[-1].file_id

    # First ensure the user exists in the database
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, balance) VALUES (?, 0)",
        (user_id, ))
    # Then update their last_bill
    cursor.execute("UPDATE users SET last_bill = ? WHERE user_id = ?",
                   (file_id, user_id))
    conn.commit()

    bot.send_message(message.chat.id,
                     "✅BILL ĐÃ ĐƯỢC LƯU! Nhấn /XACNHAN để gửi.")


# ✅ /XACNHAN - Gửi bill cho admin xác nhận
@bot.message_handler(commands=["XACNHAN"])
def confirm_deposit(message):
    user_id = message.chat.id
    cursor.execute("SELECT last_bill FROM users WHERE user_id = ?",
                   (user_id, ))
    result = cursor.fetchone()

    if not result or not result[0]:
        bot.send_message(message.chat.id, "❌ Bạn chưa gửi ảnh bill.")
        return

    bill_photo = result[0]

    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("✅ Xác nhận + Tiền",
                             callback_data=f"confirm_{user_id}"),
        InlineKeyboardButton("❌ Từ chối", callback_data=f"deny_{user_id}"))

    bot.send_photo(ADMIN_ID,
                   bill_photo,
                   caption=f"🔔 *Xác nhận nạp tiền*\n👤 User ID: {user_id}",
                   reply_markup=keyboard)
    bot.send_message(message.chat.id, "✅ Bill đã gửi, chờ xác nhận.")


# ✅ Admin xác nhận nạp tiền
@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm_"))
def handle_admin_confirm(call):
    user_id = call.data.split("_")[1]
    msg = bot.send_message(ADMIN_ID,
                           f"💰 Nhập số tiền muốn cộng cho user {user_id}: ",
                           reply_markup=ForceReply())
    bot.register_next_step_handler(msg, process_add_money, user_id)


def process_add_money(message, user_id):
    try:
        amount = int(message.text)
        cursor.execute(
            "UPDATE users SET balance = balance + ?, last_bill = NULL WHERE user_id = ?",
            (amount, user_id))
        conn.commit()

        cursor.execute("SELECT balance FROM users WHERE user_id = ?",
                       (user_id, ))
        new_balance = cursor.fetchone()[0]
        formatted_balance = "{:,}".format(new_balance).replace(",", ".")

        bot.send_message(
            int(user_id),
            f"✅ ĐÃ ĐƯỢC XÁC NHẬN, {amount:,} VND ĐÃ ĐƯỢC CỘNG VÀO TK. Số dư hiện tại: {formatted_balance} VND\n👉 VỀ TRANG CHỦ NHẤN /start"
        )
        bot.send_message(ADMIN_ID,
                         f"✔ Đã cộng {amount:,} VND cho user {user_id}.")
    except ValueError:
        bot.send_message(ADMIN_ID,
                         "❌ Số tiền không hợp lệ. Hãy nhập lại số tiền.")


@bot.callback_query_handler(func=lambda call: call.data.startswith("deny_"))
def handle_admin_deny(call):
    user_id = call.data.split("_")[1]
    bot.send_message(user_id, "❌ Đã từ chối yêu cầu nạp tiền.")


# ✅ /mua_link - Mua link (Khách nhập link vượt, bot kiểm tra và trừ tiền)
@bot.message_handler(commands=["mua_link"])
def mua_link_step1(message):
    # Yêu cầu khách hàng nhập link vượt
    bot.send_message(message.chat.id, "🔗 Nhập link vượt bạn muốn mua:")
    bot.register_next_step_handler(message, mua_link_step2)


def mua_link_step2(message):
    link_vuot = message.text
    user_id = message.chat.id

    # Kiểm tra link vượt có tồn tại không
    cursor.execute(
        "SELECT original_link, price FROM links WHERE bypass_link = ?",
        (link_vuot, ))
    link_result = cursor.fetchone()

    if not link_result:
        bot.send_message(
            message.chat.id,
            "❌ Link không tồn tại hoặc chưa được update. Vui lòng thử lại.")
        return

    # Lấy thông tin link và số dư của khách hàng
    original_link, price = link_result
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id, ))
    balance = cursor.fetchone()[0]

    # Kiểm tra số dư của khách hàng
    if balance < price:
        bot.send_message(
            message.chat.id, f"❌ Bạn không đủ tiền để mua link này.\n\n"
            f"💵 Giá link: {price} VND\n"
            f"💰 Số dư hiện tại: {balance} VND\n\n"
            f"👉 Bạn cần nạp thêm {price - balance} VND để mua link này.")
        return

    # Trừ tiền và gửi link cho khách hàng
    cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?",
                   (price, user_id))
    conn.commit()

    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id, ))
    new_balance = cursor.fetchone()[0]

    formatted_balance = "{:,}".format(int(new_balance)).replace(",", ".")
    bot.send_message(
        message.chat.id, f"🎉 Mua link thành công!\n"
        f"🔗 Link của bạn: {original_link}\n"
        f"💰 Số dư hiện tại: {formatted_balance} VND\n"
        f"Nhấn /start để trở về trang chủ.")


@bot.message_handler(commands=["admin"])
def admin_menu(message):
    # Kiểm tra xem người dùng có phải là admin không
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id,
                         "❌ Bạn không có quyền truy cập vào menu admin.")
        return

    # Tạo menu lệnh cho admin
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("➕ Thêm link", callback_data="admin_add_link"),
        InlineKeyboardButton("🗑️ Xóa link", callback_data="admin_delete_link"),
        InlineKeyboardButton("👥 Xem danh sách người dùng",
                             callback_data="admin_list_users"),
        InlineKeyboardButton("🔗 Xem danh sách link",
                             callback_data="admin_list_links"),
        InlineKeyboardButton("💰 Cộng/trừ tiền người dùng",
                             callback_data="admin_adjust_balance"),
        InlineKeyboardButton("📢 Gửi thông báo",
                             callback_data="admin_announcement"))

    bot.send_message(message.chat.id,
                     "👨‍💻 **Menu Admin**\nChọn một tùy chọn:",
                     reply_markup=keyboard)


# Xử lý lệnh /admin
@bot.callback_query_handler(
    func=lambda call: call.data == "admin_announcement")
def admin_send_announcement(call):
    if call.message.chat.id != ADMIN_ID:
        bot.send_message(call.message.chat.id,
                         "❌ Bạn không có quyền sử dụng tính năng này.")
        return

    msg = bot.send_message(ADMIN_ID, "📢 Nhập nội dung thông báo:")
    bot.register_next_step_handler(msg, process_announcement)


# Định nghĩa hàm admin_add_link_step1 trước khi gọi
def admin_add_link_step1(message):
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ Bạn không có quyền admin.")
        return

    msg = bot.send_message(ADMIN_ID, "🔗 Nhập *link vượt*:")
    bot.register_next_step_handler(msg, admin_add_link_step2)


def admin_add_link_step2(message):
    link_vuot = message.text
    msg = bot.send_message(ADMIN_ID, "🔗 Nhập *link gốc*:")
    bot.register_next_step_handler(msg, admin_add_link_step3, link_vuot)


def admin_add_link_step3(message, link_vuot):
    link_goc = message.text
    msg = bot.send_message(ADMIN_ID, "💰 Nhập *giá bán* (VND):")
    bot.register_next_step_handler(msg, admin_add_link_step4, link_vuot,
                                   link_goc)


def admin_add_link_step4(message, link_vuot, link_goc):
    try:
        price = int(message.text)
        save_link(link_vuot, link_goc, price)

        # Dùng escape_markdown để tránh lỗi khi gửi tin nhắn
        msg_text = (f"✅ Đã thêm link\\!\n\n"
                    f"🔗 *Link vượt:* {escape_markdown(link_vuot)}\n"
                    f"🔗 *Link gốc:* {escape_markdown(link_goc)}\n"
                    f"💰 *Giá:* {price} VND")

        bot.send_message(ADMIN_ID, msg_text, parse_mode="MarkdownV2")
    except ValueError:
        bot.send_message(ADMIN_ID,
                         "❌ Giá không hợp lệ. Hãy nhập lại số nguyên.")


# Xử lý callback từ menu admin
@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_"))
def handle_admin_callback(call):
    if call.data == "admin_add_link":
        # Gọi hàm thêm link từng bước
        admin_add_link_step1(call.message)
    elif call.data == "admin_delete_link":
        # Gọi hàm xóa link
        bot.send_message(call.message.chat.id,
                         "🔗 Nhập link vượt bạn muốn xóa:")
        bot.register_next_step_handler(call.message, admin_delete_link)
    elif call.data == "admin_list_users":
        # Hiển thị danh sách người dùng
        list_users(call.message)
    elif call.data == "admin_list_links":
        # Hiển thị danh sách link
        list_links(call.message)
    elif call.data == "admin_adjust_balance":
        # Gọi hàm cộng/trừ tiền người dùng
        bot.send_message(call.message.chat.id, "👤 Nhập ID người dùng:")
        bot.register_next_step_handler(call.message,
                                       admin_adjust_balance_step1)


# Xử lý callback từ menu admin
@bot.callback_query_handler(func=lambda call: call.data.startswith("admin_"))
def handle_admin_callback(call):
    if call.data == "admin_add_link":
        # Gọi hàm thêm link từng bước
        admin_add_link_step1(call.message)
    elif call.data == "admin_delete_link":
        # Gọi hàm xóa link
        bot.send_message(call.message.chat.id,
                         "🔗 Nhập link vượt bạn muốn xóa:")
        bot.register_next_step_handler(call.message, admin_delete_link)
    elif call.data == "admin_list_users":
        # Hiển thị danh sách người dùng
        list_users(call.message)
    elif call.data == "admin_list_links":
        # Hiển thị danh sách link
        list_links(call.message)
    elif call.data == "admin_adjust_balance":
        # Gọi hàm cộng/trừ tiền người dùng
        bot.send_message(call.message.chat.id, "👤 Nhập ID người dùng:")
        bot.register_next_step_handler(call.message,
                                       admin_adjust_balance_step1)


# Hàm xóa link
def admin_delete_link(message):
    link_vuot = message.text
    cursor.execute("DELETE FROM links WHERE bypass_link = ?", (link_vuot, ))
    conn.commit() # Added commit here
    if cursor.rowcount > 0:
        upload_to_dropbox("database.db", "/database.db")
        bot.send_message(message.chat.id, f"✅ Đã xóa link: {link_vuot}")
    else:
        bot.send_message(message.chat.id, "❌ Link không tồn tại.")


# Hàm hiển thị danh sách người dùng
def list_users(message):
    cursor.execute("SELECT user_id, balance FROM users")
    users = cursor.fetchall()

    if not users:
        bot.send_message(message.chat.id, "❌ Không có người dùng nào.")
        return

    user_list = "👥 *Danh sách người dùng:*\n"
    for user_id, balance in users:
        formatted_balance = "{:,}".format(balance).replace(",", ".")
        user_list += f"\\- ID: `{user_id}`, Số dư: `{formatted_balance} VND`\n"

    bot.send_message(message.chat.id, user_list, parse_mode="MarkdownV2")


def list_links(message):
    cursor.execute("SELECT bypass_link, original_link, price FROM links")
    links = cursor.fetchall()

    if not links:
        bot.send_message(message.chat.id, "❌ Không có link nào.")
        return

    link_list = "🔗 *Danh sách link:*\n"
    for bypass_link, original_link, price in links:
        formatted_price = "{:,}".format(price).replace(",", ".")

        link_list += (f"\\- Link vượt: `{escape_markdown(bypass_link)}`\n"
                      f"  Link gốc: `{escape_markdown(original_link)}`\n"
                      f"  Giá: `{formatted_price} VND`\n")

    bot.send_message(message.chat.id, link_list, parse_mode="MarkdownV2")


# Hàm cộng/trừ tiền người dùng
def admin_adjust_balance_step1(message):
    user_id = message.text
    cursor.execute("SELECT balance FROM users WHERE user_id = ?", (user_id, ))
    result = cursor.fetchone()

    if not result:
        bot.send_message(message.chat.id, "❌ Người dùng không tồn tại.")
        return

    msg = bot.send_message(message.chat.id,
                           "💰 Nhập số tiền (dương để cộng, âm để trừ):")
    bot.register_next_step_handler(msg, admin_adjust_balance_step2, user_id)


def admin_adjust_balance_step2(message, user_id):
    try:
        amount = int(message.text)
        cursor.execute(
            "UPDATE users SET balance = balance + ? WHERE user_id = ?",
            (amount, user_id))
        conn.commit()
        upload_to_dropbox("database.db", "/database.db") # Added upload here

        cursor.execute("SELECT balance FROM users WHERE user_id = ?",
                       (user_id, ))
        new_balance = cursor.fetchone()[0]
        formatted_balance = "{:,}".format(new_balance).replace(",", ".")

        bot.send_message(
            message.chat.id,
            f"✅ Đã điều chỉnh số dư của người dùng {user_id} thành {formatted_balance} VND."
        )
    except ValueError:
        bot.send_message(message.chat.id,
                         "❌ Số tiền không hợp lệ. Hãy nhập lại số nguyên.")


# ✅ Tạo server nhỏ để UptimeRobot ping
app = Flask(__name__)


@app.route('/')
def home():
    return "Bot is running!"


def run():
    app.run(host="0.0.0.0", port=8080)


# Function to sync database
def sync_database():
    while True:
        try:
            # Upload to Dropbox
            upload_to_dropbox("database.db", "/database.db")
            print("✅ Database synchronized with Dropbox")
        except Exception as e:
            print(f"❌ Sync error: {str(e)}")
            try:
                # On error, try to recover from Dropbox
                download_from_dropbox("/database.db", "database.db")
                print("✅ Database recovered from Dropbox")
            except Exception as e:
                print(f"❌ Recovery error: {str(e)}")
        time.sleep(5)  # Wait 5 seconds before next sync

# ✅ Giữ bot chạy liên tục
def keep_alive():
    t = Thread(target=run)
    t.start()

    # Start database sync in separate thread
    sync_thread = Thread(target=sync_database, daemon=True)
    sync_thread.start()


# 💡 Gọi keep_alive() trước khi chạy bot
keep_alive()
bot.polling()