import streamlit as st
import pandas as pd
from PIL import Image
import re

st.set_page_config(page_title="TASHEER AI V2.2 MRZ", page_icon="👑", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@700;800&display=swap');
* {font-family: 'Tajawal', sans-serif;}
#MainMenu, footer, header {visibility: hidden;}
.main-header {background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border: 2px solid #facc15; border-radius: 20px; padding: 28px; text-align: center;}
.main-header h1 {color: #facc15; font-size: 32px; margin: 0;}
.main-header p {color: #e2e8f0; font-size: 15px; margin-top: 10px;}
.whatsapp-float {position: fixed; bottom: 180px; right: 15px; z-index: 9999; background: #25D366; color: white !important; padding: 14px 22px; border-radius: 50px; text-decoration: none; font-weight: 800; box-shadow: 0 6px 20px rgba(37,211,102,0.5);}
.mrz-box {background:#fefce8; border:2px solid #facc15; border-radius:12px; padding:15px;}
</style>
<a href="https://wa.me/966540450738?text=السلام%20عليكم%20اريد%20TASHEER%20AI%20V2.2" target="_blank" class="whatsapp-float">💬 تواصل واتساب / WhatsApp</a>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>👑 TASHEER AI V2.2 - قراءة MRZ الذكية</h1><p>الصق سطرين MRZ من أسفل الجواز وسيتم التعبئة تلقائياً | Paste MRZ for Auto-Fill</p><p style="color:#facc15; font-size:13px; margin-top:8px">⭐ MRZ AUTO EDITION - 966540450738 ⭐</p></div><br>', unsafe_allow_html=True)

if 'rows' not in st.session_state:
    st.session_state.rows = []

def parse_mrz_text(text):
    text = text.upper().strip()
    lines = [re.sub(r'[^A-Z0-9<]', '', l.upper()) for l in text.replace(' ','').split('\n') if l.strip()]
    lines = [l for l in lines if len(l) >= 30]
    if len(lines) < 2:
        # حاول تقسيم سطر طويل
        if len(text) > 80:
            cleaned = re.sub(r'[^A-Z0-9<]', '', text.upper())
            if len(cleaned) >= 88:
                lines = [cleaned[:44], cleaned[44:88]]
    if len(lines) >= 2:
        l1, l2 = lines[-2], lines[-1]
        try:
            # الاسم من السطر 1
            name_raw = l1[5:] if len(l1) > 5 else ""
            parts = name_raw.split('<<')
            surname = parts[0].replace('<',' ').strip() if parts else ""
            given = parts[1].replace('<',' ').strip() if len(parts)>1 else ""
            full_name = f"{given} {surname}".strip()
            full_name = ' '.join(full_name.split())
            
            passport_no = l2[0:9].replace('<','').strip()
            dob = l2[13:19] if len(l2)>=19 else ""
            exp = l2[21:27] if len(l2)>=27 else ""
            def fmt(yymmdd):
                if len(yymmdd)==6 and yymmdd.isdigit():
                    return f"{yymmdd[4:6]}/{yymmdd[2:4]}/20{yymmdd[0:2]}" if int(yymmdd[0:2]) < 30 else f"{yymmdd[4:6]}/{yymmdd[2:4]}/19{yymmdd[0:2]}"
                return yymmdd
            return {"name": full_name.title(), "passport": passport_no, "dob": fmt(dob), "exp": fmt(exp), "l1": l1, "l2": l2}
        except:
            return None
    return None

# قسم MRZ
st.markdown('<div class="mrz-box">', unsafe_allow_html=True)
st.markdown("**🤖 الصق سطرين MRZ من أسفل الجواز هنا (اختياري - للتعبئة التلقائية) / Paste 2 MRZ lines here**")
mrz_input = st.text_area("MRZ", placeholder="مثال / Example:\nP<SAUMOHAMMED<<AHMED<<<<<<<<<<<<<<<<<<<<<<\nE12345678<0SAU9001011M3012312<<<<<<<<<<<<<<04", height=90, label_visibility="collapsed")
col_parse, col_clear_mrz = st.columns([3,1])
auto = {}
if mrz_input:
    auto = parse_mrz_text(mrz_input)
    if auto:
        with col_parse:
            st.success(f"✅ تم الكشف: {auto['passport']} | {auto['name']} | ميلاد: {auto['dob']} | انتهاء: {auto['exp']}")
            st.code(f"{auto['l1']}\n{auto['l2']}")
    else:
        st.warning("⚠️ لم أتعرف على MRZ - تأكد أنك لصقت سطرين كاملين بدون مسافات")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# رفع الصور
uploaded = st.file_uploader("📸 اختر صور الجواز / Upload Passport Images", type=["jpg","jpeg","png"], accept_multiple_files=True)
if uploaded:
    cols = st.columns(3)
    for i, f in enumerate(uploaded):
        with cols[i % 3]:
            st.image(Image.open(f), caption=f.name, use_container_width=True)

# الحقول مع تعبئة تلقائية
c1, c2, c3, c4 = st.columns(4)
with c1: n = st.text_input("الاسم / Name", value=auto.get("name","") if auto else "")
with c2: p = st.text_input("رقم الجواز / Passport No", value=auto.get("passport","") if auto else "")
with c3: d = st.text_input("الميلاد / DOB", value=auto.get("dob","") if auto else "")
with c4: e = st.text_input("الانتهاء / Expiry", value=auto.get("exp","") if auto else "")

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
        st.download_button("📥 تصدير Excel / Export Excel", data=csv, file_name="TASHEER_V2.2_MRZ.csv", mime="text/csv", use_container_width=True)
    with c_clr:
        if st.button("🗑️ مسح الكل / Clear All", use_container_width=True):
            st.session_state.rows = []
            st.rerun()

st.markdown("<center style='color:#64748b; font-size:12px; margin-top:30px'>© 2026 TASHEER AI V2.2 MRZ - WhatsApp: +966 54 045 0738 - Smart MRZ Parser</center>", unsafe_allow_html=True)
