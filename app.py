import streamlit as st
import pandas as pd

st.set_page_config(page_title="TASHEER AI - الرسمية", layout="wide")

st.markdown("""
<div style="background: linear-gradient(135deg, #0f172a 0%, #134e4a 50%, #a16207 100%);
border-radius: 25px; padding: 40px 20px; text-align: center;">
    <h1 style="color:white; font-size:42px; margin:0">TASHEER AI</h1>
    <p style="color:#e2e8f0; margin-top:15px">المنصة الرسمية - Founder: WAIL SALAHELDIN ABDULLA</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### 📸 قارئ الجواز الذكي")
st.success("✅ الموقع اشتغل - الآن ارفع صور الجوازات")
st.file_uploader("ارفع صور الجوازات (JPG, PNG)", type=["jpg","png","jpeg"], accept_multiple_files=True)

st.markdown("---")
st.markdown("### 💰 ادفع عبر Binance Pay أو STC Pay")

col1, col2 = st.columns(2)
with col1:
    st.info("💛 Binance Pay: 30 USDT = 50 جواز")
    st.link_button("ادفع USDT الآن", "https://app.binance.com/en/pay", use_container_width=True)
with col2:
    st.success("💚 STC Pay / بنك: 150 ر.س = 50 جواز")
    st.link_button("واتساب للدفع", "https://wa.me/966540450738", use_container_width=True)
