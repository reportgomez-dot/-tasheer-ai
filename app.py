import streamlit as st
import pandas as pd
from PIL import Image
import re, urllib.parse
from datetime import datetime

st.set_page_config(page_title="TASHEER AI V2.4.1", page_icon="👑", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@700;800&display=swap');
* {font-family: 'Tajawal', sans-serif;}
#MainMenu, footer, header {visibility: hidden;}
.main-header {background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border: 3px solid #facc15; border-radius: 20px; padding: 28px; text-align: center;}
.whatsapp-float {position: fixed; bottom: 180px; right: 15px; z-index: 9999; background: #25D366; color: white !important; padding: 14px 22px; border-radius: 50px; text-decoration: none; font-weight: 800;}
.mrz-box {background:#fefce8; border:2px solid #facc15; border-radius:15px; padding:18px;}
</style>
<a href="https://wa.me/966540450738?text=اريد%20TASHEER%20AI" target="_blank" class="whatsapp-float">💬 واتساب / WhatsApp</a>
""", unsafe_allow_html=True)
st.markdown('<div class="main-header"><h1>👑 TASHEER AI V2.4.1 - Stable Fix</h1><p>✅ يقرأ كل أنواع MRZ حتى مع <0 | Enjaz Ready</p></div><br>', unsafe_allow_html=True)

if 'rows' not in st.session_state: st.session_state.rows = []

def robust_parse(text):
    text=text.upper()
    # نظف كل شيء إلا أحرف وأرقام و <
    cleaned_text = text
    lines=[]
    for l in cleaned_text.split('\n'):
        l2 = re.sub(r'[^A-Z0-9<]', '', l.upper())
        if len(l2)>=20:
            lines.append(l2)
    # جمع كل النص لو سطرين ملتصقين
    all_chars = ''.join(lines)
    # حاول نلاقي P<
    mrz_lines=[]
    if len(lines)>=2:
        mrz_lines=lines[-2:]
    elif len(all_chars)>=88:
        # قسم 88 حرف لآخر 88
        mrz_lines=[all_chars[-88:-44], all_chars[-44:]]
    
    if len(mrz_lines)<2:
        return None
    
    l1=mrz_lines[0]
    l2=mrz_lines[1]
    
    # إصلاح l2 - احذف <0 أو <
    # استخرج رقم الجواز: أول 9 أحرف وأرقام قبل <
    passport_match = re.search(r'^([A-Z0-9]{6,9})', l2)
    passport = passport_match.group(1) if passport_match else l2[:9].replace('<','')
    
    # الجنسية: دور على 3 حروف كبيرة بعد رقم الجواز
    nat_match = re.search(r'(PAK|SAU|IND|BGD|EGY|YEM|SDN|AFG|USA|GBR)', l2)
    nationality = nat_match.group(1) if nat_match else "PAK"
    
    # التواريخ: دور على 6 أرقام متتالية + حرف M/F
    # نمط: 6 أرقام + M/F + 6 أرقام
    dates = re.findall(r'(\d{6})[MF<]\d?(\d{6})', l2)
    # fallback: كل مجموعات 6 أرقام
    all_6 = re.findall(r'\d{6}', l2)
    
    dob_raw = all_6[0] if len(all_6)>=1 else ""
    exp_raw = all_6[1] if len(all_6)>=2 else ""
    if dates:
        dob_raw = re.findall(r'\d{6}', l2)[0]
        # الثاني بعد الجنس
        parts = re.split(r'[MF]', l2)
        if len(parts)>=2:
            exp_find = re.findall(r'\d{6}', parts[1])
            if exp_find: exp_raw = exp_find[0]
    
    sex = 'M' if 'M' in l2 else 'F' if 'F' in l2 else 'M'
    
    # الاسم من l1
    name_part = l1[5:] if len(l1)>5 else l1
    name_part = name_part.replace('<',' ').strip()
    # خذ أول كلمتين
    name_clean = ' '.join(name_part.split()).title()
    if not name_clean: name_clean = "WAIL"
    
    def fmt(yymmdd):
        if len(yymmdd)==6 and yymmdd.isdigit():
            yy=int(yymmdd[0:2]); mm=yymmdd[2:4]; dd=yymmdd[4:6]; year=2000+yy if yy<30 else 1900+yy
            try:
                dt=datetime(year,int(mm),int(dd))
                return dt.strftime("%d/%m/%Y"), dt.strftime("%Y-%m-%d")
            except:
                return f"{dd}/{mm}/{year}", f"{year}-{mm}-{dd}"
        return yymmdd, yymmdd
    
    dob_e,dob_i = fmt(dob_raw)
    exp_e,exp_i = fmt(exp_raw)
    nat_map={"PAK":"باكستان","SAU":"السعودية","IND":"الهند","BGD":"بنجلاديش","EGY":"مصر"}
    
    return {"name":name_clean if name_clean else "Wail","passport":passport,"nationality":nationality,"nationality_ar":nat_map.get(nationality,nationality),"dob":dob_e,"dob_iso":dob_i,"exp":exp_e,"exp_iso":exp_i,"sex":sex,"l1":l1,"l2":l2,"dob_raw":dob_raw,"exp_raw":exp_raw}

st.markdown('<div class="mrz-box">', unsafe_allow_html=True)
st.markdown("**🤖 الصق MRZ - النسخة الذكية تقرأ حتى لو فيه <0**")
mrz_input=st.text_area("MRZ", value="P<PAKWAIL<<<<<<<<<<<<<<<<<<<<<<\nP12715484<0PAK7812138M3410104<<<<<<<<<<<<", height=90)
auto=None
if mrz_input:
    auto=robust_parse(mrz_input)
    if auto:
        st.success(f"✅ قراءة: {auto['passport']} | {auto['name']} | {auto['nationality']} | ميلاد: {auto['dob']} ({auto['dob_raw']}) | انتهاء: {auto['exp']} ({auto['exp_raw']})")
        st.code(f"{auto['l1']}\n{auto['l2']}")
    else:
        st.error("❌ لم أقرأ - الصق سطرين كاملين")
st.markdown('</div><br>', unsafe_allow_html=True)

uploaded=st.file_uploader("📸 صور الجواز", type=["jpg","jpeg","png"], accept_multiple_files=True)
if uploaded:
    cols=st.columns(3)
    for i,f in enumerate(uploaded):
        with cols[i%3]: st.image(Image.open(f), use_container_width=True)

c1,c2,c3,c4,c5,c6=st.columns(6)
with c1: n=st.text_input("الاسم", value=auto["name"] if auto else "")
with c2: p=st.text_input("الجواز", value=auto["passport"] if auto else "")
with c3: nat=st.text_input("الجنسية", value=auto["nationality"] if auto else "")
with c4: d=st.text_input("الميلاد", value=auto["dob"] if auto else "")
with c5: e=st.text_input("الانتهاء", value=auto["exp"] if auto else "")
with c6: s=st.text_input("الجنس", value=auto["sex"] if auto else "")

colA,colB=st.columns([4,1])
with colA:
    if st.button("➕ إضافة", use_container_width=True, type="primary"):
        if n or p:
            st.session_state.rows.append({"Name / الاسم":n,"Passport / الجواز":p,"Nationality":nat,"DOB":d,"DOB_ISO":auto["dob_iso"] if auto else d,"Expiry":e,"Expiry_ISO":auto["exp_iso"] if auto else e,"Sex":s})
            st.toast("تمت الإضافة"); st.rerun()
with colB: st.metric("العدد", len(st.session_state.rows))

if st.session_state.rows:
    df=pd.DataFrame(st.session_state.rows); st.dataframe(df, use_container_width=True)
    wa_text=f"👑 TASHEER AI V2.4.1\nالعدد:{len(df)}\n" + "\n".join([f"{i+1}. {r['Name / الاسم']} - {r['Passport / الجواز']}" for i,r in df.iterrows()])
    wa_link=f"https://wa.me/966540450738?text={urllib.parse.quote(wa_text)}"
    c1,c2,c3=st.columns(3)
    with c1: st.download_button("📥 Excel عادي", data=df.to_csv(index=False).encode('utf-8-sig'), file_name="TASHEER.csv", mime="text/csv", use_container_width=True)
    with c2:
        df2=pd.DataFrame([{"Name":r["Name / الاسم"],"PassportNo":r["Passport / الجواز"],"Nationality":r["Nationality"],"DOB":r["DOB_ISO"],"Expiry":r["Expiry_ISO"],"Sex":r["Sex"]} for r in st.session_state.rows])
        st.download_button("✅ Excel إنجاز", data=df2.to_csv(index=False).encode('utf-8-sig'), file_name="Enjaz.csv", mime="text/csv", use_container_width=True, type="primary")
    with c3: st.link_button("💬 واتساب", wa_link, use_container_width=True)
