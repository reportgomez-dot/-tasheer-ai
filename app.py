import streamlit as st
import pandas as pd
from PIL import Image
import cv2
import numpy as np
import re
import pytesseract

st.set_page_config(page_title="TASHEER AI V3 AUTO", page_icon="👑", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@700;800&display=swap');
* {font-family: 'Tajawal', sans-serif;}
#MainMenu, footer, header {visibility: hidden;}
.main-header {background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border: 2px solid #facc15; border-radius: 20px; padding: 28px; text-align: center;}
.main-header h1 {color: #facc15; font-size: 32px; margin: 0;}
.main-header p {color: #e2e8f0; font-size: 15px; margin-top: 10px;}
.whatsapp-float {position: fixed; bottom: 180px; right: 15px; z-index: 9999; background: #25D366; color: white !important; padding: 14px 22px; border-radius: 50px; text-decoration: none; font-weight: 800; box-shadow: 0 6px 20px rgba(37,211,102,0.5);}
.ocr-box {background:#fefce8; border:2px dashed #facc15; border-radius:12px; padding:12px; text-align:center; color:#854d0e; font-weight:700;}
</style>
<a href="https://wa.me/966540450738?text=السلام%20عليكم%20اريد%20الاستفسار%20عن%20TASHEER%20AI%20V3%20👑" target="_blank" class="whatsapp-float">💬 تواصل واتساب / WhatsApp</a>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>👑 TASHEER AI V3 - قراءة تلقائية OCR</h1><p>ارفع الجواز وسيتم قراءة MRZ تلقائياً | Upload - Auto Read MRZ</p><p style="color:#facc15; font-size:13px; margin-top:8px">⭐ AUTO EDITION - 966540450738 - AI Powered ⭐</p></div><br>', unsafe_allow_html=True)

if 'rows' not in st.session_state:
    st.session_state.rows = []

def parse_mrz(image):
    try:
        img = np.array(image)
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        h = gray.shape[0]
        roi = gray[int(h*0.6):h, 0:]  # MRZ تحت
        _, thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        text = pytesseract.image_to_string(thresh, config='--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<')
        lines = [l for l in text.split('\n') if len(l.strip()) > 20]
        # تنظيف
        mrz_lines = []
        for l in lines:
            l = re.sub(r'[^A-Z0-9<]', '', l.upper())
            if len(l) >= 30:
                mrz_lines.append(l)
        
        if len(mrz_lines) >= 2:
            line1 = mrz_lines[-2]
            line2 = mrz_lines[-1]
            
            # استخراج البيانات
            # جواز: السطر 2 أول 9 أحرف
            passport_no = line2[0:9].replace('<','').strip()
            # DOB: YYMMDD في 13-19
            dob_raw = line2[13:19] if len(line2) >= 19 else ""
            # Expiry: 21-27
            exp_raw = line2[21:27] if len(line2) >= 27 else ""
            # Name من السطر 1 بعد P<COUNTRY
            name_part = line1[5:] if len(line1) > 5 else ""
            name = name_part.replace('<',' ').strip()
            name = ' '.join(name.split())  # إزالة فراغات زائدة

            def fmt_date(yymmdd):
                if len(yymmdd)==6 and yymmdd.isdigit():
                    return f"{yymmdd[4:6]}/{yymmdd[2:4]}/{yymmdd[0:2]}"
                return yymmdd

            return {
                "name": name.title(),
                "passport": passport_no,
                "dob": fmt_date(dob_raw),
                "exp": fmt_date(exp_raw),
                "mrz_raw": f"{line1}\n{line2}"
            }
        return None
    except Exception as e:
        return {"error": str(e)}

uploaded_files = st.file_uploader("📸 اختر صور الجواز (MRZ تحت) - سيتم القراءة التلقائية / Upload for Auto-Read", type=["jpg","jpeg","png"], accept_multiple_files=True)

auto_data = {}
if uploaded_files:
    st.markdown('<div class="ocr-box">🤖 جاري القراءة التلقائية بالذكاء الاصطناعي... / AI Reading MRZ...</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, f in enumerate(uploaded_files):
        img = Image.open(f)
        with cols[i % 3]:
            st.image(img, caption=f.name, use_container_width=True)
            result = parse_mrz(img)
            if result and "name" in result:
                st.success(f"✅ {result['passport']} - {result['name'][:15]}")
                if i == 0:  # أول صورة يعبى الفورم
                    auto_data = result
            elif result and "error" in result:
                st.warning(f"⚠️ {result['error']}")
            else:
                st.info("ℹ️ لم يتم كشف MRZ - أدخل يدوياً")

st.markdown("---")

c1, c2, c3, c4 = st.columns(4)
with c1: n = st.text_input("الاسم / Name", value=auto_data.get("name",""))
with c2: p = st.text_input("رقم الجواز / Passport No", value=auto_data.get("passport",""))
with c3: d = st.text_input("الميلاد / DOB", value=auto_data.get("dob",""))
with c4: e = st.text_input("الانتهاء / Expiry", value=auto_data.get("exp",""))

if auto_data.get("mrz_raw"):
    st.code(auto_data["mrz_raw"], language="text")

colA, colB = st.columns([4,1])
with colA:
    if st.button("➕ إضافة / Add", use_container_width=True):
        if n or p:
            st.session_state.rows.append({"Name / الاسم":n, "Passport / الجواز":p, "DOB / الميلاد":d, "Expiry / الانتهاء":e})
            st.toast("✅ تمت الإضافة / Added")
            st.rerun()
with colB:
    st.metric("عدد الجوازات / Total", len(st.session_state.rows))

if st.session_state.rows:
    df = pd.DataFrame(st.session_state.rows)
    st.dataframe(df, use_container_width=True, height=350)
    c_exp, c_clr = st.columns(2)
    with c_exp:
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 تصدير Excel / Export Excel", data=csv, file_name="TASHEER_V3_Auto_Export.csv", mime="text/csv", use_container_width=True)
    with c_clr:
        if st.button("🗑️ مسح الكل / Clear All", use_container_width=True):
            st.session_state.rows = []
            st.rerun()

st.markdown("<center style='color:#64748b; font-size:12px; margin-top:20px'>© 2026 TASHEER AI V3 AUTO - WhatsApp: +966 54 045 0738 | AI MRZ Reader</center>", unsafe_allow_html=True)
