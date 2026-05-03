import streamlit as st
import streamlit.components.v1 as components
import time
import threading
import uuid
import hashlib
import os
import subprocess
import json
import urllib.parse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import database as db
import requests

st.set_page_config(
    page_title="SYAPA KING",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
#          ROYAL / KINGLY THEME CSS
# ============================================
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Great+Vibes&family=Playfair+Display:wght@400;700&display=swap');

    * {
        font-family: 'Playfair Display', serif;
    }

    .stApp {
        background-image: linear-gradient(rgba(20, 0, 40, 0.88), rgba(40, 0, 80, 0.78)),
                          url('https://i.ibb.co/0mQfX0b/dark-royal-purple-velvet-texture.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .main .block-container {
        background: rgba(30, 10, 60, 0.68);
        backdrop-filter: blur(12px);
        border-radius: 22px;
        padding: 32px;
        border: 2px solid rgba(255, 215, 0, 0.38);
        box-shadow: 0 12px 45px rgba(255, 215, 0, 0.18),
                    inset 0 0 28px rgba(255, 215, 0, 0.10);
    }

    .main-header {
        background: linear-gradient(135deg, #1a0033, #4b0082, #2a0055);
        border: 2px solid #ffd700;
        border-radius: 25px;
        padding: 2.4rem;
        text-align: center;
        margin-bottom: 2.8rem;
        box-shadow: 0 18px 55px rgba(0, 0, 0, 0.75),
                    0 0 35px rgba(255, 215, 0, 0.30);
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: "👑";
        position: absolute;
        top: -40px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 6.5rem;
        opacity: 0.14;
        color: #ffd700;
    }

    .main-header h1 {
        background: linear-gradient(90deg, #ffd700, #ffeb3b, #ffd700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Cinzel Decorative', cursive;
        font-size: 3.4rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 0 25px rgba(255, 215, 0, 0.7);
    }

    .main-header p {
        color: #d4af37;
        font-family: 'Great Vibes', cursive;
        font-size: 1.8rem;
        margin-top: 0.7rem;
        letter-spacing: 1.8px;
    }

    .prince-logo {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        margin-bottom: 22px;
        border: 4px solid #ffd700;
        box-shadow: 0 0 35px rgba(255, 215, 0, 0.8),
                    inset 0 0 18px rgba(255, 255, 255, 0.35);
    }

    .stButton>button {
        background: linear-gradient(45deg, #b8860b, #ffd700, #daa520);
        color: #1a0033;
        border: 2px solid #b8860b;
        border-radius: 16px;
        padding: 1rem 2.4rem;
        font-family: 'Cinzel Decorative', cursive;
        font-weight: 700;
        font-size: 1.2rem;
        transition: all 0.4s ease;
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.45);
        text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-5px) scale(1.04);
        box-shadow: 0 15px 40px rgba(255, 215, 0, 0.75);
        background: linear-gradient(45deg, #ffd700, #ffeb3b, #ffd700);
    }

    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stNumberInput>div>div>input {
        background: rgba(40, 20, 80, 0.75);
        border: 2px solid #b8860b;
        border-radius: 14px;
        color: #ffd700;
        padding: 1rem;
        font-size: 1.1rem;
    }

    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #ffd700;
        box-shadow: 0 0 0 4px rgba(255, 215, 0, 0.35);
        background: rgba(50, 30, 90, 0.85);
    }

    label {
        color: #ffd700 !important;
        font-weight: 600 !important;
        font-size: 1.15rem !important;
        text-shadow: 1px 1px 4px #000;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: rgba(30, 10, 60, 0.65);
        border-radius: 16px;
        padding: 10px;
        border: 1px solid #b8860b;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(75, 0, 130, 0.55);
        color: #d4af37;
        border-radius: 12px;
        padding: 14px 26px;
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #b8860b, #ffd700);
        color: #1a0033;
    }

    [data-testid="stMetricValue"] {
        color: #ffd700;
        font-size: 2.6rem;
        font-weight: 700;
        text-shadow: 0 0 18px rgba(255, 215, 0, 0.7);
    }

    [data-testid="stMetricLabel"] {
        color: #d4af37;
        font-weight: 500;
    }

    .console-section {
        background: rgba(20, 0, 40, 0.75);
        border: 2px solid #b8860b;
        border-radius: 16px;
        padding: 22px;
        margin-top: 28px;
    }

    .console-header {
        color: #ffd700;
        font-family: 'Cinzel Decorative', cursive;
        text-shadow: 0 0 18px #ffd700bb;
        margin-bottom: 18px;
    }

    .console-output {
        background: #0f001a;
        border: 2px solid #4b0082;
        border-radius: 14px;
        padding: 18px;
        color: #ffeb3b;
        font-family: 'Courier New', monospace;
        font-size: 13.5px;
        max-height: 480px;
        overflow-y: auto;
    }

    .console-line {
        background: rgba(75, 0, 130, 0.25);
        border-left: 4px solid #ffd700;
        padding: 9px 14px;
        margin: 7px 0;
        color: #ffeb3b;
    }

    .success-box {
        background: linear-gradient(135deg, #b8860b, #ffd700);
        color: #1a0033;
        border: 2px solid #1a0033;
    }

    .error-box {
        background: linear-gradient(135deg, #8b0000, #c71585);
        border: 2px solid #ffd700;
    }

    .whatsapp-btn {
        background: linear-gradient(45deg, #006400, #228b22, #006400);
        border: 2px solid #ffd700;
        color: #ffd700;
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        box-shadow: 0 8px 25px rgba(0, 100, 0, 0.55);
        text-decoration: none;
        padding: 15px 30px;
        border-radius: 15px;
        display: inline-block;
    }

    .whatsapp-btn:hover {
        background: linear-gradient(45deg, #228b22, #32cd32, #228b22);
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(50, 205, 50, 0.7);
    }

    .footer {
        background: rgba(30, 10, 60, 0.75);
        border-top: 3px solid #b8860b;
        color: #d4af37;
        font-family: 'Great Vibes', cursive;
        font-size: 1.5rem;
        padding: 2.8rem;
        text-shadow: 1px 1px 5px #000;
        text-align: center;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ============================================
# CONSTANTS
# ============================================
ADMIN_PASSWORD = "SYAPA_KING"
WHATSAPP_NUMBER = "+92364234209"
APPROVAL_FILE = "approved_keys.json"
PENDING_FILE = "pending_approvals.json"
ADMIN_UID = "Xmarty.Ayush.King.70"

# ============================================
# KEY GENERATION
# ============================================
def generate_user_key(username, password):
    combined = f"{username}:{password}"
    key_hash = hashlib.sha256(combined.encode()).hexdigest()[:8].upper()
    return f"KEY-{key_hash}"

# ============================================
# APPROVAL SYSTEM
# ============================================
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

# ============================================
# SESSION STATE INIT
# ============================================
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
if 'fb_email' not in st.session_state:
    st.session_state.fb_email = ""
if 'fb_password' not in st.session_state:
    st.session_state.fb_password = ""
if 'message_link' not in st.session_state:
    st.session_state.message_link = ""
if 'delay' not in st.session_state:
    st.session_state.delay = 5
if 'messages_list' not in st.session_state:
    st.session_state.messages_list = ['Hello!']
if 'name_prefix' not in st.session_state:
    st.session_state.name_prefix = ""

# ============================================
# AUTOMATION STATE CLASS
# ============================================
class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0
        self.stop_requested = False

if 'automation_state' not in st.session_state:
    st.session_state.automation_state = AutomationState()

# ============================================
# LOG FUNCTION
# ============================================
def log_message(msg, msg_type='info'):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    
    if msg_type == 'error':
        formatted_msg = f"❌ {formatted_msg}"
    elif msg_type == 'success':
        formatted_msg = f"✅ {formatted_msg}"
    else:
        formatted_msg = f"🔹 {formatted_msg}"
    
    st.session_state.automation_state.logs.append(formatted_msg)

# ============================================
# SELENIUM BROWSER SETUP
# ============================================
def setup_browser():
    log_message('Setting up Chrome browser...')
    
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    chromium_paths = [
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
        '/usr/bin/chrome'
    ]
    
    for chromium_path in chromium_paths:
        if Path(chromium_path).exists():
            chrome_options.binary_location = chromium_path
            log_message(f'Found Chromium at: {chromium_path}', 'success')
            break
    
    chromedriver_paths = [
        '/usr/bin/chromedriver',
        '/usr/local/bin/chromedriver'
    ]
    
    driver_path = None
    for driver_candidate in chromedriver_paths:
        if Path(driver_candidate).exists():
            driver_path = driver_candidate
            log_message(f'Found ChromeDriver at: {driver_path}', 'success')
            break
    
    try:
        from selenium.webdriver.chrome.service import Service
        
        if driver_path:
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            log_message('Chrome started with detected ChromeDriver!', 'success')
        else:
            driver = webdriver.Chrome(options=chrome_options)
            log_message('Chrome started with default driver!', 'success')
        
        driver.set_window_size(1920, 1080)
        log_message('Chrome browser setup completed!', 'success')
        return driver
    except Exception as error:
        log_message(f'Browser setup failed: {error}', 'error')
        raise error

# ============================================
# FACEBOOK AUTO LOGIN
# ============================================
def facebook_login(driver, email, password):
    log_message('Navigating to Facebook login page...')
    driver.get('https://www.facebook.com/')
    time.sleep(5)
    
    try:
        # Accept cookies if present
        try:
            accept_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Allow') or contains(text(), 'Accept')]")
            for btn in accept_buttons:
                if btn.is_displayed():
                    btn.click()
                    time.sleep(2)
                    break
        except:
            pass
        
        log_message('Entering email...')
        email_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.clear()
        email_input.send_keys(email)
        log_message('Email entered', 'success')
        
        log_message('Entering password...')
        password_input = driver.find_element(By.ID, "pass")
        password_input.clear()
        password_input.send_keys(password)
        log_message('Password entered', 'success')
        
        log_message('Clicking login button...')
        login_button = driver.find_element(By.NAME, "login")
        login_button.click()
        log_message('Login button clicked', 'success')
        
        time.sleep(10)
        
        # Check if login was successful
        current_url = driver.current_url
        if "checkpoint" in current_url or "login" in current_url:
            log_message('Login failed or requires verification', 'error')
            return False
        else:
            log_message('Facebook login successful! 👑', 'success')
            return True
            
    except Exception as e:
        log_message(f'Facebook login error: {str(e)[:100]}', 'error')
        return False

# ============================================
# FIND MESSAGE INPUT
# ============================================
def find_message_input(driver):
    log_message('Finding message input box...')
    time.sleep(8)
    
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
    except:
        pass
    
    message_input_selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        '[role="textbox"][contenteditable="true"]',
        '[contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
    
    for selector in message_input_selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            
            for element in elements:
                try:
                    if element.is_displayed():
                        element.click()
                        time.sleep(0.5)
                        log_message('✅ Found message input!', 'success')
                        return element
                except:
                    continue
        except:
            continue
    
    log_message('Message input not found!', 'error')
    return None

# ============================================
# GET NEXT MESSAGE
# ============================================
def get_next_message(messages_list):
    if not messages_list or len(messages_list) == 0:
        return 'Hello!'
    
    msg_index = st.session_state.automation_state.message_rotation_index % len(messages_list)
    message = messages_list[msg_index]
    st.session_state.automation_state.message_rotation_index += 1
    return message

# ============================================
# SEND MESSAGES
# ============================================
def send_messages(driver, messages_list, delay, name_prefix):
    message_input = find_message_input(driver)
    
    if not message_input:
        log_message('Cannot proceed without message input!', 'error')
        return 0
    
    messages_sent = 0
    
    while st.session_state.automation_state.running and not st.session_state.automation_state.stop_requested:
        try:
            base_message = get_next_message(messages_list)
            
            if name_prefix:
                full_message = f"{name_prefix} {base_message}"
            else:
                full_message = base_message
            
            # Type message
            driver.execute_script("""
                const element = arguments[0];
                const message = arguments[1];
                
                element.focus();
                element.click();
                
                if (element.tagName === 'DIV') {
                    element.textContent = message;
                } else {
                    element.value = message;
                }
                
                element.dispatchEvent(new Event('input', { bubbles: true }));
                element.dispatchEvent(new Event('change', { bubbles: true }));
            """, message_input, full_message)
            
            time.sleep(1)
            
            # Send message
            send_success = driver.execute_script("""
                const sendButtons = document.querySelectorAll('[aria-label*="Send"]');
                for (let btn of sendButtons) {
                    if (btn.offsetParent !== null) {
                        btn.click();
                        return true;
                    }
                }
                return false;
            """)
            
            if not send_success:
                # Use Enter key
                message_input.send_keys(Keys.ENTER)
            
            messages_sent += 1
            st.session_state.automation_state.message_count = messages_sent
            
            log_message(f'Message #{messages_sent} sent 👑', 'success')
            
            time.sleep(delay)
            
        except Exception as e:
            log_message(f'Send error: {str(e)[:80]}', 'error')
            time.sleep(3)
    
    return messages_sent

# ============================================
# MAIN AUTOMATION
# ============================================
def run_automation():
    driver = None
    try:
        log_message('Starting Royal Automation... 👑')
        driver = setup_browser()
        
        # Facebook Login
        if not facebook_login(driver, st.session_state.fb_email, st.session_state.fb_password):
            log_message('Facebook login failed! Stopping.', 'error')
            st.session_state.automation_state.running = False
            return
        
        # Navigate to message link
        if st.session_state.message_link:
            log_message(f'Opening message link...')
            driver.get(st.session_state.message_link)
            time.sleep(8)
            
            messages_sent = send_messages(
                driver,
                st.session_state.messages_list,
                st.session_state.delay,
                st.session_state.name_prefix
            )
            
            log_message(f'Automation complete! Total messages: {messages_sent} 👑', 'success')
        else:
            log_message('No message link provided!', 'error')
        
    except Exception as e:
        log_message(f'Fatal error: {str(e)}', 'error')
    finally:
        if driver:
            try:
                driver.quit()
                log_message('Browser closed', 'success')
            except:
                pass
        st.session_state.automation_state.running = False

# ============================================
# START / STOP AUTOMATION
# ============================================
def start_automation():
    if st.session_state.automation_state.running:
        return
    
    st.session_state.automation_state.running = True
    st.session_state.automation_state.stop_requested = False
    st.session_state.automation_state.message_count = 0
    st.session_state.automation_state.message_rotation_index = 0
    st.session_state.automation_state.logs = []
    
    thread = threading.Thread(target=run_automation)
    thread.daemon = True
    thread.start()

def stop_automation():
    st.session_state.automation_state.stop_requested = True
    st.session_state.automation_state.running = False
    log_message('⏹️ Automation stop requested!', 'error')

# ============================================
# ADMIN PANEL
# ============================================
def admin_panel():
    st.markdown("""
    <div class="main-header">
        <img src="https://i.ibb.co/8ghMsS2q/538a21e43b48.jpg" class="prince-logo">
        <h1>👑 ADMIN PANEL 👑</h1>
        <p>KEY APPROVAL MANAGEMENT</p>
    </div>
    """, unsafe_allow_html=True)
    
    pending = load_pending_approvals()
    approved_keys = load_approved_keys()
    
    st.success(f"**Total Approved Keys:** {len(approved_keys)}")
    st.warning(f"**Pending Approvals:** {len(pending)}")
    
    if pending:
        st.markdown("#### 📋 Pending Approval Requests")
        
        for key, info in pending.items():
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.text(f"👤 {info['name']}")
            with col2:
                st.text(f"🔑 {key}")
            with col3:
                if st.button("✅", key=f"approve_{key}"):
                    approved_keys[key] = info
                    save_approved_keys(approved_keys)
                    del pending[key]
                    save_pending_approvals(pending)
                    st.success(f"Approved {info['name']}!")
                    st.rerun()
    else:
        st.info("No pending approvals")
    
    if approved_keys:
        st.markdown("#### ✅ Approved Keys")
        for key, info in approved_keys.items():
            st.text(f"👤 {info['name']} - 🔑 {key}")
    
    if st.button("🚪 Logout", key="admin_logout_btn"):
        st.session_state.approval_status = 'login'
        st.rerun()

# ============================================
# APPROVAL REQUEST PAGE
# ============================================
def approval_request_page(user_key, username):
    st.markdown("""
    <div class="main-header">
        <img src="https://i.ibb.co/8ghMsS2q/538a21e43b48.jpg" class="prince-logo">
        <h1> PREMIUM KEY APPROVAL REQUIRED </h1>
        <p>ONE MONTH 500 RS PAID</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.approval_status == 'not_requested':
        st.markdown("### 📝 Request Access")
        st.info(f"**Your Unique Key:** `{user_key}`")
        st.info(f"**Username:** {username}")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("📤 Request Approval", use_container_width=True, key="request_approval_btn"):
                pending = load_pending_approvals()
                pending[user_key] = {
                    "name": username,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                save_pending_approvals(pending)
                
                st.session_state.approval_status = 'pending'
                st.session_state.whatsapp_opened = False
                st.rerun()
        
        with col2:
            if st.button("🔐 Admin Panel", use_container_width=True, key="admin_panel_btn"):
                st.session_state.approval_status = 'admin_login'
                st.rerun()
    
    elif st.session_state.approval_status == 'pending':
        st.warning("⏳ Approval Pending...")
        st.info(f"**Your Key:** `{user_key}`")
        
        whatsapp_url = send_whatsapp_message(username, user_key)
        
        if not st.session_state.whatsapp_opened:
            whatsapp_js = f"""
            <script>
                setTimeout(function() {{
                    window.open('{whatsapp_url}', '_blank');
                }}, 500);
            </script>
            """
            components.html(whatsapp_js, height=0)
            st.session_state.whatsapp_opened = True
        
        st.success(f"📱 WhatsApp opening automatically for: **{username}**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Check Approval Status", use_container_width=True, key="check_approval_btn"):
                if check_approval(user_key):
                    st.session_state.key_approved = True
                    st.session_state.approval_status = 'approved'
                    st.success("✅ Approved! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Not approved yet. Please wait!")
        
        with col2:
            if st.button("⬅️ Back", use_container_width=True, key="back_btn"):
                st.session_state.approval_status = 'not_requested'
                st.session_state.whatsapp_opened = False
                st.rerun()
    
    elif st.session_state.approval_status == 'admin_login':
        st.markdown("### 🔐 Admin Login")
        
        admin_password = st.text_input("Enter Admin Password:", type="password", key="admin_password_input")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔓 Login", use_container_width=True, key="admin_login_btn"):
                if admin_password == ADMIN_PASSWORD:
                    st.session_state.approval_status = 'admin_panel'
                    st.rerun()
                else:
                    st.error("❌ Invalid password!")
        
        with col2:
            if st.button("⬅️ Back", use_container_width=True, key="admin_back_btn"):
                st.session_state.approval_status = 'not_requested'
                st.rerun()
    
    elif st.session_state.approval_status == 'admin_panel':
        admin_panel()

# ============================================
# LOGIN PAGE
# ============================================
def login_page():
    st.markdown("""
    <div class="main-header">
        <img src="https://i.ibb.co/8ghMsS2q/538a21e43b48.jpg" class="prince-logo">
        <h1>👑SYAPA KING 👑</h1>
        <p>seven billion smiles in this world but your's is my favorites___👑👑</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Login", "✨ Sign Up"])
    
    with tab1:
        st.markdown("### Welcome Back!")
        username = st.text_input("Username", key="login_username", placeholder="Enter your username")
        password = st.text_input("Password", key="login_password", type="password", placeholder="Enter your password")
        
        if st.button("Login", key="login_btn", use_container_width=True):
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
                    
                    st.success(f"👑 Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password!")
            else:
                st.warning("⚠️ Please enter both username and password")
    
    with tab2:
        st.markdown("### Create New Account")
        new_username = st.text_input("Choose Username", key="signup_username", placeholder="Choose a unique username")
        new_password = st.text_input("Choose Password", key="signup_password", type="password", placeholder="Create a strong password")
        confirm_password = st.text_input("Confirm Password", key="confirm_password", type="password", placeholder="Re-enter your password")
        
        if st.button("Create Account", key="signup_btn", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    success, message = db.create_user(new_username, new_password)
                    if success:
                        st.success(f"✅ {message} Please login now!")
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("❌ Passwords do not match!")
            else:
                st.warning("⚠️ Please fill all fields")

# ============================================
# MAIN APP
# ============================================
def main_app():
    st.markdown('<div class="main-header"><img src="https://i.ibb.co/8ghMsS2q/538a21e43b48.jpg" class="prince-logo"><h1>👑 SYAPA KING 👑</h1><p>seven billion smiles in this world but yours is my favorites___👑👑</p></div>', unsafe_allow_html=True)
    
    st.sidebar.markdown(f"### 👑 {st.session_state.username}")
    st.sidebar.markdown(f"**User ID:** {st.session_state.user_id}")
    st.sidebar.markdown(f"**Key:** `{st.session_state.user_key}`")
    st.sidebar.success("✅ Key Approved")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        if st.session_state.automation_state.running:
            stop_automation()
        
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.user_key = None
        st.session_state.key_approved = False
        st.session_state.approval_status = 'not_requested'
        st.rerun()
    
    tab1, tab2 = st.tabs(["⚙️ Configuration", "🚀 Automation"])
    
    with tab1:
        st.markdown("### 📧 Facebook Login Credentials")
        
        col1, col2 = st.columns(2)
        with col1:
            fb_email = st.text_input("📧 Facebook Email/Phone", 
                                     value=st.session_state.get('fb_email', ''),
                                     placeholder="your@email.com")
        with col2:
            fb_password = st.text_input("🔒 Facebook Password",
                                        value=st.session_state.get('fb_password', ''),
                                        placeholder="Your password",
                                        type="password")
        
        st.markdown("---")
        st.markdown("### 🎯 Message Settings")
        
        message_link = st.text_input("🔗 Message Link (Full URL)",
                                     value=st.session_state.get('message_link', ''),
                                     placeholder="https://web.facebook.com/messages/e2ee/t/825136373513772")
        
        name_prefix = st.text_input("✍️ Hater Name (Prefix)",
                                    value=st.session_state.get('name_prefix', ''),
                                    placeholder="[END TO END]")
        
        delay = st.number_input("⏱️ Delay (Seconds)", 
                                min_value=1, 
                                max_value=300,
                                value=st.session_state.get('delay', 5))
        
        st.markdown("---")
        st.markdown("### 📂 Upload Message File (.txt)")
        
        uploaded_file = st.file_uploader("📁 Choose TXT file", type=['txt'])
        
        if uploaded_file is not None:
            try:
                messages_text = uploaded_file.read().decode('utf-8')
                st.session_state.messages_list = [msg.strip() for msg in messages_text.split('\n') if msg.strip()]
                st.success(f"✅ Loaded {len(st.session_state.messages_list)} messages!")
                
                with st.expander("👁️ Preview Messages"):
                    for i, msg in enumerate(st.session_state.messages_list[:10]):
                        st.text(f"{i+1}. {msg}")
                    if len(st.session_state.messages_list) > 10:
                        st.text(f"... and {len(st.session_state.messages_list) - 10} more")
            except Exception as e:
                st.error(f"Error reading file: {e}")
        
        if st.button("💾 Save Configuration", use_container_width=True):
            st.session_state.fb_email = fb_email
            st.session_state.fb_password = fb_password
            st.session_state.message_link = message_link
            st.session_state.name_prefix = name_prefix
            st.session_state.delay = delay
            st.success("✅ Configuration Saved! 👑")
    
    with tab2:
        st.markdown("### 🚀 Automation Control")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Messages Sent", st.session_state.automation_state.message_count)
        with col2:
            status = "🟢 Running" if st.session_state.automation_state.running else "🔴 Stopped"
            st.metric("Status", status)
        with col3:
            msg_count = len(st.session_state.get('messages_list', []))
            st.metric("Messages Loaded", msg_count)
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Start Automation", disabled=st.session_state.automation_state.running, use_container_width=True):
                if not st.session_state.get('fb_email'):
                    st.error("❌ Please set Facebook Email in Configuration!")
                elif not st.session_state.get('fb_password'):
                    st.error("❌ Please set Facebook Password in Configuration!")
                elif not st.session_state.get('message_link'):
                    st.error("❌ Please set Message Link in Configuration!")
                else:
                    start_automation()
                    st.success("👑 Automation Started!")
                    st.rerun()
        
        with col2:
            if st.button("🛑 Stop Automation", disabled=not st.session_state.automation_state.running, use_container_width=True):
                stop_automation()
                st.warning("⏹️ Automation Stopped!")
                st.rerun()
        
        if st.session_state.automation_state.logs:
            st.markdown("### 👑 Live Console Output")
            
            logs_html = '<div class="console-output">'
            for log in st.session_state.automation_state.logs[-50:]:
                logs_html += f'<div class="console-line">{log}</div>'
            logs_html += '</div>'
            
            st.markdown(logs_html, unsafe_allow_html=True)
            
            if st.button("🔄 Refresh Logs"):
                st.rerun()

# ============================================
# MAIN ROUTER
# ============================================
if not st.session_state.logged_in:
    login_page()
elif not st.session_state.key_approved:
    approval_request_page(st.session_state.user_key, st.session_state.username)
else:
    main_app()

st.markdown('<div class="footer">Made with ❤️ by syapa King | © 2025 SYAPA KING</div>', unsafe_allow_html=True)
