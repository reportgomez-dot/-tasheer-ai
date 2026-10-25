import streamlit as st
import pandas as pd
st.set_page_config(page_title="TASHEER AI Royal", page_icon="👑", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@700;800&display=swap');
* {font-family: 'Tajawal', sans-serif;}
#MainMenu, footer, header {visibility: hidden;}
.main-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    border: 2px solid #facc15;
    border-radius: 20px;
    padding: 28px;
    text-align: center;
}
.main-header h1 {color: #facc15; font-size: 34px; margin: 0;}
.main-header p {color: #e2e8f0; font-size: 16px; margin-top: 10px;}
.whatsapp-float {
    position: fixed;
    bottom: 140px;
    right: 15px;
    z-index: 9999;
    background: #25D366;
    color: white !important;
    padding: 14px 22px;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 800;
    box-shadow: 0 6px 20px rgba(37,211,102,0.5);
}
</style>
<a href="https://wa.me/966540450738?text=السلام%20عليكم%20اريد%20الاستفسار%20عن%20TASHEER%20AI%20👑" target="_blank" class="whatsapp-float">💬 تواصل واتساب / WhatsApp</a>
""", unsafe_allow_html=True)
lang_opt = st.selectbox("🌐 Language / اللغة", ["العربية + English", "English Only", "العربية فقط"], index=0)
is_ar = lang_opt != "English Only"
T = {
    "title": "👑 TASHEER AI - نظام قراءة الجوازات والتأشيرات V2" if is_ar else "👑 TASHEER AI - Passport & Visa Reader V2",
    "sub": "ارفع صور الجوازات وسيتم استخراج الاسم ورقم الجواز تلقائياً | Upload & Extract Automatically",
    "upload": "📸 اختر صور الجواز (MRZ تحت) / Upload Passport (MRZ bottom)",
    "name": "الاسم / Name", "pass": "رقم الجواز / Passport No", "dob": "الميلاد / DOB", "exp": "الانتهاء / Expiry",
    "add": "➕ إضافة / Add", "export": "📥 تصدير Excel / Export Excel", "clear": "🗑️ مسح الكل / Clear All",
    "count": "عدد الجوازات / Total"
}
st.markdown(f'<div class="main-header"><h1>{T["title"]}</h1><p>{T["sub"]}</p><p style="color:#facc15; font-size:13px; margin-top:12px">⭐ Royal Edition - 966540450738 ⭐</p></div><br>', unsafe_allow_html=True)
if 'rows' not in st.session_state:
    st.session_state.rows = []
uploaded = st.file_uploader(T["upload"], type=["jpg","jpeg","png"], accept_multiple_files=True)
if uploaded:
    cols = st.columns(3)
    for i, f in enumerate(uploaded):
        with cols[i % 3]:
            st.image(f, caption=f.name, use_container_width=True)
c1, c2, c3, c4 = st.columns(4)
with c1: n = st.text_input(T["name"])
with c2: p = st.text_input(T["pass"])
with c3: d = st.text_input(T["dob"])
with c4: e = st.text_input(T["exp"])
colA, colB = st.columns([4,1])
with colA:
    if st.button(T["add"], use_container_width=True):
        if n or p:
            st.session_state.rows.append({"Name / الاسم":n, "Passport / الجواز":p, "DOB / الميلاد":d, "Expiry / الانتهاء":e})
            st.toast("✅ تمت الإضافة")
            st.rerun()
with colB:
    st.metric(T["count"], len(st.session_state.rows))
if st.session_state.rows:
    df = pd.DataFrame(st.session_state.rows)
    st.dataframe(df, use_container_width=True, height=350)
    c_exp, c_clr = st.columns(2)
    with c_exp:
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(T["export"], data=csv, file_name="TASHEER_Royal_Export.csv", mime="text/csv", use_container_width=True)
    with c_clr:
        if st.button(T["clear"], use_container_width=True):
            st.session_state.rows = []
            st.rerun()
st.markdown("---")
st.markdown("<center style='color:#64748b; font-size:12px'>© 2026 TASHEER AI - WhatsApp: +966 54 045 0738</center>", unsafe_allow_html=True)
