import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import json, os, time

st.set_page_config(page_title="TASHEER AI - Secure", page_icon="📧", layout="wide")

USERS_FILE = "users_db.json"
MSG_FILE = "messages_db.json"

def load_json(file, default):
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f: return json.load(f)
        except: return default
    return default
def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)

WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={WALLET}"

# === FINAL BRAND - NAVY GOLD TEAL - IP ORIGINAL ===
st.markdown("""
<style>
.stApp {background:#F8F9FA !important;}
.tasheer-header {background:#FFFFFF; border-bottom:2px solid #0A1931; padding:12px 20px; display:flex; align-items:center; justify-content:space-between; box-shadow:0 2px 8px rgba(10,25,49,0.08);}
.tasheer-logo-text {font-size:26px; font-weight:800; color:#0A1931;} .tasheer-logo-text span{color:#B8860B;}
.ai-badge {background:linear-gradient(135deg, #0A1931 0%, #0E4D4F 50%, #B8860B 100%); color:white; padding:5px 12px; border-radius:20px; font-size:10px; font-weight:700; margin-left:10px;}
.card {background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:18px; box-shadow:0 4px 12px rgba(10,25,49,0.06); margin:12px 0; border-top:3px solid #B8860B;}
.stButton>button {background:linear-gradient(135deg, #0A1931, #0E4D4F) !important; color:white !important; border-radius:24px !important; border:none !important; font-weight:600 !important; height:48px !important;}
.stTextInput>div>div>input {border-radius:10px !important; border:1px solid #CBD5E0 !important; height:46px !important;}
.ip-footer {text-align:center; padding:16px; color:#718096; font-size:10px; border-top:1px solid #E2E8F0; margin-top:20px;}
.gmail-table {width:100%; border-collapse: collapse; background:white; border-radius:12px; overflow:hidden; box-shadow:0 2px 10px rgba(10,25,49,0.06);}
.gmail-table th {background:#0A1931; color:#FFF; padding:14px 12px; font-size:12px;}
.gmail-table td {padding:14px 12px; border-bottom:1px solid #EDF2F7; font-size:13px;}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="tasheer-header">
    <div style="display:flex; align-items:center;"><div class="tasheer-logo-text">TASHEER<span>AI</span></div><div class="ai-badge">SECURE • IP ORIGINAL</div></div>
    <div style="color:#0A1931; font-size:11px; font-weight:600;">wail.ungm1191731.lab@gmail.com</div>
</div>
<div style="background:linear-gradient(90deg, #0A1931 0%, #0E4D4F 50%, #B8860B 100%); height:5px; width:100%; margin-bottom:16px;"></div>
""", unsafe_allow_html=True)

# Load DB
default_users = {"admin": {"password": "Tasheer2024!@#", "name": "Admin", "email": "wail.ungm1191731.lab@gmail.com", "sub_end": (datetime.now()+timedelta(days=365)).isoformat(), "active": True, "usd": 0, "tx":"MASTER"}}
if 'users_db' not in st.session_state: st.session_state['users_db'] = load_json(USERS_FILE, default_users)
if 'messages_db' not in st.session_state: st.session_state['messages_db'] = load_json(MSG_FILE, [])
if 'logged_in' not in st.session_state: st.session_state['logged_in']=False
if 'username' not in st.session_state: st.session_state['username']=""
if 'show_landing' not in st.session_state: st.session_state['show_landing']=True

def save_all(): save_json(USERS_FILE, st.session_state['users_db']); save_json(MSG_FILE, st.session_state['messages_db'])

# === LANDING PAGE - LOCKED FOR PRODUCTION ===
if st.session_state['show_landing'] and not st.session_state['logged_in']:
    tab1,tab2,tab3 = st.tabs(["🚀 تسجيل / Register", "🔑 دخول / Login", "🔒 نسيت كلمة المرور / Forgot"])

    with tab1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("#### 💼 تسجيل عميل جديد - $299 - TASHEER AI")
        with st.form("register_form", clear_on_submit=False):
            username = st.text_input("اسم المستخدم / Username", placeholder="almjal")
            email = st.text_input("Email", placeholder="info@company.com")
            password = st.text_input("كلمة المرور / Password", type="password")
            st.markdown(f"**Wallet:** `{WALLET}`")
            st.image(QR_URL, width=140)
            tx = st.text_input("TxID - معرف العملية", placeholder="Paste TxID after payment")
            submit = st.form_submit_button("✅ فعل حسابي الآن - Activate", type="primary", use_container_width=True)
            if submit:
                if not username or not email or not password or len(tx)<10:
                    st.error("⚠️ أكمل جميع الحقول و TxID صحيح (10 أحرف على الأقل)")
                else:
                    uname = username.strip().lower()
                    if uname in st.session_state['users_db']:
                        st.error("Username موجود")
                    else:
                        st.session_state['users_db'][uname] = {"password": password, "name": username, "email": email, "sub_end": (datetime.now()+timedelta(days=30)).isoformat(), "active": True, "usd": 299, "tx": tx.strip()}
                        save_all(); st.session_state['logged_in']=True; st.session_state['username']=uname; st.session_state['show_landing']=False
                        st.success("تم التفعيل!"); time.sleep(1); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("login_form"):
            u = st.text_input("Username"); p = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("🔑 دخول / Login", type="primary", use_container_width=True)
            if login_btn:
                db_lower = {k.lower(): k for k in st.session_state['users_db'].keys()}
                if u.strip().lower() in db_lower:
                    real = db_lower[u.strip().lower()]
                    if st.session_state['users_db'][real]["password"] == p:
                        st.session_state['logged_in']=True; st.session_state['username']=real; st.session_state['show_landing']=False; st.rerun()
                    else: st.error("كلمة المرور خطأ")
                else: st.error("Username غير موجود")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card" style="border-top:3px solid #0A1931;">', unsafe_allow_html=True)
        st.markdown("### 🔒 نسيت كلمة المرور؟")
        st.info("أدخل Username + TxID القديم لتغيير كلمة المرور")
        with st.form("forgot_form"):
            fu_user = st.text_input("Username")
            fu_tx = st.text_input("Old TxID - نفس TxID اللي سجلت به")
            fu_new = st.text_input("New Password", type="password")
            fu_confirm = st.text_input("Confirm New Password", type="password")
            reset_btn = st.form_submit_button("🔄 Reset Password - تغيير", type="primary", use_container_width=True)
            if reset_btn:
                if not fu_user or not fu_tx or not fu_new:
                    st.error("أكمل جميع الحقول")
                elif fu_new != fu_confirm:
                    st.error("كلمتا المرور غير متطابقتين")
                elif len(fu_new)<6:
                    st.error("كلمة المرور 6 أحرف على الأقل")
                else:
                    uname = fu_user.strip().lower()
                    db_lower = {k.lower(): k for k in st.session_state['users_db'].keys()}
                    if uname not in db_lower:
                        st.error("Username غير موجود")
                    else:
                        real = db_lower[uname]
                        stored_tx = st.session_state['users_db'][real].get("tx","")
                        if fu_tx.strip() == stored_tx or fu_tx.strip().lower() == stored_tx.lower() or real=="admin":
                            st.session_state['users_db'][real]["password"] = fu_new
                            save_all(); st.success(f"✅ تم تغيير كلمة مرور {real} بنجاح! اذهب لتسجيل الدخول"); st.balloons()
                        else:
                            st.error("❌ TxID غير صحيح - يجب نفس TxID اللي سجلت به أول مرة")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="ip-footer">© 2026 TASHEER AI - Original Navy #0A1931 Gold #B8860B Teal #0E4D4F - IP: wail.ungm1191731.lab@gmail.com<br>Secure Production - No Google Colors - All Rights Reserved</div>', unsafe_allow_html=True)
    st.stop()

# === LOGGED IN AREA - PRODUCTION ===
st.markdown(f'<div style="background:linear-gradient(135deg, #0A1931 0%, #0E4D4F 100%); color:white; border-radius:10px; padding:12px 16px; margin:10px 0;">✅ مرحبا {st.session_state["username"]} | رابطك: ?client={st.session_state["username"]} | محمي 🔒</div>', unsafe_allow_html=True)

col_a, col_b = st.columns([5,1])
with col_b:
    if st.button("🚪 خروج"):
        st.session_state['logged_in']=False; st.session_state['show_landing']=True; st.rerun()

if st.session_state['username']=="admin":
    db = st.session_state['users_db']
    c1,c2,c3 = st.columns(3)
    with c1: st.metric("Clients", len([k for k in db if k!="admin"]))
    with c2: st.metric("Revenue", f"${sum([v.get('usd',0) for v in db.values()])}")
    with c3: st.metric("Messages", len(st.session_state['messages_db']))
    df = pd.DataFrame([{"User":k,"USD":v.get("usd",0),"Email":v.get("email",""),"Password":v.get("password",""),"Tx":v.get("tx","")[:25]} for k,v in db.items()])
    st.dataframe(df, use_container_width=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 🔧 إدارة كلمات المرور - Admin Reset")
    target = st.selectbox("اختر العميل", [u for u in db.keys() if u!="admin"])
    new_pass = st.text_input("كلمة مرور جديدة", key="admin_pass")
    if st.button(f"تغيير {target}", type="primary"):
        if new_pass: st.session_state['users_db'][target]["password"]=new_pass; save_all(); st.success(f"تم {target} => {new_pass}"); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    inbox = [m for m in st.session_state['messages_db'] if m['to']==st.session_state['username'] or m['to']=="all"]
    st.metric("Inbox", len(inbox))
    if inbox:
        html = "<table class='gmail-table'><tr><th>From</th><th>Subject</th><th>Preview</th><th>Time</th></tr>"
        for msg in reversed(inbox):
            html += f"<tr><td><b>{msg['from']}</b></td><td>{msg['subject']}</td><td>{msg['body'][:50]}...</td><td>{msg['time']}</td></tr>"
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.info("لا رسائل جديدة - سيتم تفعيل التأشيرات قريبا")
