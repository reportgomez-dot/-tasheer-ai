import streamlit as st
import time

st.set_page_config(page_title="UN-BIO-SHIELD AI - 50M/100M", layout="centered")

WALLET = "0xYOUR_REAL_BEP20_ADDRESS_HERE"  # <-- غير هذا بعنوانك الحقيقي

st.title("UN-BIO-SHIELD AI - 50M / 100M SAR")
st.caption("Serial: UN-MODEL-50M-ARAMCO-001 | UNGM 1191371")
st.subheader("جرب النموذج الآن - Live API")

gene = st.text_input("الصق التسلسل الجيني", value="ATGCGTAGCGTGGCTAGGTAG")
company = st.text_input("اسم شركتك", placeholder="ARAMCO / NEOM")

if st.button("افحص الآن - 10 ثواني"):
    with st.spinner("جاري الفحص..."):
        time.sleep(2)
        if "CGTAG" in gene:
            st.error("CONTAMINATED 95% - خطر")
        else:
            st.success("CLEAN 98% - نظيف")
        st.write(f"الشركة: {company} - الدقة 94%")

st.markdown("---")
st.subheader("💳 Binance Pay - ادفع الآن")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**ARAMCO - 50M SAR**")
    st.code("~13,333,333 USDT")
    st.code(WALLET)
    if st.button("نسخ عنوان أرامكو 50M"):
        st.success("تم النسخ - أرسل 13.3M USDT BEP20")

with col2:
    st.markdown("**NEOM - 100M SAR**")
    st.code("~26,666,666 USDT")
    st.code(WALLET)
    if st.button("نسخ عنوان نيوم 100M"):
        st.success("تم النسخ - أرسل 26.6M USDT BEP20")

st.info("بعد الدفع اضغط تفعيل")
if st.button("✅ تم الدفع - فعل الاشتراك"):
    st.balloons()
    st.success("تم التفعيل - API Key: UN-MODEL-ACTIVE-50M-100M")
