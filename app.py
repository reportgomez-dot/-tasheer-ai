import streamlit as st
import pandas as pd
from PIL import Image
import re

st.set_page_config(page_title="TASHEER AI V2", page_icon="👑", layout="wide")

# --- تصميم ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
* {font-family: 'Tajawal', sans-serif;}
.main {direction: rtl;}
.stButton>button {background:#2563eb; color:white; width:100%; border-radius:10px; font-weight:bold; padding:12px}
</style>
""", unsafe_allow_html=True)

st.title("👑 TASHEER AI - نظام قراءة الجوازات والتأشيرات V2")
st.markdown("### ارفع صور الجوازات وسيتم استخراج الاسم ورقم الجواز تلقائياً")

# --- الدوال ---
def parse_mrz(text):
    text = text.upper()
    lines = [l for l in text.split('\n') if '<' in l and len(l) > 20]
    data = {"name":"--", "passport":"--", "dob":"--", "expiry":"--"}
    if len(lines) >= 2:
        try:
            l1 = lines[-2]
            l2 = lines[-1]
            # الاسم
            name_part = l1[5:].split('<<')
            surname = name_part[0].replace('<',' ').strip()
            given = name_part[1].replace('<',' ').strip() if len(name_part)>1 else ''
            data["name"] = f"{surname} {given}".strip()
            # رقم الجواز
            data["passport"] = l2[0:9].replace('<','')
            # تواريخ
            dob_raw = l2[13:19]
            exp_raw = l2[21:27]
            def fmt(s):
                if len(s)!=6 or not s.isdigit(): return s
                dd=s[4:6]; mm=s[2:4]; yy=s[0:2]
                yyyy = f"19{yy}" if int(yy)>50 else f"20{yy}"
                return f"{dd}/{mm}/{yyyy}"
            data["dob"] = fmt(dob_raw)
            data["expiry"] = fmt(exp_raw)
        except:
            pass
    return data

# --- حالة البيانات ---
if 'rows' not in st.session_state:
    st.session_state.rows = []

# --- رفع الصور ---
uploaded_files = st.file_uploader("📸 اختر صور الجواز (MRZ تحت)", type=["jpg","jpeg","png"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        img = Image.open(file)
        st.image(img, caption=file.name, width=400)
        
        # ملاحظة: على Streamlit السحابي نحتاج كتابة يدوية للـ MRZ لأن Tesseract غير مثبت افتراضياً
        # لذلك نطلب من المستخدم لصق السطرين
        mrz_input = st.text_area(f"الصق نص MRZ لـ {file.name} (السطرين اللي تحت في الجواز)", key=file.name, placeholder="P<SAU...<<\n... ")
        if mrz_input:
            parsed = parse_mrz(mrz_input)
            if st.button(f"إضافة {file.name}", key=f"add_{file.name}"):
                st.session_state.rows.append(parsed)
                st.success(f"تمت إضافة: {parsed['name']}")

st.divider()

# --- إدخال يدوي سريع ---
col1, col2, col3, col4 = st.columns(4)
with col1:
    n = st.text_input("الاسم")
with col2:
    p = st.text_input("رقم الجواز")
with col3:
    d = st.text_input("الميلاد")
with col4:
    e = st.text_input("الانتهاء")

if st.button("➕ إضافة يدوية"):
    if n or p:
        st.session_state.rows.append({"name":n, "passport":p, "dob":d, "expiry":e})
        st.rerun()

# --- عرض الجدول ---
if st.session_state.rows:
    df = pd.DataFrame(st.session_state.rows)
    st.dataframe(df, use_container_width=True)
    
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 تصدير Excel (CSV)", data=csv, file_name="tasheer_export.csv", mime="text/csv")
    
    if st.button("🗑️ مسح الكل"):
        st.session_state.rows = []
        st.rerun()
else:
    st.info("لم تتم إضافة أي جوازات بعد. ارفع صورة والصق الـ MRZ أو أدخل يدوياً.")
