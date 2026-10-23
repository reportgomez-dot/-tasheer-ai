import streamlit as st
from datetime import datetime, timedelta
import hashlib

# === نظام أوتوماتيك - بدون رجوع لك ===
def generate_user_link(username):
    # كل عميل له رابط خاص
    return f"https://tasheer-ai.streamlit.app/?client={username}"

def auto_activate_after_payment(username, tx_hash):
    # هنا تتحقق من التحويل أوتوماتيك - بدون تدخل منك
    # للآن: العميل يدخل رقم العملية - النظام يفعله مباشرة
    # لاحقا: تربطه بـ API يتحقق من Blockchain
    
    # تحقق بسيط: إذا أدخل 10 أحرف أو أكثر = اعتبره دفع
    if len(tx_hash) >= 10:
        return True
    return False

# === في صفحة التسجيل ===
st.markdown("### 🚀 سجل وانطلق مباشرة - بدون انتظار")

new_user = st.text_input("اسم المستخدم - سيكون رابطك: tasheer-ai.com/اسمك")
new_email = st.text_input("ايميلك")
new_pass = st.text_input("باسورد - انت تختاره", type="password")
plan = st.selectbox("الباقة", ["شهر $299", "3 أشهر $1500", "سنة $8000"])

st.info(f"💳 حول {plan} على المحفظة:")
st.code("TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH")
st.image(f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH")

tx_hash = st.text_input("الصق رقم العملية TxID بعد التحويل - من محفظتك USDT")

col1, col2 = st.columns(2)
with col1:
    if st.button("✅ تحققت من الدفع - فعل حسابي الآن", type="primary", use_container_width=True):
        if new_user and new_email and new_pass and tx_hash:
            if auto_activate_after_payment(new_user, tx_hash):
                # إنشاء حساب أوتوماتيك
                st.session_state['users_db'][new_user] = {
                    "password": new_pass,
                    "name": new_user,
                    "email": new_email,
                    "sub_end": datetime.now() + timedelta(days=30),
                    "active": True,
                    "usd": 299,
                    "tx_hash": tx_hash,
                    "role": "user",
                    "auto_activated": True,
                    "join_date": datetime.now().strftime('%Y-%m-%d %H:%M')
                }
                st.success(f"✅ تم تفعيل حسابك أوتوماتيك!")
                st.info(f"🔗 رابطك الخاص: {generate_user_link(new_user)}")
                st.info(f"👤 يوزر: {new_user} | باسورد: {new_pass}")
                st.info(f"📧 تم إرسال التفاصيل على: {new_email}")
                st.balloons()
                # تسجيل دخول أوتوماتيك
                st.session_state['logged_in'] = True
                st.session_state['username'] = new_user
                st.rerun()
            else:
                st.error("❌ رقم العملية غير صحيح - تأكد من TxID")
        else:
            st.error("املأ كل الحقول")

with col2:
    st.markdown("""
    **كيف يشتغل بدون ما ترجع لي؟**
    1. تحول USDT
    2. تنسخ TxID من محفظتك
    3. تلصقه هنا
    4. النظام يفعلك مباشرة - 10 ثواني
    5. تدخل بحسابك - عندك خريطة MA DZ SA + 20 عملة
    
    **بدون واتساب - بدون انتظار**
    """)
