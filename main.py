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
user_sessions = {}  # Lưu session của từng user: {user_id: {tool_running, tool_thread, stop_event, config, last_spam_time}}
user_states = {}  # Lưu trạng thái của từng user
session_lock = threading.Lock()  # Lock để đảm bảo thread-safe khi thao tác với user_sessions

# Admin configuration
ADMIN_IDS = [6913983524, 1615483759]  # Thay bằng user ID của admin

# Helper functions for user session management
def is_admin(user_id):
    """Kiểm tra xem user có phải admin không"""
    return user_id in ADMIN_IDS

def get_user_session(user_id):
    """Lấy session của user, tạo mới nếu chưa có"""
    with session_lock:
        if user_id not in user_sessions:
            user_sessions[user_id] = {
                'tool_running': False,
                'tool_thread': None,
                'stop_event': None,
                'config': None,
                'last_spam_time': 0
            }
        return user_sessions[user_id]

def cleanup_user_session(user_id):
    """Dọn dẹp session của user khi tool dừng"""
    with session_lock:
        if user_id in user_sessions:
            session = user_sessions[user_id]
            session['tool_running'] = False
            session['tool_thread'] = None
            session['stop_event'] = None
            # Giữ lại config và last_spam_time

def is_user_tool_running(user_id):
    """Kiểm tra xem tool của user có đang chạy không"""
    session = get_user_session(user_id)
    return session['tool_running']

def set_user_tool_running(user_id, running):
    """Đặt trạng thái tool của user"""
    session = get_user_session(user_id)
    session['tool_running'] = running

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
        self.NAME_TOOL="zLocket Spam BIGCHANG"
        self.VERSION_TOOL="v3.0.1"
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

def setup_bot_handlers():
    """Setup all bot message handlers"""

    @bot.message_handler(commands=['start'])
    def start_command(message):
        welcome_text = f"""
🔒 <b>zLocket Spam BIGCHANG - Telegram Bot</b>

Chào mừng! Đây là bot điều khiển tool zLocket.

<b>Các lệnh có sẵn:</b>
/start - Hiển thị menu chính
/spam - Bắt đầu spam
/stop - Dừng spam
/status - Kiểm tra trạng thái
/help - Hướng dẫn sử dụng

<b>Ví dụ sử dụng:</b>
<code>/spam username123</code>
<code>/spam https://locket.cam/username123</code>

<b>Tính năng:</b>
• Tool chạy tối thiểu 5 phút mỗi lần
• Cooldown 1 phút giữa các lần spam

<i>Phát triển bởi https://t.me/BIGKER1</i>
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
        user_id = message.from_user.id
        current_time = time.time()
        user_session = get_user_session(user_id)

        # Kiểm tra cooldown cho user này
        if user_session['last_spam_time'] > 0:
            time_since_last = current_time - user_session['last_spam_time']
            if time_since_last < 60:  # 1 phút cooldown
                remaining = int(60 - time_since_last)
                bot.reply_to(message, f"⏰ Vui lòng đợi {remaining} giây nữa để có thể spam tiếp!")
                return

        if is_user_tool_running(user_id):
            bot.reply_to(message, "❌ Tool của bạn đang chạy! Sử dụng /stop để dừng trước.")
            return

        args = message.text.split()[1:]
        if len(args) < 1:
            bot.reply_to(message, "❌ Thiếu tham số!\n\nSử dụng: /spam [target]\nVí dụ: /spam username123")
            return

        target = args[0]

        # Lưu target vào user state và yêu cầu nhập tên
        user_states[user_id] = {
            'step': 'waiting_for_name',
            'target': target,
            'timestamp': current_time
        }

        markup = types.ForceReply(selective=False)
        bot.reply_to(message, f"🎯 Target: <code>{target}</code>\n\n👤 Vui lòng nhập tên tùy ý cho spam (hoặc gửi 'default' để dùng tên mặc định):", 
                    parse_mode='HTML', reply_markup=markup)

    @bot.message_handler(func=lambda message: message.from_user.id in user_states and user_states[message.from_user.id].get('step') == 'waiting_for_name')
    def handle_custom_name(message):
        user_id = message.from_user.id
        current_time = time.time()
        user_session = get_user_session(user_id)

        if user_id not in user_states:
            return

        user_state = user_states[user_id]
        target = user_state['target']

        # Kiểm tra timeout (5 phút)
        if current_time - user_state['timestamp'] > 300:
            del user_states[user_id]
            bot.reply_to(message, "⏰ Hết thời gian chờ. Vui lòng sử dụng lại lệnh /spam")
            return

        # Lấy tên từ tin nhắn
        custom_name = message.text.strip()
        if custom_name.lower() == 'default' or not custom_name:
            custom_name = "zLocket Spam BIGCHANG"
        elif len(custom_name) > 30:
            bot.reply_to(message, "❌ Tên quá dài! Vui lòng nhập tên dưới 30 ký tự.")
            return

        # Xóa user state
        del user_states[user_id]

        # Khởi tạo config cho user này
        if not user_session['config']:
            user_session['config'] = zLocket()

        # Xử lý target URL
        url = target.strip()
        if not url.startswith(("http://", "https://")) and not url.startswith("locket."):
            url = f"https://locket.cam/{url}"
        if url.startswith("locket."):
            url = f"https://{url}"

        # Extract UID
        user_config = user_session['config']
        user_config.messages = []
        uid = user_config._extract_uid_locket(url)

        if not uid:
            error_msg = "❌ Không thể lấy UID từ target:\n"
            for msg in user_config.messages:
                error_msg += f"• {msg}\n"
            bot.reply_to(message, error_msg)
            return

        # Cấu hình cho user này
        user_config.TARGET_FRIEND_UID = uid
        user_config.NAME_TOOL = custom_name
        user_config.USE_EMOJI = True

        # Gửi thông báo khởi động
        init_msg = bot.reply_to(message, f"✅ Đã cấu hình thành công!\n\n🎯 Target UID: <code>{uid}</code>\n👤 Custom Name: <code>{custom_name}</code>\n\n🚀 Đang khởi động tool...", parse_mode='HTML')

        # Cập nhật thời gian spam cuối cho user này
        user_session['last_spam_time'] = current_time

        # Bắt đầu spam thread với timeout 30 giây
        def run_spam():
            status_msg = None
            try:
                set_user_tool_running(user_id, True)
                user_session['stop_event'] = threading.Event()
                user_stop_event = user_session['stop_event']

                # Khởi tạo proxy cho user này
                proxy_queue, num_threads = init_proxy_for_user(user_config)
                num_threads = min(num_threads, 20)  # Giới hạn threads

                # Gửi trạng thái ban đầu
                status_text = f"🟢 <b>Tool đang chạy (User: {user_id})</b>\n\n⏱️ Runtime: <code>00:00:00</code>\n✅ Success: <code>0</code>\n❌ Failed: <code>0</code>\n📊 Success Rate: <code>0.0%</code>\n🧵 Threads: <code>{num_threads}</code>\n🎯 Target: <code>{user_config.TARGET_FRIEND_UID}</code>\n👤 Name: <code>{user_config.NAME_TOOL}</code>"
                status_msg = bot.send_message(message.chat.id, status_text, parse_mode='HTML')

                threads = []
                for i in range(num_threads):
                    if not is_user_tool_running(user_id):
                        break
                    thread = threading.Thread(
                        target=step1_create_account_for_user,
                        args=(i, proxy_queue, user_stop_event, user_config)
                    )
                    threads.append(thread)
                    thread.daemon = True
                    thread.start()

                # Chạy ít nhất 5 phút và cập nhật trạng thái mỗi 3 giây
                start_time = time.time()
                last_update = 0

                while time.time() - start_time < 300 and is_user_tool_running(user_id):
                    current_runtime = time.time() - start_time

                    # Cập nhật trạng thái mỗi 3 giây
                    if current_runtime - last_update >= 3:
                        try:
                            elapsed = int(current_runtime)
                            hours, remainder = divmod(elapsed, 3600)
                            minutes, seconds = divmod(remainder, 60)
                            success_rate = (user_config.successful_requests / (user_config.successful_requests + user_config.failed_requests)) * 100 if (user_config.successful_requests + user_config.failed_requests) > 0 else 0

                            remaining_time = max(0, 300 - elapsed)
                            rem_minutes, rem_seconds = divmod(remaining_time, 60)

                            status_text = f"🟢 <b>Tool đang chạy (User: {user_id})</b>\n\n⏱️ Runtime: <code>{hours:02d}:{minutes:02d}:{seconds:02d}</code>\n⏳ Remaining: <code>{rem_minutes:02d}:{rem_seconds:02d}</code>\n✅ Success: <code>{user_config.successful_requests}</code>\n❌ Failed: <code>{user_config.failed_requests}</code>\n📊 Success Rate: <code>{success_rate:.1f}%</code>\n🧵 Threads: <code>{num_threads}</code>\n🎯 Target: <code>{user_config.TARGET_FRIEND_UID}</code>\n👤 Name: <code>{user_config.NAME_TOOL}</code>"

                            bot.edit_message_text(
                                chat_id=status_msg.chat.id,
                                message_id=status_msg.message_id,
                                text=status_text,
                                parse_mode='HTML'
                            )
                            last_update = current_runtime
                        except Exception:
                            pass  # Ignore edit errors

                    time.sleep(1)

                # Sau 5 phút, bắt buộc dừng tool
                set_user_tool_running(user_id, False)
                user_stop_event.set()

                # Cập nhật trạng thái cuối cùng
                try:
                    elapsed = 300
                    hours, remainder = divmod(elapsed, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    success_rate = (user_config.successful_requests / (user_config.successful_requests + user_config.failed_requests)) * 100 if (user_config.successful_requests + user_config.failed_requests) > 0 else 0

                    final_status = f"🔴 <b>Tool đã dừng (User: {user_id})</b>\n\n⏱️ Total Runtime: <code>{hours:02d}:{minutes:02d}:{seconds:02d}</code>\n✅ Total Success: <code>{user_config.successful_requests}</code>\n❌ Total Failed: <code>{user_config.failed_requests}</code>\n📊 Success Rate: <code>{success_rate:.1f}%</code>\n🧵 Threads: <code>{num_threads}</code>\n🎯 Target: <code>{user_config.TARGET_FRIEND_UID}</code>\n👤 Name: <code>{user_config.NAME_TOOL}</code>"

                    bot.edit_message_text(
                        chat_id=status_msg.chat.id,
                        message_id=status_msg.message_id,
                        text=final_status,
                        parse_mode='HTML'
                    )
                except Exception:
                    pass

                # Thông báo dừng
                bot.send_message(message.chat.id, "⛔ Tool đã chạy đủ 5 phút và đang dừng...")

                # Chờ tất cả threads dừng với timeout
                for thread in threads:
                    thread.join(timeout=3)

                # Thông báo hoàn tất
                bot.send_message(message.chat.id, "✅ Tool đã dừng hoàn toàn!")

                # Cập nhật thời gian spam cuối cùng khi tool dừng hoàn toàn
                user_session['last_spam_time'] = time.time()

            except Exception as e:
                if status_msg:
                    try:
                        bot.edit_message_text(
                            chat_id=status_msg.chat.id,
                            message_id=status_msg.message_id,
                            text=f"❌ <b>Tool gặp lỗi và đã dừng (User: {user_id})</b>",
                            parse_mode='HTML'
                        )
                    except Exception:
                        pass
            finally:
                cleanup_user_session(user_id)
                # Đảm bảo cập nhật thời gian ngay cả khi có lỗi
                user_session['last_spam_time'] = time.time()

        user_session['tool_thread'] = threading.Thread(target=run_spam)
        user_session['tool_thread'].start()

    @bot.message_handler(commands=['stop'])
    def stop_command(message):
        user_id = message.from_user.id
        user_session = get_user_session(user_id)

        if not is_user_tool_running(user_id):
            bot.reply_to(message, "ℹ️ Tool của bạn hiện không chạy.")
            return

        set_user_tool_running(user_id, False)
        if user_session['stop_event']:
            user_session['stop_event'].set()

        # Đợi tool thread dừng
        if user_session['tool_thread'] and user_session['tool_thread'].is_alive():
            user_session['tool_thread'].join(timeout=5)

        # Cập nhật thời gian spam cuối khi người dùng dừng thủ công
        user_session['last_spam_time'] = time.time()
        cleanup_user_session(user_id)
        bot.reply_to(message, "⛔ Tool của bạn đã được dừng!")

    @bot.message_handler(commands=['status'])
    def status_command(message):
        user_id = message.from_user.id
        user_session = get_user_session(user_id)

        if is_user_tool_running(user_id):
            status_text = f"🟢 <b>Tool đang chạy (User: {user_id})</b>\n\n"
            if user_session['config']:
                elapsed = time.time() - user_session['config'].start_time
                hours, remainder = divmod(int(elapsed), 3600)
                minutes, seconds = divmod(remainder, 60)
                success_rate = (user_session['config'].successful_requests / (user_session['config'].successful_requests + user_session['config'].failed_requests)) * 100 if (user_session['config'].successful_requests + user_session['config'].failed_requests) > 0 else 0

                status_text += f"⏱️ Runtime: <code>{hours:02d}:{minutes:02d}:{seconds:02d}</code>\n"
                status_text += f"✅ Success: <code>{user_session['config'].successful_requests}</code>\n"
                status_text += f"❌ Failed: <code>{user_session['config'].failed_requests}</code>\n"
                status_text += f"📊 Success Rate: <code>{success_rate:.1f}%</code>\n"
                status_text += f"🎯 Target: <code>{user_session['config'].TARGET_FRIEND_UID}</code>\n"
                status_text += f"👤 Name: <code>{user_session['config'].NAME_TOOL}</code>"
        else:
            status_text = f"🔴 <b>Tool đang dừng (User: {user_id})</b>"

        bot.reply_to(message, status_text, parse_mode='HTML')

    @bot.message_handler(commands=['admin'])
    def admin_command(message):
        user_id = message.from_user.id
        
        if not is_admin(user_id):
            bot.reply_to(message, "❌ Bạn không có quyền sử dụng lệnh này!")
            return
        
        # Thống kê người dùng
        with session_lock:
            total_users = len(user_sessions)
            active_users = sum(1 for session in user_sessions.values() if session['tool_running'])
            users_with_config = sum(1 for session in user_sessions.values() if session['config'] is not None)
            
            # Thống kê theo thời gian (users có hoạt động trong 24h qua)
            current_time = time.time()
            recent_users = sum(1 for session in user_sessions.values() if current_time - session['last_spam_time'] <= 86400 and session['last_spam_time'] > 0)
        
        # Thống kê tổng requests (từ tất cả users active)
        total_success = 0
        total_failed = 0
        for session in user_sessions.values():
            if session['config']:
                total_success += session['config'].successful_requests
                total_failed += session['config'].failed_requests
        
        admin_text = f"""
🔧 <b>ADMIN PANEL - Bot Statistics</b>

👥 <b>User Statistics:</b>
• Total Users: <code>{total_users}</code>
• Active Users: <code>{active_users}</code> (đang chạy tool)
• Users with Config: <code>{users_with_config}</code>
• Recent Users (24h): <code>{recent_users}</code>

📊 <b>Request Statistics:</b>
• Total Success: <code>{total_success}</code>
• Total Failed: <code>{total_failed}</code>
• Success Rate: <code>{(total_success/(total_success+total_failed)*100) if (total_success+total_failed) > 0 else 0:.1f}%</code>

🕒 <b>Uptime:</b>
Bot started at: <code>{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</code>

<b>Admin Commands:</b>
• <code>/admin</code> - Xem thống kê
• <code>/broadcast [message]</code> - Gửi tin nhắn tới tất cả users
• <code>/userlist</code> - Xem danh sách user IDs
"""
        
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("🔄 Refresh", callback_data="admin_refresh"),
            types.InlineKeyboardButton("👥 User List", callback_data="admin_userlist")
        )
        markup.row(
            types.InlineKeyboardButton("📢 Broadcast", callback_data="admin_broadcast")
        )
        
        bot.reply_to(message, admin_text, parse_mode='HTML', reply_markup=markup)

    @bot.message_handler(commands=['broadcast'])
    def broadcast_command(message):
        user_id = message.from_user.id
        
        if not is_admin(user_id):
            bot.reply_to(message, "❌ Bạn không có quyền sử dụng lệnh này!")
            return
        
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            bot.reply_to(message, "❌ Thiếu nội dung tin nhắn!\n\nSử dụng: /broadcast [message]")
            return
        
        broadcast_message = args[1]
        
        # Gửi tin nhắn tới tất cả users đã từng sử dụng bot
        success_count = 0
        error_count = 0
        
        with session_lock:
            user_ids = list(user_sessions.keys())
        
        bot.reply_to(message, f"📢 Đang gửi broadcast tới {len(user_ids)} users...")
        
        for target_user_id in user_ids:
            try:
                bot.send_message(target_user_id, f"📢 <b>Thông báo từ Admin:</b>\n\n{broadcast_message}", parse_mode='HTML')
                success_count += 1
            except Exception as e:
                error_count += 1
        
        result_text = f"✅ Broadcast hoàn thành!\n\n📤 Gửi thành công: {success_count}\n❌ Gửi thất bại: {error_count}"
        bot.send_message(message.chat.id, result_text)

    @bot.message_handler(commands=['userlist'])
    def userlist_command(message):
        user_id = message.from_user.id
        
        if not is_admin(user_id):
            bot.reply_to(message, "❌ Bạn không có quyền sử dụng lệnh này!")
            return
        
        with session_lock:
            if not user_sessions:
                bot.reply_to(message, "📝 Chưa có user nào sử dụng bot.")
                return
            
            user_list = []
            for uid, session in user_sessions.items():
                status = "🟢" if session['tool_running'] else "🔴"
                last_spam = session.get('last_spam_time', 0)
                if last_spam > 0:
                    last_time = datetime.datetime.fromtimestamp(last_spam).strftime('%m-%d %H:%M')
                else:
                    last_time = "Never"
                user_list.append(f"{status} <code>{uid}</code> | Last: {last_time}")
        
        # Chia nhỏ danh sách nếu quá dài
        chunk_size = 20
        for i in range(0, len(user_list), chunk_size):
            chunk = user_list[i:i+chunk_size]
            userlist_text = f"👥 <b>User List ({i+1}-{min(i+chunk_size, len(user_list))}/{len(user_list)}):</b>\n\n"
            userlist_text += "\n".join(chunk)
            bot.send_message(message.chat.id, userlist_text, parse_mode='HTML')

    @bot.message_handler(commands=['help'])
    def help_command(message):
        user_id = message.from_user.id
        
        if is_admin(user_id):
            help_text = """
<b>🔒 zLocket Spam BIGCHANG - Hướng dẫn sử dụng</b>

<b>Các lệnh chính:</b>
• <code>/start</code> - Menu chính
• <code>/spam [target]</code> - Bắt đầu spam
• <code>/stop</code> - Dừng spam
• <code>/status</code> - Kiểm tra trạng thái
• <code>/help</code> - Hướng dẫn này

<b>🔧 Lệnh Admin:</b>
• <code>/admin</code> - Xem thống kê bot
• <code>/broadcast [message]</code> - Gửi thông báo
• <code>/userlist</code> - Danh sách users

<b>Cách sử dụng lệnh /spam:</b>
<code>/spam username123</code>
<code>/spam https://locket.cam/username123</code>

<b>Quy trình spam:</b>
1. Gửi lệnh <code>/spam [target]</code>
2. Bot sẽ yêu cầu nhập tên tùy ý
3. Nhập tên hoặc gửi "default" để dùng tên mặc định
4. Tool sẽ chạy tối thiểu 30 giây

<b>Lưu ý:</b>
• Target có thể là username hoặc link đầy đủ
• Custom name tối đa 30 ký tự
• Cooldown 1 phút giữa các lần spam
• Tool chạy tối thiểu 5 phút mỗi lần
• Tool sẽ tự động random emoji

<b>Liên hệ:</b> @BigChang19
"""
        else:
            help_text = """
<b>🔒 zLocket Spam BIGCHANG - Hướng dẫn sử dụng</b>

<b>Các lệnh chính:</b>
• <code>/start</code> - Menu chính
• <code>/spam [target]</code> - Bắt đầu spam
• <code>/stop</code> - Dừng spam
• <code>/status</code> - Kiểm tra trạng thái
• <code>/help</code> - Hướng dẫn này

<b>Cách sử dụng lệnh /spam:</b>
<code>/spam username123</code>
<code>/spam https://locket.cam/username123</code>

<b>Quy trình spam:</b>
1. Gửi lệnh <code>/spam [target]</code>
2. Bot sẽ yêu cầu nhập tên tùy ý
3. Nhập tên hoặc gửi "default" để dùng tên mặc định
4. Tool sẽ chạy tối thiểu 30 giây

<b>Lưu ý:</b>
• Target có thể là username hoặc link đầy đủ
• Custom name tối đa 30 ký tự
• Cooldown 1 phút giữa các lần spam
• Tool chạy tối thiểu 5 phút mỗi lần
• Tool sẽ tự động random emoji

<b>Liên hệ:</b> @BigChang19
"""
        bot.reply_to(message, help_text, parse_mode='HTML')

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        user_id = call.from_user.id
        
        if call.data == "start_spam":
            bot.send_message(call.message.chat.id, "🚀 Để bắt đầu spam, sử dụng lệnh:\n\n<code>/spam [target]</code>\n\nVí dụ:\n<code>/spam username123</code>\n\nBot sẽ hỏi tên tùy ý sau đó!", parse_mode='HTML')
        elif call.data == "stop_spam":
            stop_command(call.message)
        elif call.data == "status":
            status_command(call.message)
        elif call.data == "help":
            help_command(call.message)
        elif call.data == "admin_refresh" and is_admin(user_id):
            admin_command(call.message)
        elif call.data == "admin_userlist" and is_admin(user_id):
            userlist_command(call.message)
        elif call.data == "admin_broadcast" and is_admin(user_id):
            bot.send_message(call.message.chat.id, "📢 Để gửi broadcast, sử dụng lệnh:\n\n<code>/broadcast [nội dung tin nhắn]</code>\n\nVí dụ:\n<code>/broadcast Chào mừng các bạn sử dụng bot!</code>", parse_mode='HTML')

# Helper functions (giữ nguyên từ code cũ)
def _rand_str_(length=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(length))

def _rand_name_():
    return _rand_str_(8, chars=string.ascii_lowercase)

def _rand_email_():
    return f"{_rand_str_(15)}@thanhdieu.com"

def _rand_pw_():
    return 'zlocket' + _rand_str_(4)

def init_proxy_for_user(user_config):
    """Khởi tạo proxy cho user cụ thể"""
    proxies = load_proxies_for_user(user_config)
    if not proxies:
        user_config._print(f"{xColor.RED}[!] {xColor.YELLOW}Note: Please add proxies to continue running the tool.")
        user_config._loader_("Shutting down system", 1)
        return [], 0
    random.shuffle(proxies)
    user_config._loader_("Optimizing proxy rotation algorithm", 1)
    proxy_queue = Queue()
    for proxy in proxies:
        proxy_queue.put(proxy)
    num_threads = min(len(proxies), 50)  # Giới hạn threads
    user_config._print(f"{xColor.GREEN}[+] {xColor.CYAN}Proxy system initialized with {xColor.WHITE}{num_threads} {xColor.CYAN}endpoints")
    return proxy_queue, num_threads

def load_proxies_for_user(user_config):
    proxies=[]
    proxy_urls=user_config.PROXY_LIST
    user_config._print(
        f"{xColor.MAGENTA}{Style.BRIGHT}[*] {xColor.CYAN}Initializing proxy collection system...")
    try:
        with open('proxy.txt', 'r', encoding='utf-8') as f:
            file_proxies=[line.strip() for line in f if line.strip()]
            user_config._print(
                f"{xColor.MAGENTA}[+] {xColor.GREEN}Found {xColor.WHITE}{len(file_proxies)} {xColor.GREEN}proxies in local storage (proxy.txt)")
            user_config._loader_("Processing local proxies", 1)
            proxies.extend(file_proxies)
    except FileNotFoundError:
        user_config._print(
            f"{xColor.YELLOW}[!] {xColor.RED}No local proxy file detected, trying currently available proxies...")
    for url in proxy_urls:
        try:
            user_config._print(
                f"{xColor.MAGENTA}[*] {xColor.CYAN}Fetching proxies from {xColor.WHITE}{url}")
            user_config._loader_(f"Connecting to {url.split('/')[2]}", 1)
            response=requests.get(url, timeout=user_config.request_timeout)
            response.raise_for_status()
            url_proxies=[line.strip()
                           for line in response.text.splitlines() if line.strip()]
            proxies.extend(url_proxies)
            user_config._print(
                f"{xColor.MAGENTA}[+] {xColor.GREEN}Harvested {xColor.WHITE}{len(url_proxies)} {xColor.GREEN}proxies from {url.split('/')[2]}")
        except requests.exceptions.RequestException as e:
            user_config._print(
                f"{xColor.RED}[!] {xColor.YELLOW}Connection failed: {url.split('/')[2]} - {str(e)}")
    proxies=list(set(proxies))
    if not proxies:
        user_config._print(
            f"{xColor.RED}[!] Warning: No proxies available for operation")
        return []
    user_config.total_proxies=len(proxies)
    user_config._print(
        f"{xColor.GREEN}[+] {xColor.CYAN}Proxy harvesting complete{xColor.WHITE} {len(proxies)} {xColor.CYAN}unique proxies loaded")
    return proxies

def load_proxies():
    """Deprecated function - use load_proxies_for_user instead"""
    pass

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

def step1_create_account_for_user(thread_id, proxy_queue, stop_event, user_config):
    """Tạo account cho user cụ thể"""
    while not stop_event.is_set():
        current_proxy=get_proxy(proxy_queue, thread_id, stop_event)
        proxies_dict=format_proxy(current_proxy)
        proxy_usage_count=0
        failed_attempts=0
        max_failed_attempts=10
        if not current_proxy or stop_event.is_set():
            user_config._print(
                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.RED}[!] Thread stopping...")
            break
        user_config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.GREEN}● Thread activated with proxy: {xColor.YELLOW}{current_proxy}")

        while not stop_event.is_set() and proxy_usage_count < user_config.ACCOUNTS_PER_PROXY and failed_attempts < max_failed_attempts:
            if stop_event.is_set():
                return
            if not current_proxy:
                current_proxy=get_proxy(proxy_queue, thread_id, stop_event)
                proxies_dict=format_proxy(current_proxy)
                if not current_proxy:
                    user_config._print(
                        f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.RED}[!] Proxy unavailable, will try again")
                    break
                user_config._print(
                    f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.GREEN}● Switching to new proxy: {xColor.YELLOW}{current_proxy}")

            prefix=f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Register{Style.RESET_ALL}]"
            email=_rand_email_()
            password=_rand_pw_()
            user_config._print(
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
            response_data=user_config.excute(
                f"{user_config.API_BASE_URL}/createAccountWithEmailPassword",
                headers=user_config.headers_locket(),
                payload=payload,
                thread_id=thread_id,
                step="Register",
                proxies_dict=proxies_dict
            )
            if stop_event.is_set():
                return
            if response_data == "proxy_dead":
                user_config._print(
                    f"{prefix} {xColor.RED}[!] Proxy terminated, acquiring new endpoint")
                current_proxy=None
                failed_attempts+=1
                continue
            if response_data == "too_many_requests":
                user_config._print(
                    f"{prefix} {xColor.RED}[!] Connection throttled, switching endpoint")
                current_proxy=None
                failed_attempts+=1
                continue
            if isinstance(response_data, dict) and response_data.get('result', {}).get('status') == 200:
                user_config._print(
                    f"{prefix} {xColor.GREEN}[✓] Identity created: {xColor.YELLOW}{email}")
                proxy_usage_count+=1
                failed_attempts=0
                if stop_event.is_set():
                    return
                id_token=step1b_sign_in_for_user(
                    email, password, thread_id, proxies_dict, user_config)
                if stop_event.is_set():
                    return
                if id_token:
                    if step2_finalize_user_for_user(id_token, thread_id, proxies_dict, user_config):
                        if stop_event.is_set():
                            return
                        first_request_success=step3_send_friend_request_for_user(
                            id_token, thread_id, proxies_dict, user_config)
                        if first_request_success:
                            user_config._print(
                                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Boost{Style.RESET_ALL}] {xColor.YELLOW}🚀 Boosting friend requests: Sending 50 more requests")
                            for _ in range(50):
                                if stop_event.is_set():
                                    return
                                step3_send_friend_request_for_user(
                                    id_token, thread_id, proxies_dict, user_config)
                            user_config._print(
                                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Boost{Style.RESET_ALL}] {xColor.GREEN}[✓] Boost complete: 101 total requests sent")
                    else:
                        user_config._print(
                            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Auth{Style.RESET_ALL}] {xColor.RED}[✗] Authentication failure")
                else:
                    user_config._print(
                        f"{prefix} {xColor.RED}[✗] Identity creation failed")
                failed_attempts+=1
        if failed_attempts >= max_failed_attempts:
            user_config._print(
                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.RED}[!] Thread restarting: Excessive failures ({failed_attempts})")
        else:
            user_config._print(
                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.YELLOW}● Proxy limit reached ({proxy_usage_count}/{user_config.ACCOUNTS_PER_PROXY}), getting new proxy")

def step1b_sign_in_for_user(email, password, thread_id, proxies_dict, user_config):
    if not email or not password:
        user_config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Auth{Style.RESET_ALL}] {xColor.RED}[✗] Authentication failed: Invalid credentials")
        return None
    payload={
        "email": email,
        "password": password,
        "clientType": "CLIENT_TYPE_IOS",
        "returnSecureToken": True
    }
    vtd=user_config.excute(
        f"{user_config.FIREBASE_AUTH_URL}/verifyPassword?key={user_config.FIREBASE_API_KEY}",
        headers=user_config.firebase_headers_locket(),
        payload=payload,
        thread_id=thread_id,
        step="Auth",
        proxies_dict=proxies_dict
    )
    if vtd and 'idToken' in vtd:
        user_config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Auth{Style.RESET_ALL}] {xColor.GREEN}[✓] Authentication successful")
        return vtd.get('idToken')
    user_config._print(
        f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Auth{Style.RESET_ALL}] {xColor.RED}[✗] Authentication failed")
    return None

def step2_finalize_user_for_user(id_token, thread_id, proxies_dict, user_config):
    if not id_token:
        user_config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Profile{Style.RESET_ALL}] {xColor.RED}[✗] Profile creation failed: Invalid token")
        return False
    first_name=user_config.NAME_TOOL
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
    headers=user_config.headers_locket()
    headers['Authorization']=f"Bearer {id_token}"
    result=user_config.excute(
        f"{user_config.API_BASE_URL}/finalizeTemporaryUser",
        headers=headers,
        payload=payload,
        thread_id=thread_id,
        step="Profile",
        proxies_dict=proxies_dict
    )
    if result:
        user_config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Profile{Style.RESET_ALL}] {xColor.GREEN}[✓] Profile created: {xColor.YELLOW}{username}")
        return True
    user_config._print(
        f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Profile{Style.RESET_ALL}] {xColor.RED}[✗] Profile creation failed")
    return False

def step3_send_friend_request_for_user(id_token, thread_id, proxies_dict, user_config):
    if not id_token:
        user_config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Friend{Style.RESET_ALL}] {xColor.RED}[✗] Connection failed: Invalid token")
        return False
    payload={
        "data": {
            "user_uid": user_config.TARGET_FRIEND_UID,
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
    headers=user_config.headers_locket()
    headers['Authorization']=f"Bearer {id_token}"
    result=user_config.excute(
        f"{user_config.API_BASE_URL}/sendFriendRequest",
        headers=headers,
        payload=payload,
        thread_id=thread_id,
        step="Friend",
        proxies_dict=proxies_dict
    )
    if result:
        user_config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Friend{Style.RESET_ALL}] {xColor.GREEN}[✓] Connection established with target")
        return True
    user_config._print(
        f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL} | {xColor.MAGENTA}Friend{Style.RESET_ALL}] {xColor.RED}[✗] Connection failed")
    return False

def step1_create_account(thread_id, proxy_queue, stop_event):
    while not stop_event.is_set() and tool_running:
        current_proxy=get_proxy(proxy_queue, thread_id, stop_event)
        proxies_dict=format_proxy(current_proxy)
        proxy_usage_count=0
        failed_attempts=0
        max_failed_attempts=10
        if not current_proxy or stop_event.is_set() or not tool_running:
            config._print(
                f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.RED}[!] Thread stopping...")
            break
        config._print(
            f"[{xColor.CYAN}Thread-{thread_id:03d}{Style.RESET_ALL}] {xColor.GREEN}● Thread activated with proxy: {xColor.YELLOW}{current_proxy}")

        while not stop_event.is_set() and tool_running and proxy_usage_count < config.ACCOUNTS_PER_PROXY and failed_attempts < max_failed_attempts:
            if stop_event.is_set() or not tool_running:
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
    BOT_TOKEN = "7602313290:AAHsT87l1mlXNIW5FtHTe8oPTtf-kUPIQZY"

    bot = telebot.TeleBot(BOT_TOKEN)

    # Setup bot handlers after bot initialization
    setup_bot_handlers()

    print(f"🤖 Bot đang khởi động...")
    print(f"📱 Token: {BOT_TOKEN[:10]}...")
    
    # Test bot connection first
    try:
        bot_info = bot.get_me()
        print(f"✅ Kết nối thành công! Bot: @{bot_info.username}")
        print(f"📱 Gửi /start cho bot để bắt đầu sử dụng")
    except telebot.apihelper.ApiTelegramException as e:
        if "409" in str(e):
            print("❌ CẢNH BÁO: Có instance khác của bot đang chạy!")
            print("⛔ Dừng bot này để tránh xung đột...")
            sys.exit(1)
        else:
            print(f"❌ Lỗi kết nối bot: {e}")
            sys.exit(1)

    try:
        # First, try to clear any existing webhooks
        try:
            bot.remove_webhook()
            print("🔄 Đã xóa webhook cũ (nếu có)")
            time.sleep(2)  # Wait a bit before starting polling
        except Exception:
            pass
        
        # Try to stop any existing polling
        try:
            bot.stop_polling()
            time.sleep(2)
        except Exception:
            pass
            
        print("🚀 Đang bắt đầu polling...")
        bot.polling(none_stop=True, restart_on_change=False, timeout=30, long_polling_timeout=20)
        
    except telebot.apihelper.ApiTelegramException as e:
        if "409" in str(e) or "Conflict" in str(e):
            print("\n❌ Lỗi 409: Có bot instance khác đang chạy!")
            print("🔄 Đang thử khởi động lại sau 30 giây...")
            time.sleep(30)
            
            # Try one more time with webhook approach
            try:
                print("🔄 Thử sử dụng webhook thay vì polling...")
                bot.remove_webhook()
                time.sleep(3)
                
                # Use webhook for deployment environment
                from flask import Flask, request
                app = Flask(__name__)
                
                @app.route(f"/{BOT_TOKEN}", methods=['POST'])
                def webhook():
                    json_str = request.get_data().decode('UTF-8')
                    update = telebot.types.Update.de_json(json_str)
                    bot.process_new_updates([update])
                    return '', 200
                
                @app.route('/')
                def index():
                    return "Bot is running!"
                
                # Set webhook
                webhook_url = f"https://{os.environ.get('REPL_SLUG', 'your-repl')}-{os.environ.get('REPL_OWNER', 'your-username')}.replit.app/{BOT_TOKEN}"
                bot.set_webhook(url=webhook_url)
                print(f"✅ Webhook đã được thiết lập: {webhook_url}")
                
                app.run(host='0.0.0.0', port=5000, debug=False)
                
            except Exception as webhook_error:
                print(f"❌ Lỗi webhook: {webhook_error}")
                print("💡 Giải pháp:")
                print("   1. Đợi 2-3 phút rồi restart repl")
                print("   2. Hoặc sử dụng token bot khác")
                print("   3. Kiểm tra xem có repl nào khác đang chạy bot này không")
        else:
            print(f"\n❌ Lỗi bot: {e}")
            print("🔄 Thử lại sau 10 giây...")
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n⛔ Bot đã dừng!")
        # Cleanup user sessions
        for user_id in list(user_sessions.keys()):
            user_session = user_sessions[user_id]
            if user_session.get('tool_running'):
                user_session['tool_running'] = False
                if user_session.get('stop_event'):
                    user_session['stop_event'].set()
                    
    except Exception as e:
        print(f"\n❌ Lỗi không xác định: {e}")
        print("🔄 Sẽ thử khởi động lại...")
        
    finally:
        print("🔄 Bot đã thoát hoàn toàn")
