import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import json, os

st.set_page_config(page_title="TASHEER AI - IP Registered", page_icon="📧", layout="wide")

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

# === هوية بصرية جديدة - للملكية الفكرية - بعيد عن جوجل ===
st.markdown("""
<style>
.stApp {background:#F8F9FA !important;}
/* TASHEER Brand Colors - IP Original: Navy #0A1931 Gold #B8860B Teal #0E4D4F */
.tasheer-header {background:#FFFFFF; border-bottom:2px solid #0A1931; padding:14px 20px; display:flex; align-items:center; justify-content:space-between; box-shadow:0 2px 8px rgba(10,25,49,0.08);}
.tasheer-logo-text {font-family:'Inter', sans-serif; font-size:28px; font-weight:800; color:#0A1931; letter-spacing:-0.5px;}
.tasheer-logo-text span {color:#B8860B;}
.ai-badge-ip {background:linear-gradient(135deg, #0A1931 0%, #0E4D4F 50%, #B8860B 100%); color:white; padding:5px 14px; border-radius:20px; font-size:11px; font-weight:700; letter-spacing:0.5px; margin-left:12px; box-shadow:0 2px 8px rgba(10,25,49,0.2);}
.welcome-box {background:linear-gradient(135deg, #0A1931 0%, #0E4D4F 100%); color:white; border-radius:10px; padding:14px 18px; margin:12px 0;}
.card-ip {background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:18px; box-shadow:0 4px 12px rgba(10,25,49,0.06); margin:12px 0; border-top:3px solid #B8860B;}
.stButton>button {background:linear-gradient(135deg, #0A1931, #0E4D4F) !important; color:white !important; border-radius:24px !important; border:none !important; font-weight:600 !important; letter-spacing:0.3px !important; box-shadow:0 2px 8px rgba(10,25,49,0.2) !important;}
.stButton>button:hover {background:linear-gradient(135deg, #B8860B, #D4A017) !important;}
.gmail-table {width:100%; border-collapse: collapse; background:white; border-radius:12px; overflow:hidden; box-shadow:0 2px 10px rgba(10,25,49,0.06); border:1px solid #E2E8F0;}
.gmail-table th {background:#0A1931; color:#FFFFFF; font-weight:600; padding:14px 12px; text-align:left; font-size:13px; letter-spacing:0.3px;}
.gmail-table td {padding:14px 12px; border-bottom:1px solid #EDF2F7; font-size:14px; color:#1A202C;}
.gmail-table tr:hover {background:#F7FAFC;}
.ip-footer {text-align:center; padding:20px; color:#718096; font-size:11px; border-top:1px solid #E2E8F0; margin-top:30px;}
</style>
""", unsafe_allow_html=True)

# Header - IP Original
st.markdown("""
<div class="tasheer-header">
    <div style="display:flex; align-items:center;">
        <div class="tasheer-logo-text">TASHEER<span>AI</span></div>
        <div class="ai-badge-ip">IP ORIGINAL • NAVY GOLD TEAL • SECURE</div>
    </div>
    <div style="color:#0A1931; font-size:12px; font-weight:600;">© TASHEER AI - الملكية الفكرية</div>
</div>
<div style="background:linear-gradient(90deg, #0A1931 0%, #0E4D4F 50%, #B8860B 100%); height:5px; width:100%; margin-bottom:18px;"></div>
""", unsafe_allow_html=True)

# Show logo if uploaded
if os.path.exists("logo.png"):
    st.image("logo.png", width=360)

default_users = {"admin": {"password": "Tasheer2024!", "name": "Admin", "email": "report.gomez@gmail.com", "sub_end": (datetime.now()+timedelta(days=365)).isoformat(), "active": True, "usd": 0, "tx":""}}
if 'users_db' not in st.session_state: st.session_state['users_db'] = load_json(USERS_FILE, default_users)
if 'messages_db' not in st.session_state: st.session_state['messages_db'] = load_json(MSG_FILE, [{"from": "admin", "to": "almjal", "subject": "Welcome - تم التفعيل", "body": "تم تفعيل حسابك $299 - TASHEER AI IP Original", "time": datetime.now().strftime('%Y-%m-%d %H:%M'), "read": False, "id": 1}])
if 'logged_in' not in st.session_state: st.session_state['logged_in']=False
if 'username' not in st.session_state: st.session_state['username']=""
if 'show_landing' not in st.session_state: st.session_state['show_landing']=True
if 'lang' not in st.session_state: st.session_state['lang']="AR"

def save_all(): save_json(USERS_FILE, st.session_state['users_db']); save_json(MSG_FILE, st.session_state['messages_db'])
def send_msg(f,to_user,subj,body):
    st.session_state['messages_db'].append({"from": f, "to": to_user, "subject": subj, "body": body, "time": datetime.now().strftime('%Y-%m-%d %H:%M'), "read": False, "id": len(st.session_state['messages_db'])+1}); save_all()

col1,col2 = st.columns([4,1])
with col2:
    lc = st.radio("Lang", ["AR - عربي", "EN - English"], horizontal=True, label_visibility="collapsed")
    st.session_state['lang']="AR" if "AR" in lc else "EN"

if st.session_state['show_landing'] and not st.session_state['logged_in']:
    tab1,tab2,tab3 = st.tabs(["🚀 تسجيل / Register", "🔑 دخول / Login", "🔒 نسيت كلمة المرور / Forgot Password"])
    
    with tab1:
        st.markdown('<div class="card-ip">', unsafe_allow_html=True)
        st.markdown("#### هوية بصرية أصلية - TASHEER AI © الملكية الفكرية")
        username = st.text_input("اسم الشركة / Username", placeholder="almjal", key="reg_u")
        email = st.text_input("Email", placeholder="info@company.com", key="reg_e")
        password = st.text_input("كلمة المرور / Password", type="password", key="reg_p")
        st.code(WALLET); st.image(QR_URL, width=150)
        tx = st.text_input("TxID", placeholder="a1b2c3...", key="reg_tx")
        if st.button("فعل حسابي الآن / Activate Now", type="primary", use_container_width=True):
            if username and email and password and len(tx)>=10:
                uname = username.strip().lower()
                st.session_state['users_db'][uname] = {"password": password, "name": username, "email": email, "sub_end": (datetime.now()+timedelta(days=30)).isoformat(), "active": True, "usd": 299, "tx": tx}
                save_all(); st.session_state['logged_in']=True; st.session_state['username']=uname; st.session_state['show_landing']=False; send_msg("admin", uname, "Welcome", f"Activated - {tx}"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card-ip">', unsafe_allow_html=True)
        with st.form("login"):
            u = st.text_input("Username"); p = st.text_input("Password", type="password")
            if st.form_submit_button("Login / دخول", type="primary"):
                db = st.session_state['users_db']; u_clean = u.strip().lower(); db_lower = {k.lower(): k for k in db.keys()}
                if u_clean in db_lower:
                    real_key = db_lower[u_clean]
                    if db[real_key]["password"] == p:
                        st.session_state['logged_in']=True; st.session_state['username']=real_key; st.session_state['show_landing']=False; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card-ip" style="border-top:3px solid #0A1931;">', unsafe_allow_html=True)
        st.markdown("### 🔒 نسيت كلمة المرور؟")
        fu_user = st.text_input("Username", key="forgot_u")
        fu_tx = st.text_input("Old TxID", key="forgot_tx")
        fu_new = st.text_input("New Password", type="password", key="forgot_new")
        fu_confirm = st.text_input("Confirm New Password", type="password", key="forgot_confirm")
        if st.button("🔄 Reset Password", type="primary", use_container_width=True):
            if fu_user and fu_tx and fu_new and fu_confirm:
                uname = fu_user.strip().lower()
                db = st.session_state['users_db']
                db_lower = {k.lower(): k for k in db.keys()}
                if uname in db_lower:
                    real_key = db_lower[uname]
                    if fu_tx.strip() == db[real_key].get("tx",""):
                        if fu_new == fu_confirm:
                            st.session_state['users_db'][real_key]["password"] = fu_new
                            save_all(); st.success(f"تم التغيير - Changed for {real_key}"); st.balloons()
                        else: st.error("Passwords don't match")
                    else: st.error("TxID incorrect")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="ip-footer">© 2026 TASHEER AI - Original Brand Identity: Navy #0A1931 Gold #B8860B Teal #0E4D4F<br>All rights reserved - مسجل للملكية الفكرية - IP Original Design - No Google Colors</div>', unsafe_allow_html=True)
    st.stop()

st.markdown(f'<div class="welcome-box">✅ مرحبا {st.session_state["username"]} - TASHEER AI الأصلي - رابطك: ?client={st.session_state["username"]}</div>', unsafe_allow_html=True)
if st.button("🚪 خروج / Logout"):
    st.session_state['logged_in']=False; st.session_state['show_landing']=True; st.rerun()

if st.session_state['username']=="admin":
    db = st.session_state['users_db']
    c1,c2,c3 = st.columns(3)
    with c1: st.metric("Clients", len([k for k in db.keys() if k!="admin"]))
    with c2: st.metric("Revenue", f"${sum([v.get('usd',0) for v in db.values()])}")
    with c3: st.metric("Messages", len(st.session_state['messages_db']))
    df = pd.DataFrame([{"User":k,"USD":v.get("usd",0),"Email":v.get("email",""),"Password":v.get("password",""),"Tx":v.get("tx","")[:20]} for k,v in db.items()])
    st.dataframe(df, use_container_width=True)
    st.markdown('<div class="card-ip">', unsafe_allow_html=True)
    st.markdown("#### 🔒 تغيير كلمة مرور عميل / Reset Password - Forgot Column")
    target = st.selectbox("اختر العميل", [u for u in db.keys() if u!="admin"])
    new_pass = st.text_input("كلمة مرور جديدة", key="admin_new_pass")
    if st.button(f"تغيير كلمة مرور {target}"):
        if new_pass:
            st.session_state['users_db'][target]["password"] = new_pass
            save_all(); st.success(f"تم - {target} => {new_pass}"); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    my_inbox = [m for m in st.session_state['messages_db'] if m['to']==st.session_state['username'] or m['to']=="all"]
    st.metric("New Messages", len(my_inbox))
    if my_inbox:
        html = "<table class='gmail-table'><tr><th>From</th><th>Subject</th><th>Preview</th><th>Time</th></tr>"
        for msg in reversed(my_inbox):
            html += f"<tr><td><b>{msg['from']}</b></td><td>{msg['subject']}</td><td>{msg['body'][:50]}...</td><td>{msg['time']}</td></tr>"
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)
