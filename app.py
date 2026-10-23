import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import json, os

st.set_page_config(page_title="TASHEER AI - Google Colors", page_icon="📧", layout="wide")

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
def create_invoice_pdf(client_name, amount, txid, date_str):
    try:
        import fitz
        doc = fitz.open()
        page = doc.new_page(width=595, height=842)
        page.draw_rect(fitz.Rect(0,0,595,842), color=(1,1,1), fill=(1,1,1))
        page.draw_rect(fitz.Rect(0,0,595,100), color=(0.09,0.45,0.91), fill=(0.09,0.45,0.91))
        page.insert_text(fitz.Point(40,50), "TASHEER AI - INVOICE", fontsize=24, color=(1,1,1))
        y=130
        page.insert_text(fitz.Point(40,y), f"Invoice #: INV-{client_name.upper()}-{datetime.now().strftime('%Y%m%d')}", fontsize=14, color=(0,0,0)); y+=30
        page.insert_text(fitz.Point(40,y), f"Client: {client_name}", fontsize=12, color=(0,0,0)); y+=25
        page.insert_text(fitz.Point(40,y), f"TxID: {txid}", fontsize=10, color=(0.3,0.3,0.3)); y+=40
        page.insert_text(fitz.Point(40,y), f"TOTAL PAID: ${amount}", fontsize=16, color=(0.09,0.45,0.91))
        pdf_bytes = doc.tobytes(); doc.close(); return pdf_bytes
    except: return None

WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={WALLET}"

st.markdown("""
<style>
.stApp {background:#ffffff !important;}
.google-header {background:#ffffff; border-bottom:1px solid #dadce0; padding:18px 20px; display:flex; align-items:center; justify-content:space-between;}
.google-logo {font-family: 'Roboto', sans-serif; font-size:26px; font-weight:400;}
.google-logo .b {color:#4285F4;} .google-logo .r {color:#EA4335;} .google-logo .y {color:#FBBC05;} .google-logo .g {color:#34A853;}
.ai-badge {background: linear-gradient(135deg, #4285F4, #9C27B0); color:white; padding:4px 10px; border-radius:16px; font-size:12px; font-weight:600; margin-left:10px;}
.gmail-table {width:100%; border-collapse: collapse; background:white; border-radius:8px; overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,0.1);}
.gmail-table th {background:#f1f3f4; color:#5f6368; font-weight:500; padding:12px; text-align:left; font-size:13px; border-bottom:1px solid #dadce0;}
.gmail-table td {padding:14px 12px; border-bottom:1px solid #eceff1; font-size:14px; color:#202124;}
.gmail-table tr:hover {background:#f8f9fa;}
.welcome-box {background:#e8f0fe; border:1px solid #d2e3fc; border-radius:8px; padding:12px 16px; color:#1967d2; margin:10px 0;}
.card-google {background:#ffffff; border:1px solid #e8eaed; border-radius:12px; padding:16px; box-shadow:0 1px 2px rgba(60,64,67,0.1); margin:10px 0;}
.stButton>button {background:#1a73e8 !important; color:white !important; border-radius:24px !important;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="google-header">
    <div class="google-logo">
        <span class="b">T</span><span class="r">A</span><span class="y">S</span><span class="b">H</span><span class="g">E</span><span class="r">E</span><span class="b">R</span>
        <span style="color:#5f6368; font-size:22px; margin-left:4px;">AI</span>
        <span class="ai-badge">3D • Gmail • PRO</span>
    </div>
</div>
<div style="background:linear-gradient(90deg, #4285F4 0%, #EA4335 33%, #FBBC05 66%, #34A853 100%); height:4px; width:100%; margin-bottom:16px;"></div>
""", unsafe_allow_html=True)

LANG = {"AR": {"login":"دخول","register":"تسجيل أوتوماتيك","logout":"خروج","subject":"الموضوع","send":"إرسال","receive":"الوارد / Inbox","sent":"الصادر","welcome":"مرحبا","link":"رابطك","msg_sent":"تم الإرسال!","username":"اسم الشركة","password":"كلمة المرور","txid":"TxID","activate":"فعل حسابي الآن","reply":"رد سريع","invoice":"تحميل الفاتورة"},"EN": {"login":"Login","register":"Auto Register","logout":"Logout","subject":"Subject","send":"Send","receive":"Inbox","sent":"Sent","welcome":"Welcome","link":"Your Link","msg_sent":"Sent!","username":"Username","password":"Password","txid":"TxID","activate":"Activate Now","reply":"Quick Reply","invoice":"Download Invoice"}}

default_users = {"admin": {"password": "Tasheer2024!", "name": "Gomez Admin", "email": "report.gomez@gmail.com", "sub_end": (datetime.now()+timedelta(days=365)).isoformat(), "role": "admin", "active": True, "usd": 0, "tx":""}}
if 'users_db' not in st.session_state: st.session_state['users_db'] = load_json(USERS_FILE, default_users)
if 'messages_db' not in st.session_state: st.session_state['messages_db'] = load_json(MSG_FILE, [{"from": "admin", "to": "almjal", "subject": "Welcome - تم التفعيل", "body": "تم تفعيل حسابك - Tx: TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH - $299", "time": datetime.now().strftime('%Y-%m-%d %H:%M'), "read": False, "id": 1}])
if 'logged_in' not in st.session_state: st.session_state['logged_in']=False
if 'username' not in st.session_state: st.session_state['username']=""
if 'show_landing' not in st.session_state: st.session_state['show_landing']=True
if 'lang' not in st.session_state: st.session_state['lang']="AR"
if 'reply_to' not in st.session_state: st.session_state['reply_to']=None

def t(k): return LANG[st.session_state['lang']].get(k,k)
def save_all(): save_json(USERS_FILE, st.session_state['users_db']); save_json(MSG_FILE, st.session_state['messages_db'])
def check_tx(tx): return len(tx.strip())>=10
def send_msg(f,to_user,subj,body):
    st.session_state['messages_db'].append({"from": f, "to": to_user, "subject": subj, "body": body, "time": datetime.now().strftime('%Y-%m-%d %H:%M'), "read": False, "id": len(st.session_state['messages_db'])+1}); save_all()

col1,col2 = st.columns([4,1])
with col2:
    lc = st.radio("Lang", ["AR - عربي", "EN - English"], horizontal=True, label_visibility="collapsed")
    st.session_state['lang']="AR" if "AR" in lc else "EN"

if st.session_state['show_landing'] and not st.session_state['logged_in']:
    tab1,tab2 = st.tabs([f"🚀 {t('register')}", f"🔑 {t('login')}"])
    with tab1:
        st.markdown('<div class="card-google">', unsafe_allow_html=True)
        username = st.text_input(t('username'), placeholder="almjal")
        email = st.text_input("Email", placeholder="info@company.com")
        password = st.text_input(t('password'), type="password")
        st.code(WALLET); st.image(QR_URL, width=160)
        tx = st.text_input(t('txid'), placeholder="a1b2c3...")
        if st.button(t('activate'), type="primary", use_container_width=True):
            if username and email and password and check_tx(tx):
                uname = username.strip().lower()
                st.session_state['users_db'][uname] = {"password": password, "name": username, "email": email, "sub_end": (datetime.now()+timedelta(days=30)).isoformat(), "active": True, "role": "user", "tx": tx, "usd": 299}
                save_all(); st.session_state['logged_in']=True; st.session_state['username']=uname; st.session_state['show_landing']=False; send_msg("admin", uname, "Welcome - تم التفعيل", f"تم تفعيل حسابك - Tx: {tx} - $299"); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with tab2:
        st.markdown('<div class="card-google">', unsafe_allow_html=True)
        with st.form("login"):
            u = st.text_input(t('username')); p = st.text_input(t('password'), type="password")
            st.caption("Admin: admin / Tasheer2024!")
            if st.form_submit_button(t('login'), type="primary"):
                db = st.session_state['users_db']; u_clean = u.strip().lower(); db_lower = {k.lower(): k for k in db.keys()}
                if u_clean in db_lower:
                    real_key = db_lower[u_clean]
                    if db[real_key]["password"] == p:
                        st.session_state['logged_in']=True; st.session_state['username']=real_key; st.session_state['show_landing']=False; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

st.markdown(f'<div class="welcome-box">✅ {t("welcome")} {st.session_state["username"]} - {t("link")}: ?client={st.session_state["username"]}</div>', unsafe_allow_html=True)
if st.button(f"🚪 {t('logout')}"):
    st.session_state['logged_in']=False; st.session_state['show_landing']=True; st.rerun()

if st.session_state['username']=="admin":
    st.markdown('<div class="card-google"><h3>📊 Admin Dashboard</h3></div>', unsafe_allow_html=True)
    db = st.session_state['users_db']; msgs = st.session_state['messages_db']
    c1,c2,c3 = st.columns(3)
    with c1: st.metric("Clients", len([k for k in db.keys() if k!="admin"]))
    with c2: st.metric("Revenue", f"${sum([v.get('usd',0) for v in db.values()])}")
    with c3: st.metric("Messages", len(msgs))
    df = pd.DataFrame([{"User":k,"USD":v.get("usd",0),"Email":v.get("email","")} for k,v in db.items()])
    st.dataframe(df, use_container_width=True)
    t1,t2 = st.tabs(["Inbox", "Send"])
    with t1:
        inbox = [m for m in msgs if m['to']=="admin"]
        for msg in reversed(inbox):
            st.info(f"From: {msg['from']} | {msg['subject']} - {msg['body']}")
    with t2:
        target = st.selectbox("To", [u for u in db.keys() if u!="admin"])
        subj = st.text_input("Subject"); body = st.text_area("Message")
        if st.button("Send"):
            if subj and body: send_msg("admin", target, subj, body); st.success("Sent"); st.rerun()
else:
    ut1,ut2,ut3 = st.tabs([f"📥 {t('receive')} - Gmail Table", f"📤 {t('send')}", f"📨 {t('sent')}"])
    with ut1:
        my_inbox = [m for m in st.session_state['messages_db'] if m['to']==st.session_state['username'] or m['to']=="all"]
        st.metric("New Messages", len(my_inbox))
        if my_inbox:
            html = "<table class='gmail-table'><tr><th>From</th><th>Subject</th><th>Message Preview</th><th>Time</th></tr>"
            for msg in reversed(my_inbox):
                html += f"<tr><td><b>{msg['from']}</b></td><td><b>{msg['subject']}</b></td><td>{msg['body'][:60]}...</td><td>{msg['time']}</td></tr>"
            html += "</table>"
            st.markdown(html, unsafe_allow_html=True)
            st.divider()
            for msg in reversed(my_inbox):
                st.markdown(f"<div class='card-google' style='border-left:4px solid #1a73e8;'><b>From: {msg['from']}</b> | <small>{msg['time']}</small><br><b>Subject: {msg['subject']}</b><br>{msg['body']}</div>", unsafe_allow_html=True)
                if st.button(f"↩️ {t('reply')} - {msg['subject'][:20]}", key=f"qr_{msg['id']}"):
                    st.session_state['reply_to'] = msg['id']
                if st.session_state['reply_to'] == msg['id']:
                    reply_text = st.text_area("Reply", key=f"reply_text_{msg['id']}")
                    if st.button("📤 Send", key=f"send_reply_{msg['id']}", type="primary"):
                        if reply_text: send_msg(st.session_state['username'], msg['from'], f"Re: {msg['subject']}", reply_text); st.success(t('msg_sent')); st.session_state['reply_to']=None; st.rerun()
    with ut2:
        st.markdown('<div class="card-google">', unsafe_allow_html=True)
        subj = st.text_input("Subject *"); body = st.text_area("Message *", height=150)
        if st.button("📤 Send -> admin", type="primary", use_container_width=True):
            if subj and body: send_msg(st.session_state['username'], "admin", subj, body); st.success(t('msg_sent')); st.balloons(); st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with ut3:
        my_sent = [m for m in st.session_state['messages_db'] if m['from']==st.session_state['username']]
        for msg in reversed(my_sent):
            st.write(f"To: {msg['to']} | {msg['subject']} - {msg['body'][:50]}")
