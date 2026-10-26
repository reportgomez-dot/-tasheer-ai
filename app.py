# --- قسم الدفع Binance Pay ---
st.markdown("---")
st.markdown("### 💰 ادفع عبر Binance Pay أو STC Pay")

# هنا حط الـ ID حقك
BINANCE_PAY_ID = "حط_رقمك_هنا_مثلا_123456789" 
BINANCE_PAY_LINK = f"https://app.binance.com/en/pay/cre?channel=binancepay&to={BINANCE_PAY_ID}"

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#F3BA2F 0%,#000 100%); border-radius:15px; padding:20px; text-align:center">
        <h3 style="color:white">💛 Binance Pay</h3>
        <p style="color:white">30 USDT = 50 جواز</p>
    </div>
    """, unsafe_allow_html=True)
    st.link_button("🔗 ادفع 30 USDT الآن", BINANCE_PAY_LINK, use_container_width=True)
    st.caption(f"Pay ID: {BINANCE_PAY_ID}")

with col2:
    st.markdown("""
    <div style="background:linear-gradient(135deg,#00D632 0%,#0f172a 100%); border-radius:15px; padding:20px; text-align:center">
        <h3 style="color:white">💚 STC Pay / بنك</h3>
        <p style="color:white">150 ر.س = 50 جواز</p>
    </div>
    """, unsafe_allow_html=True)
    st.link_button("💬 واتساب للدفع", "https://wa.me/966540450738?text=اريد%20الاشتراك%20في%20TASHEER%20AI", use_container_width=True)
    st.caption("STC Pay: 0540450738")

st.info("بعد الدفع ارسل لنا سكرين شوت على الواتساب وبيتم تفعيل حسابك فوراً")
