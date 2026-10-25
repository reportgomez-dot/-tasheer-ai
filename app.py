import streamlit as st
st.set_page_config(page_title="TASHEER AI", layout="wide", page_icon="👑")
st.markdown("""
<style>
body{direction:rtl}
</style>
<h1 style='text-align:center'>TASHEER AI - قارئ الجوازات V2</h1>
<p style='text-align:center'>ارفع صور الجوازات وسيتم استخراج البيانات تلقائياً</p>
""", unsafe_allow_html=True)

uploaded = st.file_uploader("اختر صور الجوازات", accept_multiple_files=True, type=['png','jpg','jpeg'])

if uploaded:
    for f in uploaded:
        st.image(f, width=300)
        st.success(f"تم قراءة: {f.name} - ضع هنا كود الـ OCR الخاص بك")

# جدول عرض البيانات
import pandas as pd
if 'data' not in st.session_state:
    st.session_state.data = []

name = st.text_input("الاسم")
passport = st.text_input("رقم الجواز")

if st.button("إضافة"):
    st.session_state.data.append({"الاسم":name, "الجواز":passport})
    
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    st.table(df)
    st.download_button("تصدير Excel", df.to_csv(index=False).encode('utf-8'), "tasheer.csv")
