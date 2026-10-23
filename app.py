import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

try:
    import folium
    from streamlit_folium import st_folium
    MAP_AVAILABLE = True
except:
    MAP_AVAILABLE = False

st.set_page_config(page_title="TASHEER AI - Inbox", page_icon="📧", layout="wide")

WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={WALLET}"

COUNTRIES_COORDS = {
    "🇸🇦 السعودية": {"lat": 23.8859, "lon": 45.0792, "code": "SA", "currency": "SAR 3.75", "search": "saudi السعودية sa"},
    "🇦🇪 الإمارات": {"lat": 23.4241, "lon": 53.8478, "code": "AE", "currency": "AED 3.67", "search": "uae الإمارات ae"},
    "🇲🇦 المغرب": {"lat": 31.7917, "lon": -7.0926, "code": "MA", "currency": "MAD 10.2", "search": "morocco المغرب ma maroc"},
    "🇩🇿 الجزائر": {"lat": 28.0339, "lon": 1.6596, "code": "DZ", "currency": "DZD 135", "search": "algeria الجزائر dz"},
    "🇪🇬 مصر": {"lat": 26.8206, "lon": 30.8025, "code": "EG", "currency": "EGP 50.5", "search": "egypt مصر eg"},
    "🇶🇦 قطر": {"lat": 25.3548, "lon": 51.1839, "code": "QA", "currency": "QAR 3.64", "search": "qatar qa"},
    "🇺🇸 أمريكا": {"lat": 37.0902, "lon": -95.7129, "code": "US", "currency": "USD", "search": "usa america us"},
}

# === Database - كل شيء هنا - ما في line 2 لحاله ===
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
if 'search_center' not in st.session_state:
    st.session_state['search_center'] = [25, 20]
if 'search_zoom' not in st.session_state:
    st.session_state['search_zoom'] = 2.5

def check_payment_auto(tx_hash):
    return len(tx_hash.strip()) >= 10

def send_internal_message(from_user, to_user, subject, body):
    st.session_state['messages_db'].append({
        "from": from_user, "to": to_user, "subject": subject, "body": body,
        "time": datetime.now().strftime('%Y-%m-%d %H:%M'), "read": False, "id": len(st.session_state['messages_db']) + 1
    })

# === FIX: Get client param safely ===
client_view = ""
try:
    client_view = st.query_params.get("client", "")
except:
    try:
        params = st.experimental_get_query_params()
        client_view = params.get("client", [""])[0]
    except:
        client_view = ""

# === LANDING ===
if st.session_state['show_landing'] and not st.session_state['logged_in']:
    st.markdown("""
    <div style="background: linear-gradient(135deg,#0a7a42,#0d4a2a); color:white; padding:30px 20px; border-radius:20px; text-align:center;">
        <h1>📧 TASHEER AI - مع صندوق رسائل Gmail داخلي</h1>
        <h3>سجل - ادفع - راسلنا من داخل الموقع - بدون واتساب</h3>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🚀 تسجيل أوتوماتيك", "🗺️ خريطة", "🔑 دخول"])
    
    with tab1:
        col_a, col_b = st.columns([2,1])
        with col_a:
            username = st.text_input("اسم شركتك", placeholder="almajal", key="auto_user")
            email = st.text_input("ايميلك", placeholder="info@company.com", key="auto_email")
            password = st.text_input("باسورد", type="password", key="auto_pass")
            package = st.selectbox("الباقة", ["شهر $299", "سنة $8000"], key="auto_pack")
            st.code(WALLET)
            st.image(QR_URL, width=200)
            tx = st.text_input("الصق TxID", placeholder="a1b2c3...", key="auto_tx")
            if st.button("✅ فعل حسابي الآن", type="primary", use_container_width=True):
                if username and email and password and tx and check_payment_auto(tx):
                    days = 30 if "شهر" in package else 365
                    st.session_state['users_db'][username] = {
                        "password": password, "name": username, "email": email,
                        "sub_end": datetime.now() + timedelta(days=days),
                        "active": True, "role": "user", "tx": tx, "usd": 299 if "شهر" in package else 8000,
                        "link": f"?client={username}"
                    }
                    st.success(f"✅ تم! رابطك: ?client={username}")
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.session_state['show_landing'] = False
                    st.rerun()
                else:
                    st.error("املأ كل الحقول - TxID على الأقل 10 أحرف")
        with col_b:
            st.info("بدون واتساب - تسجل وتدخل مباشرة")
    
    with tab2:
        if MAP_AVAILABLE:
            m = folium.Map(location=st.session_state['search_center'], zoom_start=st.session_state['search_zoom'])
            for name, data in COUNTRIES_COORDS.items():
                folium.Marker([data['lat'], data['lon']], popup=name).add_to(m)
            st_folium(m, height=400)
    
    with tab3:
        with st.form("login_form"):
            u = st.text_input("اسم المستخدم")
            p = st.text_input("كلمة المرور", type="password")
            if st.form_submit_button("دخول", type="primary"):
                db = st.session_state['users_db']
                if u in db and db[u]["password"] == p:
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = u
                    st.session_state['show_landing'] = False
                    st.rerun()
                else:
                    st.error("خطأ")
    st.stop()

# === LOGGED IN ===
st.success(f"✅ مرحبا {st.session_state['username']} - رابطك: ?client={st.session_state['username']}")
if st.button("🚪 خروج"):
    st.session_state['logged_in'] = False
    st.session_state['show_landing'] = True
    st.rerun()

# === ADMIN PANEL ===
if st.session_state['username'] == "admin":
    st.markdown("### 📊 لوحة الأدمن + Gmail داخلي")
    db = st.session_state['users_db']
    rows = [{"User": k, "USD": v.get("usd",0), "Link": v.get("link","")} for k,v in db.items()]
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    # === INBOX SYSTEM - FIXED ===
    st.markdown("---")
    st.markdown("### 📧 نظام الرسائل - Gmail داخل موقعك")
    t1, t2, t3 = st.tabs(["📥 رسائل العملاء", "📤 ارسل لعميل", "📢 ارسل للكل"])
    
    with t1:
        inbox = [m for m in st.session_state['messages_db'] if m['to'] == "admin"]
        st.metric("رسائل جديدة", len(inbox))
        for msg in reversed(inbox):
            with st.expander(f"من: {msg['from']} - {msg['subject']} - {msg['time']}"):
                st.write(msg['body'])
                reply = st.text_area(f"رد على {msg['from']}", key=f"reply_{msg['id']}")
                if st.button(f"📤 رد", key=f"send_{msg['id']}"):
                    if reply:
                        send_internal_message("admin", msg['from'], f"Re: {msg['subject']}", reply)
                        st.success("تم الرد")
    
    with t2:
        all_users = [u for u in db.keys() if u != "admin"]
        if all_users:
            target = st.selectbox("اختر العميل", all_users)
            subj = st.text_input("الموضوع", key="admin_subj")
            body = st.text_area("الرسالة", key="admin_body")
            if st.button(f"📤 ارسل لـ {target}", type="primary"):
                if subj and body:
                    send_internal_message("admin", target, subj, body)
                    st.success(f"أرسلت لـ {target}")
    
    with t3:
        subj_all = st.text_input("موضوع الحملة", key="broad_subj")
        body_all = st.text_area("نص الحملة", key="broad_body")
        if st.button("📢 ارسل للكل", type="primary"):
            if subj_all and body_all:
                send_internal_message("admin", "all", subj_all, body_all)
                st.success(f"أرسلت للكل")

# === USER INBOX ===
else:
    st.markdown("---")
    st.markdown("### 📧 صندوق رسائلك - كلم الأدمن هنا")
    ut1, ut2 = st.tabs(["📥 الوارد", "📤 ارسل للأدمن"])
    
    with ut1:
        my_msgs = [m for m in st.session_state['messages_db'] if m['to'] == st.session_state['username'] or m['to'] == "all"]
        if my_msgs:
            for msg in reversed(my_msgs):
                with st.expander(f"من: {msg['from']} - {msg['subject']} - {msg['time']}"):
                    st.write(f"**الموضوع:** {msg['subject']}")
                    st.write(f"**الرسالة:** {msg['body']}")
        else:
            st.info("📭 لا يوجد رسائل")
    
    with ut2:
        subj = st.text_input("الموضوع", key="user_subj")
        body = st.text_area("الرسالة", key="user_body")
        if st.button("📤 ارسل للأدمن", type="primary"):
            if subj and body:
                send_internal_message(st.session_state['username'], "admin", subj, body)
                st.success("✅ تم الإرسال - الأدمن بيرد عليك هنا")
