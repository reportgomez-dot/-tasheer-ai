import streamlit as st

st.set_page_config(page_title="TASHEER AI", page_icon="🏢", layout="centered")

WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={WALLET}"

# القائمة النهائية - عربي + إنجليزي + السعر الأعلى
COMPANY_PRICING = {
    "شركة عادية - Regular Company": {"sar": 5000, "usdt": 1333},
    "شركة تقنية - Tech Company": {"sar": 7500, "usdt": 2000},
    "مكتب استقدام - Recruitment Office": {"sar": 9900, "usdt": 2640},
    "شركة نظافة وصيانة - Cleaning & Maintenance": {"sar": 9900, "usdt": 2640},
    "شركة مقاولات - Construction": {"sar": 12900, "usdt": 3440},
    "مصنع - Factory / Industrial": {"sar": 14900, "usdt": 3973},
    "شركة زراعية - Agricultural (ALMARAI / NADEC)": {"sar": 35000, "usdt": 9333},
    "شركة طبية / مستشفى - Medical (Al Habib / Dallah)": {"sar": 55000, "usdt": 14666},
    "شركة طيران - Airline (SAUDIA / FLYNAS)": {"sar": 75000, "usdt": 20000},
    "شركة استثمار / قابضة - Investment (PIF / Holding)": {"sar": 85000, "usdt": 22666},
    "شركة مياه وكهرباء - Water & Electricity (SEC / NWC / SWCC)": {"sar": 90000, "usdt": 24000},
    "شركة بترول وبتروكيماويات - Oil & Petrochemical (ARAMCO / SABIC)": {"sar": 100000, "usdt": 26666},
}

st.markdown("<h2 style='text-align:center'>🏢 TASHEER AI<br><span style='font-size:14px; color:gray'>Smart Visa Management - نظام إدارة التأشيرات الذكي</span></h2>", unsafe_allow_html=True)
st.success("✅ النظام يعمل | System Online | tasheer-ai.streamlit.app - Official Binance Wallet: TFMRQF...")

tab1, tab2, tab3 = st.tabs(["🚀 تجربة / Demo", "💳 دفع Binance / Pay", "💰 كل الباقات / Packages"])

if 'selected' not in st.session_state:
    st.session_state['selected'] = "شركة بترول وبتروكيماويات - Oil & Petrochemical (ARAMCO / SABIC)"

with tab1:
    st.markdown("### اختر نوع شركتك / Select Company Type")
    company_name = st.text_input("اسم شركتك / Company Name", "ARAMCO - أرامكو")
    
    selected = st.selectbox(
        "نوع الشركة - Company Type (عربي + English)",
        list(COMPANY_PRICING.keys()),
        index=11
    )
    st.session_state['selected'] = selected
    data = COMPANY_PRICING[selected]
    
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#f0fff4,#e6fffa); border:3px solid #0a7a42; padding:25px; border-radius:20px; text-align:center;'>
        <div style='font-size:16px; color:#333; font-weight:700;'>{selected}</div>
        <div style='font-size:42px; font-weight:900; color:#0a7a42; margin:10px 0;'>{data['sar']:,} SAR</div>
        <div style='font-size:28px; font-weight:800; color:#000;'>= {data['usdt']:,} USDT / شهر - per month</div>
        <div style='margin-top:10px; color:gray; font-size:12px;'>Original Wallet: TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH | Network TRC20</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("احسب سعري / Calculate My Price - تأكيد", type="primary", use_container_width=True):
        st.balloons()
        st.success(f"✅ تم اختيار باقتك / Package Selected: {company_name} - {data['sar']:,} SAR ({data['usdt']:,} USDT)")

with tab2:
    data = COMPANY_PRICING[st.session_state['selected']]
    st.markdown(f"### 💳 الدفع عبر Binance - Pay via Binance - {data['sar']:,} SAR / {data['usdt']:,} USDT")
    st.markdown(f"**الباقة المختارة / Selected:** {st.session_state['selected']}")
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric("SAR / شهر - per month", f"{data['sar']:,} SAR")
        st.metric("USDT / شهر - per month", f"{data['usdt']:,} USDT")
        st.divider()
        st.markdown("**عنوان المحفظة / Wallet Address (TRC20):**")
        st.code(WALLET)
        st.info(f"الشبكة: TRC20 - TRON\nNetwork: TRC20\n\nالمبلغ المطلوب: {data['usdt']} USDT")
        st.warning("⚠️ تنبيه: أرسل فقط عبر شبكة TRC20 / Send ONLY via TRC20")
    
    with c2:
        st.markdown("**امسح للدفع - Scan to Pay - QR الأصلي من Binance**")
        st.image(QR_URL, caption=f"Pay {data['usdt']} USDT - TRC20 - {WALLET[:10]}...")
        st.file_uploader("ارفع إيصال التحويل / Upload Receipt", type=['png','jpg','jpeg','pdf'])
        if st.button("تأكيد الدفع / Confirm Payment", use_container_width=True, type="primary"):
            st.success(f"✅ تم استلام طلبك {data['sar']:,} SAR - سنتواصل معك / Request Received!")

with tab3:
    st.markdown("### 💰 جميع الباقات - All Packages - عربي + English")
    for name, d in COMPANY_PRICING.items():
        st.markdown(f"""
        <div style='border:1px solid #eee; padding:12px; border-radius:10px; margin:5px 0;'>
            <b>{name}</b><br>
            <span style='color:#0a7a42; font-weight:800; font-size:18px;'>{d['sar']:,} SAR</span> 
            <span style='color:#666;'>= {d['usdt']:,} USDT / شهر</span>
        </div>
        """, unsafe_allow_html=True)
