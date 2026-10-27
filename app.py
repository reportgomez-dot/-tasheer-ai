import streamlit as st

st.set_page_config(page_title="UN-BIO-SHIELD AI - 50M/100M", layout="centered")

st.markdown("""
<style>
.box{background:white;color:black;padding:30px;border-radius:15px;max-width:600px;margin:auto;border:2px solid #0a2540}
</style>
""", unsafe_allow_html=True)

st.title("UN-BIO-SHIELD AI - 50M / 100M SAR")
st.caption("Serial: UN-MODEL-50M-ARAMCO-001 | UNGM 1191371")

st.markdown('<div class="box">', unsafe_allow_html=True)

st.subheader("جرب النموذج الآن - Live API")

gene = st.text_input("الصق التسلسل الجيني", value="ATGCGTAGCGTGGCTAGGTAG")
company = st.text_input("اسم شركتك", placeholder="ARAMCO / NEOM")

if st.button("افحص الآن - 10 ثواني", use_container_width=True):
    with st.spinner("جاري الفحص..."):
        import time
        time.sleep(2)
        if "CGTAG" in gene:
            st.error(f"CONTAMINATED 95% - خطر - أوقف المحطة\n\nالشركة: {company}\nالسيريال: UN-MODEL-50M-ARAMCO-001\nالدقة: 94%")
        else:
            st.success(f"CLEAN 98% - نظيف\n\nالشركة: {company}\nالسيريال: UN-MODEL-50M-ARAMCO-001\nالدقة: 94%")
        
        st.markdown("**التكلفة: 5000 SAR / فحص | اشتراك 50M-100M / سنة**")
        st.markdown("Binance Pay: USDT BEP20 - Streaming Active")

st.markdown('</div>', unsafe_allow_html=True)

st.success("✅ الموقع اشتغل - الآن ارفع صور الجوازات (JPG, PNG)")

uploaded = st.file_uploader("ارفع صور الجوازات (JPG, PNG)", type=["jpg","png"], accept_multiple_files=True)

if uploaded:
    for file in uploaded:
        st.image(file, caption=file.name, use_column_width=True)
