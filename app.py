import streamlit as st
import pandas as pd
from PIL import Image, ImageOps, ImageEnhance
import re, urllib.parse
from datetime import datetime
import pytesseract

st.set_page_config(page_title="TASHEER AI V2.5.1 AUTO", page_icon="👑", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@700;800&display=swap');
* {font-family: 'Tajawal', sans-serif;}
#MainMenu, footer, header {visibility: hidden;}
.main-header {background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); border: 3px solid #facc15; border-radius: 20px; padding: 28px; text-align: center;}
.main-header h1 {color: #facc15; font-size: 30px; margin: 0;}
.auto-badge {background:linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color:white; padding:8px 15px; border-radius:20px; font-weight:800;}
.whatsapp-float {position: fixed; bottom: 180px; right: 15px; z-index: 9999; background: #25D366; color: white !important; padding: 14px 22px; border-radius: 50px; text-decoration: none; font-weight: 800;}
.mrz-box {background:#fefce8; border:2px solid #facc15; border-radius:15px; padding:18px;}
</style>
<a href="https://wa.me/966540450738?text=اريد%20V2.5.1" target="_blank" class="whatsapp-float">💬 واتساب / WhatsApp</a>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>👑 TASHEER AI V2.5.1 - قراءة تلقائية بدون أخطاء</h1><p>AUTO MRZ FROM IMAGE - No cv2 - Works 100%</p><p><span class="auto-badge">🤖 AUTO OCR V2.5.1</span> <span style="color:#facc15; margin-left:10px">⭐ 966540450738 ⭐</span></p></div><br>', unsafe_allow_html=True)

if 'rows' not in st.session_state: st.session_state.rows = []
if 'auto' not in st.session_state: st.session_state.auto = {}

def parse_mrz(l1,l2):
    try:
        name_raw=l1[5:] if len(l1)>5 else ""; parts=name_raw.split('<<')
        surname=parts[0].replace('<',' ').strip() if parts else ""; given=parts[1].replace('<',' ').strip() if len(parts)>1 else ""
        full=' '.join(f"{given} {surname}".split()).title()
        pp=l2[0:9].replace('<','').strip(); nat=l2[10:13].replace('<','').strip() if len(l2)>=13 else "PAK"
        dob_raw=l2[13:19] if len(l2)>=19 else ""; sex=l2[20] if len(l2)>=21 else "M"; exp_raw=l2[21:27] if len(l2)>=27 else ""
        def fmt(yymmdd):
            if len(yymmdd)==6 and yymmdd.isdigit():
                yy=int(yymmdd[0:2]); mm=yymmdd[2:4]; dd=yymmdd[4:6]; year=2000+yy if yy<30 else 1900+yy
                try: dt=datetime(year,int(mm),int(dd)); return dt.strftime("%d/%m/%Y"), dt.strftime("%Y-%m-%d")
                except: return f"{dd}/{mm}/{year}", f"{year}-{mm}-{dd}"
            return yymmdd,yymmdd
        dob_e,dob_i=fmt(dob_raw); exp_e,exp_i=fmt(exp_raw)
        m={"PAK":"باكستان","SAU":"السعودية","IND":"الهند","BGD":"بنجلاديش","EGY":"مصر"}
        return {"name":full,"passport":pp,"nationality":nat,"nationality_ar":m.get(nat,nat),"dob":dob_e,"dob_iso":dob_i,"exp":exp_e,"exp_iso":exp_i,"sex":sex,"l1":l1,"l2":l2}
    except: return None

def ocr_image(pil_img):
    try:
        w,h=pil_img.size
        # قص 40% السفلي
        box=(0,int(h*0.60),w,h)
        roi=pil_img.crop(box)
        # تكبير وتحسين
        roi=roi.resize((roi.width*3, roi.height*3), Image.LANCZOS)
        roi=ImageOps.grayscale(roi)
        roi=ImageEnhance.Contrast(roi).enhance(2.5)
        roi=ImageEnhance.Brightness(roi).enhance(1.2)
        config=r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<'
        text=pytesseract.image_to_string(roi, config=config)
        clean=re.sub(r'[^A-Z0-9<\n]', '', text.upper())
        lines=[l for l in clean.split('\n') if len(l)>=30 and '<' in l]
        for i in range(len(lines)-1):
            l1=lines[i].strip(); l2=lines[i+1].strip() if i+1<len(lines) else ""
            if len(l1)>=40 and len(l2)>=40 and l1.startswith('P<'):
                p=parse_mrz(l1,l2)
                if p and p['passport']: return p, text
        # fallback
        allc=re.sub(r'[^A-Z0-9<]', '', text.upper())
        if len(allc)>=88:
            for j in range(len(allc)-88):
                chunk=allc[j:j+88]
                if 'P<' in chunk[:10]:
                    p=parse_mrz(chunk[:44], chunk[44:88])
                    if p and len(p['passport'])>=6: return p, text
        return None, text
    except Exception as e:
        return None, str(e)

st.markdown("### 📸 ارفع صورة الجواز - سيقرأ MRZ تلقائياً")
uploaded=st.file_uploader("Upload", type=["jpg","jpeg","png"], accept_multiple_files=True, label_visibility="collapsed")

if uploaded:
    cols=st.columns(3)
    for idx,f in enumerate(uploaded):
        pil=Image.open(f)
        with cols[idx%3]:
            st.image(pil, caption=f.name, use_container_width=True)
            with st.spinner("🤖 يقرأ..."):
                parsed, raw = ocr_image(pil)
                if parsed:
                    st.session_state.auto=parsed
                    st.success(f"✅ {parsed['passport']} - {parsed['name']}")
                    st.code(f"{parsed['l1']}\n{parsed['l2']}")
                else:
                    st.warning("⚠️ الصورة غير واضحة - الصق MRZ يدوياً")

st.markdown('<div class="mrz-box" style="margin-top:15px">', unsafe_allow_html=True)
st.markdown("**أو الصق MRZ يدوياً / Or paste manually**")
mrz_manual=st.text_area("MRZ", placeholder="P<PAKWAIL<<<<<<<<<<<<\nP12715484<0PAK7812138M3410104<<<<", height=70, label_visibility="collapsed")
if mrz_manual:
    ls=[re.sub(r'[^A-Z0-9<]', '', l.upper()) for l in mrz_manual.split('\n') if len(l.strip())>10]
    if len(ls)>=2:
        p=parse_mrz(ls[-2], ls[-1])
        if p: st.session_state.auto=p
st.markdown('</div><br>', unsafe_allow_html=True)

auto=st.session_state.auto
c1,c2,c3,c4,c5,c6=st.columns(6)
with c1: n=st.text_input("الاسم / Name", value=auto.get("name",""))
with c2: p=st.text_input("الجواز / Passport", value=auto.get("passport",""))
with c3: nat=st.text_input("الجنسية", value=auto.get("nationality",""))
with c4: d=st.text_input("الميلاد", value=auto.get("dob",""))
with c5: e=st.text_input("الانتهاء", value=auto.get("exp",""))
with c6: s=st.text_input("الجنس", value=auto.get("sex",""))

colA,colB=st.columns([4,1])
with colA:
    if st.button("➕ إضافة", use_container_width=True, type="primary"):
        if n or p:
            st.session_state.rows.append({"Name":n,"Passport":p,"Nat":nat,"DOB":d,"DOB_ISO":auto.get("dob_iso",d),"Exp":e,"Exp_ISO":auto.get("exp_iso",e),"Sex":s})
            st.toast("تمت الإضافة"); st.session_state.auto={}; st.rerun()
with colB: st.metric("العدد", len(st.session_state.rows))

if st.session_state.rows:
    df=pd.DataFrame(st.session_state.rows)
    st.dataframe(df[["Name","Passport","Nat","DOB","Exp","Sex"]], use_container_width=True)
    total=len(df)
    names="\n".join([f"{i+1}. {r['Name']} - {r['Passport']}" for i,r in df.iterrows()])
    wa=f"👑 TASHEER V2.5.1 AUTO\nالعدد:{total}\n{names}\n\ntasheer-ai-juub2hzyqf9boqzthpwv4n.streamlit.app"
    link=f"https://wa.me/966540450738?text={urllib.parse.quote(wa)}"
    c1,c2,c3,c4=st.columns(4)
    with c1: st.download_button("📥 عادي", data=df[["Name","Passport","Nat","DOB","Exp","Sex"]].to_csv(index=False).encode('utf-8-sig'), file_name="TASHEER_V2.5.1.csv", mime="text/csv", use_container_width=True)
    with c2:
        df2=pd.DataFrame([{"Name":r["Name"],"PassportNo":r["Passport"],"Nationality":r["Nat"],"DOB":r.get("DOB_ISO",r["DOB"]),"Expiry":r.get("Exp_ISO",r["Exp"]),"Sex":r["Sex"]} for r in st.session_state.rows])
        st.download_button("✅ إنجاز", data=df2.to_csv(index=False).encode('utf-8-sig'), file_name="TASHEER_Enjaz.csv", mime="text/csv", use_container_width=True, type="primary")
    with c3: st.link_button("💬 واتساب", link, use_container_width=True)
    with c4:
        if st.button("🗑️ مسح"): st.session_state.rows=[]; st.session_state.auto={}; st.rerun()
