import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="TASHEER AI - 3D", page_icon="🌐", layout="wide")

WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={WALLET}"

# === 3D CSS ===
st.markdown("""
<style>
.stApp {background: radial-gradient(circle at 20% 30%, #0a4a2a 0%, #021a0f 60%, #000000 100%);}
.header-3d {
    background: linear-gradient(135deg, rgba(10,122,66,0.95), rgba(0,0,0,0.9));
    border: 2px solid rgba(0,255,136,0.3);
    border-radius: 25px; padding: 25px; text-align:center; color:white;
    box-shadow: 0 20px 40px rgba(0,255,136,0.2), 0 0 80px rgba(0,255,136,0.1);
    animation: float3d 4s ease-in-out infinite;
}
@keyframes float3d {0%,100%{transform:translateY(0px)} 50%{transform:translateY(-8px)}}
.card-3d {
    background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.02));
    border: 1px solid rgba(0,255,136,0.2); border-radius:20px; padding:20px;
    backdrop-filter: blur(15px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.3), 0 0 20px rgba(0,255,136,0.1);
    transform: perspective(1000px) rotateY(-1deg); transition: all 0.4s;
    color:white;
}
.card-3d:hover {transform: perspective(1000px) rotateY(0deg) translateY(-5px) scale(1.01); border-color:rgba(0,255,136,0.5);}
.msg-3d {
    background: linear-gradient(145deg, rgba(0,255,136,0.1), rgba(0,0,0,0.3));
    border-left: 4px solid #00ff88; border-radius:15px; padding:15px; margin:10px 0;
    box-shadow: 0 5px 15px rgba(0,0,0,0.2); color:white;
}
</style>
""", unsafe_allow_html=True)

LANG = {
    "AR": {"title": "🌐 TASHEER AI - نظام 3D", "subtitle": "إرسال - استقبال - فاتورة - بتقنية 3D", "login":"دخول","register":"تسجيل أوتوماتيك","map":"خريطة","logout":"خروج","subject":"الموضوع / Subject","from":"من / From","to":"إلى / To","body":"نص الرسالة / Message","send":"📤 إرسال / Send","receive":"📥 الوارد / Inbox","sent":"📤 الصادر / Sent","welcome":"مرحبا","link":"رابطك / Your Link","msg_sent":"تم الإرسال - Sent! 🚀","no_msg":"لا يوجد رسائل","new_msg":"رسائل جديدة","username":"اسم الشركة / Username","password":"كلمة المرور / Password","txid":"TxID","activate":"🚀 فعل حسابي 3D الآن"},
    "EN": {"title": "🌐 TASHEER AI - 3D System", "subtitle": "Send - Receive - Invoice - In 3D", "login":"Login","register":"Auto Register","map":"Map","logout":"Logout","subject":"Subject / الموضوع","from":"From / من","to":"To / إلى","body":"Message / نص الرسالة","send":"📤 Send / إرسال","receive":"📥 Inbox / الوارد","sent":"📤 Sent / الصادر","welcome":"Welcome","link":"Your Link / رابطك","msg_sent":"Sent! - تم الإرسال 🚀","no_msg":"No Messages","new_msg":"New Messages","username":"Username / اسم الشركة","password":"Password / كلمة المرور","txid":"TxID","activate":"🚀 Activate 3D Now"}
}

if 'users_db' not in st.session_state:
    st.session_state['users_db'] = {"admin": {"password": "Tasheer2024!", "name": "Gomez Admin", "email": "report.gomez@gmail.com", "sub_end": datetime.now()+timedelta(days=365), "role": "admin", "active": True, "usd": 0}}
if 'messages_db' not in st.session_state:
    st.session_state['messages_db'] = [
        {"from": "admin", "to": "almjal", "subject": "Welcome - مرحبا بك في TASHEER AI 3D", "body": "تم تفعيل حسابك بنجاح - فاتورتك $299 - يمكنك الآن إرسال واستقبال الإيميلات - Subject/Send/Receive شغال", "time": datetime.now().strftime('%Y-%m-%d %H:%M'), "read": False, "id": 1},
        {"from": "admin", "to": "all", "subject": "Invoice #100 - فاتورة #100", "body": "فاتورة عامة لكل العملاء - Broadcast message", "time": datetime.now().strftime('%Y-%m-%d %H:%M'), "read": False, "id": 2}
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
    st.markdown(f'<div class="header-3d"><h2>{t("title")}</h2><p>{t("subtitle")}</p><p>Features: Subject | From | To | Send | Receive | Reply | Invoice | 3D</p></div>', unsafe_allow_html=True)
    tab1,tab2,tab3 = st.tabs([f"🚀 {LANG[st.session_state['lang']]['register']}", f"🗺️ {LANG[st.session_state['lang']]['map']}", f"🔑 {LANG[st.session_state['lang']]['login']}"])
    with tab1:
        c1,c2 = st.columns([2,1])
        with c1:
            username = st.text_input(LANG[st.session_state['lang']]['username'], placeholder="almjal", key="au_user")
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
                    send_msg("admin", uname, "Welcome - مرحبا", "تم تفعيل حسابك - Welcome to TASHEER AI 3D")
                    st.rerun()
    with tab2:
        st.info("3D Map - Dark mode with neon markers - خريطة ثلاثية الأبعاد")
    with tab3:
        with st.form("login"):
            u = st.text_input(LANG[st.session_state['lang']]['username'])
            p = st.text_input(LANG[st.session_state['lang']]['password'], type="password")
            st.caption("Admin: admin / Tasheer2024! - غير حساس لحالة الأحرف الآن - Case insensitive")
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
                        st.error("Wrong password / كلمة المرور خطأ")
                else:
                    st.error("Wrong username / اسم المستخدم خطأ")
    st.stop()

st.markdown(f'<div class="card-3d">✅ {t("welcome")} {st.session_state["username"]} - {t("link")}: ?client={st.session_state["username"]}</div>', unsafe_allow_html=True)
if st.button(f"🚪 {LANG[st.session_state['lang']]['logout']}"):
    st.session_state['logged_in']=False
    st.session_state['show_landing']=True
    st.rerun()

if st.session_state['username']=="admin":
    st.markdown(f'<div class="card-3d" style="margin-top:15px;"><h3>🌐 3D Admin Panel</h3></div>', unsafe_allow_html=True)
    db = st.session_state['users_db']
    st.dataframe(pd.DataFrame([{"User":k,"USD":v.get("usd",0),"Email":v.get("email","")} for k,v in db.items()]), use_container_width=True)
    t1,t2,t3 = st.tabs([f"📥 {t('receive')}", f"📤 {t('send')}", f"📢 Broadcast"])
    with t1:
        inbox = [m for m in st.session_state['messages_db'] if m['to']=="admin"]
        for msg in reversed(inbox):
            st.markdown(f'<div class="msg-3d"><b>{t("from")}: {msg["from"]}</b> | {t("subject")}: {msg["subject"]}<br>{t("body")}: {msg["body"]}<br><small>{msg["time"]}</small></div>', unsafe_allow_html=True)
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
    st.markdown(f'<div class="card-3d" style="margin-top:15px;"><h3>📧 صندوق رسائلك - Send & Receive - 3D</h3></div>', unsafe_allow_html=True)
    ut1,ut2,ut3 = st.tabs([f"📥 {t('receive')}", f"📤 {t('send')}", f"📨 {t('sent')}"])
    with ut1:
        my_inbox = [m for m in st.session_state['messages_db'] if m['to']==st.session_state['username'] or m['to']=="all"]
        st.metric(t('new_msg'), len(my_inbox))
        if not my_inbox:
            st.markdown(f'<div class="msg-3d">{t("no_msg")}</div>', unsafe_allow_html=True)
        for msg in reversed(my_inbox):
            st.markdown(f'<div class="msg-3d"><b>{t("from")}: {msg["from"]}</b><br><b>{t("subject")}: {msg["subject"]}</b><br>{t("body")}: {msg["body"]}<br><small>{msg["time"]}</small></div>', unsafe_allow_html=True)
    with ut2:
        st.text_input(f"{t('to')}", value="admin", disabled=True)
        subj = st.text_input(f"{t('subject')} *", key="u_subj")
        body = st.text_area(f"{t('body')} *", height=150, key="u_body")
        if st.button(f"📤 {t('send')} -> admin", type="primary", use_container_width=True):
            if subj and body:
                send_msg(st.session_state['username'], "admin", subj, body)
                st.success(t('msg_sent'))
                st.balloons()
    with ut3:
        my_sent = [m for m in st.session_state['messages_db'] if m['from']==st.session_state['username']]
        for msg in reversed(my_sent):
            st.markdown(f'<div class="msg-3d"><b>{t("to")}: {msg["to"]}</b><br><b>{t("subject")}: {msg["subject"]}</b><br>{msg["body"]}</div>', unsafe_allow_html=True)
