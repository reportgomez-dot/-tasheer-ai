# أضف هذا في أول app.py
import streamlit as st
from datetime import datetime, timedelta

# === نظام أوتوماتيك كامل ===
if 'users_db' not in st.session_state:
    st.session_state['users_db'] = {
        "admin": {"password": "Tasheer2024!", "name": "Admin", "email": "report.gomez@gmail.com", "sub_end": datetime.now() + timedelta(days=365), "role": "admin", "active": True}
    }

WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"

# === دالة التحقق الأوتوماتيك ===
def check_payment_auto(tx_hash):
    # للآن: أي TxHash طوله >10 = مقبول
    # لاحقا: تربطه بـ Tronscan API يتحقق حقيقي من Blockchain
    return len(tx_hash.strip()) >= 10

# === رابط العميل ===
params = st.query_params
client_view = params.get("client", "")

if client_view and not st.session_state.get('logged_in'):
    st.markdown(f"### 🏢 مرحبا {client_view} - موقعك الخاص - Powered by TASHEER AI")

# === تسجيل أوتوماتيك ===
st.markdown("## 🚀 سجل - ادفع - انطلق - بدون انتظار")

col_a, col_b = st.columns([2,1])

with col_a:
    username = st.text_input("اختر اسم شركتك / يوزرك - سيكون رابطك", placeholder="almajal")
    email = st.text_input("ايميلك الرسمي", placeholder="info@almajal.com")
    password = st.text_input("باسورد - انت تحدده", type="password")
    package = st.selectbox("الباقة", ["شهر $299 - 1121 SAR - 100 حساب", "سنة $8000 - 30,000 SAR"])
    
    st.markdown(f"#### 💳 خطوة 2: حول على المحفظة")
    st.code(WALLET)
    st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={WALLET}", width=200)
    
    tx = st.text_input("الصق TxID - رقم العملية من محفظتك بعد التحويل", placeholder="a1b2c3d4e5f6...")

    if st.button("✅ فعل حسابي الآن - أوتوماتيك", type="primary", use_container_width=True):
        if username and email and password and tx:
            if check_payment_auto(tx):
                # تفعيل فوري
                days = 30 if "شهر" in package else 365
                st.session_state['users_db'][username] = {
                    "password": password, "name": username, "email": email,
                    "sub_end": datetime.now() + timedelta(days=days),
                    "active": True, "role": "user", "tx": tx,
                    "link": f"tasheer-ai.com/?client={username}"
                }
                st.success(f"✅ تم! حسابك مفعل - رابطك: tasheer-ai.com/?client={username}")
                st.balloons()
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.rerun()
            else:
                st.error("TxID غير صحيح - انسخه من محفظة USDT بعد التحويل")
        else:
            st.error("املأ كل الحقول")

with col_b:
    st.markdown("""
    **🎯 بدون ما ترجع لي:**
    
    1. تحول USDT
    2. تلصق TxID
    3. تنطلق مباشرة
    
    **مميزاتك بعد التفعيل:**
    - 🔗 رابطك: tasheer-ai.com/?client=اسمك
    - 🗺️ خريطة MA DZ SA EG
    - 💱 27 عملة
    - 👥 100 حساب لموظفينك
    - 📊 تقارير يومية
    - 🔄 تجديد أوتوماتيك
    
    **📱 واتساب دعم: 00966540450738**
    """)
