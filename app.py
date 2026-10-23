import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

try:
    import folium
    from streamlit_folium import st_folium
    MAP_AVAILABLE = True
except:
    MAP_AVAILABLE = False

st.set_page_config(page_title="TASHEER AI - Bilingual Email System", page_icon="📧", layout="wide")

WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={WALLET}"

COUNTRIES_COORDS = {
    "🇸🇦 السعودية / Saudi": {"lat": 23.8859, "lon": 45.0792, "code": "SA", "currency": "SAR 3.75"},
    "🇦🇪 الإمارات / UAE": {"lat": 23.4241, "lon": 53.8478, "code": "AE", "currency": "AED 3.67"},
    "🇲🇦 المغرب / Morocco": {"lat": 31.7917, "lon": -7.0926, "code": "MA", "currency": "MAD 10.2"},
    "🇩🇿 الجزائر / Algeria": {"lat": 28.0339, "lon": 1.6596, "code": "DZ", "currency": "DZD 135"},
    "🇪🇬 مصر / Egypt": {"lat": 26.8206, "lon": 30.8025, "code": "EG", "currency": "EGP 50.5"},
}

# === TRANSLATIONS - عربي انجليزي ===
LANG = {
    "AR": {
        "title": "📧 TASHEER AI - نظام إيميل داخلي - عربي / إنجليزي",
        "subtitle": "إرسال - استقبال - رد - فاتورة - كلها داخل موقعك",
        "login": "دخول", "register": "تسجيل أوتوماتيك", "map": "خريطة", "logout": "خروج",
        "subject": "الموضوع / Subject", "from": "من / From", "to": "إلى / To", "body": "نص الرسالة / Message",
        "send": "📤 إرسال / Send", "receive": "📥 الوارد / Inbox", "sent": "📤 الصادر / Sent", "reply": "↩️ رد / Reply",
        "send_to_admin": "إرسال للأدمن", "inbox_title": "صندوق رسائلك - Send & Receive",
        "new_msg": "رسائل جديدة", "no_msg": "لا يوجد رسائل", "msg_sent": "تم الإرسال - Sent!",
        "admin_inbox": "رسائل العملاء / Client Messages", "send_to_client": "إرسال لعميل / Send to Client",
        "send_to_all": "إرسال للكل / Broadcast", "invoice_sent": "أرسلت للكل - Broadcast Sent",
        "username": "اسم الشركة / Username", "email": "الإيميل / Email", "password": "كلمة المرور / Password",
        "txid": "TxID - معرف الدفع", "activate": "✅ فعل حسابي الآن / Activate Now",
        "welcome": "مرحبا", "link": "رابطك / Your Link"
    },
    "EN": {
        "title": "📧 TASHEER AI - Internal Email System - AR / EN",
        "subtitle": "Send - Receive - Reply - Invoice - All inside your site",
        "login": "Login", "register": "Auto Register", "map": "Map", "logout": "Logout",
        "subject": "Subject / الموضوع", "from": "From / من", "to": "To / إلى", "body": "Message / نص الرسالة",
        "send": "📤 Send / إرسال", "receive": "📥 Inbox / الوارد", "sent": "📤 Sent / الصادر", "reply": "↩️ Reply / رد",
        "send_to_admin": "Send to Admin", "inbox_title": "Your Inbox - Send & Receive",
        "new_msg": "New Messages", "no_msg": "No Messages", "msg_sent": "Sent! - تم الإرسال",
        "admin_inbox": "Client Messages / رسائل العملاء", "send_to_client": "Send to Client / إرسال لعميل",
        "send_to_all": "Broadcast / إرسال للكل", "invoice_sent": "Broadcast Sent - أرسلت للكل",
        "username": "Username / اسم الشركة", "email": "Email / الإيميل", "password": "Password / كلمة المرور",
        "txid": "TxID - Payment ID", "activate": "✅ Activate Now / فعل حسابي الآن",
        "welcome": "Welcome", "link": "Your Link / رابطك"
    }
}

# === DB ===
if 'users_db' not in st.session_state:
    st.session_state['users_db'] = {
        "admin": {"password": "Tasheer2024!", "name": "Gomez Admin", "email": "report.gomez@gmail.com", "sub_end": datetime.now() + timedelta(days=365), "role": "admin", "active": True, "usd": 0}
    }
if 'messages_db' not in st.session_state:
    st.session_state['messages_db'] = []
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'show_landing' not in st.session_state:
    st.session_state['show_landing'] = True
if 'lang' not in st.session_state:
    st.session_state['lang'] = "AR"

def t(key):
    return LANG[st.session_state['lang']].get(key, key)

def check_payment_auto(tx_hash):
    return len(tx_hash.strip()) >= 10

def send_internal_message(from_user, to_user, subject, body):
    st.session_state['messages_db'].append({
        "from": from_user, "to": to_user, "subject": subject, "body": body,
        "time": datetime.now().strftime('%Y-%m-%d %H:%M'), "read": False,
        "id": len(st.session_state['messages_db']) + 1
    })

# === Language Selector Top ===
col_lang1, col_lang2 = st.columns([4,1])
with col_lang2:
    lang_choice = st.radio("Language / اللغة", ["AR - عربي", "EN - English"], horizontal=True, label_visibility="collapsed")
    st.session_state['lang'] = "AR" if "AR" in lang_choice else "EN"

# === LANDING ===
if st.session_state['show_landing'] and not st.session_state['logged_in']:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg,#0a7a42,#0d4a2a); color:white; padding:25px; border-radius:15px; text-align:center;">
        <h2>{t('title')}</h2>
        <p>{t('subtitle')}</p>
        <p><b>Features:</b> Subject | From | To | Send | Receive | Reply | Invoice</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs([f"🚀 {t('register')}", f"🗺️ {t('map')}", f"🔑 {t('login')}"])
    
    with tab1:
        c1, c2 = st.columns([2,1])
        with c1:
            username = st.text_input(t('username'), placeholder="almajal", key="au_user")
            email = st.text_input(t('email'), placeholder="info@company.com", key="au_email")
            password = st.text_input(t('password'), type="password", key="au_pass")
            st.code(WALLET)
            st.image(QR_URL, width=180)
            tx = st.text_input(t('txid'), placeholder="a1b2c3...", key="au_tx")
            if st.button(t('activate'), type="primary", use_container_width=True):
                if username and email and password and check_payment_auto(tx):
                    st.session_state['users_db'][username] = {
                        "password": password, "name": username, "email": email,
                        "sub_end": datetime.now() + timedelta(days=30), "active": True, "role": "user", "tx": tx, "usd": 299, "link": f"?client={username}"
                    }
                    st.success(f"{t('msg_sent')} - ?client={username}")
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.session_state['show_landing'] = False
                    st.rerun()
                else:
                    st.error("Fill all / املأ كل الحقول")
        with c2:
            st.info("Auto Activation / تفعيل أوتوماتيك - No WhatsApp")
    
    with tab2:
        if MAP_AVAILABLE:
            m = folium.Map(location=[25,20], zoom_start=2.5)
            for name, data in COUNTRIES_COORDS.items():
                folium.Marker([data['lat'], data['lon']], popup=name).add_to(m)
            st_folium(m, height=400)
    
    with tab3:
        with st.form("login"):
            u = st.text_input(t('username'))
            p = st.text_input(t('password'), type="password")
            if st.form_submit_button(t('login'), type="primary"):
                db = st.session_state['users_db']
                if u in db and db[u]["password"] == p:
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = u
                    st.session_state['show_landing'] = False
                    st.rerun()
                else:
                    st.error("Wrong / خطأ")
    st.stop()

# === LOGGED IN HEADER ===
st.success(f"✅ {t('welcome')} {st.session_state['username']} - {t('link')}: ?client={st.session_state['username']}")
if st.button(f"🚪 {t('logout')}"):
    st.session_state['logged_in'] = False
    st.session_state['show_landing'] = True
    st.rerun()

# === ADMIN PANEL ===
if st.session_state['username'] == "admin":
    st.markdown(f"### 📊 Admin + Gmail - {t('subject')} | {t('from')} | {t('to')} | {t('send')} | {t('receive')}")
    db = st.session_state['users_db']
    rows = [{"User": k, "USD": v.get("usd",0), "Email": v.get("email",""), "Link": v.get("link","")} for k,v in db.items()]
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    st.markdown("---")
    st.markdown(f"### 📧 {t('admin_inbox')} - Full Email System")
    t1, t2, t3 = st.tabs([f"📥 {t('admin_inbox')}", f"📤 {t('send_to_client')}", f"📢 {t('send_to_all')}"])
    
    with t1:
        inbox = [m for m in st.session_state['messages_db'] if m['to'] == "admin"]
        st.metric(t('new_msg'), len(inbox))
        for msg in reversed(inbox):
            with st.expander(f"🔴 {t('from')}: {msg['from']} | {t('subject')}: {msg['subject']} | {msg['time']}"):
                st.write(f"**{t('from')}:** {msg['from']}")
                st.write(f"**{t('to')}:** {msg['to']}")
                st.write(f"**{t('subject')}:** {msg['subject']}")
                st.write(f"**{t('body')}:** {msg['body']}")
                st.write(f"**Time:** {msg['time']}")
                reply_sub = st.text_input(f"{t('subject')} - Re: {msg['subject']}", value=f"Re: {msg['subject']}", key=f"sub_{msg['id']}")
                reply_body = st.text_area(f"{t('body')}", key=f"reply_{msg['id']}")
                if st.button(f"{t('send')} -> {msg['from']}", key=f"send_{msg['id']}"):
                    if reply_body:
                        send_internal_message("admin", msg['from'], reply_sub, reply_body)
                        st.success(t('msg_sent'))
    
    with t2:
        all_users = [u for u in db.keys() if u != "admin"]
        if all_users:
            target = st.selectbox(f"{t('to')} / Select Client", all_users)
            subj = st.text_input(f"{t('subject')}", placeholder="Invoice #100 / فاتورة #100", key="adm_subj")
            body = st.text_area(f"{t('body')}", placeholder="Your invoice... / فاتورتك...", key="adm_body")
            if st.button(f"{t('send')} -> {target}", type="primary", use_container_width=True):
                if subj and body:
                    send_internal_message("admin", target, subj, body)
                    st.success(f"{t('msg_sent')} -> {target}")
    
    with t3:
        subj_all = st.text_input(f"{t('subject')} - Broadcast", placeholder="Invoice 100 / فاتورة 100", key="broad_subj")
        body_all = st.text_area(f"{t('body')} - Broadcast", placeholder="Dear clients... / عملائنا...", key="broad_body")
        if st.button(f"📢 {t('send_to_all')}", type="primary", use_container_width=True):
            if subj_all and body_all:
                send_internal_message("admin", "all", subj_all, body_all)
                st.success(t('invoice_sent'))

# === USER INBOX - Send / Receive ===
else:
    st.markdown("---")
    st.markdown(f"### 📧 {t('inbox_title')} - {t('subject')} | {t('send')} | {t('receive')}")
    ut1, ut2, ut3 = st.tabs([f"📥 {t('receive')}", f"📤 {t('send')}", f"📨 {t('sent')}"])
    
    with ut1:
        my_inbox = [m for m in st.session_state['messages_db'] if m['to'] == st.session_state['username'] or m['to'] == "all"]
        st.metric(t('new_msg'), len(my_inbox))
        if my_inbox:
            for msg in reversed(my_inbox):
                with st.expander(f"{'🔴' if not msg['read'] else '✅'} {t('from')}: {msg['from']} | {t('subject')}: {msg['subject']} | {msg['time']}"):
                    st.write(f"**{t('from')}:** {msg['from']}")
                    st.write(f"**{t('subject')}:** {msg['subject']}")
                    st.write(f"**{t('body')}:** {msg['body']}")
                    st.write(f"**Time:** {msg['time']}")
                    # Reply
                    if st.button(f"{t('reply')} - {msg['id']}", key=f"u_reply_btn_{msg['id']}"):
                        st.session_state[f'replying_{msg["id"]}'] = True
                    if st.session_state.get(f'replying_{msg["id"]}', False):
                        r_sub = st.text_input(f"{t('subject')}", value=f"Re: {msg['subject']}", key=f"u_r_sub_{msg['id']}")
                        r_body = st.text_area(f"{t('body')}", key=f"u_r_body_{msg['id']}")
                        if st.button(f"{t('send')}", key=f"u_r_send_{msg['id']}"):
                            if r_body:
                                send_internal_message(st.session_state['username'], "admin", r_sub, r_body)
                                st.success(t('msg_sent'))
                                st.session_state[f'replying_{msg["id"]}'] = False
        else:
            st.info(t('no_msg'))
    
    with ut2:
        st.markdown(f"**{t('send_to_admin')} - {t('subject')} + {t('body')} + {t('send')}**")
        to_field = st.text_input(f"{t('to')}", value="admin", disabled=True, key="u_to")
        subj = st.text_input(f"{t('subject')} *", placeholder="Invoice inquiry / استفسار فاتورة", key="u_subj")
        body = st.text_area(f"{t('body')} *", placeholder="Write message... / اكتب رسالتك...", height=150, key="u_body")
        if st.button(f"📤 {t('send')} -> admin", type="primary", use_container_width=True):
            if subj and body:
                send_internal_message(st.session_state['username'], "admin", subj, body)
                st.success(f"✅ {t('msg_sent')} - {t('receive')} in Inbox")
                st.balloons()
    
    with ut3:
        my_sent = [m for m in st.session_state['messages_db'] if m['from'] == st.session_state['username']]
        if my_sent:
            for msg in reversed(my_sent):
                with st.expander(f"{t('to')}: {msg['to']} | {t('subject')}: {msg['subject']} | {msg['time']}"):
                    st.write(f"**{t('to')}:** {msg['to']}")
                    st.write(f"**{t('subject')}:** {msg['subject']}")
                    st.write(f"**{t('body')}:** {msg['body']}")
        else:
            st.info(f"{t('no_msg')} - No sent messages")
