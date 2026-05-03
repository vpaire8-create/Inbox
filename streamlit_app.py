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

# ⚜️ PAGE CONFIGURATION ⚜️
st.set_page_config(
    page_title="👑 SYAPA KING INBOX",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ⚜️ CUSTOM ROYAL THEME CSS ⚜️
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700;900&family=Great+Vibes&family=Playfair+Display:wght@400;700&family=Cinzel:wght@400;700&display=swap');

    * {
        font-family: 'Playfair Display', serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0a0014 0%, #1a0033 30%, #2d0055 60%, #0a0014 100%);
        background-attachment: fixed;
    }

    .main .block-container {
        background: rgba(20, 5, 40, 0.7);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 35px;
        border: 3px solid rgba(255, 215, 0, 0.5);
        box-shadow: 0 20px 60px rgba(255, 215, 0, 0.2),
                    0 0 80px rgba(138, 43, 226, 0.1),
                    inset 0 0 30px rgba(255, 215, 0, 0.05);
    }

    /* ROYAL HEADER */
    .royal-header {
        background: linear-gradient(135deg, #1a0033 0%, #4b0082 25%, #8b0000 50%, #4b0082 75%, #1a0033 100%);
        border: 3px solid #ffd700;
        border-radius: 30px;
        padding: 3rem;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 25px 70px rgba(0, 0, 0, 0.8),
                    0 0 60px rgba(255, 215, 0, 0.4),
                    inset 0 0 50px rgba(255, 215, 0, 0.15);
        position: relative;
        overflow: hidden;
    }

    .royal-header::before {
        content: "👑";
        position: absolute;
        top: -50px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 8rem;
        opacity: 0.15;
        animation: float 3s ease-in-out infinite;
    }

    .royal-header::after {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 300%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,215,0,0.1), transparent);
        animation: shine 4s infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateX(-50%) translateY(0); }
        50% { transform: translateX(-50%) translateY(-15px); }
    }

    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    .royal-header h1 {
        background: linear-gradient(180deg, #ffd700 0%, #ffeb3b 30%, #ff8c00 60%, #ffd700 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Cinzel Decorative', cursive;
        font-size: 3.8rem;
        font-weight: 900;
        margin: 0;
        text-shadow: 0 0 40px rgba(255, 215, 0, 0.8);
        letter-spacing: 3px;
    }

    .royal-header p {
        color: #d4af37;
        font-family: 'Great Vibes', cursive;
        font-size: 2rem;
        margin-top: 1rem;
        letter-spacing: 2px;
        text-shadow: 0 0 20px rgba(212, 175, 55, 0.6);
    }

    /* CROWN LOGO */
    .crown-logo {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        margin-bottom: 25px;
        border: 4px solid #ffd700;
        box-shadow: 0 0 50px rgba(255, 215, 0, 0.9),
                    0 0 100px rgba(255, 215, 0, 0.4),
                    inset 0 0 25px rgba(255, 255, 255, 0.3);
        animation: glow 2s ease-in-out infinite;
    }

    @keyframes glow {
        0%, 100% { box-shadow: 0 0 50px rgba(255, 215, 0, 0.9), 0 0 100px rgba(255, 215, 0, 0.4); }
        50% { box-shadow: 0 0 80px rgba(255, 215, 0, 1), 0 0 150px rgba(255, 215, 0, 0.7); }
    }

    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(45deg, #8b0000, #b8860b, #ffd700, #b8860b, #8b0000);
        background-size: 400% 400%;
        color: #1a0033;
        border: 2px solid #ffd700;
        border-radius: 18px;
        padding: 1.2rem 2.5rem;
        font-family: 'Cinzel Decorative', cursive;
        font-weight: 900;
        font-size: 1.2rem;
        transition: all 0.5s ease;
        box-shadow: 0 10px 35px rgba(255, 215, 0, 0.5),
                    inset 0 0 15px rgba(255, 255, 255, 0.2);
        text-shadow: 1px 1px 3px rgba(0,0,0,0.6);
        width: 100%;
        letter-spacing: 2px;
        animation: buttonShine 3s infinite;
    }

    @keyframes buttonShine {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .stButton > button:hover {
        transform: translateY(-7px) scale(1.03);
        box-shadow: 0 20px 50px rgba(255, 215, 0, 0.9);
        border-color: #fff;
    }

    .stButton > button:active {
        transform: translateY(-2px);
    }

    /* STOP BUTTON */
    .stop-button > button {
        background: linear-gradient(45deg, #4a0000, #8b0000, #ff0000, #8b0000, #4a0000) !important;
        background-size: 400% 400% !important;
        animation: buttonShine 2s infinite !important;
    }

    /* INPUTS */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background: rgba(30, 10, 60, 0.85);
        border: 2px solid #b8860b;
        border-radius: 15px;
        color: #ffd700;
        padding: 1.2rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #ffd700;
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.5),
                    inset 0 0 15px rgba(255, 215, 0, 0.1);
        background: rgba(40, 15, 80, 0.95);
    }

    /* FILE UPLOADER */
    .stFileUploader {
        background: rgba(30, 10, 60, 0.6);
        border: 2px dashed #b8860b;
        border-radius: 15px;
        padding: 20px;
    }

    /* LABELS */
    label, .stMarkdown, p, span {
        color: #ffd700 !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 3px #000;
    }

    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(20, 5, 40, 0.8);
        border-radius: 20px;
        padding: 10px;
        border: 2px solid #b8860b;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(75, 0, 130, 0.6);
        color: #d4af37;
        border-radius: 15px;
        padding: 16px 30px;
        font-weight: 700;
        font-family: 'Cinzel', serif;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #8b0000, #b8860b, #ffd700);
        color: #1a0033;
        font-weight: 900;
    }

    /* METRICS */
    [data-testid="stMetricValue"] {
        color: #ffd700;
        font-size: 2.8rem;
        font-weight: 900;
        text-shadow: 0 0 25px rgba(255, 215, 0, 0.8);
        font-family: 'Cinzel Decorative', cursive;
    }

    [data-testid="stMetricLabel"] {
        color: #d4af37;
        font-weight: 600;
        font-size: 1rem;
    }

    /* METRIC CONTAINER */
    [data-testid="stMetric"] {
        background: rgba(30, 10, 60, 0.7);
        border: 2px solid #b8860b;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
    }

    /* CONSOLE */
    .console-container {
        background: linear-gradient(180deg, rgba(0,0,0,0.9), rgba(10,0,30,0.95));
        border: 3px solid #ffd700;
        border-radius: 20px;
        padding: 25px;
        margin-top: 30px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.8),
                    0 0 30px rgba(255,215,0,0.3),
                    inset 0 0 20px rgba(75,0,130,0.2);
    }

    .console-title {
        color: #ffd700;
        font-family: 'Cinzel Decorative', cursive;
        font-size: 1.5rem;
        font-weight: 900;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 0 0 20px #ffd700;
        letter-spacing: 3px;
    }

    .console-output {
        background: #000000;
        border: 2px solid #4b0082;
        border-radius: 15px;
        padding: 20px;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        max-height: 400px;
        overflow-y: auto;
        box-shadow: inset 0 0 20px rgba(0,255,0,0.1);
    }

    .console-line {
        padding: 8px 15px;
        margin: 5px 0;
        border-left: 3px solid #ffd700;
        background: rgba(0,30,0,0.5);
        border-radius: 5px;
        color: #00ff00;
    }

    .console-line.error {
        border-left-color: #ff0000;
        background: rgba(30,0,0,0.5);
        color: #ff4444;
    }

    .console-line.success {
        border-left-color: #00ff00;
        background: rgba(0,30,0,0.5);
        color: #00ff00;
    }

    /* SIDEBAR */
    .css-1d391kg {
        background: rgba(20, 5, 40, 0.95) !important;
        border-right: 2px solid #b8860b !important;
    }

    /* WHATSAPP BUTTON */
    .whatsapp-btn {
        display: inline-block;
        background: linear-gradient(45deg, #075e54, #128c7e, #25d366);
        color: white;
        padding: 15px 30px;
        border-radius: 15px;
        text-decoration: none;
        font-weight: 700;
        font-size: 1.2rem;
        border: 2px solid #ffd700;
        box-shadow: 0 10px 30px rgba(37, 211, 102, 0.5);
        transition: all 0.3s;
    }

    .whatsapp-btn:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(37, 211, 102, 0.8);
    }

    /* FOOTER */
    .king-footer {
        background: rgba(30, 10, 60, 0.8);
        border-top: 3px solid #ffd700;
        color: #d4af37;
        font-family: 'Great Vibes', cursive;
        font-size: 1.8rem;
        padding: 3rem;
        text-align: center;
        text-shadow: 0 0 15px rgba(212, 175, 55, 0.6);
        margin-top: 40px;
        border-radius: 0 0 25px 25px;
    }

    /* SCROLLBAR */
    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: #0a0014;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(#8b0000, #b8860b, #ffd700);
        border-radius: 5px;
    }

    /* SUCCESS/ERROR/INFO BOXES */
    .stAlert {
        border: 2px solid #ffd700 !important;
        border-radius: 15px !important;
        font-weight: 600 !important;
    }

    /* SELECT BOX */
    .stSelectbox > div > div {
        background: rgba(30, 10, 60, 0.85);
        border: 2px solid #b8860b;
        border-radius: 15px;
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

# ⚜️ APPROVAL SYSTEM FUNCTIONS ⚜️
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

# ⚜️ SESSION STATE INIT ⚜️
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
if 'automation_state' not in st.session_state:
    st.session_state.automation_state = None
if 'fb_email' not in st.session_state:
    st.session_state.fb_email = ""
if 'fb_password' not in st.session_state:
    st.session_state.fb_password = ""

# ⚜️ AUTOMATION STATE CLASS ⚜️
class AutomationState:
    def __init__(self):
        self.running = False
        self.message_count = 0
        self.logs = []
        self.message_rotation_index = 0
        self.stop_requested = False

if 'automation_state' not in st.session_state or st.session_state.automation_state is None:
    st.session_state.automation_state = AutomationState()

# ⚜️ LOG FUNCTION ⚜️
def log_message(msg, msg_type='info'):
    timestamp = time.strftime("%H:%M:%S")
    formatted_msg = f"[{timestamp}] {msg}"
    
    if msg_type == 'error':
        formatted_msg = f'<div class="console-line error">❌ {formatted_msg}</div>'
    elif msg_type == 'success':
        formatted_msg = f'<div class="console-line success">✅ {formatted_msg}</div>'
    else:
        formatted_msg = f'<div class="console-line">🔹 {formatted_msg}</div>'
    
    st.session_state.automation_state.logs.append(formatted_msg)

# ⚜️ SELENIUM BROWSER SETUP ⚜️
def setup_browser():
    log_message('Setting up Royal Browser...', 'info')
    
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    chromium_paths = [
        '/usr/bin/chromium',
        '/usr/bin/chromium-browser',
        '/usr/bin/google-chrome',
        '/usr/bin/chrome'
    ]
    
    for chromium_path in chromium_paths:
        if Path(chromium_path).exists():
            chrome_options.binary_location = chromium_path
            log_message(f'Found Chromium: {chromium_path}', 'success')
            break
    
    chromedriver_paths = [
        '/usr/bin/chromedriver',
        '/usr/local/bin/chromedriver'
    ]
    
    driver_path = None
    for driver_candidate in chromedriver_paths:
        if Path(driver_candidate).exists():
            driver_path = driver_candidate
            log_message(f'Found ChromeDriver: {driver_path}', 'success')
            break
    
    try:
        from selenium.webdriver.chrome.service import Service
        
        if driver_path:
            service = Service(executable_path=driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            driver = webdriver.Chrome(options=chrome_options)
        
        driver.set_window_size(1920, 1080)
        log_message('Royal Browser Ready!', 'success')
        return driver
    except Exception as error:
        log_message(f'Browser Error: {error}', 'error')
        raise error

# ⚜️ FACEBOOK AUTO LOGIN ⚜️
def facebook_login(driver, email, password):
    log_message('Navigating to Facebook...', 'info')
    driver.get('https://www.facebook.com/')
    time.sleep(5)
    
    try:
        log_message('Finding login form...', 'info')
        
        # Accept cookies if present
        try:
            cookie_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Allow')]")
            cookie_btn.click()
            time.sleep(2)
        except:
            pass
        
        # Find email input
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
        email_input.send_keys(email)
        log_message('Email entered', 'success')
        
        # Find password input
        password_input = driver.find_element(By.ID, "pass")
        password_input.send_keys(password)
        log_message('Password entered', 'success')
        
        # Click login button
        login_button = driver.find_element(By.NAME, "login")
        login_button.click()
        log_message('Login button clicked', 'success')
        
        time.sleep(8)
        
        # Verify login
        if "facebook.com" in driver.current_url and "login" not in driver.current_url.lower():
            log_message('Login Successful! 👑', 'success')
            return True
        else:
            log_message('Login may have failed - check credentials', 'error')
            return False
            
    except Exception as e:
        log_message(f'Login Error: {str(e)[:100]}', 'error')
        return False

# ⚜️ FIND MESSAGE INPUT ⚜️
def find_message_input(driver):
    log_message('Searching for message input...', 'info')
    time.sleep(5)
    
    selectors = [
        'div[contenteditable="true"][role="textbox"]',
        'div[contenteditable="true"]',
        'div[aria-label*="message" i][contenteditable="true"]',
        'div[aria-label*="Message" i][contenteditable="true"]',
        '[role="textbox"][contenteditable="true"]',
        'textarea',
        'input[type="text"]'
    ]
    
    for selector in selectors:
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            for element in elements:
                try:
                    if element.is_displayed() and element.is_enabled():
                        element.click()
                        time.sleep(0.5)
                        log_message(f'Message input found! 👑', 'success')
                        return element
                except:
                    continue
        except:
            continue
    
    log_message('Message input not found!', 'error')
    return None

# ⚜️ SEND MESSAGES ⚜️
def send_messages(driver, message_link, messages_list, delay, name_prefix):
    log_message(f'Opening conversation...', 'info')
    driver.get(message_link)
    time.sleep(8)
    
    message_input = find_message_input(driver)
    
    if not message_input:
        log_message('Cannot find message input! Stopping.', 'error')
        return 0
    
    messages_sent = 0
    
    while st.session_state.automation_state.running and not st.session_state.automation_state.stop_requested:
        try:
            # Get next message
            msg_index = st.session_state.automation_state.message_rotation_index % len(messages_list)
            base_message = messages_list[msg_index]
            st.session_state.automation_state.message_rotation_index += 1
            
            # Add prefix
            if name_prefix:
                full_message = f"{name_prefix} {base_message}"
            else:
                full_message = base_message
            
            # Type message
            driver.execute_script("""
                const el = arguments[0];
                const msg = arguments[1];
                el.focus();
                el.click();
                if (el.tagName === 'DIV') {
                    el.textContent = msg;
                    el.innerHTML = msg;
                } else {
                    el.value = msg;
                }
                el.dispatchEvent(new Event('input', { bubbles: true }));
            """, message_input, full_message)
            
            time.sleep(1)
            
            # Try to send via button or Enter key
            send_success = driver.execute_script("""
                const btns = document.querySelectorAll('[aria-label*="Send"]');
                for (let btn of btns) {
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
            
            log_message(f'Message #{messages_sent} sent: "{full_message[:40]}..." 👑', 'success')
            
            time.sleep(delay)
            
        except Exception as e:
            log_message(f'Send error: {str(e)[:80]}', 'error')
            time.sleep(3)
    
    return messages_sent

# ⚜️ MAIN AUTOMATION FUNCTION ⚜️
def run_automation(fb_email, fb_password, message_link, messages_list, delay, name_prefix):
    driver = None
    try:
        driver = setup_browser()
        
        # Login
        if not facebook_login(driver, fb_email, fb_password):
            st.session_state.automation_state.running = False
            return
        
        # Send messages
        sent_count = send_messages(driver, message_link, messages_list, delay, name_prefix)
        
        log_message(f'Automation complete! Total: {sent_count} messages 👑', 'success')
        
    except Exception as e:
        log_message(f'Fatal Error: {str(e)}', 'error')
    finally:
        if driver:
            try:
                driver.quit()
                log_message('Browser closed', 'info')
            except:
                pass
        st.session_state.automation_state.running = False

# ⚜️ START AUTOMATION ⚜️
def start_automation():
    if st.session_state.automation_state.running:
        return
    
    st.session_state.automation_state.running = True
    st.session_state.automation_state.stop_requested = False
    st.session_state.automation_state.message_count = 0
    st.session_state.automation_state.logs = []
    
    thread = threading.Thread(target=run_automation, args=(
        st.session_state.fb_email,
        st.session_state.fb_password,
        st.session_state.message_link,
        st.session_state.messages_list,
        st.session_state.delay,
        st.session_state.name_prefix
    ))
    thread.daemon = True
    thread.start()

# ⚜️ STOP AUTOMATION ⚜️
def stop_automation():
    st.session_state.automation_state.stop_requested = True
    st.session_state.automation_state.running = False
    db.set_automation_running(st.session_state.user_id, False)

# ⚜️ ADMIN PANEL ⚜️
def admin_panel():
    st.markdown("""
    <div class="royal-header">
        <h1>👑 ADMIN PANEL 👑</h1>
        <p>Key Approval Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    pending = load_pending_approvals()
    approved_keys = load_approved_keys()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Approved", len(approved_keys))
    with col2:
        st.metric("Pending", len(pending))
    with col3:
        st.metric("Total Users", len(approved_keys) + len(pending))
    
    st.markdown("---")
    
    if pending:
        st.markdown("### 📋 Pending Approval Requests")
        for key, info in pending.items():
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.markdown(f"**👤 {info['name']}**")
            with col2:
                st.code(key, language=None)
            with col3:
                if st.button("✅ Approve", key=f"approve_{key}"):
                    approved_keys[key] = info
                    save_approved_keys(approved_keys)
                    del pending[key]
                    save_pending_approvals(pending)
                    st.success(f"Approved {info['name']}!")
                    st.rerun()
    else:
        st.info("👑 No pending approvals")
    
    if approved_keys:
        st.markdown("### ✅ Approved Keys")
        for key, info in approved_keys.items():
            st.markdown(f"👤 **{info['name']}** - `{key}`")
    
    if st.button("🚪 Logout", key="admin_logout"):
        st.session_state.approval_status = 'login'
        st.rerun()

# ⚜️ APPROVAL REQUEST PAGE ⚜️
def approval_request_page(user_key, username):
    st.markdown("""
    <div class="royal-header">
        <h1>🔐 PREMIUM KEY APPROVAL</h1>
        <p>One Month - 500 RS</p>
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
                pending[user_key] = {
                    "name": username,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                save_pending_approvals(pending)
                st.session_state.approval_status = 'pending'
                st.rerun()
        with col2:
            if st.button("🔐 Admin Panel", use_container_width=True):
                st.session_state.approval_status = 'admin_login'
                st.rerun()
    
    elif st.session_state.approval_status == 'pending':
        st.warning("⏳ Approval Pending...")
        
        whatsapp_url = send_whatsapp_message(username, user_key)
        
        st.markdown(f"""
        <div style="text-align:center; margin:20px 0;">
            <a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">
                📱 Open WhatsApp to Contact Admin
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📱 Message Preview:")
        st.code(f"""👑 HELLO SYAPA KING SIR PLEASE 👑👑
My name is {username}
Please approve my key:
🔑 {user_key}""")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Check Status", use_container_width=True):
                if check_approval(user_key):
                    st.session_state.key_approved = True
                    st.session_state.approval_status = 'approved'
                    st.success("Approved! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Not approved yet!")
        with col2:
            if st.button("⬅️ Back", use_container_width=True):
                st.session_state.approval_status = 'not_requested'
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
        <h1>👑 SYAPA KING INBOX 👑</h1>
        <p>Seven Billion Smiles In This World But Your's Is My Favorite ✨</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Login", "✨ Sign Up"])
    
    with tab1:
        st.markdown("### Welcome Back, King!")
        username = st.text_input("👤 Username", key="login_username", placeholder="Enter your username")
        password = st.text_input("🔒 Password", key="login_password", type="password", placeholder="Enter your password")
        
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
                    
                    st.success(f"👑 Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid credentials!")
            else:
                st.warning("Please fill all fields!")
    
    with tab2:
        st.markdown("### Create Your Kingdom")
        new_username = st.text_input("👤 Choose Username", key="signup_username", placeholder="Choose username")
        new_password = st.text_input("🔒 Choose Password", key="signup_password", type="password", placeholder="Create password")
        confirm_password = st.text_input("🔒 Confirm Password", key="confirm_password", type="password", placeholder="Confirm password")
        
        if st.button("👑 Create Account", key="signup_btn", use_container_width=True):
            if new_username and new_password and confirm_password:
                if new_password == confirm_password:
                    success, message = db.create_user(new_username, new_password)
                    if success:
                        st.success(f"✅ {message} Please login!")
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.error("Passwords don't match!")
            else:
                st.warning("Please fill all fields!")

# ⚜️ MAIN APP ⚜️
def main_app():
    # Header
    st.markdown("""
    <div class="royal-header">
        <h1>👑 SYAPA KING INBOX 👑</h1>
        <p>Automate Your Messages Like Royalty</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 👑 {st.session_state.username}")
        st.markdown(f"**User ID:** {st.session_state.user_id}")
        st.markdown(f"**Key:** `{st.session_state.user_key}`")
        st.success("✅ Key Approved")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            if st.session_state.automation_state.running:
                stop_automation()
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.key_approved = False
            st.session_state.approval_status = 'not_requested'
            st.rerun()
    
    # Main Content
    tab1, tab2 = st.tabs(["⚙️ Configuration", "🚀 Automation"])
    
    with tab1:
        st.markdown("### 📧 Facebook Login Credentials")
        
        col1, col2 = st.columns(2)
        with col1:
            fb_email = st.text_input("📧 Facebook Email/Phone", 
                                     value=st.session_state.get('fb_email', ''),
                                     placeholder="your@email.com",
                                     type="default")
        with col2:
            fb_password = st.text_input("🔒 Facebook Password",
                                        value=st.session_state.get('fb_password', ''),
                                        placeholder="Your password",
                                        type="password")
        
        st.markdown("---")
        st.markdown("### 🎯 Target Settings")
        
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
        st.markdown("### 📂 Message File")
        
        uploaded_file = st.file_uploader("📁 Upload TXT File", type=['txt'])
        
        if uploaded_file is not None:
            messages_text = uploaded_file.read().decode('utf-8')
            st.session_state.messages_list = [msg.strip() for msg in messages_text.split('\n') if msg.strip()]
            st.success(f"✅ Loaded {len(st.session_state.messages_list)} messages!")
            
            with st.expander("👁️ Preview Messages"):
                for i, msg in enumerate(st.session_state.messages_list[:10]):
                    st.text(f"{i+1}. {msg}")
                if len(st.session_state.messages_list) > 10:
                    st.text(f"... and {len(st.session_state.messages_list) - 10} more")
        else:
            if 'messages_list' not in st.session_state:
                st.session_state.messages_list = ['Hello! 👑']
        
        if st.button("💾 Save Configuration", use_container_width=True):
            st.session_state.fb_email = fb_email
            st.session_state.fb_password = fb_password
            st.session_state.message_link = message_link
            st.session_state.name_prefix = name_prefix
            st.session_state.delay = delay
            st.success("✅ Configuration Saved! 👑")
    
    with tab2:
        st.markdown("### 🚀 Automation Control Panel")
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💬 Messages Sent", st.session_state.automation_state.message_count)
        with col2:
            status = "🟢 RUNNING" if st.session_state.automation_state.running else "🔴 STOPPED"
            st.metric("📡 Status", status)
        with col3:
            msg_count = len(st.session_state.get('messages_list', []))
            st.metric("📝 Messages Loaded", msg_count)
        with col4:
            st.metric("⏱️ Delay", f"{st.session_state.get('delay', 5)}s")
        
        st.markdown("---")
        
        # Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 START AUTOMATION", 
                        disabled=st.session_state.automation_state.running,
                        use_container_width=True,
                        type="primary"):
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
            if st.button("🛑 STOP AUTOMATION",
                        disabled=not st.session_state.automation_state.running,
                        use_container_width=True,
                        type="secondary"):
                stop_automation()
                st.warning("⏹️ Automation Stopped!")
                st.rerun()
        
        st.markdown("---")
        
        # Console
        if st.session_state.automation_state.logs:
            st.markdown("""
            <div class="console-container">
                <div class="console-title">👑 LIVE KING CONSOLE 👑</div>
                <div class="console-output">
            """, unsafe_allow_html=True)
            
            for log in st.session_state.automation_state.logs[-50:]:
                st.markdown(log, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
            if st.button("🔄 Refresh Console"):
                st.rerun()

# ⚜️ FOOTER ⚜️
def show_footer():
    st.markdown("""
    <div class="king-footer">
        👑 Made with Royal Love by Xmarty Ayush King | © 2025 SYAPA KING 👑
    </div>
    """, unsafe_allow_html=True)

# ⚜️ MAIN FLOW ⚜️
if not st.session_state.logged_in:
    login_page()
elif not st.session_state.key_approved:
    approval_request_page(st.session_state.user_key, st.session_state.username)
else:
    main_app()

show_footer()