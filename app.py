import streamlit as st

st.set_page_config(page_title="TASHEER AI", page_icon="🏢", layout="centered", initial_sidebar_state="collapsed")

# ====== الإعدادات الأصلية - لا تغيرها ======
WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={WALLET}"

# ====== الأسعار - الحد الأعلى لكل شركة ======
COMPANY_PRICING = {
    "شركة عادية": {"sar": 5000, "en": "Regular Company", "usdt": 1333},
    "شركة تقنية": {"sar": 7500, "en": "Tech Company", "usdt": 2000},
    "مكتب استقدام": {"sar": 9900, "en": "Recruitment Office", "usdt": 2640},
    "شركة نظافة وصيانة": {"sar": 9900, "en": "Cleaning & Maintenance", "usdt": 2640},
    "شركة مقاولات": {"sar": 12900, "en": "Construction", "usdt": 3440},
    "مصنع": {"sar": 14900, "en": "Factory", "usdt": 3973},
    "شركة زراعية": {"sar": 35000, "en": "Agricultural - ALMARAI", "usdt": 9333},
    "شركة طبية / مستشفى": {"sar": 55000, "en": "Medical - Al Habib / Dallah", "usdt": 14666},
    "شركة طيران": {"sar": 75000, "en": "Airline - SAUDIA / FLYNAS", "usdt": 20000},
    "شركة استثمار / قابضة": {"sar": 85000, "en": "Investment - PIF / Holding", "usdt": 22666},
    "شركة مياه وكهرباء": {"sar": 90000, "en": "Water & Electricity - SEC / NWC / SWCC", "usdt": 24000},
    "شركة بترول وبتروكيماويات": {"sar": 100000, "en": "Oil & Petrochemical - ARAMCO / SABIC", "usdt": 26666},
}

lang = st.sidebar.selectbox("Language / اللغة", ["العربية", "English"])
T = {
 "العربية": {
  "title": "نظام ذكي لإدارة التأشيرات - شركات الرياض",
  "ok": "النظام يعمل | tasheer-ai.streamlit.app",
  "tab1": "🚀 تجربة", "tab2": "💳 دفع Binance", "tab3": "💰 كل الباقات",
  "company": "اسم شركتك", "type": "نوع الشركة - اختر سعرك الأعلى",
  "btn": "احسب سعري", "welcome": "تم اختيار باقتك",
  "pay_title": "الدفع عبر Binance - USDT TRC20",
  "addr": "عنوان المحفظة (TRC20):", "net": "الشبكة: TRC20 - TRON - TRON", "warn": "تنبيه: أرسل فقط عبر شبكة TRC20",
  "scan": "امسح للدفع - نفس QR الأصلي من Binance الخاص بك", "upload": "ارفع إيصال التحويل",
 },
 "English": {
  "title": "Smart Visa Management - Riyadh Companies",
  "ok": "System Online | tasheer-ai.streamlit.app",
  "tab1": "🚀 Demo", "tab2": "💳 Binance Pay", "tab3": "💰 All Packages",
  "company": "Your Company Name", "type": "Company Type - Select Max Price",
  "btn": "Calculate My Price", "welcome": "Package Selected",
  "pay_title": "Pay via Binance - USDT TRC20",
  "addr": "Wallet Address (TRC20):", "net": "Network: TRC20 - TRON", "warn": "Warning: Send ONLY via TRC20",
  "scan": "Scan to Pay - Same Original QR from your Binance", "upload": "Upload Receipt",
 }
}
t = T[lang]

st.markdown(f"<h2 style='text-align:center'>🏢 TASHEER AI</h2><p style='text-align:center;color:gray'>{t['title']}</p><p style='text-align:center;color:green;font-weight:bold'>{t['ok']}</p>", unsafe_allow_html=True)

if 'price' not in st.session_state:
    st.session_state['price'] = COMPANY_PRICING["شركة عادية"]

tab1, tab2, tab3 = st.tabs([t['tab1'], t['tab2'], t['tab3']])

with tab1:
    st.markdown(f"### {t['type']}")
    c1 = st.text_input(t['company'], "ARAMCO")
    selected_type = st.selectbox(" ", list(COMPANY_PRICING.keys()), index=11, label_visibility="collapsed")
    data = COMPANY_PRICING[selected_type]
    st.session_state['price'] = data
    
    st.markdown(f"""
    <div style='background:#f0fff4; border:2px solid #0a7a42; padding:20px; border-radius:15px; text-align:center; margin:15px 0;'>
        <div style='color:gray'>{selected_type}</div>
        <div style='font-size:36px; font-weight:900; color:#0a7a42;'>{data['sar']:,} SAR</div>
        <div style='font-size:24px; font-weight:700;'>= {data['usdt']:,} USDT / شهر</div>
        <div style='color:#666; margin-top:5px;'>{data['en']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(t['btn'], type="primary", use_container_width=True):
        st.success(f"✅ {t['welcome']}: {c1} - {data['sar']:,} SAR ({data['usdt']:,} USDT)")
        st.balloons()

with tab2:
    data = st.session_state['price']
    st.markdown(f"### {t['pay_title']} - {data['sar']:,} SAR")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"## {data['sar']:,} SAR")
        st.markdown(f"### {data['usdt']:,} USDT")
        st.caption(data['en'])
        st.divider()
        st.markdown(f"**{t['addr']}**")
        st.code(WALLET, language="text")
        st.info(f"{t['net']}\n\nالمبلغ المطلوب: {data['usdt']} USDT\nAmount: {data['usdt']} USDT")
        st.warning(f"⚠️ {t['warn']}")
    
    with col2:
        st.markdown(f"**{t['scan']}**")
        st.image(QR_URL, caption=f"Pay {data['usdt']} USDT - TRC20")
        st.caption(f"Wallet: {WALLET[:15]}...{WALLET[-10:]}")
        st.file_uploader(t['upload'], type=['png','jpg','jpeg','pdf'])
        if st.button("تأكيد الدفع / Confirm Payment", use_container_width=True, type="primary"):
            st.success(f"تم استلام طلبك - {data['sar']:,} SAR - سنتواصل معك!")

with tab3:
    st.markdown("### 💰 كل الشركات بأسعارها القصوى - All Companies Max Price")
    for name, data in COMPANY_PRICING.items():
        col_a, col_b = st.columns([2,1])
        with col_a:
            st.markdown(f"**{name}**<br><span style='color:gray; font-size:12px'>{data['en']}</span>", unsafe_allow_html=True)
        with col_b:
            st.markdown(f"**{data['sar']:,} SAR**<br>{data['usdt']:,} USDT")
        st.divider()
    
    st.success("من 5,000 إلى 100,000 ريال / من 1,333 إلى 26,666 USDT - نفس محفظة Binance الأصلية!")
