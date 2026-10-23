import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="TASHEER AI - اشتراكات", page_icon="⏰", layout="centered")

WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={WALLET}"
WHATSAPP = "966540450738"
EMAIL = "report.gomez@gmail.com"

# === قاعدة بيانات المستخدمين مع الاشتراكات ===
if 'users_db' not in st.session_state:
    st.session_state['users_db'] = {
        "admin": {"password": "Tasheer2024!", "name": "Gomez Admin", "email": EMAIL, "phone": "00966540450738", "sub_end": datetime.now() + timedelta(days=365), "active": True},
        "gomez": {"password": "123456", "name": "Report Gomez", "email": EMAIL, "phone": "00966540450738", "sub_end": datetime.now() + timedelta(days=365), "active": True},
        "client": {"password": "client123", "name": "عميل تجريبي", "email": "client@test.com", "phone": "", "sub_end": datetime.now() + timedelta(days=2), "active": True},
    }

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""

COMPANY_PRICING = {
    "شهر واحد - 1 Month - 299 SAR": {"sar": 299, "usdt": 80, "days": 30},
    "3 أشهر - 3 Months - 699 SAR (وفر 198)": {"sar": 699, "usdt": 186, "days": 90},
    "سنة كاملة - 12 Months - 1999 SAR (وفر 1589)": {"sar": 1999, "usdt": 533, "days": 365},
    "شركة مياه وكهرباء - 90,000 SAR/شهر": {"sar": 90000, "usdt": 24000, "days": 30},
    "شركة بترول - 100,000 SAR/شهر": {"sar": 100000, "usdt": 26666, "days": 30},
}
INDIVIDUAL_PRICING = {
    "🇸🇦 السعودية 499": {"sar": 499, "usdt": 133, "days": 30},
    "🇦🇪 الإمارات 399": {"sar": 399, "usdt": 106, "days": 30},
}

# === شاشة تسجيل الدخول ===
if not st.session_state['logged_in']:
    st.markdown(f"""
    <div style='text-align:center;'>
        <div style='background:linear-gradient(135deg,#0a7a42,#00c853); width:90px; height:90px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-size:45px; color:white; margin:auto;'>⏰</div>
        <h1 style='color:#0a7a42;'>TASHEER AI</h1>
        <p style='color:gray;'>نظام اشتراكات - Subscription System</p>
        <p style='color:#0a7a42; font-size:11px; font-weight:700;'>📱 00966540450738 | ✉️ {EMAIL}</p>
    </div>
    """, unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["🔐 دخول", "📝 تسجيل جديد - بعد الدفع"])
    
    with t1:
        with st.form("login"):
            u = st.text_input("اسم المستخدم")
            p = st.text_input("كلمة المرور", type="password")
            btn = st.form_submit_button("دخول / Login", type="primary", use_container_width=True)
            if btn:
                db = st.session_state['users_db']
                if u in db and db[u]["password"] == p:
                    # فحص الاشتراك
                    sub_end = db[u]["sub_end"]
                    days_left = (sub_end - datetime.now()).days
                    if days_left < 0:
                        st.error(f"❌ انتهى اشتراكك في {sub_end.strftime('%Y-%m-%d')} - جدد الآن - Expired, Renew Now")
                        st.session_state['expired_user'] = u
                    else:
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = u
                        st.success(f"✅ مرحبا {db[u]['name']} - باقي لك {days_left} يوم")
                        st.rerun()
                else:
                    st.error("❌ خطأ في البيانات")
    
    with t2:
        st.markdown("### 💳 ادفع لتفعيل حسابك شهر - Pay to Activate 1 Month")
        st.info("بعد الدفع، سجل حسابك وسيتفعل تلقائيا لمدة 30 يوم")
        new_user = st.text_input("اختر اسم مستخدم جديد")
        new_pass = st.text_input("اختر كلمة مرور", type="password")
        new_email = st.text_input("إيميلك", placeholder=EMAIL)
        plan = st.selectbox("اختر الباقة / Plan", list(COMPANY_PRICING.keys()))
        data = COMPANY_PRICING[plan]
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("المبلغ", f"{data['sar']} SAR = {data['usdt']} USDT")
            st.code(WALLET)
            st.caption(f"TRC20 - {data['days']} يوم")
        with c2:
            st.image(QR_URL, caption=f"Pay {data['usdt']} USDT")
        
        if st.button("✅ دفع وتفعيل حسابي - Activate My Account", type="primary", use_container_width=True):
            if new_user and new_pass:
                if new_user in st.session_state['users_db']:
                    st.error("اسم المستخدم موجود - اختر اسم ثاني")
                else:
                    st.session_state['users_db'][new_user] = {
                        "password": new_pass, "name": new_user, "email": new_email,
                        "phone": "00966540450738", "sub_end": datetime.now() + timedelta(days=data['days']), "active": True
                    }
                    st.balloons()
                    st.success(f"✅ تم تفعيل حساب {new_user} لمدة {data['days']} يوم حتى {(datetime.now() + timedelta(days=data['days'])).strftime('%Y-%m-%d')} - سجل دخول الآن")
                    st.markdown(f"[💬 إرسال إيصال واتساب](https://wa.me/{WHATSAPP}?text=دفعت {data['sar']} SAR - حسابي {new_user} - فعلوه)")
            else:
                st.error("ادخل اسم المستخدم وكلمة المرور")
    
    # عرض انتهاء الاشتراك وتجديد
    if 'expired_user' in st.session_state:
        u = st.session_state['expired_user']
        st.divider()
        st.markdown(f"### 🔄 تجديد اشتراك {u} - Renew Subscription")
        renew_plan = st.selectbox("باقة التجديد", list(COMPANY_PRICING.keys()), key="renew")
        rdata = COMPANY_PRICING[renew_plan]
        c1, c2 = st.columns(2)
        with c1:
            st.metric("تجديد", f"{rdata['sar']} SAR = {rdata['usdt']} USDT - {rdata['days']} يوم")
            st.code(WALLET)
        with c2:
            st.image(QR_URL)
        if st.button(f"💳 جدد الآن {rdata['sar']} SAR", type="primary", use_container_width=True):
            st.session_state['users_db'][u]["sub_end"] = datetime.now() + timedelta(days=rdata['days'])
            st.success(f"✅ تم التجديد! حسابك فعال حتى {st.session_state['users_db'][u]['sub_end'].strftime('%Y-%m-%d')}")
            del st.session_state['expired_user']
            st.rerun()
    st.stop()

# === بعد الدخول ===
db = st.session_state['users_db']
u = st.session_state['username']
user = db[u]
days_left = (user["sub_end"] - datetime.now()).days

# تحذير قرب الانتهاء
if days_left <= 5:
    st.warning(f"⚠️ تنبيه: اشتراكك ينتهي بعد {days_left} يوم في {user['sub_end'].strftime('%Y-%m-%d')} - جدد الآن لتجنب الإيقاف")
else:
    st.success(f"✅ حسابك فعال - باقي {days_left} يوم حتى {user['sub_end'].strftime('%Y-%m-%d')} | {user['name']}")

st.markdown(f"<div style='display:flex; justify-content:space-between;'><span>👋 {user['name']} | {EMAIL}</span><span>📱 00966540450738</span></div>", unsafe_allow_html=True)
col_l, col_r = st.columns([1,4])
with col_l:
    if st.button("🚪 خروج"):
        st.session_state['logged_in'] = False
        st.rerun()
with col_r:
    st.markdown(f"<a href='https://wa.me/{WHATSAPP}' target='_blank'><button style='background:#25D366; color:white; border:none; padding:8px; border-radius:8px; width:100%;'>💬 واتساب دعم</button></a>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 تشييك", "🏢 شركات", "🛂 أفراد", "📦 تتبع", "💳 تجديد"])

if 'selected' not in st.session_state:
    st.session_state['selected'] = ("شهر واحد", COMPANY_PRICING["شهر واحد - 1 Month - 299 SAR"], "sub")

with tab1:
    p_no = st.text_input("رقم الجواز للتشييك", "A12345678")
    if st.button("افحص الآن", type="primary", use_container_width=True):
        st.success(f"✅ الجواز {p_no} ساري - حسابك فعال {days_left} يوم")

with tab2:
    sel = st.selectbox("باقة شركة", list(COMPANY_PRICING.keys()))
    st.metric("سعر", f"{COMPANY_PRICING[sel]['sar']} SAR / {COMPANY_PRICING[sel]['days']} يوم")
    st.session_state['selected'] = (sel, COMPANY_PRICING[sel], "company")

with tab3:
    sel = st.selectbox("باقة فرد", list(INDIVIDUAL_PRICING.keys()))
    st.metric("سعر", f"{INDIVIDUAL_PRICING[sel]['sar']} SAR")

with tab4:
    st.info(f"رقم حسابك: {u} | ينتهي: {user['sub_end'].strftime('%Y-%m-%d')} | باقي: {days_left} يوم")

with tab5:
    st.markdown(f"### 🔄 تجديد اشتراكك - {u}")
    st.markdown(f"**حسابك ينتهي:** {user['sub_end'].strftime('%Y-%m-%d')} - **باقي:** {days_left} يوم")
    renew_sel = st.selectbox("اختر باقة التجديد", list(COMPANY_PRICING.keys()))
    rdata = COMPANY_PRICING[renew_sel]
    c1, c2 = st.columns(2)
    with c1:
        st.metric("التجديد", f"{rdata['sar']} SAR = {rdata['usdt']} USDT")
        st.code(WALLET)
        st.caption(f"سيضاف {rdata['days']} يوم لرصيدك")
    with c2:
        st.image(QR_URL, caption=f"Pay {rdata['usdt']} USDT TRC20")
    if st.button(f"💳 جدد الآن - Renew {rdata['days']} Days", type="primary", use_container_width=True):
        db[u]["sub_end"] = db[u]["sub_end"] + timedelta(days=rdata['days']) if days_left>0 else datetime.now() + timedelta(days=rdata['days'])
        st.balloons()
        st.success(f"✅ تم التجديد! اشتراكك الآن حتى {db[u]['sub_end'].strftime('%Y-%m-%d')} - باقي {(db[u]['sub_end']-datetime.now()).days} يوم")
        st.markdown(f"[💬 تأكيد واتساب](https://wa.me/{WHATSAPP}?text=جددت {renew_sel} - حسابي {u})")
