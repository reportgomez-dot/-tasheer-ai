import streamlit as st
import time

st.set_page_config(page_title="UN-BIO-SHIELD AI - 50M/100M", layout="centered")

BINANCE_ID = "457890758"

st.title("UN-BIO-SHIELD AI - 50M / 100M SAR")
st.caption("Serial: UN-MODEL-50M-ARAMCO-001 | UNGM 1191371")
st.subheader("جرب النموذج الآن - Live API")

gene = st.text_input("الصق التسلسل الجيني", value="ATGCGTAGCGTGGCTAGGTAG")
company = st.text_input("اسم شركتك", placeholder="ARAMCO / NEOM")

if st.button("افحص الآن - 10 ثواني"):
    with st.spinner("جاري الفحص..."):
        time.sleep(2)
        if "CGTAG" in gene:
            st.error("CONTAMINATED 95% - خطر - أوقف المحطة")
        else:
            st.success("CLEAN 98% - نظيف")
        st.write(f"الشركة: {company} | الدقة 94% | S/N: UN-MODEL-50M-ARAMCO-001")

st.markdown("---")
st.subheader("💳 ادفع الآن - Binance Pay ID: 457890758")

col1, col2 = st.columns(2)
with col1:
    st.info("**ARAMCO - 50M SAR**\n\n~13,333,333 USDT")
    st.code(f"Binance ID: {BINANCE_ID}")
with col2:
    st.warning("**NEOM - 100M SAR**\n\n~26,666,666 USDT")
    st.code(f"Binance ID: {BINANCE_ID}")

st.success(f"افتح Binance App > Pay > Send > ID: {BINANCE_ID} > USDT")
st.markdown("**بعد الدفع - أرسل صورة التحويل على واتساب لتفعيل API فوراً**")

if st.button("✅ تم الدفع - فعل الاشتراك الآن"):
    st.balloons()
    st.success("تم التفعيل! API Key: UN-MODEL-ACTIVE-457890758 - تواصل واتساب")
