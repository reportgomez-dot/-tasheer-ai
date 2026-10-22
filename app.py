import streamlit as st

st.set_page_config(page_title="TASHEER AI - الرياض", layout="centered", page_icon="🛂")

st.title("🛂 TASHEER AI - نظام شركات الرياض")
st.markdown("### نظام ذكي لإدارة التأشيرات والموظفين")

st.success("✅ النظام يعمل بنجاح! رابطك الدائم جاهز")

col1, col2 = st.columns(2)
with col1:
    st.metric("اشتراك الشركات", "5,000 ريال/شهر")
with col2:
    st.metric("عدد الشركات", "0 -> 1000")

st.divider()
name = st.text_input("اسم الشركة للتجربة")
if st.button("🚀 تجربة النظام", type="primary"):
    st.balloons()
    st.success(f"أهلا {name} - تم تفعيل تجربتك!")
    st.write("رابطك: tasheer-ai.streamlit.app")

st.info("الخطوة التالية بعد الـ Deploy: نربط قاعدة البيانات والواتساب")
