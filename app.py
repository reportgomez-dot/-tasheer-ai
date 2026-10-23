import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="TASHEER AI - اشتراكات $", page_icon="💵", layout="centered")

WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={WALLET}"
WHATSAPP = "966540450738"
EMAIL = "report.gomez@gmail.com"

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

# === الأسعار الجديدة بالدولار ===
COMPANY_PRICING = {
    "شهر واحد - 1 Month - $299": {"usd": 299, "sar": 1121, "usdt": 299, "days": 30},
    "3 أشهر - 3 Months - $1,500": {"usd": 1500, "sar": 5625, "usdt": 1500, "days": 90},
    "سنة كاملة - 12 Months - $8,000": {"usd": 8000, "sar": 30000, "usdt": 8000, "days": 365},
    "شركة عادية - Regular Company - $100,000 /شهر": {"usd": 100000, "sar": 375000, "usdt": 100000, "days": 30},
    "شركة مياه وكهرباء - SEC/NWC - $110,000 /شهر": {"usd": 110000, "sar": 412500, "usdt": 110000, "days": 30},
    "شركة بترول - ARAMCO/SABIC - $120,000 /شهر": {"usd": 120000, "sar": 450000, "usdt": 120000, "days": 30},
}

if not st.session_state['logged_in']:
    st.markdown(f"""
    <div style='text-align:center;'>
        <div style='background:linear-gradient(135deg,#0a7a42,#FFD700); width:90px; height:90px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-size:45px; color:white; margin:auto;'>💵</div>
        <h1 style='color:#0a7a42;'>TASHEER AI</h1>
        <p style='color:gray;'>اشتراكات بالدولار - USD Subscriptions</p>
        <p style='color:#0a7a42; font-size:11px; font-weight:700;'>📱 00966540450738 | ✉️ {EMAIL}</p>
    </div>
    """, unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["🔐 دخول Login", "📝 تسجيل جديد - ادفع وتفعل"])
    
    with t1:
        with st.form("login"):
            u = st.text_input("اسم المستخدم / Username")
            p = st.text_input("كلمة المرور / Password", type="password")
            btn = st.form_submit_button("دخول / Login", type="primary", use_container_width=True)
            if btn:
                db = st.session_state['users_db']
                if u in db and db[u]["password"] == p:
                    sub_end = db[u]["sub_end"]
                    days_left = (sub_end - datetime.now()).days
                    if days_left < 0:
                        st.error(f"❌ انتهى اشتراكك {sub_end.strftime('%Y-%m-%d')} - جدد الآن ${db[u].get('usd','')}")
                        st.session_state['expired_user'] = u
                    else:
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = u
                        st.success(f"✅ مرحبا {db[u]['name']} - باقي {days_left} يوم")
                        st.rerun()
                else:
                    st.error("❌ خطأ")
    
    with t2:
        st.markdown("### 💳 ادفع بالدولار لتفعيل حسابك - Pay in USD")
        new_user = st.text_input("اسم مستخدم جديد / New Username")
        new_pass = st.text_input("كلمة مرور / Password", type="password")
        new_email = st.text_input("إيميلك / Email", placeholder=EMAIL)
        plan = st.selectbox("اختر الباقة / Choose Plan $", list(COMPANY_PRICING.keys()))
        data = COMPANY_PRICING[plan]
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("المبلغ / Amount", f"${data['usd']:,} USD")
            st.caption(f"= {data['sar']:,} SAR = {data['usdt']} USDT TRC20")
            st.caption(f"المدة: {data['days']} يوم / days")
            st.code(WALLET)
        with c2:
            st.image(QR_URL, caption=f"Pay ${data['usd']} USDT TRC20")
        
        if st.button(f"✅ دفع ${data['usd']} وتفعيل حسابي {data['days']} يوم", type="primary", use_container_width=True):
            if new_user and new_pass:
                if new_user in st.session_state['users_db']:
                    st.error("الاسم موجود")
                else:
                    st.session_state['users_db'][new_user] = {
                        "password": new_pass, "name": new_user, "email": new_email,
                        "phone": "00966540450738", "sub_end": datetime.now() + timedelta(days=data['days']), "active": True, "usd": data['usd']
                    }
                    st.balloons()
                    st.success(f"✅ تم تفعيل {new_user} لمدة {data['days']} يوم حتى {(datetime.now() + timedelta(days=data['days'])).strftime('%Y-%m-%d')} - سجل دخول")
                    st.markdown(f"[💬 واتساب تأكيد](https://wa.me/{WHATSAPP}?text=دفعت ${data['usd']} - حسابي {new_user})")
            else:
                st.error("ادخل البيانات")
    
    if 'expired_user' in st.session_state:
        u = st.session_state['expired_user']
        st.divider()
        st.markdown(f"### 🔄 تجديد {u} - Renew")
        renew_plan = st.selectbox("باقة التجديد $", list(COMPANY_PRICING.keys()), key="renew")
        rdata = COMPANY_PRICING[renew_plan]
        c1, c2 = st.columns(2)
        with c1:
            st.metric("تجديد", f"${rdata['usd']:,} USD - {rdata['days']} يوم")
            st.code(WALLET)
        with c2:
            st.image(QR_URL)
        if st.button(f"💳 جدد الآن ${rdata['usd']:,}", type="primary", use_container_width=True):
            st.session_state['users_db'][u]["sub_end"] = datetime.now() + timedelta(days=rdata['days'])
            st.success(f"✅ تم التجديد حتى {st.session_state['users_db'][u]['sub_end'].strftime('%Y-%m-%d')}")
            del st.session_state['expired_user']
            st.rerun()
    st.stop()

# === داخل النظام ===
db = st.session_state['users_db']
u = st.session_state['username']
user = db[u]
days_left = (user["sub_end"] - datetime.now()).days

if days_left <= 5:
    st.warning(f"⚠️ اشتراكك ينتهي بعد {days_left} يوم - {user['sub_end'].strftime('%Y-%m-%d')} - جدد الآن")
else:
    st.success(f"✅ فعال - Active | باقي {days_left} يوم حتى {user['sub_end'].strftime('%Y-%m-%d')} | {user['name']}")

st.markdown(f"<div style='display:flex; justify-content:space-between; font-size:12px;'><span>👋 {user['name']} | ✉️ {EMAIL}</span><span>📱 00966540450738</span></div>", unsafe_allow_html=True)
if st.button("🚪 خروج Logout"):
    st.session_state['logged_in'] = False
    st.rerun()

st.markdown(f"<div style='text-align:center;'><h3>🌍 TASHEER AI Global - USD</h3><p style='font-size:11px;color:gray;'>Wallet TFMRQF... TRC20 | ${COMPANY_PRICING['شهر واحد - 1 Month - $299']['usd']} / $1500 / $8000 / $100K-$120K</p></div>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🔍 تشييك جوازات", "💵 الباقات $", "📦 تتبع", "💳 تجديد اشتراك"])

with tab1:
    p_no = st.text_input("رقم الجواز", "A12345678")
    if st.button("افحص الآن", type="primary", use_container_width=True):
        st.success(f"✅ {p_no} ساري - حسابك فعال {days_left} يوم")

with tab2:
    sel = st.selectbox("اختر باقتك $", list(COMPANY_PRICING.keys()))
    data = COMPANY_PRICING[sel]
    st.metric("السعر", f"${data['usd']:,} USD", f"{data['sar']:,} SAR = {data['usdt']} USDT | {data['days']} يوم")

with tab3:
    st.info(f"حساب: {u} | ينتهي: {user['sub_end'].strftime('%Y-%m-%d')} | باقي: {days_left} يوم | للدعم 00966540450738")

with tab4:
    st.markdown(f"### 🔄 تجديد - {u}")
    renew_sel = st.selectbox("باقة التجديد $", list(COMPANY_PRICING.keys()), key="renew2")
    rdata = COMPANY_PRICING[renew_sel]
    c1, c2 = st.columns(2)
    with c1:
        st.metric("تجديد", f"${rdata['usd']:,} USD")
        st.caption(f"{rdata['sar']:,} SAR = {rdata['usdt']} USDT - {rdata['days']} يوم")
        st.code(WALLET)
    with c2:
        st.image(QR_URL, caption=f"Pay ${rdata['usdt']} USDT")
    if st.button(f"💳 جدد ${rdata['usd']:,} - {rdata['days']} Days", type="primary", use_container_width=True):
        db[u]["sub_end"] = db[u]["sub_end"] + timedelta(days=rdata['days']) if days_left>0 else datetime.now() + timedelta(days=rdata['days'])
        st.balloons()
        st.success(f"✅ تم التجديد حتى {db[u]['sub_end'].strftime('%Y-%m-%d')} - باقي {(db[u]['sub_end']-datetime.now()).days} يوم")
        st.markdown(f"[💬 واتساب](https://wa.me/{WHATSAPP}?text=جددت ${rdata['usd']} - {u}) | [✉️ {EMAIL}](mailto:{EMAIL})")
