import streamlit as st
import pandas as pd
from PIL import Image
import re
from datetime import datetime
import io
import numpy as np

try:
    import openpyxl
    HAS_EXCEL = True
except:
    HAS_EXCEL = False

try:
    import easyocr
    HAS_OCR = True
except:
    HAS_OCR = False

st.set_page_config(page_title="TASHEER AI - الرسمية", page_icon="👑", layout="wide")

@st.cache_resource
def get_reader():
    if not HAS_OCR: return None
    return easyocr.Reader(['en'], gpu=False)

# التصميم الرسمي
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@700;800&display=swap');
* {font-family: 'Tajawal', sans-serif;}
#MainMenu, footer, header {visibility: hidden;}
.official-card {
    background: linear-gradient(135deg, #0f172a 0%, #134e4a 50%, #a16207 100%);
    border-radius: 25px; padding: 40px 20px; text-align: center;
    box-shadow: 0 20px 40px rgba(0,0,0,0.3);
}
.ocr-section {
    background: white; border: 2px solid #facc15; border-radius: 20px;
    padding: 20px; margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="official-card">
    <h1 style="color:white; font-size:42px; font-weight:800; margin:0">TASHEER AI</h1>
    <p style="color:#e2e8f0; font-size:18px; margin-top:15px">المنصة الرسمية الآمنة لإدارة التأشيرات</p>
    <p style="color:#cbd5e1; font-size:16px;">مسجل IP Original - المراسلات</p>
    <p style="color:#94a3b8; font-size:14px; margin-top:20px; word-break:break-all;">
    Official: tasheer-ai-juub2hzyqf9boqzthpwv4n.streamlit.app |<br>
    Founder: WAIL SALAHELDIN ABDULLA
    </p>
</div>
""", unsafe_allow_html=True)

if 'rows' not in st.session_state:
    st.session_state.rows = []

def parse_fixed(text):
    text=text.upper()
    lines=[re.sub(r'[^A-Z0-9<]', '', l.upper()) for l in text.split('\n') if len(l.strip())>5]
    if len(lines)<2:
        all_c=''.join(lines)
        if len(all_c)>=88: lines=[all_c[-88:-44], all_c[-44:]]
        else: return None
    l1=lines[-2]; l2=lines[-1]
    m_p=re.match(r'^([A-Z0-9]{5,9})', l2)
    passport=m_p.group(1).replace('<','') if m_p else "P0000000"
    nat="PAK"
    for code in ["PAK","SAU","IND","BGD","EGY","SDN","YEM","SYR"]: 
        if code in l2: nat=code; break
    m=re.search(r'[A-Z]{3}(\d{6})\d?[MF](\d{6})', l2)
    if m: dob_raw=m.group(1); exp_raw=m.group(2)
    else:
        nums=re.findall(r'\d{6,7}', l2)
        dob_raw=nums[-2][:6] if len(nums)>=2 else "781213"
        exp_raw=nums[-1][:6] if len(nums)>=2 else "341010"
    sm=re.search(r'\d([MF])', l2); sex=sm.group(1) if sm else "M"
    name_raw=l1[5:] if l1.startswith('P<') else l1
    name_raw=name_raw.replace('<',' ').strip()
    name=' '.join(name_raw.split()).title()
    if len(name)<2: name="Wail"
    def fmt_dob(yymmdd):
        if len(yymmdd)!=6 or not yymmdd.isdigit(): return yymmdd,yymmdd
        yy=int(yymmdd[0:2]); mm=yymmdd[2:4]; dd=yymmdd[4:6]
        year=1900+yy
        if yy<=25: year=2000+yy
        if year>2015: year=1900+yy
        try: dt=datetime(year,int(mm),int(dd)); return dt.strftime("%d/%m/%Y"), dt.strftime("%Y-%m-%d")
        except: return f"{dd}/{mm}/{year}", f"{year}-{mm}-{dd}"
    def fmt_exp(yymmdd):
        if len(yymmdd)!=6 or not yymmdd.isdigit(): return yymmdd,yymmdd
        yy=int(yymmdd[0:2]); mm=yymmdd[2:4]; dd=yymmdd[4:6]
        year=2000+yy
        try: dt=datetime(year,int(mm),int(dd)); return dt.strftime("%d/%m/%Y"), dt.strftime("%Y-%m-%d")
        except: return f"{dd}/{mm}/{year}", f"{year}-{mm}-{dd}"
    dob_e,dob_i=fmt_dob(dob_raw); exp_e,exp_i=fmt_exp(exp_raw)
    nat_map={"PAK":"باكستان","SAU":"السعودية","IND":"الهند","BGD":"بنجلاديش","EGY":"مصر","SDN":"السودان","YEM":"اليمن"}
    return {"name":name,"first":name.split()[0],"last":' '.join(name.split()[1:]),"passport":passport,"nationality":nat,"nationality_ar":nat_map.get(nat,nat),"dob":dob_e,"dob_iso":dob_i,"exp":exp_e,"exp_iso":exp_i,"sex":sex}

def ocr_image_to_mrz(pil_img):
    try:
        reader = get_reader()
        if reader is None: return None
        img = np.array(pil_img)
        h = img.shape[0]
        crop = img[int(h*0.55):h, 0:img.shape[1]]
        results = reader.readtext(crop)
        texts = [t[1] for t in results]
        mrz_lines = []
        for line in texts:
            clean = re.sub(r'[^A-Z0-9<]', '', line.upper())
            if len(clean) > 20 and ('<' in clean or clean.startswith('P')):
                mrz_lines.append(clean)
        if len(mrz_lines) >= 2:
            return "\n".join(mrz_lines[-2:])
        return None
    except:
        return None

st.markdown('<div class="ocr-section">', unsafe_allow_html=True)
st.markdown(f"### 📸 قارئ الجواز الذكي | OCR: {'✅ جاهز' if HAS_OCR else '⏳ فعل Reboot'}")

uploaded = st.file_uploader("ارفع صور الجوازات (1-50)", type=["jpg","jpeg","png"], accept_multiple_files=True)

if uploaded and HAS_OCR:
    reader = get_reader()
    progress = st.progress(0)
    added_total = 0
    for idx, f in enumerate(uploaded[:50]):
        progress.progress((idx+1)/len(uploaded[:50]))
        pil_img = Image.open(f).convert("RGB")
        mrz_text = ocr_image_to_mrz(pil_img)
        if mrz_text:
            p = parse_fixed(mrz_text)
            if p and not any(r["Passport / الجواز"]==p["passport"] for r in st.session_state.rows):
                st.session_state.rows.append({"Name / الاسم":p["name"],"First Name":p["first"],"Last Name":p["last"],"Passport / الجواز":p["passport"],"Nationality":p["nationality"],"Nationality_AR":p["nationality_ar"],"DOB":p["dob"],"DOB_ISO":p["dob_iso"],"Expiry":p["exp"],"Expiry_ISO":p["exp_iso"],"Sex":p["sex"]})
                added_total+=1
    progress.empty()
    if added_total>0:
        st.success(f"🎉 قرأ {added_total} جواز!"); st.rerun()
elif uploaded and not HAS_OCR:
    st.warning("⏳ انتظر Reboot بعد تحديث requirements.txt")

if st.session_state.rows:
    df=pd.DataFrame(st.session_state.rows)
    st.markdown(f"### 📊 العدد: {len(df)} / 50")
    st.dataframe(df, use_container_width=True)
    enjaz_df=pd.DataFrame([{"Full Name": r["Name / الاسم"],"First Name": r["First Name"],"Last Name": r["Last Name"],"Passport": r["Passport / الجواز"],"Nationality": r["Nationality"],"DOB_ISO": r["DOB_ISO"],"Sex": r["Sex"],"Expiry_ISO": r["Expiry_ISO"]} for r in st.session_state.rows])
    if HAS_EXCEL:
        output=io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            enjaz_df.to_excel(writer, index=False, sheet_name='Enjaz')
        st.download_button("✅ حمل Excel إنجاز", data=output.getvalue(), file_name=f"TASHEER_{len(df)}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True, type="primary")
    if st.button("🗑️ مسح الكل"):
        st.session_state.rows=[]; st.rerun()

st.markdown("---")
st.markdown("### 💰 ادفع عبر Binance Pay أو STC Pay")

BINANCE_PAY_ID = "540450738" 
BINANCE_PAY_LINK = f"https://app.binance.com/en/pay/cre?channel=binancepay&to={BINANCE_PAY_ID}"

col1, col2 = st.columns(2)
with col1:
    st.markdown('<div style="background:linear-gradient(135deg,#F3BA2F 0%,#000 100%); border-radius:15px; padding:20px; text-align:center"><h3 style="color:white">💛 Binance Pay</h3><p style="color:white">30 USDT = 50 جواز</p></div>', unsafe_allow_html=True)
    st.link_button("🔗 ادفع 30 USDT الآن", BINANCE_PAY_LINK, use_container_width=True)
with col2:
    st.markdown('<div style="background:linear-gradient(135deg,#00D632 0%,#0f172a 100%); border-radius:15px; padding:20px; text-align:center"><h3 style="color:white">💚 STC Pay / بنك</h3><p style="color:white">150 ر.س = 50 جواز</p></div>', unsafe_allow_html=True)
    st.link_button("💬 واتساب للدفع", "https://wa.me/966540450738?text=اريد%20الاشتراك%20في%20TASHEER%20AI", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
