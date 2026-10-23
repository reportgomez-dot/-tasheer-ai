import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import json, os, io

# حفظ دائم
USERS_FILE = "users_db.json"
MSG_FILE = "messages_db.json"

def load_json(file, default):
    if os.path.exists(file):
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return default
    return default

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# PDF Invoice
def create_invoice_pdf(client_name, amount, txid, date_str):
    try:
        import fitz
        doc = fitz.open()
        page = doc.new_page(width=595, height=842)
        # خلفية بيضاء
        page.draw_rect(fitz.Rect(0,0,595,842), color=(1,1,1), fill=(1,1,1))
        # Header
        page.draw_rect(fitz.Rect(0,0,595,100), color=(0.09,0.45,0.91), fill=(0.09,0.45,0.91))
        page.insert_text(fitz.Point(40,50), f"TASHEER AI - INVOICE", fontsize=24, color=(1,1,1))
        page.insert_text(fitz.Point(40,75), f"Google Style Billing System", fontsize=12, color=(1,1,1))
        
        y = 130
        page.insert_text(fitz.Point(40,y), f"Invoice #: INV-{client_name.upper()}-{datetime.now().strftime('%Y%m%d')}", fontsize=14, color=(0,0,0)); y+=30
        page.insert_text(fitz.Point(40,y), f"Date: {date_str}", fontsize=12, color=(0.3,0.3,0.3)); y+=25
        page.insert_text(fitz.Point(40,y), f"Client: {client_name}", fontsize=12, color=(0,0,0)); y+=25
        page.insert_text(fitz.Point(40,y), f"TxID: {txid}", fontsize=10, color=(0.3,0.3,0.3)); y+=25
        page.insert_text(fitz.Point(40,y), f"Link: ?client={client_name}", fontsize=10, color=(0.3,0.3,0.3)); y+=40
        
        page.draw_line(fitz.Point(40,y), fitz.Point(555,y), color=(0.8,0.8,0.8), width=1); y+=20
        page.insert_text(fitz.Point(40,y), "Description", fontsize=12, color=(0,0,0))
        page.insert_text(fitz.Point(350,y), "Amount", fontsize=12, color=(0,0,0)); y+=25
        page.insert_text(fitz.Point(40,y), "TASHEER AI - 3D Email System - 30 Days", fontsize=11, color=(0.2,0.2,0.2))
        page.insert_text(fitz.Point(350,y), f"${amount} USDT", fontsize=14, color=(0.09,0.45,0.91)); y+=40
        
        page.draw_rect(fitz.Rect(40,y,555,y+50), color=(0.9,0.94,1), fill=(0.9,0.94,1))
        page.insert_text(fitz.Point(40,y+30), f"TOTAL PAID: ${amount}", fontsize=16, color=(0.09,0.45,0.91))
        
        page.insert_text(fitz.Point(40,750), "Thank you - شكرا لكم | TASHEER AI - report.gomez@gmail.com", fontsize=10, color=(0.5,0.5,0.5))
        
        pdf_bytes = doc.tobytes()
        doc.close()
        return pdf_bytes
    except Exception as e:
        return None

st.set_page_config(page_title="TASHEER AI - Google + Invoice + Dashboard", page_icon="📧", layout="wide")

WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={WALLET}"

st.markdown("""
<style>
* {font-family: 'Roboto', sans-serif;}
.stApp {background:#ffffff !important;}
.header-google {background:#ffffff; border:1px solid #dadce0; border-radius:12px; padding:20px; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.1);}
.card-google {background:#ffffff; border:1px solid #e8eaed; border-radius:12px; padding:16px; box-shadow:0 1px 2px rgba(60,64,67,0.1); margin:10px 0;}
.msg-gmail {background:#ffffff; border:1px solid #dadce0; border-radius:8px; padding:14px; margin:8px 0; border-left:4px solid #1a73e8;}
.stButton>button {background:#1a73e8 !important; color:white !important; border-radius:8px !important; border:none !important;}
.welcome-box {background:#e8f0fe; border:1px solid #d2e3fc; border-radius:8px; padding:12px 16px; color:#1967d2;}
.metric-box {background:#f8f9fa; border:1px solid #e8eaed; border-radius:12px; padding:15px; text-align:center;}
</style>
""", unsafe_allow_html=True)

LANG = {
    "AR": {"title":"TASHEER AI - نظام احترافي","subtitle":"خلفية بيضاء مثل Google + فاتورة PDF + لوحة تحكم","login":"دخول","register":"تسجيل أوتوماتيك","logout":"خروج","subject":"الموضوع / Subject","from":"من / From","to":"إلى / To","body":"نص الرسالة / Message","send":"📤 إرسال / Send","receive":"📥 الوارد / Inbox","sent":"📤 الصادر / Sent","welcome":"مرحبا","link":"رابطك","msg_sent":"تم الإرسال - Sent!","username":"اسم الشركة / Username","password":"كلمة المرور / Password","txid":"TxID","activate":"فعل حسابي الآن","dashboard":"لوحة التحكم / Dashboard","invoice":"تحميل الفاتورة / Download Invoice"},
    "EN": {"title":"TASHEER AI - Professional System","subtitle":"White like Google + PDF Invoice + Dashboard","login":"Login","register":"Auto Register","logout":"Logout","subject":"Subject","from":"From","to":"To","body":"Message","send":"📤 Send","receive":"📥 Inbox","sent":"📤 Sent","welcome":"Welcome","link":"Your Link","msg_sent":"Sent!","username":"Username","password":"Password","txid":"TxID","activate":"Activate Now","dashboard":"Dashboard","invoice":"Download Invoice"}
}

# Load persistent
default_users = {"admin": {"password": "Tasheer2024!", "name": "Gomez Admin", "email": "report.gomez@gmail.com", "sub_end": (datetime.now()+timedelta(days=365)).isoformat(), "role": "admin", "active": True, "usd": 0, "tx":""}}
if 'users_db' not in st.session_state:
    st.session_state['users_db'] = load_json(USERS_FILE, default_users)
if 'messages_db' not in st.session_state:
    st.session_state['messages_db'] = load_json(MSG_FILE, [{"from": "admin", "to": "almjal", "subject": "Welcome", "body": "تم تفعيل حسابك $299", "time": datetime.now().strftime('%Y-%m-%d %H:%M'), "read": False, "id": 1}])

if 'logged_in' not in st.session_state: st.session_state['logged_in']=False
if 'username' not in st.session_state: st.session_state['username']=""
if 'show_landing' not in st.session_state: st.session_state['show_landing']=True
if 'lang' not in st.session_state: st.session_state['lang']="AR"

def t(k): return LANG[st.session_state['lang']].get(k,k)
def save_all():
    save_json(USERS_FILE, st.session_state['users_db'])
    save_json(MSG_FILE, st.session_state['messages_db'])
def check_tx(tx): return len(tx.strip())>=10
def send_msg(f,to_user,subj,body):
    st.session_state['messages_db'].append({"from": f, "to": to_user, "subject": subj, "body": body, "time": datetime.now().strftime('%Y-%m-%d %H:%M'), "read": False, "id": len(st.session_state['messages_db'])+1})
    save_all()

col1,col2 = st.columns([4,1])
with col2:
    lc = st.radio("Lang", ["AR - عربي", "EN - English"], horizontal=True, label_visibility="collapsed")
    st.session_state['lang']="AR" if "AR" in lc else "EN"

if st.session_state['show_landing'] and not st.session_state['logged_in']:
    st.markdown(f'<div class="header-google"><h2>📧 {t("title")}</h2><p>{t("subtitle")}</p><p style="font-size:12px; color:#5f6368;">✅ 1. حفظ دائم | ✅ 2. فاتورة PDF | ✅ 3. لوحة تحكم احترافية</p></div>', unsafe_allow_html=True)
    tab1,tab2 = st.tabs([f"🚀 {t('register')}", f"🔑 {t('login')}"])
    with tab1:
        c1,c2 = st.columns([2,1])
        with c1:
            st.markdown('<div class="card-google">', unsafe_allow_html=True)
            username = st.text_input(t('username'), placeholder="almjal", key="au_user")
            email = st.text_input("Email", placeholder="info@company.com", key="au_email")
            password = st.text_input(t('password'), type="password", key="au_pass")
            st.code(WALLET)
            st.image(QR_URL, width=160)
            tx = st.text_input(t('txid'), placeholder="a1b2c3...", key="au_tx")
            if st.button(t('activate'), type="primary", use_container_width=True):
                if username and email and password and check_tx(tx):
                    uname = username.strip().lower()
                    st.session_state['users_db'][uname] = {"password": password, "name": username, "email": email, "sub_end": (datetime.now()+timedelta(days=30)).isoformat(), "active": True, "role": "user", "tx": tx, "usd": 299, "link": f"?client={uname}"}
                    save_all()
                    st.session_state['logged_in']=True
                    st.session_state['username']=uname
                    st.session_state['show_landing']=False
                    send_msg("admin", uname, "Welcome - تم التفعيل", f"تم تفعيل حسابك - Tx: {tx} - $299")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    with tab2:
        st.markdown('<div class="card-google">', unsafe_allow_html=True)
        with st.form("login"):
            u = st.text_input(t('username'))
            p = st.text_input(t('password'), type="password")
            st.caption("Admin: admin / Tasheer2024! - Case insensitive")
            if st.form_submit_button(t('login'), type="primary"):
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
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

st.markdown(f'<div class="welcome-box">✅ {t("welcome")} {st.session_state["username"]} - {t("link")}: ?client={st.session_state["username"]}</div>', unsafe_allow_html=True)
if st.button(f"🚪 {t('logout')}"):
    st.session_state['logged_in']=False
    st.session_state['show_landing']=True
    st.rerun()

# === ADMIN DASHBOARD 1+2+3 ===
if st.session_state['username']=="admin":
    st.markdown('<div class="card-google" style="margin-top:16px;"><h3 style="color:#202124; margin:0;">📊 TASHEER AI - Admin Dashboard - لوحة التحكم</h3></div>', unsafe_allow_html=True)
    db = st.session_state['users_db']
    msgs = st.session_state['messages_db']
    
    # 3 - Dashboard metrics
    c1,c2,c3,c4 = st.columns(4)
    total_clients = len([k for k in db.keys() if k!="admin"])
    total_usd = sum([v.get("usd",0) for v in db.values()])
    total_msgs = len(msgs)
    new_msgs = len([m for m in msgs if m['to']=="admin"])
    with c1: st.markdown(f'<div class="metric-box"><h2 style="color:#1a73e8; margin:0;">{total_clients}</h2><p style="margin:0; color:#5f6368;">Clients</p></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-box"><h2 style="color:#0d652d; margin:0;">${total_usd}</h2><p style="margin:0; color:#5f6368;">Total Revenue</p></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="metric-box"><h2 style="color:#e8710a; margin:0;">{total_msgs}</h2><p style="margin:0; color:#5f6368;">Messages</p></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="metric-box"><h2 style="color:#d93025; margin:0;">{new_msgs}</h2><p style="margin:0; color:#5f6368;">Inbox Admin</p></div>', unsafe_allow_html=True)
    
    # Chart
    df = pd.DataFrame([{"User":k,"USD":v.get("usd",0),"Email":v.get("email",""),"Tx":v.get("tx","")} for k,v in db.items()])
    st.dataframe(df, use_container_width=True)
    if total_clients>0:
        st.bar_chart(df.set_index("User")["USD"])
    
    t1,t2,t3 = st.tabs([f"📥 Inbox ({new_msgs})", f"📤 Send to Client", f"📢 Broadcast + Invoice"])
    with t1:
        inbox = [m for m in msgs if m['to']=="admin"]
        for msg in reversed(inbox):
            st.markdown(f'<div class="msg-gmail"><b>From: {msg["from"]}</b> | Subject: {msg["subject"]}<br>{msg["body"]}<br><small>{msg["time"]}</small></div>', unsafe_allow_html=True)
            rb = st.text_area("Reply", key=f"reply_{msg['id']}")
            if st.button(f"📤 Send -> {msg['from']}", key=f"send_{msg['id']}"):
                if rb:
                    send_msg("admin", msg['from'], f"Re: {msg['subject']}", rb)
                    st.success("Sent")
    with t2:
        all_users = [u for u in db.keys() if u!="admin"]
        if all_users:
            target = st.selectbox("To", all_users)
            subj = st.text_input("Subject", key="adm_subj")
            body = st.text_area("Message", key="adm_body")
            if st.button(f"📤 Send -> {target}", type="primary", use_container_width=True):
                if subj and body:
                    send_msg("admin", target, subj, body)
                    st.success(f"Sent -> {target}")
    with t3:
        subj_all = st.text_input("Subject - Broadcast", key="broad_subj")
        body_all = st.text_area("Message - Broadcast", key="broad_body")
        if st.button("📢 Broadcast to All", type="primary", use_container_width=True):
            if subj_all and body_all:
                send_msg("admin", "all", subj_all, body_all)
                st.success("Broadcast Sent - محفوظ دائما")

else:
    # Client view + Invoice PDF
    st.markdown('<div class="card-google" style="margin-top:16px;"><h3 style="color:#202124; margin:0;">📧 صندوق رسائلك - Send & Receive</h3></div>', unsafe_allow_html=True)
    # 2 - PDF Invoice button
    user_info = st.session_state['users_db'].get(st.session_state['username'], {})
    if user_info:
        col_inv1, col_inv2 = st.columns([2,1])
        with col_inv1:
            st.info(f"💳 Subscription: ${user_info.get('usd',299)} | Tx: {user_info.get('tx','')[:15]}...")
        with col_inv2:
            pdf_bytes = create_invoice_pdf(st.session_state['username'], user_info.get('usd',299), user_info.get('tx',''), datetime.now().strftime('%Y-%m-%d'))
            if pdf_bytes:
                st.download_button(f"📄 {t('invoice')}", data=pdf_bytes, file_name=f"Invoice_{st.session_state['username']}.pdf", mime="application/pdf", type="primary", use_container_width=True)
    
    ut1,ut2,ut3 = st.tabs([f"📥 {t('receive')}", f"📤 {t('send')}", f"📨 {t('sent')}"])
    with ut1:
        my_inbox = [m for m in st.session_state['messages_db'] if m['to']==st.session_state['username'] or m['to']=="all"]
        st.metric("New Messages", len(my_inbox))
        for msg in reversed(my_inbox):
            st.markdown(f'<div class="msg-gmail"><b>From: {msg["from"]}</b><br><b>Subject: {msg["subject"]}</b><br>{msg["body"]}<br><small>{msg["time"]}</small></div>', unsafe_allow_html=True)
    with ut2:
        st.markdown('<div class="card-google">', unsafe_allow_html=True)
        st.text_input("To", value="admin", disabled=True)
        subj = st.text_input("Subject *", key="u_subj")
        body = st.text_area("Message *", height=150, key="u_body")
        if st.button("📤 Send -> admin", type="primary", use_container_width=True):
            if subj and body:
                send_msg(st.session_state['username'], "admin", subj, body)
                st.success(t('msg_sent'))
                st.balloons()
        st.markdown('</div>', unsafe_allow_html=True)
    with ut3:
        my_sent = [m for m in st.session_state['messages_db'] if m['from']==st.session_state['username']]
        for msg in reversed(my_sent):
            st.markdown(f'<div class="msg-gmail"><b>To: {msg["to"]}</b><br><b>Subject: {msg["subject"]}</b><br>{msg["body"]}</div>', unsafe_allow_html=True)
