import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="TASHEER AI - Login", page_icon="🔐", layout="centered")

# === بيانات الدخول - تقدر تغيرها ===
USERS = {
    "admin": {"password": "Tasheer2024!", "name": "Gomez Admin", "email": "report.gomez@gmail.com", "phone": "00966540450738"},
    "gomez": {"password": "123456", "name": "Report Gomez", "email": "report.gomez@gmail.com", "phone": "00966540450738"},
    "client": {"password": "client123", "name": "عميل - Client", "email": "client@test.com", "phone": ""},
}

WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={WALLET}"
WHATSAPP = "966540450738"
EMAIL = "report.gomez@gmail.com"

# === نظام تسجيل الدخول ===
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""

if not st.session_state['logged_in']:
    st.markdown("""
    <div style='text-align:center; margin-bottom:20px;'>
        <div style='background:linear-gradient(135deg,#0a7a42,#00c853); width:90px; height:90px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-size:45px; color:white; margin:auto;'>🔐</div>
        <h1 style='color:#0a7a42;'>TASHEER AI</h1>
        <p style='color:gray;'>تسجيل الدخول - Login</p>
        <p style='color:#0a7a42; font-size:12px; font-weight:700;'>📱 00966540450738 | ✉️ report.gomez@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("اسم المستخدم / Username", placeholder="admin أو gomez أو client")
        password = st.text_input("كلمة المرور / Password", type="password", placeholder="••••••••")
        col1, col2 = st.columns(2)
        with col1:
            login_btn = st.form_submit_button("دخول / Login", type="primary", use_container_width=True)
        with col2:
            st.form_submit_button("نسيت الباسورد؟ تواصل واتساب", use_container_width=True)
        
        if login_btn:
            if username in USERS and USERS[username]["password"] == password:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['user_info'] = USERS[username]
                st.success(f"✅ مرحبا {USERS[username]['name']} - جاري الدخول...")
                st.rerun()
            else:
                st.error("❌ اسم المستخدم أو كلمة المرور خطأ - Wrong username or password")
    
    st.divider()
    st.info("""
    **حسابات تجريبية / Demo Accounts:**
    - 👑 **admin** / **Tasheer2024!** (أدمن - Gomez)
    - 👤 **gomez** / **123456** (Report Gomez)
    - 👥 **client** / **client123** (عميل عادي)
    
    📱 للدعم: 00966540450738 | ✉️ report.gomez@gmail.com
    """)
    st.stop()  # يوقف هنا إذا مو مسجل دخول

# === بعد تسجيل الدخول - الموقع الكامل ===
user = st.session_state['user_info']
st.markdown(f"""
<div style='background:#f0fff4; padding:10px; border-radius:10px; border:1px solid #0a7a42; display:flex; justify-content:space-between; align-items:center;'>
    <span>👋 مرحبا <b>{user['name']}</b> ({st.session_state['username']}) | 📱 {user['phone']} | ✉️ {user['email']}</span>
    <span style='font-size:12px; color:gray;'>TASHEER AI Global</span>
</div>
""", unsafe_allow_html=True)

if st.button("🚪 تسجيل خروج / Logout", type="secondary"):
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""
    st.rerun()

# === بقية الموقع ===
COMPANY_PRICING = {
    "شركة مياه وكهرباء - SEC / NWC (90K)": {"sar": 90000, "usdt": 24000},
    "شركة بترول - ARAMCO / SABIC (100K)": {"sar": 100000, "usdt": 26666},
}
INDIVIDUAL_PRICING = {
    "🇸🇦 السعودية": {"sar": 499, "usdt": 133},
    "🇦🇪 الإمارات": {"sar": 399, "usdt": 106},
    "🇪🇺 شنغن": {"sar": 799, "usdt": 213},
    "🇺🇸 أمريكا": {"sar": 1199, "usdt": 319},
}

st.markdown(f"<div style='text-align:center;'><h3>🌍 TASHEER AI Global</h3><p style='font-size:11px;color:gray;'>📱 00966540450738 | ✉️ {EMAIL} | Wallet: TFMRQF... TRC20</p></div>", unsafe_allow_html=True)
st.markdown(f"<a href='https://wa.me/{WHATSAPP}?text=مرحبا من حساب {st.session_state['username']}' target='_blank'><button style='background:#25D366; color:white; border:none; padding:10px; border-radius:8px; width:100%; font-weight:800;'>💬 واتساب - 00966540450738</button></a>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 تشييك", "🏢 شركات", "🛂 أفراد", "📦 تتبع", "💳 دفع"])
if 'orders' not in st.session_state:
    st.session_state['orders'] = []
if 'selected' not in st.session_state:
    st.session_state['selected'] = ("ARAMCO", COMPANY_PRICING["شركة بترول - ARAMCO / SABIC (100K)"], "company")

with tab1:
    p_no = st.text_input("رقم الجواز", "A12345678")
    if st.button("افحص الآن", type="primary", use_container_width=True):
        expiry = datetime.now() + timedelta(days=random.randint(10,700))
        st.success(f"الجواز {p_no} - ينتهي {expiry.strftime('%Y-%m-%d')} - الحالة: {'✅ ساري' if expiry>datetime.now() else '❌ منتهي'}")

with tab2:
    sel = st.selectbox("شركة", list(COMPANY_PRICING.keys()), index=1)
    st.metric("سعر", f"{COMPANY_PRICING[sel]['sar']:,} SAR")
    st.session_state['selected'] = (sel, COMPANY_PRICING[sel], "company")

with tab3:
    sel = st.selectbox("تأشيرة", list(INDIVIDUAL_PRICING.keys()))
    st.metric("سعر", f"{INDIVIDUAL_PRICING[sel]['sar']:,} SAR")
    st.session_state['selected'] = (sel, INDIVIDUAL_PRICING[sel], "individual")

with tab4:
    track = st.text_input("رقم التتبع", "TRK-12345")
    if st.button("تتبع"):
        st.progress(random.random())
        st.info(f"الطلب {track} - قيد المعالجة - للدعم 00966540450738")

with tab5:
    name, data, _ = st.session_state['selected']
    st.markdown(f"### دفع {name} - {data['sar']:,} SAR = {data['usdt']:,} USDT")
    c1, c2 = st.columns(2)
    with c1:
        st.code(WALLET)
        if st.button("تأكيد دفع", type="primary", use_container_width=True):
            st.balloons()
            st.success(f"تم - حساب {st.session_state['username']} - تابع واتساب 00966540450738")
    with c2:
        st.image(QR_URL)
