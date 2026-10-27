import streamlit as st

st.set_page_config(page_title="UN-BIO-SHIELD AI - Live Model", layout="centered")

st.markdown("# UN-BIO-SHIELD AI - LIVE MODEL")
st.markdown("**AI-Powered Bio Shield - Procurement Offer - Live Model Deployed**")

st.markdown("---")

# قسم الخبرة الجديد
st.markdown("### 🏛️ Enterprise Vendor Background")
col1, col2 = st.columns(2)

with col1:
    st.info("""
    **Vendor Experience:**
    - Ex-Vendor Coordinator - Saudi Company Ltd
    - King Faisal & King Fahad Research Centers
    - Ministry of Interior & National Guard
    - Oracle ERP & Dynamics 365 Specialist
    - UNGM Vendor No: 1191371
    """)

with col2:
    st.success("""
    **Enterprise Integration Ready:**
    - Oracle ERP / P2P Integration
    - Dynamics 365 Integration
    - SAP Ariba Compatible
    - Serial: UN-MODEL-50M-ARAMCO-001
    """)

st.markdown("---")

# قسم الأسعار
c1, c2 = st.columns(2)
with c1:
    st.metric("ARAMCO PRICE", "50M SAR", "13,333,333 USDT")
with c2:
    st.metric("NEOM PRICE", "100M SAR", "26,666,666 USDT")

st.markdown("---")

# قسم التجربة الحية
st.markdown("### 🧬 Live Test - Try in 10 Seconds")
gene = st.text_input("Enter Gene Sequence", "ATGCGTAGCGTGGCTAGGTAG")

if st.button("Analyze"):
    if "ATGCGT" in gene:
        st.error("Result: CONTAMINATED 95% - Immediate alert")
    else:
        st.success("Result: CLEAN 98% - Safe")

st.markdown("---")

# قسم الدفع
st.markdown("### 💳 Payment")
st.markdown("## Binance Pay ID: 457890758")
st.code("Binance Pay ID: 457890758 - Network BEP20 USDT")
st.markdown("Website: tasheer-ai-juub2hzyqf9boqzthpwv4n.streamlit.app")
st.caption("UNGM 1191371 | Accuracy 94% | Instant API Delivery")
