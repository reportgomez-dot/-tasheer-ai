import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="TASHEER AI - Google Style", page_icon="📧", layout="wide")

WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={WALLET}"

# === Google / Microsoft Clean White Theme ===
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Cairo:wght@400;600&display=swap');
* {font-family: 'Roboto', 'Cairo', sans-serif;}
.stApp {
    background: #ffffff !important;
    background-color: #ffffff !important;
}
.main {background: #ffffff;}
/* Google-style header */
.header-google {
    background: #ffffff;
    border: 1px solid #dadce0;
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.header-google h1 {
    color: #202124;
    font-size: 28px;
    font-weight: 500;
    margin: 0;
}
.header-google p {
    color: #5f6368;
    font-size: 14px;
    margin-top: 8px;
}
/* Microsoft fluent card */
.card-google {
    background: #ffffff;
    border: 1px solid #e8eaed;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 1px 2px rgba(60,64,67,0.1), 0 1px 3px rgba(60,64,67,0.1);
    margin: 12px 0;
}
.card-google:hover {
    box-shadow: 0 2px 8px rgba(60,64,67,0.15), 0 1px 4px rgba(60,64,67,0.1);
}
/* Google inputs */
.stTextInput>div>div, .stTextArea>div>div {
    background: #ffffff !important;
    border: 1px solid #dadce0 !important;
    border-radius: 8px !important;
}
.stTextInput>div>div:focus-within, .stTextArea>div>div:focus-within {
    border: 2px solid #1a73e8 !important;
    box-shadow: 0 0 0 1px #1a73e8 !important;
}
/* Buttons - Google blue */
.stButton>button {
    background: #1a73e8 !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: 500 !important;
    padding: 10px 24px !important;
}
.stButton>button:hover {
    background: #185abc !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.2) !important;
}
/* Tabs - Google style */
.stTabs [data-baseweb="tab-list"] {
    background: #ffffff;
    border-bottom: 1px solid #dadce0;
    gap: 0px;
}
.stTabs [data-baseweb="tab"] {
    color: #5f6368;
    font-weight: 500;
    border-radius: 0px;
    border-bottom: 3px solid transparent;
}
.stTabs [aria-selected="true"] {
    color: #1a73e8 !important;
    border-bottom: 3px solid #1a73e8 !important;
    background: #ffffff !important;
}
/* Messages - Gmail style */
.msg-gmail {
    background: #ffffff;
    border: 1px solid #dadce0;
    border-radius: 8px;
    padding: 16px;
    margin: 8px 0;
    border-left: 4px solid #1a73e8;
}
.msg-gmail:hover {
    background: #f8f9fa;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.welcome-box {
    background: #e8f0fe;
    border: 1px solid #d2e3fc;
    border-radius: 8px;
    padding: 12px 16px;
    color: #1967d2;
}
</style>
""", unsafe_allow_html=True)

LANG = {
    "AR": {"title": "TASHEER AI - نظام إيميل", "subtitle": "واجهة نظيفة مثل Google / Microsoft - واضحة 100%", "login":"دخول","register":"تسجيل أوتوماتيك","map":"خريطة","logout":"خروج","subject":"الموضوع / Subject","from":"من / From","to":"إلى / To","body":"نص الرسالة / Message","send":"📤 إرسال / Send","receive":"📥 الوارد / Inbox","sent":"📤 الصادر / Sent","welcome":"مرحبا","link":"رابطك / Your Link","msg_sent":"تم الإرسال - Sent!","no_msg":"لا يوجد رسائل","new_msg":"رسائل جديدة","username":"اسم الشركة / Username","password":"كلمة المرور / Password","txid":"TxID","activate":"فعل حسابي الآن / Activate Now"},
    "EN": {"title": "TASHEER AI - Email System", "subtitle": "Clean interface like Google / Microsoft - 100% clear", "login":"Login","register":"Auto Register","map":"Map","logout":"Logout","subject":"Subject / الموضوع","from":"From / من","to":"To / إلى","body":"Message / نص الرسالة","send":"📤 Send / إرسال","receive":"📥 Inbox / الوارد","sent":"📤 Sent / الصادر","welcome":"Welcome","link":"Your Link / رابطك","msg_sent":"Sent! - تم الإرسال","no_msg":"No Messages","new_msg":"New Messages","username":"Username / اسم الشركة","password":"Password / كلمة المرور","txid":"TxID","activate":"Activate Now"}
}

if 'users_db' not in st.session_state:
    st.session_state['users_db'] = {"admin": {"password": "Tasheer2024!", "name": "Gomez Admin", "email": "report.gomez@gmail.com", "sub_end": datetime.now()+timedelta(days=365), "role": "admin", "active": True, "usd": 0}}
if 'messages_db' not in st.session_state:
    st.session_state['messages_db'] = [
        {"from": "admin", "to": "almjal", "subject": "Welcome - مرحبا بك", "body": "تم تفعيل حسابك - فاتورتك $299", "time": datetime.now().strftime('%Y-%m-%d %H:%M'), "read": False, "id": 1}
    ]
if 'logged_in' not in st.session_state:
    st.session_state['logged_in']=False
if 'username' not in st.session_state:
    st.session_state['username']=""
if 'show_landing' not in st.session_state:
    st.session_state['show_landing']=True
if 'lang' not in st.session_state:
    st.session_state['lang']="AR"

def t(k): return LANG[st.session_state['lang']].get(k,k)
def check_tx(tx): return len(tx.strip())>=10
def send_msg(f,to_user,subj,body):
    st.session_state['messages_db'].append({"from": f, "to": to_user, "subject": subj, "body": body, "time": datetime.now().strftime('%Y-%m-%d %H:%M'), "read": False, "id": len(st.session_state['messages_db'])+1})

col1,col2 = st.columns([4,1])
with col2:
    lc = st.radio("Lang", ["AR - عربي", "EN - English"], horizontal=True, label_visibility="collapsed")
    st.session_state['lang']="AR" if "AR" in lc else "EN"

if st.session_state['show_landing'] and not st.session_state['logged_in']:
    st.markdown(f"""
    <div class="header-google">
        <div style="display:flex; align-items:center; justify-content:center; gap:10px;">
            <span style="font-size:32px;">📧</span>
            <h1>{t("title")}</h1>
        </div>
        <p>{t("subtitle")}</p>
        <div style="margin-top:16px; display:flex; justify-content:center; gap:8px; flex-wrap:wrap;">
            <span style="background:#f1f3f4; padding:6px 12px; border-radius:16px; font-size:12px; color:#5f6368;">Subject</span>
            <span style="background:#f1f3f4; padding:6px 12px; border-radius:16px; font-size:12px; color:#5f6368;">From / To / Send</span>
            <span style="background:#f1f3f4; padding:6px 12px; border-radius:16px; font-size:12px; color:#5f6368;">Receive / Reply</span>
            <span style="background:#e8f0fe; padding:6px 12px; border-radius:16px; font-size:12px; color:#1967d2;">✓ Google Style</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1,tab2,tab3 = st.tabs([f"🚀 {LANG[st.session_state['lang']]['register']}", f"🗺️ {LANG[st.session_state['lang']]['map']}", f"🔑 {LANG[st.session_state['lang']]['login']}"])
    with tab1:
        c1,c2 = st.columns([2,1])
        with c1:
            st.markdown('<div class="card-google">', unsafe_allow_html=True)
            username = st.text_input(LANG[st.session_state['lang']]['username'], placeholder="almajal", key="au_user")
            email = st.text_input("Email / الإيميل", placeholder="info@company.com", key="au_email")
            password = st.text_input(LANG[st.session_state['lang']]['password'], type="password", key="au_pass")
            st.code(WALLET)
            st.image(QR_URL, width=160)
            tx = st.text_input(LANG[st.session_state['lang']]['txid'], placeholder="a1b2c3...", key="au_tx")
            if st.button(LANG[st.session_state['lang']]['activate'], type="primary", use_container_width=True):
                if username and email and password and check_tx(tx):
                    uname = username.strip().lower()
                    st.session_state['users_db'][uname] = {"password": password, "name": username, "email": email, "sub_end": datetime.now()+timedelta(days=30), "active": True, "role": "user", "tx": tx, "usd": 299, "link": f"?client={uname}"}
                    st.session_state['logged_in']=True
                    st.session_state['username']=uname
                    st.session_state['show_landing']=False
                    send_msg("admin", uname, "Welcome - مرحبا", "تم تفعيل حسابك")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown("""
            <div class="card-google" style="background:#f8f9fa;">
                <h4 style="color:#202124; margin:0;">✨ Google Style Features</h4>
                <p style="color:#5f6368; font-size:13px; margin-top:10px;">
                ✓ White clean background<br>
                ✓ Gmail-like inbox<br>
                ✓ Subject/From/To/Send<br>
                ✓ Receive/Reply<br>
                ✓ AR/EN Bilingual<br>
                ✓ Clear & readable
                </p>
            </div>
            """, unsafe_allow_html=True)
    with tab2:
        st.markdown('<div class="card-google">', unsafe_allow_html=True)
        st.info("🗺️ Map - Clean white background - خريطة")
        st.markdown('</div>', unsafe_allow_html=True)
    with tab3:
        st.markdown('<div class="card-google">', unsafe_allow_html=True)
        with st.form("login"):
            u = st.text_input(LANG[st.session_state['lang']]['username'])
            p = st.text_input(LANG[st.session_state['lang']]['password'], type="password")
            st.caption("Admin: admin / Tasheer2024! - Case insensitive")
            if st.form_submit_button(LANG[st.session_state['lang']]['login'], type="primary"):
                db = st.session_state['users_db']
                u_clean = u.strip().lower()
                db_lower = {k.lower(): k for k in db.keys()}
                if u_clean in db_lower:
                    real_key = db_lower[u_clean]
                    if db[real_key]["password"] == p:
                        st.session_state['logged_in']=True
                        st.session_state['username']=real_key
                        st.session_state['show_landing']=False
                        st.rerun()
                    else:
                        st.error("Wrong password")
                else:
                    st.error("Wrong username")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# Logged in view
st.markdown(f'<div class="welcome-box">✅ {t("welcome")} {st.session_state["username"]} - {t("link")}: ?client={st.session_state["username"]}</div>', unsafe_allow_html=True)
if st.button(f"🚪 {LANG[st.session_state['lang']]['logout']}"):
    st.session_state['logged_in']=False
    st.session_state['show_landing']=True
    st.rerun()

if st.session_state['username']=="admin":
    st.markdown('<div class="card-google" style="margin-top:16px;"><h3 style="color:#202124; margin:0;">📊 Admin Panel - Google Style</h3></div>', unsafe_allow_html=True)
    db = st.session_state['users_db']
    st.dataframe(pd.DataFrame([{"User":k,"USD":v.get("usd",0),"Email":v.get("email","")} for k,v in db.items()]), use_container_width=True)
    t1,t2,t3 = st.tabs([f"📥 {t('receive')}", f"📤 {t('send')}", f"📢 Broadcast"])
    with t1:
        inbox = [m for m in st.session_state['messages_db'] if m['to']=="admin"]
        for msg in reversed(inbox):
            st.markdown(f'<div class="msg-gmail"><b>{t("from")}: {msg["from"]}</b> | {t("subject")}: {msg["subject"]}<br>{t("body")}: {msg["body"]}<br><small style="color:#5f6368;">{msg["time"]}</small></div>', unsafe_allow_html=True)
            rb = st.text_area("Reply", key=f"reply_{msg['id']}")
            if st.button(f"{t('send')} -> {msg['from']}", key=f"send_{msg['id']}"):
                if rb:
                    send_msg("admin", msg['from'], f"Re: {msg['subject']}", rb)
                    st.success(t('msg_sent'))
    with t2:
        all_users = [u for u in db.keys() if u!="admin"]
        if all_users:
            target = st.selectbox(f"{t('to')}", all_users)
            subj = st.text_input(f"{t('subject')}", key="adm_subj")
            body = st.text_area(f"{t('body')}", key="adm_body")
            if st.button(f"{t('send')} -> {target}", type="primary", use_container_width=True):
                if subj and body:
                    send_msg("admin", target, subj, body)
                    st.success(f"{t('msg_sent')} -> {target}")
    with t3:
        subj_all = st.text_input(f"{t('subject')} - Broadcast", key="broad_subj")
        body_all = st.text_area(f"{t('body')} - Broadcast", key="broad_body")
        if st.button("📢 Broadcast", type="primary", use_container_width=True):
            if subj_all and body_all:
                send_msg("admin", "all", subj_all, body_all)
                st.success("Broadcast Sent")
else:
    st.markdown('<div class="card-google" style="margin-top:16px;"><h3 style="color:#202124; margin:0;">📧 صندوق رسائلك - Send & Receive</h3><p style="color:#5f6368; margin:5px 0 0 0; font-size:13px;">Gmail-like interface - واجهة مثل جيميل</p></div>', unsafe_allow_html=True)
    ut1,ut2,ut3 = st.tabs([f"📥 {t('receive')}", f"📤 {t('send')}", f"📨 {t('sent')}"])
    with ut1:
        my_inbox = [m for m in st.session_state['messages_db'] if m['to']==st.session_state['username'] or m['to']=="all"]
        st.metric(t('new_msg'), len(my_inbox))
        for msg in reversed(my_inbox):
            st.markdown(f'<div class="msg-gmail"><b>{t("from")}: {msg["from"]}</b><br><b>{t("subject")}: {msg["subject"]}</b><br>{msg["body"]}<br><small style="color:#5f6368;">{msg["time"]}</small></div>', unsafe_allow_html=True)
    with ut2:
        st.markdown('<div class="card-google">', unsafe_allow_html=True)
        st.text_input(f"{t('to')}", value="admin", disabled=True)
        subj = st.text_input(f"{t('subject')} *", key="u_subj")
        body = st.text_area(f"{t('body')} *", height=150, key="u_body")
        if st.button(f"📤 {t('send')} -> admin", type="primary", use_container_width=True):
            if subj and body:
                send_msg(st.session_state['username'], "admin", subj, body)
                st.success(t('msg_sent'))
                st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)
    with ut3:
        my_sent = [m for m in st.session_state['messages_db'] if m['from']==st.session_state['username']]
        for msg in reversed(my_sent):
            st.markdown(f'<div class="msg-gmail"><b>{t("to")}: {msg["to"]}</b><br><b>{t("subject")}: {msg["subject"]}</b><br>{msg["body"]}</div>', unsafe_allow_html=True)
