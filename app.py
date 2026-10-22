import streamlit as st

st.set_page_config(page_title="TASHEER AI", page_icon="🏢", layout="centered")

st.markdown("""
<style>
.logo {font-size:42px; font-weight:900; text-align:center; color:#0F172A}
.sub {text-align:center; color:gray; margin-bottom:15px}
.box {background:#F8FAFC; border:1px solid #E2E8F0; border-radius:12px; padding:12px; text-align:center}
</style>
<div class="logo">🏢 TASHEER AI</div>
<div class="sub">نظام ذكي لإدارة التأشيرات والموظفين - شركات الرياض</div>
""", unsafe_allow_html=True)

st.success("✅ النظام يعمل | رابطك: tasheer-ai.streamlit.app")
c1,c2 = st.columns(2)
c1.metric("اشتراك الشركات","5,000 ريال/شهر")
c2.metric("عدد الشركات","0 → 1000")
st.divider()

t1,t2,t3 = st.tabs(["🚀 تجربة","🏢 تسجيل شركة","💳 دفع Binance"])

with t1:
    name = st.text_input("اسم الشركة للتجربة")
    if st.button("🚀 تجربة النظام", type="primary", use_container_width=True):
        if name: 
            st.success(f"أهلاً {name} - تم تفعيل تجربتك!")
            st.balloons()
        else: st.warning("اكتب اسم الشركة")

with t2:
    st.write("### تسجيل شركة جديدة")
    with st.form("reg"):
        cn = st.text_input("اسم الشركة *")
        own = st.text_input("اسم المسؤول *")
        phone = st.text_input("واتساب *", placeholder="05xxxxxxxx")
        email = st.text_input("البريد")
        size = st.selectbox("حجم الشركة",["1-10","11-50","51-200","200+"])
        agree = st.checkbox("أوافق على الشروط")
        ok = st.form_submit_button("📝 تسجيل الآن", use_container_width=True)
        if ok:
            if cn and own and phone and agree:
                st.success(f"تم تسجيل {cn}! رقم طلبك: TASHEER-{phone[-4:]}")
                st.info(f"سنتواصل معك على {phone}")
            else: st.error("عبي الحقول المطلوبة *")

with t3:
    st.write("### 💳 الدفع عبر Binance")
    st.markdown('<div class="box"><h3>5,000 ريال / شهر</h3><p>≈ 1,333 USDT</p></div>', unsafe_allow_html=True)
    st.write("")
    st.code("Binance Pay ID: 123456789\nUSDT TRC20: TXYourAddressHere", language="text")
    st.link_button("💛 ادفع عبر Binance Pay", "https://www.binance.com/en/binance-pay", use_container_width=True)
    st.warning("⚠️ اختر شبكة TRC20 لتكون الرسوم رخيصة")
    up = st.file_uploader("ارفع إيصال الدفع", type=["jpg","png"])
    if up: st.success("تم رفع الإيصال - سيتم التفعيل خلال ساعة!")
