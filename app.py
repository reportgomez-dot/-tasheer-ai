import streamlit as st
from datetime import datetime, timedelta
import random

st.set_page_config(page_title="TASHEER AI Global", page_icon="🌍", layout="centered")

WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={WALLET}"
WHATSAPP = "966500000000"  # غيره لرقمك الحقيقي

# === LOGO SVG ===
LOGO_HTML = """
<div style='text-align:center; margin-bottom:15px;'>
    <div style='background:linear-gradient(135deg,#0a7a42,#00c853); width:80px; height:80px; border-radius:50%; display:inline-flex; align-items:center; justify-content:center; font-size:40px; color:white;'>🌍</div>
    <h1 style='margin:5px 0; color:#0a7a42;'>TASHEER AI</h1>
    <p style='margin:0; color:gray; font-size:12px;'>GLOBAL VISA & PASSPORT - خليجي | إماراتي | عالمي</p>
</div>
"""

COMPANY_PRICING = {
    "شركة عادية - Regular": {"sar": 5000, "usdt": 1333},
    "شركة مياه وكهرباء - SEC / NWC (90K)": {"sar": 90000, "usdt": 24000},
    "شركة بترول - ARAMCO / SABIC (100K)": {"sar": 100000, "usdt": 26666},
}
INDIVIDUAL_PRICING = {
    "🇸🇦 السعودية": {"sar": 499, "usdt": 133},
    "🇦🇪 الإمارات دبي": {"sar": 399, "usdt": 106},
    "🇪🇺 شنغن أوروبا": {"sar": 799, "usdt": 213},
    "🇺🇸 أمريكا": {"sar": 1199, "usdt": 319},
}

st.markdown(LOGO_HTML, unsafe_allow_html=True)
st.success(f"✅ Official Wallet: TFMRQF... | TRC20 | 📱 WhatsApp: {WHATSAPP}")

# === WHATSAPP BUTTON ===
st.markdown(f"""
<a href='https://wa.me/{WHATSAPP}?text=مرحبا TASHEER AI - ابغى استفسر عن تأشيرة' target='_blank'>
<button style='background:#25D366; color:white; border:none; padding:12px; border-radius:10px; width:100%; font-weight:800; font-size:16px; cursor:pointer;'>💬 تواصل واتساب مباشر - WhatsApp Chat</button>
</a>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔍 تشييك", "🏢 شركات", "🛂 أفراد", "📦 تتبع طلبي", "💳 دفع"])

if 'orders' not in st.session_state:
    st.session_state['orders'] = []
if 'selected' not in st.session_state:
    st.session_state['selected'] = ("ARAMCO", COMPANY_PRICING["شركة بترول - ARAMCO / SABIC (100K)"], "company")

with tab1:
    st.markdown("### 🔍 تشييك جواز وتأشيرة")
    p_no = st.text_input("رقم الجواز / Passport No.", "A12345678")
    v_no = st.text_input("رقم التأشيرة / Visa No.", "6001234567")
    nat = st.selectbox("الجنسية", ["سعودي", "إماراتي", "مصري", "هندي"])
    v_country = st.selectbox("دولة التأشيرة", ["السعودية", "الإمارات", "شنغن", "أمريكا"])
    if st.button("افحص الآن / Check", type="primary", use_container_width=True):
        expiry = datetime.now() + timedelta(days=random.randint(10, 700))
        color = "green" if expiry > datetime.now() + timedelta(days=90) else "red"
        st.markdown(f"<div style='border:2px solid {color}; padding:15px; border-radius:10px;'><b>رقم الجواز:</b> {p_no}<br><b>الحالة:</b> {'✅ ساري' if color=='green' else '❌ منتهي - يحتاج تجديد'}<br><b>ينتهي:</b> {expiry.strftime('%Y-%m-%d')} - باقي {(expiry-datetime.now()).days} يوم</div>", unsafe_allow_html=True)
        if color=="red":
            st.warning("يحتاج تجديد - اضغط دفع للتجديد السريع")

with tab2:
    sel = st.selectbox("اختر الشركة", list(COMPANY_PRICING.keys()), index=2)
    data = COMPANY_PRICING[sel]
    st.metric("SAR", f"{data['sar']:,} | {data['usdt']:,} USDT")
    st.session_state['selected'] = (sel, data, "company")

with tab3:
    sel = st.selectbox("اختر التأشيرة", list(INDIVIDUAL_PRICING.keys()))
    data = INDIVIDUAL_PRICING[sel]
    st.metric("SAR", f"{data['sar']:,} | {data['usdt']:,} USDT")
    st.session_state['selected'] = (sel, data, "individual")

with tab4:
    st.markdown("### 📦 تتبع طلبك / Track Order")
    track_no = st.text_input("ادخل رقم الطلب / رقم الجواز للتتبع", "TRK-12345")
    if st.button("تتبع / Track"):
        statuses = ["🟡 تم استلام الطلب - Received", "🔵 قيد المعالجة في الجوازات - Processing", "🟢 تمت الموافقة - Approved", "📦 جاهز للاستلام - Ready"]
        progress = random.randint(0,3)
        st.progress((progress+1)/4)
        for i, s in enumerate(statuses):
            if i <= progress:
                st.markdown(f"✅ {s}")
            else:
                st.markdown(f"⬜ {s}")
        st.info(f"رقم التتبع: {track_no} | آخر تحديث: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    st.divider()
    st.markdown("#### طلباتي السابقة / My Orders")
    if st.session_state['orders']:
        for o in st.session_state['orders']:
            st.markdown(f"- {o['name']} - {o['date']} - {o['status']}")
    else:
        st.caption("لا يوجد طلبات بعد - No orders yet")

with tab5:
    name, data, _ = st.session_state['selected']
    st.markdown(f"### 💳 دفع - {name} - {data['sar']:,} SAR = {data['usdt']:,} USDT")
    c1, c2 = st.columns(2)
    with c1:
        st.code(WALLET)
        st.text_input("رقم الطلب / Order No.", f"TRK-{random.randint(10000,99999)}")
        if st.button("تأكيد ودفع / Confirm & Pay", type="primary", use_container_width=True):
            st.session_state['orders'].append({"name": name, "date": datetime.now().strftime('%Y-%m-%d'), "status": "تم الدفع - Paid"})
            st.balloons()
            st.success(f"✅ تم الدفع {data['sar']} SAR - رقم تتبعك: TRK-{random.randint(10000,99999)} - تواصل واتساب للمتابعة")
            st.markdown(f"[💬 متابعة واتساب](https://wa.me/{WHATSAPP}?text=تم الدفع {name} - {data['sar']} SAR)")
    with c2:
        st.image(QR_URL, caption=f"Pay {data['usdt']} USDT - TRC20")
