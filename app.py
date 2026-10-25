import streamlit as st
import pandas as pd
from PIL import Image
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
.whatsapp-float {position: fixed; bottom: 180px; right: 15px; z-index: 9999; background: #25D366; color: white !important; padding: 14px 22px; border-radius: 50px; text-decoration: none; font-weight: 800;}
.ocr-box {background:#fefce8; border:2px dashed #facc15; border-radius:12px; padding:12px; text-align:center; font-weight:700;}
</style>
<a href="https://wa.me/966540450738?text=السلام%20عليكم%20اريد%20TASHEER%20AI%20V3" target="_blank" class="whatsapp-float">💬 واتساب / WhatsApp</a>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>👑 TASHEER AI V3 - قراءة تلقائية OCR</h1><p>ارفع الجواز وسيتم قراءة MRZ تلقائياً</p><p style="color:#facc15; font-size:13px; margin-top:8px">⭐ AUTO LITE EDITION - 966540450738 ⭐</p></div><br>', unsafe_allow_html=True)

if 'rows' not in st.session_state:
    st.session_state.rows = []

def parse_mrz_pil(image):
    try:
        w, h = image.size
        roi = image.crop((0, int(h*0.60), w, h))
        roi = roi.convert('L').point(lambda x: 255 if x > 130 else 0, mode='1')
        text = pytesseract.image_to_string(roi, config='--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<')
        lines = [re.sub(r'[^A-Z0-9<]', '', l.upper()) for l in text.split('\n') if len(l.strip()) > 20]
        mrz = [l for l in lines if len(l) >= 30]
        if len(mrz) >= 2:
            line1, line2 = mrz[-2], mrz[-1]
            passport_no = line2[0:9].replace('<','').strip()
            dob_raw = line2[13:19] if len(line2)>=19 else ""
            exp_raw = line2[21:27] if len(line2)>=27 else ""
            name_part = line1[5:] if len(line1)>5 else ""
            name = ' '.join(name_part.replace('<',' ').split())
            def fmt(d): return f"{d[4:6]}/{d[2:4]}/{d[0:2]}" if len(d)==6 and d.isdigit() else d
            return {"name": name.title(), "passport": passport_no, "dob": fmt(dob_raw), "exp": fmt(exp_raw), "mrz_raw": f"{line1}\n{line2}"}
        return None
    except Exception as e:
        return {"error": str(e)}

uploaded_files = st.file_uploader("📸 اختر صور الجواز - قراءة تلقائية", type=["jpg","jpeg","png"], accept_multiple_files=True)

auto_data = {}
if uploaded_files:
    st.markdown('<div class="ocr-box">🤖 جاري القراءة التلقائية... / AI Reading...</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, f in enumerate(uploaded_files):
        img = Image.open(f)
        with cols[i % 3]:
            st.image(img, caption=f.name, use_container_width=True)
            res = parse_mrz_pil(img)
            if res and "name" in res:
                st.success(f"✅ {res['passport']} - {res['name'][:20]}")
                if i==0: auto_data=res
            else:
                st.info("ℹ️ MRZ غير واضح - أدخل يدوياً")

st.markdown("---")
c1, c2, c3, c4 = st.columns(4)
with c1: n = st.text_input("الاسم / Name", value=auto_data.get("name",""))
with c2: p = st.text_input("رقم الجواز / Passport No", value=auto_data.get("passport",""))
with c3: d = st.text_input("الميلاد / DOB", value=auto_data.get("dob",""))
with c4: e = st.text_input("الانتهاء / Expiry", value=auto_data.get("exp",""))
if auto_data.get("mrz_raw"): st.code(auto_data["mrz_raw"])

colA, colB = st.columns([4,1])
with colA:
    if st.button("➕ إضافة / Add", use_container_width=True):
        if n or p:
            st.session_state.rows.append({"Name":n, "Passport":p, "DOB":d, "Expiry":e})
            st.toast("✅ تمت الإضافة")
            st.rerun()
with colB: st.metric("Total", len(st.session_state.rows))

if st.session_state.rows:
    df = pd.DataFrame(st.session_state.rows)
    st.dataframe(df, use_container_width=True)
    c1, c2 = st.columns(2)
    with c1: st.download_button("📥 تصدير Excel", data=df.to_csv(index=False).encode('utf-8-sig'), file_name="TASHEER_V3.csv", mime="text/csv", use_container_width=True)
    with c2:
        if st.button("🗑️ مسح الكل", use_container_width=True):
            st.session_state.rows=[]; st.rerun()
