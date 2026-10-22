import streamlit as st

st.set_page_config(page_title="TASHEER AI", page_icon="🏢", layout="centered")

# Language / اللغة
lang = st.sidebar.selectbox("Language / اللغة", ["العربية", "English"])

T = {
 "العربية": {
  "sub": "نظام ذكي لإدارة التأشيرات والموظفين - شركات الرياض",
  "ok": "النظام يعمل | رابطك: tasheer-ai.streamlit.app",
  "price": "اشتراك الشركات",
  "count": "عدد الشركات",
  "tab1": "🚀 تجربة",
  "tab2": "🏢 تسجيل شركة",
  "tab3": "💳 دفع Binance",
  "try_title": "جرب النظام",
  "company": "اسم الشركة",
  "btn": "تجربة النظام",
  "welcome": "تم تفعيل تجربتك - أهلاً",
  "pay_title": "الدفع عبر Binance - USDT TRC20",
  "sar": "5,000 ريال / شهر",
  "usdt": "≈ 1,333 USDT",
  "addr": "العنوان (TRC20):",
  "net": "الشبكة: TRC20 - TRON",
  "amount": "المبلغ: 1333 USDT = 5000 ريال",
  "warn": "مهم: فقط TRC20 - اختر شبكة TRC20",
  "upload": "ارفع إيصال الدفع",
  "copy": "نسخ العنوان",
  "scan": "امسح للدفع"
 },
 "English": {
  "sub": "Smart Visa & Employee Management - Riyadh Companies",
  "ok": "System Online | Your Link: tasheer-ai.streamlit.app",
  "price": "Companies Subscription",
  "count": "Companies Count",
  "tab1": "🚀 Demo",
  "tab2": "🏢 Register",
  "tab3": "💳 Binance Pay",
  "try_title": "Try System",
  "company": "Company Name",
  "btn": "Try System",
  "welcome": "Demo Activated - Welcome",
  "pay_title": "Pay via Binance - USDT TRC20",
  "sar": "5,000 SAR / Month",
  "usdt": "≈ 1,333 USDT",
  "addr": "Address (TRC20):",
  "net": "Network: TRC20 - TRON",
  "amount": "Amount: 1333 USDT = 5000 SAR",
  "warn": "Important: TRC20 ONLY",
  "upload": "Upload Payment Receipt",
  "copy": "Copy Address",
  "scan": "Scan to Pay"
 }
}
t = T[lang]

st.markdown(f"<div style='text-align:center; font-size:32px; font-weight:900; color:#0F172A'>🏢 TASHEER AI</div><div style='text-align:center; color:gray; margin-bottom:15px'>{t['sub']}</div>", unsafe_allow_html=True)
st.success(f"✅ {t['ok']}")

c1,c2 = st.columns(2)
c1.metric(t['price'], t['sar'])
c2.metric(t['count'], "0 → 1000")
st.divider()

tab1, tab2, tab3 = st.tabs([t['tab1'], t['tab2'], t['tab3']])

with tab1:
    name = st.text_input(t['company'], "sab")
    if st.button(t['btn'], use_container_width=True, type="primary"):
        st.success(f"✅ {t['welcome']} - {name}")

with tab2:
    st.markdown(f"### {t['tab2']}")
    st.text_input("Email / الإيميل")
    st.text_input("Phone / الجوال")
    st.button("Register / تسجيل", use_container_width=True)

with tab3:
    st.markdown(f"### {t['pay_title']}")
    colA, colB = st.columns([1,1])
    with colA:
        st.markdown(f"## {t['sar']}\n### {t['usdt']}")
        st.code("TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH", language="text")
        st.info(f"{t['addr']} TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH\n\n{t['net']}\n\n{t['amount']}")
        st.warning(f"⚠️ {t['warn']}")
    with colB:
        st.markdown(f"**{t['scan']}**")
        st.image("https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH", caption="USDT TRC20")
        st.link_button(f"❤️ {t['copy']}", "https://api.qrserver.com/v1/create-qr-code/?size=500x500&data=TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH")

    st.file_uploader(t['upload'], type=['png','jpg','pdf'])
