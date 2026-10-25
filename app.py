import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="TASHEER AI Royal V2.1", page_icon="👑", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@700;800&display=swap');
* {font-family: 'Tajawal', sans-serif;}
#MainMenu, footer, header {visibility: hidden;}
.main-header {background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border: 2px solid #facc15; border-radius: 20px; padding: 28px; text-align: center;}
.main-header h1 {color: #facc15; font-size: 32px; margin: 0;}
.main-header p {color: #e2e8f0; font-size: 15px; margin-top: 10px;}
.whatsapp-float {position: fixed; bottom: 180px; right: 15px; z-index: 9999; background: #25D366; color: white !important; padding: 14px 22px; border-radius: 50px; text-decoration: none; font-weight: 800; box-shadow: 0 6px 20px rgba(37,211,102,0.5);}
</style>
<a href="https://wa.me/966540450738?text=السلام%20عليكم%20اريد%20الاستفسار%20عن%20TASHEER%20AI%20👑" target="_blank" class="whatsapp-float">💬 تواصل واتساب / WhatsApp</a>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>👑 TASHEER AI - نظام الجوازات والتأشيرات V2.1</h1><p>النسخة الملكية المستقرة | Royal Stable Edition</p><p style="color:#facc15; font-size:13px; margin-top:8px">⭐ 966540450738 ⭐ tasheer-ai-juub2hzyqf9boqzthpwv4n.streamlit.app</p></div><br>', unsafe_allow_html=True)

if 'rows' not in st.session_state:
    st.session_state.rows = []

uploaded = st.file_uploader("📸 اختر صور الجواز / Upload Passport Images", type=["jpg","jpeg","png"], accept_multiple_files=True)
if uploaded:
    cols = st.columns(3)
    for i, f in enumerate(uploaded):
        with cols[i % 3]:
            st.image(Image.open(f), caption=f.name, use_container_width=True)

c1, c2, c3, c4 = st.columns(4)
with c1: n = st.text_input("الاسم / Name")
with c2: p = st.text_input("رقم الجواز / Passport No")
with c3: d = st.text_input("الميلاد / DOB")
with c4: e = st.text_input("الانتهاء / Expiry")

colA, colB = st.columns([4,1])
with colA:
    if st.button("➕ إضافة / Add", use_container_width=True):
        if n or p:
            st.session_state.rows.append({"Name / الاسم": n, "Passport / الجواز": p, "DOB / الميلاد": d, "Expiry / الانتهاء": e})
            st.toast("✅ تمت الإضافة")
            st.rerun()
with colB:
    st.metric("عدد الجوازات / Total", len(st.session_state.rows))

if st.session_state.rows:
    df = pd.DataFrame(st.session_state.rows)
    st.dataframe(df, use_container_width=True, height=350)
    c_exp, c_clr = st.columns(2)
    with c_exp:
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 تصدير Excel / Export Excel", data=csv, file_name="TASHEER_Royal.csv", mime="text/csv", use_container_width=True)
    with c_clr:
        if st.button("🗑️ مسح الكل / Clear All", use_container_width=True):
            st.session_state.rows = []
            st.rerun()

st.markdown("<center style='color:#64748b; font-size:12px; margin-top:30px'>© 2026 TASHEER AI Royal - WhatsApp: +966 54 045 0738</center>", unsafe_allow_html=True)
