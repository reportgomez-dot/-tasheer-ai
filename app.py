import streamlit as st

st.title("UN-BIO-SHIELD - Gene Balance")
st.write("تصنيع رصيد من أكواد الجينات")

gene = st.text_input("Enter Gene Sequence", "ATCGATCG")

if st.button("Analyze / Create Balance"):
    if len(gene) > 10:
        balance = len(gene) * 1000
        st.success(f"تم تصنيع الرصيد: {balance} GENE")
        st.metric("رصيدك", f"{balance} GENE")
        st.metric("Award Price", "50M SAR")
        st.metric("Recom Price", "100M SAR")
        st.info(f"Binance Pay ID: 457890758 - Network BEP20 USDT")
    else:
        st.error("كود الجين قصير جدا")
