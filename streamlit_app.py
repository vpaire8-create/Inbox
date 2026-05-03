import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import uuid
import hashlib
import os
import json
import urllib.parse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import database as db

# ⚜️ PAGE CONFIG ⚜️
st.set_page_config(
    page_title="👑 SYAPA KING INBOX",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ⚜️ ROYAL THEME CSS ⚜️
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700;900&family=Great+Vibes&family=Playfair+Display:wght@400;700&display=swap');

    * { font-family: 'Playfair Display', serif; }

    .stApp {
        background: linear-gradient(135deg, #0a0014 0%, #1a0033 30%, #2d0055 60%, #0a0014 100%);
        background-attachment: fixed;
    }

    .main .block-container {
        background: rgba(20, 5, 40, 0.75);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 35px;
        border: 3px solid rgba(255, 215, 0, 0.5);
        box-shadow: 0 20px 60px rgba(255, 215, 0, 0.2);
    }

    .royal-header {
        background: linear-gradient(135deg, #1a0033, #4b0082, #2a0055);
        border: 3px solid #ffd700;
        border-radius: 25px;
        padding: 2.5rem;
        text-align: center;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.8), 0 0 40px rgba(255,215,0,0.3);
        position: relative;
        overflow: hidden;
    }

    .royal-header::before {
        content: "👑";
        position: absolute;
        top: -45px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 7rem;
        opacity: 0.12;
        animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateX(-50%) translateY(0); }
        50% { transform: translateX(-50%) translateY(-15px); }
    }

    .royal-header h1 {
        background: linear-gradient(90deg, #ffd700, #ffeb3b, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Cinzel Decorative', cursive;
        font-size: 3.5rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 0 30px rgba(255,215,0,0.7);
        letter-spacing: 3px;
    }

    .royal-header p {
        color: #d4af37;
        font-family: 'Great Vibes', cursive;
        font-size: 1.9rem;
        margin-top: 0.8rem;
        letter-spacing: 2px;
    }

    .prince-logo {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        margin-bottom: 20px;
        border: 4px solid #ffd700;
        box-shadow: 0 0 40px rgba(255,215,0,0.9), inset 0 0 20px rgba(255,255,255,0.3);
        animation: glow 2s infinite;
    }

    @keyframes glow {
        0%, 100% { box-shadow: 0 0 40px rgba(255,215,0,0.9); }
        50% { box-shadow: 0 0 70px rgba(255,215,0,1); }
    }

    .stButton>button {
        background: linear-gradient(45deg, #b8860b, #ffd700, #daa520);
        color: #1a0033;
        border: 2px solid #b8860b;
        border-radius: 16px;
        padding: 1rem 2.5rem;
        font-family: 'Cinzel Decorative', cursive;
        font-weight: 700;
        font-size: 1.2rem;
        transition: all 0.4s;
        box-shadow: 0 8px 25px rgba(255,215,0,0.45);
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-5px) scale(1.03);
        box-shadow: 0 15px 40px rgba(255,215,0,0.8);
        background: linear-gradient(45deg, #ffd700, #ffeb3b, #ffd700);
    }

    .login-btn>button {
        background: linear-gradient(45deg, #1877f2, #4267b2, #1877f2) !important;
        color: white !important;
        border: 2px solid #1877f2 !important;
    }

    .stop-btn>button {
        background: linear-gradient(45deg, #8b0000, #ff0000, #8b0000) !important;
        color: white !important;
        border: 2px solid #ff0000 !important;
    }

    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        background: rgba(30, 10, 60, 0.85);
        border: 2px solid #b8860b;
        border-radius: 14px;
        color: #ffd700;
        padding: 1rem;
        font-size: 1.1rem;
    }

    .stTextInput>div>div>input:focus {
        border-color: #ffd700;
        box-shadow: 0 0 20px rgba(255,215,0,0.5);
    }

    label {
        color: #ffd700 !important;
        font-weight: 600 !important;
        font-size: 1.15rem !important;
        text-shadow: 1px 1px 3px #000;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: rgba(20, 5, 40, 0.8);
        border-radius: 16px;
        padding: 10px;
        border: 2px solid #b8860b;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(75, 0, 130, 0.6);
        color: #d4af37;
        border-radius: 12px;
        padding: 14px 26px;
        font-weight: 700;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #b8860b, #ffd700);
        color: #1a0033;
        font-weight: 900;
    }

    [data-testid="stMetricValue"] {
        color: #ffd700;
        font-size: 2.6rem;
        font-weight: 900;
        text-shadow: 0 0 20px rgba(255,215,0,0.7);
    }

    [data-testid="stMetricLabel"] {
        color: #d4af37;
    }

    [data-testid="stMetric"] {
        background: rgba(30, 10, 60, 0.7);
        border: 2px solid #b8860b;
        border-radius: 15px;
        padding: 15px;
    }

    .console-output {
        background: #000000;
        border: 2px solid #4b0082;
        border-radius: 14px;
        padding: 20px;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        max-height: 450px;
        overflow-y: auto;
        box-shadow: inset 0 0 20px rgba(0,255,0,0.1);
    }

    .console-line {
        padding: 8px 14px;
        margin: 5px 0;
        border-left: 4px solid #ffd700;
        background: rgba(0,30,0,0.5);
        border-radius: 5px;
    }

    .login-status {
        padding: 15px 20px;
        border-radius: 12px;
        margin: 10px 0;
        font-weight: 700;
        text-align: center;
    }

    .login-success {
        background: linear-gradient(135deg, #006400, #228b22);
        border: 2px solid #00ff00;
        color: white;
    }

    .login-failed {
        background: linear-gradient(135deg, #8b0000, #ff0000);
        border: 2px solid #ff4444;
        color: white;
    }

    .footer {
        background: rgba(30, 10, 60, 0.8);
        border-top: 3px solid #b8860b;
        color: #d4af37;
        font-family: 'Great Vibes', cursive;
        font-size: 1.6rem;
        padding: 2.5rem;
        text-align: center;
        margin-top: 20px;
    }

    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0a0014; }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(#8b0000, #b8860b, #ffd700);
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ⚜️ CONSTANTS ⚜️
ADMIN_PASSWORD = "SYAPA_KING"
WHATSAPP_NUMBER = "+92364234209"
APPROVAL_FILE = "approved_keys.json"
PENDING_FILE = "pending_approvals.json"
ADMIN_UID = "Xmarty.Ayush.King.70"

# ⚜️ KEY GENERATION ⚜️
def generate_user_key(username, password):
    combined = f"{username}:{password}"
    key_hash = hashlib.sha256(combined.encode()).hexdigest()[:8].upper()
    return f"KEY-{key_hash}"

# ⚜️ APPROVAL SYSTEM ⚜️
def load_approved_keys():
    if os.path.exists(APPROVAL_FILE):
        try:
            with open(APPROVAL_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_approved_keys(keys):
    with open(APPROVAL_FILE, 'w') as f:
        json.dump(keys, f, indent=2)

def load_pending_approvals():
    if os.path.exists(PENDING_FILE):
        try:
            with open(PENDING_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_pending_approvals(pending):
    with open(PENDING_FILE, 'w') as f:
        json.dump(pending, f, indent=2)

def send_whatsapp_message(user_name, approval_key):
    message = f"👑 HELLO SYAPA KING SIR PLEASE 👑👑\nMy name is {user_name}\nPlease approve my key:\n🔑 {approval_key}"
    encoded_message = urllib.parse.quote(message)
    whatsapp_url = f"https://api.whatsapp.com/send?phone={WHATSAPP_NUMBER}&text={encoded_message}"
    return whatsapp_url

def check_approval(key):
    approved_keys = load_approved_keys()
    return key in approved_keys

# ⚜️ SESSION STATE ⚜️
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_key' not in st.session_state:
    st.session_state.user_key = None
if 'key_approved' not in st.session_state:
    st.session_state.key_approved = False
if 'approval_status' not in st.session_state:
    st.session_state.approval_status = 'not_requested'
if 'whatsapp_opened' not in st.session_state:
    st.session_state.whatsapp_opened = False
if 'fb_login_status' not in st.session_state:
    st.session_state.fb_login_status = None
if 'fb_login_message' not in st.session_state:
    st.session_state.fb_login_message = ""
if 'automation_running' not in st.session_state:
    st.session_state.automation_running = False
if 'messages_sent' not in st.session_state:
    st.session_state.messages_sent = 0
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'driver' not in st.session_state:
    st.session_state.driver = None

# ⚜️ LOG FUNCTION ⚜️
def add_log(msg, msg_type='info'):
    timestamp = time.strftime("%H:%M:%S")
    if msg_type == 'success':
        prefix = "✅"
    elif msg_type == 'error':
        prefix = "❌"
    else:
        prefix = "🔹"
    st.session_state.logs.append(f"[{timestamp}] {prefix} {msg}")

# ⚜️ SELENIUM SETUP ⚜️
def setup_chrome():
    add_log("Setting up Chrome browser...")
    
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    chromium_paths = ['/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/google-chrome', '/usr/bin/chrome']
    
    for path in chromium_paths:
        if Path(path).exists():
            options.binary_location = path
            add_log(f"Found Chromium: {path}", 'success')
            break
    
    driver_paths = ['/usr/bin/chromedriver', '/usr/local/bin/chromedriver']
    driver_path = None
    
    for path in driver_paths:
        if Path(path).exists():
            driver_path = path
            add_log(f"Found ChromeDriver: {path}", 'success')
            break
    
    try:
        if driver_path:
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=options)
        else:
            driver = webdriver.Chrome(options=options)
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.set_window_size(1920, 1080)
        add_log("Chrome browser ready!", 'success')
        return driver
    except Exception as e:
        add_log(f"Browser setup failed: {e}", 'error')
        return None

# ⚜️ FACEBOOK LOGIN ⚜️
def facebook_login(driver, email, password):
    add_log("Opening Facebook login page...")
    
    try:
        driver.get('https://www.facebook.com/')
        time.sleep(5)
        
        # Accept cookies
        try:
            buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Allow') or contains(text(), 'Accept')]")
            for btn in buttons:
                try:
                    if btn.is_displayed():
                        btn.click()
                        time.sleep(2)
                        break
                except:
                    pass
        except:
            pass
        
        add_log("Entering email...")
        email_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_field.clear()
        email_field.send_keys(email)
        add_log("Email entered ✓", 'success')
        
        add_log("Entering password...")
        password_field = driver.find_element(By.ID, "pass")
        password_field.clear()
        password_field.send_keys(password)
        add_log("Password entered ✓", 'success')
        
        add_log("Clicking Login button...")
        login_btn = driver.find_element(By.NAME, "login")
        login_btn.click()
        
        time.sleep(10)
        
        current_url = driver.current_url
        
        if "checkpoint" in current_url:
            add_log("Facebook security checkpoint detected!", 'error')
            return False, "Security Checkpoint - Please verify from your phone"
        
        if "login" in current_url or "login_attempt" in current_url:
            add_log("Login failed - Check credentials", 'error')
            return False, "Login Failed - Wrong Email or Password"
        
        add_log("🎉 FACEBOOK LOGIN SUCCESSFUL! 👑", 'success')
        return True, "Login Successful! ✅"
        
    except TimeoutException:
        add_log("Timeout - Facebook page not loading", 'error')
        return False, "Timeout - Facebook not responding"
    except Exception as e:
        add_log(f"Login error: {str(e)[:100]}", 'error')
        return False, f"Error: {str(e)[:50]}"

# ⚜️ FIND MESSAGE INPUT ⚜️
def find_message_box(driver):
    add_log("Searching for message input box...")
    time.sleep(8)
    
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    except:
        pass
    
    selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        '[role="textbox"][contenteditable="true"]',
        '[contenteditable="true"]',
        'textarea'
    ]
    
    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for elem in elements:
                try:
                    if elem.is_displayed() and elem.is_enabled():
                        elem.click()
                        time.sleep(0.5)
                        add_log("✅ Message input box found!", 'success')
                        return elem
                except:
                    continue
        except:
            continue
    
    add_log("Message input box NOT found!", 'error')
    return None

# ⚜️ SEND ONE MESSAGE ⚜️
def send_one_message(driver, message_box, message, index):
    try:
        # Type the message
        driver.execute_script("""
            var el = arguments[0];
            var msg = arguments[1];
            el.focus();
            el.click();
            el.textContent = msg;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        """, message_box, message)
        
        time.sleep(1.5)
        
        # Try clicking send button
        sent = driver.execute_script("""
            var btns = document.querySelectorAll('[aria-label*="Send"]');
            for (var i = 0; i < btns.length; i++) {
                if (btns[i].offsetParent !== null) {
                    btns[i].click();
                    return true;
                }
            }
            return false;
        """)
        
        if not sent:
            # Use Enter key
            message_box.send_keys(Keys.ENTER)
        
        add_log(f"Message #{index} sent! 👑", 'success')
        return True
        
    except Exception as e:
        add_log(f"Error sending message #{index}: {str(e)[:60]}", 'error')
        return False

# ⚜️ MAIN AUTOMATION ⚜️
def run_automation(email, password, link, messages, delay, prefix):
    driver = None
    
    try:
        add_log("=" * 50)
        add_log("🚀 STARTING AUTOMATION...", 'success')
        add_log("=" * 50)
        
        # Setup browser
        driver = setup_chrome()
        if not driver:
            return
        
        # Login
        login_ok, login_msg = facebook_login(driver, email, password)
        
        if not login_ok:
            st.session_state.fb_login_status = False
            st.session_state.fb_login_message = login_msg
            driver.quit()
            return
        
        st.session_state.fb_login_status = True
        st.session_state.fb_login_message = login_msg
        
        # Open inbox link
        add_log(f"Opening inbox link...")
        driver.get(link)
        time.sleep(10)
        add_log(f"Inbox opened!", 'success')
        
        # Find message box
        message_box = find_message_box(driver)
        
        if not message_box:
            add_log("Cannot find message box! Exiting.", 'error')
            driver.quit()
            return
        
        # Send messages
        add_log(f"Starting to send {len(messages)} messages...")
        add_log(f"Delay: {delay} seconds")
        add_log(f"Prefix: {prefix if prefix else 'None'}")
        
        sent_count = 0
        
        while st.session_state.automation_running and sent_count < len(messages):
            msg = messages[sent_count]
            
            if prefix:
                full_msg = f"{prefix} {msg}"
            else:
                full_msg = msg
            
            success = send_one_message(driver, message_box, full_msg, sent_count + 1)
            
            if success:
                sent_count += 1
                st.session_state.messages_sent = sent_count
                add_log(f"Waiting {delay} seconds...")
                time.sleep(delay)
            else:
                add_log("Retrying in 5 seconds...", 'error')
                time.sleep(5)
                
                # Re-find message box
                message_box = find_message_box(driver)
                if not message_box:
                    add_log("Lost message box! Stopping.", 'error')
                    break
        
        add_log("=" * 50)
        add_log(f"🏁 AUTOMATION COMPLETE! Total sent: {sent_count}", 'success')
        add_log("=" * 50)
        
    except Exception as e:
        add_log(f"FATAL ERROR: {str(e)}", 'error')
    finally:
        if driver:
            try:
                driver.quit()
                add_log("Browser closed", 'success')
            except:
                pass
        st.session_state.automation_running = False

# ⚜️ START/STOP ⚜️
def start_automation():
    if st.session_state.automation_running:
        add_log("Automation is already running!", 'error')
        return
    
    st.session_state.automation_running = True
    st.session_state.messages_sent = 0
    st.session_state.logs = []
    st.session_state.fb_login_status = None
    st.session_state.fb_login_message = ""
    
    email = st.session_state.get('fb_email', '')
    password = st.session_state.get('fb_password', '')
    link = st.session_state.get('message_link', '')
    messages = st.session_state.get('messages_list', ['Hello!'])
    delay = st.session_state.get('delay', 5)
    prefix = st.session_state.get('name_prefix', '')
    
    thread = threading.Thread(target=run_automation, args=(email, password, link, messages, delay, prefix))
    thread.daemon = True
    thread.start()
    add_log("Automation thread started!", 'success')

def stop_automation():
    st.session_state.automation_running = False
    add_log("⏹️ STOP signal sent!", 'error')

# ⚜️ ADMIN PANEL ⚜️
def admin_panel():
    st.markdown("""
    <div class="royal-header">
        <img src="https://i.ibb.co/8ghMsS2q/538a21e43b48.jpg" class="prince-logo">
        <h1>👑 ADMIN PANEL 👑</h1>
        <p>KEY APPROVAL MANAGEMENT</p>
    </div>
    """, unsafe_allow_html=True)
    
    pending = load_pending_approvals()
    approved_keys = load_approved_keys()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("✅ Approved Keys", len(approved_keys))
    with col2:
        st.metric("⏳ Pending", len(pending))
    
    st.markdown("---")
    
    if pending:
        st.markdown("### 📋 Pending Requests")
        for key, info in pending.items():
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.text(f"👤 {info['name']}")
            with col2:
                st.text(f"🔑 {key}")
            with col3:
                if st.button("✅", key=f"app_{key}"):
                    approved_keys[key] = info
                    save_approved_keys(approved_keys)
                    del pending[key]
                    save_pending_approvals(pending)
                    st.success(f"Approved {info['name']}!")
                    st.rerun()
    else:
        st.info("No pending approvals")
    
    if approved_keys:
        st.markdown("### ✅ Approved Keys")
        for key, info in approved_keys.items():
            st.text(f"👤 {info['name']} - 🔑 {key}")
    
    if st.button("🚪 Logout"):
        st.session_state.approval_status = 'login'
        st.rerun()

# ⚜️ APPROVAL PAGE ⚜️
def approval_request_page(user_key, username):
    st.markdown("""
    <div class="royal-header">
        <img src="https://i.ibb.co/8ghMsS2q/538a21e43b48.jpg" class="prince-logo">
        <h1>🔐 PREMIUM KEY APPROVAL</h1>
        <p>ONE MONTH 500 RS PAID</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.approval_status == 'not_requested':
        st.markdown("### 📝 Request Access")
        st.info(f"**Your Key:** `{user_key}`")
        st.info(f"**Username:** {username}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Request Approval", use_container_width=True):
                pending = load_pending_approvals()
                pending[user_key] = {"name": username, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
                save_pending_approvals(pending)
                st.session_state.approval_status = 'pending'
                st.rerun()
        with col2:
            if st.button("🔐 Admin Panel", use_container_width=True):
                st.session_state.approval_status = 'admin_login'
                st.rerun()
    
    elif st.session_state.approval_status == 'pending':
        st.warning("⏳ Pending Approval...")
        
        whatsapp_url = send_whatsapp_message(username, user_key)
        
        if not st.session_state.whatsapp_opened:
            components.html(f"""<script>setTimeout(function(){{window.open('{whatsapp_url}','_blank');}}, 500);</script>""", height=0)
            st.session_state.whatsapp_opened = True
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Check Status", use_container_width=True):
                if check_approval(user_key):
                    st.session_state.key_approved = True
                    st.session_state.approval_status = 'approved'
                    st.success("✅ Approved!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Not approved yet!")
        with col2:
            if st.button("⬅️ Back", use_container_width=True):
                st.session_state.approval_status = 'not_requested'
                st.session_state.whatsapp_opened = False
                st.rerun()
    
    elif st.session_state.approval_status == 'admin_login':
        st.markdown("### 🔐 Admin Login")
        admin_pass = st.text_input("Admin Password:", type="password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔓 Login", use_container_width=True):
                if admin_pass == ADMIN_PASSWORD:
                    st.session_state.approval_status = 'admin_panel'
                    st.rerun()
                else:
                    st.error("Wrong password!")
        with col2:
            if st.button("⬅️ Back", use_container_width=True):
                st.session_state.approval_status = 'not_requested'
                st.rerun()
    
    elif st.session_state.approval_status == 'admin_panel':
        admin_panel()

# ⚜️ LOGIN PAGE ⚜️
def login_page():
    st.markdown("""
    <div class="royal-header">
        <img src="https://i.ibb.co/8ghMsS2q/538a21e43b48.jpg" class="prince-logo">
        <h1>👑 SYAPA KING 👑</h1>
        <p>Seven Billion Smiles In This World But Your's Is My Favorite ✨</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Login", "✨ Sign Up"])
    
    with tab1:
        st.markdown("### Welcome Back!")
        username = st.text_input("Username", key="login_username", placeholder="Enter username")
        password = st.text_input("Password", key="login_password", type="password", placeholder="Enter password")
        
        if st.button("🚀 Login", key="login_btn", use_container_width=True):
            if username and password:
                user_id = db.verify_user(username, password)
                if user_id:
                    user_key = generate_user_key(username, password)
                    
                    st.session_state.logged_in = True
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.session_state.user_key = user_key
                    
                    if check_approval(user_key):
                        st.session_state.key_approved = True
                        st.session_state.approval_status = 'approved'
                    else:
                        st.session_state.key_approved = False
                        st.session_state.approval_status = 'not_requested'
                    
                    st.success(f"👑 Welcome, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials!")
            else:
                st.warning("Fill all fields!")
    
    with tab2:
        st.markdown("### Create Account")
        new_user = st.text_input("Username", key="signup_username", placeholder="Choose username")
        new_pass = st.text_input("Password", key="signup_password", type="password", placeholder="Create password")
        confirm_pass = st.text_input("Confirm Password", key="confirm_pass", type="password", placeholder="Confirm password")
        
        if st.button("👑 Create Account", key="signup_btn", use_container_width=True):
            if new_user and new_pass and confirm_pass:
                if new_pass == confirm_pass:
                    success, msg = db.create_user(new_user, new_pass)
                    if success:
                        st.success(f"✅ {msg}")
                    else:
                        st.error(f"❌ {msg}")
                else:
                    st.error("Passwords don't match!")
            else:
                st.warning("Fill all fields!")

# ⚜️ MAIN APP ⚜️
def main_app():
    st.markdown("""
    <div class="royal-header">
        <img src="https://i.ibb.co/8ghMsS2q/538a21e43b48.jpg" class="prince-logo">
        <h1>👑 SYAPA KING INBOX 👑</h1>
        <p>Royal Automation System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👑 {st.session_state.username}")
        st.markdown(f"**Key:** `{st.session_state.user_key}`")
        st.success("✅ Approved")
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            if st.session_state.automation_running:
                stop_automation()
            for key in ['logged_in', 'user_id', 'username', 'user_key', 'key_approved', 'automation_running', 'fb_login_status']:
                if key in st.session_state:
                    st.session_state[key] = False if key in ['logged_in', 'key_approved', 'automation_running'] else None
            st.session_state.approval_status = 'not_requested'
            st.rerun()
    
    tab1, tab2 = st.tabs(["⚙️ CONFIGURATION", "🚀 AUTOMATION"])
    
    with tab1:
        st.markdown("### 📧 FACEBOOK LOGIN")
        st.markdown("*Real Facebook login with email & password*")
        
        col1, col2 = st.columns(2)
        with col1:
            fb_email = st.text_input("📧 Facebook Email or Phone", 
                                     value=st.session_state.get('fb_email', ''),
                                     placeholder="your@email.com or phone number")
        with col2:
            fb_password = st.text_input("🔒 Facebook Password",
                                        value=st.session_state.get('fb_password', ''),
                                        placeholder="Your Facebook password",
                                        type="password")
        
        # Login status display
        if st.session_state.fb_login_status == True:
            st.markdown(f'<div class="login-status login-success">✅ {st.session_state.fb_login_message}</div>', unsafe_allow_html=True)
        elif st.session_state.fb_login_status == False:
            st.markdown(f'<div class="login-status login-failed">❌ {st.session_state.fb_login_message}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🎯 INBOX SETTINGS")
        
        message_link = st.text_input("🔗 Full Message Link",
                                     value=st.session_state.get('message_link', ''),
                                     placeholder="https://web.facebook.com/messages/e2ee/t/825136373513772")
        
        name_prefix = st.text_input("✍️ Hater Name (Prefix)",
                                    value=st.session_state.get('name_prefix', ''),
                                    placeholder="[END TO END]")
        
        delay = st.number_input("⏱️ Delay Between Messages (seconds)", 
                                min_value=1, max_value=300,
                                value=st.session_state.get('delay', 5))
        
        st.markdown("---")
        st.markdown("### 📂 UPLOAD MESSAGE FILE")
        
        uploaded_file = st.file_uploader("📁 Choose .txt file (one message per line)", type=['txt'])
        
        if uploaded_file:
            try:
                content = uploaded_file.read().decode('utf-8')
                st.session_state.messages_list = [line.strip() for line in content.split('\n') if line.strip()]
                st.success(f"✅ Loaded {len(st.session_state.messages_list)} messages!")
                
                with st.expander("👁️ Preview"):
                    for i, m in enumerate(st.session_state.messages_list[:10]):
                        st.text(f"{i+1}. {m}")
                    if len(st.session_state.messages_list) > 10:
                        st.text(f"... +{len(st.session_state.messages_list)-10} more")
            except:
                st.error("Error reading file!")
        else:
            if 'messages_list' not in st.session_state:
                st.session_state.messages_list = []
        
        if st.button("💾 SAVE CONFIGURATION", use_container_width=True):
            st.session_state.fb_email = fb_email
            st.session_state.fb_password = fb_password
            st.session_state.message_link = message_link
            st.session_state.name_prefix = name_prefix
            st.session_state.delay = delay
            st.success("✅ Saved!")
    
    with tab2:
        st.markdown("### 🚀 AUTOMATION CONTROL")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📨 Messages Sent", st.session_state.messages_sent)
        with col2:
            status_text = "🟢 RUNNING" if st.session_state.automation_running else "🔴 STOPPED"
            st.metric("📡 Status", status_text)
        with col3:
            loaded = len(st.session_state.get('messages_list', []))
            st.metric("📝 Loaded", loaded)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 START AUTOMATION", 
                        disabled=st.session_state.automation_running,
                        use_container_width=True):
                if not st.session_state.get('fb_email'):
                    st.error("Set Facebook Email first!")
                elif not st.session_state.get('fb_password'):
                    st.error("Set Facebook Password first!")
                elif not st.session_state.get('message_link'):
                    st.error("Set Message Link first!")
                elif not st.session_state.get('messages_list'):
                    st.error("Upload message file first!")
                else:
                    start_automation()
                    st.success("Started!")
                    st.rerun()
        
        with col2:
            if st.button("🛑 STOP AUTOMATION",
                        disabled=not st.session_state.automation_running,
                        use_container_width=True,
                        type="secondary"):
                stop_automation()
                st.warning("Stopping...")
                st.rerun()
        
        st.markdown("---")
        
        # Console
        if st.session_state.logs:
            st.markdown("### 👑 LIVE CONSOLE")
            
            console_html = '<div class="console-output">'
            for log in st.session_state.logs[-40:]:
                console_html += f'<div class="console-line">{log}</div>'
            console_html += '</div>'
            
            st.markdown(console_html, unsafe_allow_html=True)
            
            if st.button("🔄 REFRESH LOGS"):
                st.rerun()

# ⚜️ ROUTER ⚜️
if not st.session_state.logged_in:
    login_page()
elif not st.session_state.key_approved:
    approval_request_page(st.session_state.user_key, st.session_state.username)
else:
    main_app()

st.markdown('<div class="footer">👑 Made with Royal Love by Xmarty Ayush King | © 2025 SYAPA KING 👑</div>', unsafe_allow_html=True)
