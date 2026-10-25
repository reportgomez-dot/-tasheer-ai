import streamlit as st
import pandas as pd
from PIL import Image
import re, urllib.parse
from datetime import datetime
import cv2
import numpy as np
import pytesseract

st.set_page_config(page_title="TASHEER AI V2.5 AUTO", page_icon="👑", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@700;800&display=swap');
* {font-family: 'Tajawal', sans-serif;}
#MainMenu, footer, header {visibility: hidden;}
.main-header {background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); border: 3px solid #facc15; border-radius: 20px; padding: 28px; text-align: center; box-shadow: 0 8px 30px rgba(0,0,0,0.3);}
.main-header h1 {color: #facc15; font-size: 32px; margin: 0;}
.main-header p {color: #e2e8f0; font-size: 15px; margin-top: 10px;}
.whatsapp-float {position: fixed; bottom: 180px; right: 15px; z-index: 9999; background: #25D366; color: white !important; padding: 14px 22px; border-radius: 50px; text-decoration: none; font-weight: 800; box-shadow: 0 6px 20px rgba(37,211,102,0.5);}
.mrz-box {background:linear-gradient(135deg, #fefce8 0%, #fef9c3 100%); border:2px solid #facc15; border-radius:15px; padding:18px;}
.auto-badge {background:linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color:white; padding:8px 15px; border-radius:20px; font-weight:800; display:inline-block; animation: pulse 2s infinite;}
@keyframes pulse {0%{transform:scale(1)}50%{transform:scale(1.05)}100%{transform:scale(1)}}
</style>
<a href="https://wa.me/966540450738?text=السلام%20عليكم%20اريد%20TASHEER%20AI%20V2.5%20AUTO" target="_blank" class="whatsapp-float">💬 تواصل واتساب / WhatsApp</a>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>👑 TASHEER AI V2.5 - قراءة تلقائية من الصورة</h1><p>ارفع صورة الجواز وسيتم قراءة MRZ أوتوماتيك + إنجاز + واتساب | AUTO MRZ FROM IMAGE</p><p><span class="auto-badge">🤖 AUTO OCR ENABLED</span> <span style="color:#facc15; margin-left:10px">⭐ V2.5 - 966540450738 ⭐</span></p></div><br>', unsafe_allow_html=True)

if 'rows' not in st.session_state:
    st.session_state.rows = []
if 'auto' not in st.session_state:
    st.session_state.auto = {}

def parse_mrz_lines(l1, l2):
    try:
        name_raw = l1[5:] if len(l1) > 5 else ""
        parts = name_raw.split('<<')
        surname = parts[0].replace('<',' ').strip() if parts else ""
        given = parts[1].replace('<',' ').strip() if len(parts)>1 else ""
        full_name = f"{given} {surname}".strip()
        full_name = ' '.join(full_name.split()).title()
        passport_no = l2[0:9].replace('<','').strip()
        nationality = l2[10:13].replace('<','').strip() if len(l2)>=13 else "PAK"
        dob_raw = l2[13:19] if len(l2)>=19 else ""
        sex = l2[20] if len(l2)>=21 else "M"
        exp_raw = l2[21:27] if len(l2)>=27 else ""
        def fmt(yymmdd):
            if len(yymmdd)==6 and yymmdd.isdigit():
                yy=int(yymmdd[0:2]); mm=yymmdd[2:4]; dd=yymmdd[4:6]
                year=2000+yy if yy<30 else 1900+yy
                try:
                    dt=datetime(year,int(mm),int(dd))
                    return dt.strftime("%d/%m/%Y"), dt.strftime("%Y-%m-%d")
                except:
                    return f"{dd}/{mm}/{year}", f"{year}-{mm}-{dd}"
            return yymmdd, yymmdd
        dob_enjaz,dob_iso=fmt(dob_raw)
        exp_enjaz,exp_iso=fmt(exp_raw)
        nat_map={"PAK":"باكستان","SAU":"السعودية","IND":"الهند","BGD":"بنجلاديش","EGY":"مصر","YEM":"اليمن","SDN":"السودان"}
        return {"name":full_name,"passport":passport_no,"nationality":nationality,"nationality_ar":nat_map.get(nationality,nationality),"dob":dob_enjaz,"dob_iso":dob_iso,"exp":exp_enjaz,"exp_iso":exp_iso,"sex":sex,"l1":l1,"l2":l2}
    except:
        return None

def extract_mrz_from_image(pil_img):
    try:
        img = np.array(pil_img.convert('RGB'))
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        h,w = img.shape[:2]
        # قص أسفل 35% حيث يوجد MRZ
        roi = img[int(h*0.60):h, 0:w]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # OCR
        custom = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<'
        text = pytesseract.image_to_string(thresh, config=custom)
        text_clean = re.sub(r'[^A-Z0-9<\n]', '', text.upper())
        lines = [l for l in text_clean.split('\n') if len(l) >= 30 and '<' in l]
        # ابحث عن سطرين MRZ
        for i in range(len(lines)-1):
            l1 = lines[i].strip()
            l2 = lines[i+1].strip() if i+1 < len(lines) else ""
            if len(l1)>=40 and len(l2)>=40 and l1.startswith('P<'):
                parsed = parse_mrz_lines(l1,l2)
                if parsed and parsed['passport']:
                    return parsed, text, thresh
        # fallback: جرب كل النص
        all_text = re.sub(r'[^A-Z0-9<]', '', text.upper())
        if len(all_text)>=88:
            for j in range(len(all_text)-88):
                chunk = all_text[j:j+88]
                if 'P<' in chunk[:10]:
                    l1=chunk[:44]; l2=chunk[44:88]
                    parsed=parse_mrz_lines(l1,l2)
                    if parsed and len(parsed['passport'])>=6:
                        return parsed, text, thresh
        return None, text, thresh
    except Exception as e:
        return None, str(e), None

# رفع الصور مع قراءة أوتوماتيك
st.markdown("### 📸 ارفع صورة الجواز - القراءة التلقائية ستعمل مباشرة / Upload Passport - Auto Read")
uploaded = st.file_uploader("Upload", type=["jpg","jpeg","png"], accept_multiple_files=True, label_visibility="collapsed")

if uploaded:
    cols = st.columns(3)
    for idx, f in enumerate(uploaded):
        pil_img = Image.open(f)
        with cols[idx % 3]:
            st.image(pil_img, caption=f.name, use_container_width=True)
            with st.spinner("🤖 جاري قراءة MRZ..."):
                parsed, raw_text, _ = extract_mrz_from_image(pil_img)
                if parsed:
                    st.session_state.auto = parsed
                    st.success(f"✅ قراءة تلقائية: {parsed['passport']}")
                    st.code(f"{parsed['l1']}\n{parsed['l2']}")
                else:
                    st.warning("⚠️ لم أقرأ MRZ - جرب صورة أوضح أو الصق يدوياً")

st.markdown('<div class="mrz-box" style="margin-top:15px">', unsafe_allow_html=True)
st.markdown("**🤖 أو الصق MRZ يدوياً إذا الصورة غير واضحة / Or paste MRZ manually**")
mrz_manual = st.text_area("MRZ Manual", placeholder="P<PAKWAIL<<<<<<<<<<<<<<<<<<<<<<<<<<\nP12715484<0PAK7812138M3410104<<<<<<<<<<<<", height=80, label_visibility="collapsed")
if mrz_manual:
    lines = [re.sub(r'[^A-Z0-9<]', '', l.upper()) for l in mrz_manual.split('\n') if len(l.strip())>10]
    if len(lines)>=2:
        p = parse_mrz_lines(lines[-2], lines[-1])
        if p: st.session_state.auto = p
st.markdown('</div><br>', unsafe_allow_html=True)

auto = st.session_state.auto

c1,c2,c3,c4,c5,c6 = st.columns(6)
with c1: n = st.text_input("الاسم / Name", value=auto.get("name",""))
with c2: p = st.text_input("رقم الجواز / Passport", value=auto.get("passport",""))
with c3: nat = st.text_input("الجنسية / Nationality", value=auto.get("nationality",""))
with c4: d = st.text_input("الميلاد / DOB", value=auto.get("dob",""))
with c5: e = st.text_input("الانتهاء / Expiry", value=auto.get("exp",""))
with c6: s = st.text_input("الجنس / Sex", value=auto.get("sex",""))

colA,colB = st.columns([4,1])
with colA:
    if st.button("➕ إضافة / Add", use_container_width=True, type="primary"):
        if n or p:
            st.session_state.rows.append({"Name / الاسم":n,"Passport / الجواز":p,"Nationality / الجنسية":nat,"DOB / الميلاد":d,"DOB_ISO":auto.get("dob_iso",d),"Expiry / الانتهاء":e,"Expiry_ISO":auto.get("exp_iso",e),"Sex / الجنس":s,"Nationality_AR":auto.get("nationality_ar","")})
            st.toast(f"✅ {n} تمت الإضافة")
            st.session_state.auto = {}
            st.rerun()
with colB:
    st.metric("عدد الجوازات / Total", len(st.session_state.rows))

if st.session_state.rows:
    df_display = pd.DataFrame(st.session_state.rows)[["Name / الاسم","Passport / الجواز","Nationality / الجنسية","DOB / الميلاد","Expiry / الانتهاء","Sex / الجنس"]]
    st.dataframe(df_display, use_container_width=True, height=300)
    total=len(df_display)
    names_list="\n".join([f"{i+1}. {row['Name / الاسم']} - {row['Passport / الجواز']}" for i,row in df_display.iterrows()])
    wa_text=f"👑 TASHEER AI V2.5 AUTO\n📊 العدد: {total}\n\n{names_list}\n\n✅ قراءة تلقائية من الصورة\n📎 tasheer-ai-juub2hzyqf9boqzthpwv4n.streamlit.app"
    wa_link=f"https://wa.me/966540450738?text={urllib.parse.quote(wa_text)}"
    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.download_button("📥 Excel عادي", data=df_display.to_csv(index=False).encode('utf-8-sig'), file_name="TASHEER_V2.5_Normal.csv", mime="text/csv", use_container_width=True)
    with c2:
        df_iso=pd.DataFrame([{"Name":r["Name / الاسم"],"PassportNo":r["Passport / الجواز"],"Nationality":r["Nationality / الجنسية"],"DOB":r.get("DOB_ISO",r["DOB / الميلاد"]),"Expiry":r.get("Expiry_ISO",r["Expiry / الانتهاء"]),"Sex":r["Sex / الجنس"]} for r in st.session_state.rows])
        st.download_button("✅ Excel إنجاز", data=df_iso.to_csv(index=False).encode('utf-8-sig'), file_name="TASHEER_V2.5_Enjaz.csv", mime="text/csv", use_container_width=True, type="primary")
    with c3:
        st.link_button("💬 واتساب", wa_link, use_container_width=True)
    with c4:
        if st.button("🗑️ مسح الكل", use_container_width=True):
            st.session_state.rows=[]; st.session_state.auto={}; st.rerun()

st.markdown("<center style='color:#64748b; font-size:12px; margin-top:30px'>© 2026 TASHEER AI V2.5 AUTO OCR - +966 54 045 0738 - قراءة تلقائية من الصورة</center>", unsafe_allow_html=True)
