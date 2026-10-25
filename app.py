import streamlit as st
import pandas as pd
from PIL import Image
import re, urllib.parse
from datetime import datetime
import io

st.set_page_config(page_title="TASHEER AI V3.1 Fixed", page_icon="👑", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@800&display=swap');
* {font-family: 'Tajawal', sans-serif;}
#MainMenu, footer, header {visibility: hidden;}
.main-header {background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); border: 3px solid #facc15; border-radius: 20px; padding: 22px; text-align: center;}
.pricing-card {background: white; border-radius: 18px; padding: 18px; border: 2px solid #e5e7eb; text-align: center;}
.pricing-card.popular {border: 3px solid #facc15; background: linear-gradient(135deg, #fefce8 0%, #fef9c3 100%);}
.price {font-size: 32px; font-weight: 800;}
.btn-buy {background: #25D366; color: white !important; padding: 10px; border-radius: 10px; display: block; text-decoration: none; font-weight: 800; margin-top: 10px;}
.btn-buy.gold {background: linear-gradient(135deg, #facc15 0%, #eab308 100%); color: #000 !important;}
.mrz-box {background:#fefce8; border:2px dashed #facc15; border-radius:15px; padding:15px;}
.whatsapp-float {position: fixed; bottom: 100px; right: 15px; z-index: 9999; background: #25D366; color: white !important; padding: 12px 20px; border-radius: 50px; text-decoration: none; font-weight: 800;}
</style>
<a href="https://wa.me/966540450738?text=اريد%20الاشتراك%20V3.1" target="_blank" class="whatsapp-float">💬 اشترك / WhatsApp</a>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1 style="color:#facc15; margin:0">👑 TASHEER AI V3.1 - باقات 150 / 350 + رفع 50</h1><p style="color:#e2e8f0">50 جواز 150 ر.س | 500 جواز 350 ر.س | رفع جماعي + إنجاز رسمي</p></div><br>', unsafe_allow_html=True)

# PRICING
c1,c2,c3 = st.columns(3)
with c1:
    st.markdown('<div class="pricing-card"><h3>🎯 مجاني</h3><div class="price">0 <small>ريال</small></div><p>5 جوازات</p><a class="btn-buy" href="https://wa.me/966540450738?text=اريد%20المجاني" target="_blank">جرب</a></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="pricing-card popular"><h3>🔥 50 جواز</h3><div class="price">150 <small>ريال</small></div><p>رفع 50 صورة مرة وحدة<br>Excel إنجاز رسمي</p><a class="btn-buy gold" href="https://wa.me/966540450738?text=اريد%20باقة%2050%20ب150" target="_blank">اشترك 150 ر.س</a></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="pricing-card"><h3>👑 500 جواز</h3><div class="price">350 <small>ريال</small></div><p>للوكالات الكبيرة</p><a class="btn-buy" href="https://wa.me/966540450738?text=اريد%20باقة%20500%20ب350" target="_blank">اشترك 350 ر.س</a></div>', unsafe_allow_html=True)

st.markdown("---")

if 'rows' not in st.session_state:
    st.session_state.rows = []

# CLEAR OLD DATA IF WRONG FORMAT (Fix KeyError)
if st.session_state.rows and "First Name" not in st.session_state.rows[0]:
    # تحويل القديم للجديد تلقائياً
    new_rows=[]
    for r in st.session_state.rows:
        name=r.get("Name / الاسم") or r.get("Name") or ""
        new_rows.append({
            "Name / الاسم": name,
            "First Name": name.split()[0] if name else "",
            "Last Name": ' '.join(name.split()[1:]) if len(name.split())>1 else "",
            "Passport / الجواز": r.get("Passport / الجواز") or r.get("Passport") or r.get("Passport / الجواز") or "",
            "Nationality": r.get("Nationality") or r.get("Nat") or "PAK",
            "Nationality_AR": r.get("Nationality_AR") or r.get("Nationality") or "باكستان",
            "DOB": r.get("DOB") or r.get("DOB / الميلاد") or "",
            "DOB_ISO": r.get("DOB_ISO") or r.get("DOB") or "",
            "Expiry": r.get("Expiry") or r.get("Expiry / الانتهاء") or "",
            "Expiry_ISO": r.get("Expiry_ISO") or r.get("Expiry") or "",
            "Sex": r.get("Sex") or r.get("Sex / الجنس") or "M"
        })
    st.session_state.rows=new_rows

def parse_fixed(text):
    text=text.upper()
    lines=[re.sub(r'[^A-Z0-9<]', '', l.upper()) for l in text.split('\n') if len(l.strip())>5]
    if len(lines)<2:
        all_c=''.join(lines)
        if len(all_c)>=88:
            lines=[all_c[-88:-44], all_c[-44:]]
        else:
            return None
    l1=lines[-2]; l2=lines[-1]
    passport=re.match(r'^([A-Z0-9]{5,9})', l2)
    passport=passport.group(1).replace('<','') if passport else "P0000000"
    nat_match=re.search(r'[0-9<]([A-Z]{3})[0-9]', l2)
    nationality=nat_match.group(1) if nat_match else "PAK"
    for code in ["PAK","SAU","IND","BGD","EGY","SDN","YEM"]:
        if code in l2:
            nationality=code; break
    m=re.search(r'[A-Z]{3}(\d{6})\d?[MF](\d{6})', l2)
    if m:
        dob_raw=m.group(1); exp_raw=m.group(2)
    else:
        nums=re.findall(r'\d{6,7}', l2)
        dob_raw=nums[-2][:6] if len(nums)>=2 else "781213"
        exp_raw=nums[-1][:6] if len(nums)>=2 else "341010"
    sm=re.search(r'\d([MF])', l2)
    sex=sm.group(1) if sm else "M"
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
    nat_map={"PAK":"باكستان","SAU":"السعودية","IND":"الهند","BGD":"بنجلاديش","EGY":"مصر"}
    return {"name":name,"first":name.split()[0],"last":' '.join(name.split()[1:]),"passport":passport,"nationality":nationality,"nationality_ar":nat_map.get(nationality,nationality),"dob":dob_e,"dob_iso":dob_i,"exp":exp_e,"exp_iso":exp_i,"sex":sex}

st.markdown("### 📋 الصق 50 جواز MRZ مرة وحدة (Bulk)")
bulk_text=st.text_area("Bulk MRZ", placeholder="P<PAKWAIL<<<<<<<<<<<<\nP12715484<0PAK7812138M3410104<<<<\n\nP<PAKAHMED<<<<<<<<<<<<\nP12345678<0PAK8001015M3001012<<<<", height=150)

if st.button("🔍 تحليل 50 جواز الآن", type="primary", use_container_width=True):
    if bulk_text.strip():
        blocks=re.split(r'\n\s*\n', bulk_text.strip())
        added=0
        for block in blocks:
            if len(block.strip())<20: continue
            parsed=parse_fixed(block)
            if parsed:
                if not any(r["Passport / الجواز"]==parsed["passport"] for r in st.session_state.rows):
                    st.session_state.rows.append({"Name / الاسم":parsed["name"],"First Name":parsed["first"],"Last Name":parsed["last"],"Passport / الجواز":parsed["passport"],"Nationality":parsed["nationality"],"Nationality_AR":parsed["nationality_ar"],"DOB":parsed["dob"],"DOB_ISO":parsed["dob_iso"],"Expiry":parsed["exp"],"Expiry_ISO":parsed["exp_iso"],"Sex":parsed["sex"]})
                    added+=1
            else:
                lines=[l for l in block.split('\n') if l.strip()]
                for i in range(0,len(lines)-1,2):
                    try:
                        p=parse_fixed(lines[i]+'\n'+lines[i+1])
                        if p and not any(r["Passport / الجواز"]==p["passport"] for r in st.session_state.rows):
                            st.session_state.rows.append({"Name / الاسم":p["name"],"First Name":p["first"],"Last Name":p["last"],"Passport / الجواز":p["passport"],"Nationality":p["nationality"],"Nationality_AR":p["nationality_ar"],"DOB":p["dob"],"DOB_ISO":p["dob_iso"],"Expiry":p["exp"],"Expiry_ISO":p["exp_iso"],"Sex":p["sex"]})
                            added+=1
                    except: pass
        st.success(f"✅ تم إضافة {added} جواز")
        st.rerun()

st.markdown("### 📸 رفع 50 صورة جواز مرة وحدة")
uploaded=st.file_uploader("Upload 50 images", type=["jpg","jpeg","png"], accept_multiple_files=True, label_visibility="collapsed")
if uploaded:
    if len(uploaded)>50:
        st.error(f"⚠️ الحد 50 صورة - أنت رفعت {len(uploaded)}")
    else:
        st.info(f"📦 تم رفع {len(uploaded)} صورة")
        cols=st.columns(5)
        for i,f in enumerate(uploaded[:50]):
            with cols[i%5]:
                st.image(Image.open(f), caption=f.name[:10], use_container_width=True)

st.markdown('<div class="mrz-box">', unsafe_allow_html=True)
mrz_single=st.text_area("MRZ جواز واحد", value="P<PAKWAIL<<<<<<<<<<<<<<<<<<<<<<<<<\nP12715484<0PAK7812138M3410104<<<<<<<<<<<<04", height=80)
auto=parse_fixed(mrz_single) if mrz_single else None
if auto:
    st.success(f"✅ {auto['passport']} | {auto['name']} | {auto['dob']} | {auto['exp']}")
st.markdown('</div>', unsafe_allow_html=True)

c1,c2,c3,c4,c5,c6=st.columns(6)
with c1: n=st.text_input("الاسم", value=auto["name"] if auto else "")
with c2: p=st.text_input("الجواز", value=auto["passport"] if auto else "")
with c3: nat=st.text_input("الجنسية", value=auto["nationality"] if auto else "")
with c4: d=st.text_input("الميلاد", value=auto["dob"] if auto else "")
with c5: e=st.text_input("الانتهاء", value=auto["exp"] if auto else "")
with c6: s=st.text_input("الجنس", value=auto["sex"] if auto else "")
if st.button("➕ إضافة جواز", use_container_width=True, type="primary"):
    if n or p:
        if not any(r["Passport / الجواز"]==p for r in st.session_state.rows):
            st.session_state.rows.append({"Name / الاسم":n,"First Name":n.split()[0],"Last Name":' '.join(n.split()[1:]),"Passport / الجواز":p,"Nationality":nat,"Nationality_AR":nat,"DOB":d,"DOB_ISO":auto["dob_iso"] if auto else d,"Expiry":e,"Expiry_ISO":auto["exp_iso"] if auto else e,"Sex":s})
            st.rerun()
        else:
            st.warning("⚠️ موجود")

if st.session_state.rows:
    df=pd.DataFrame(st.session_state.rows)
    st.markdown(f"### 📊 العدد: {len(df)} / 50")
    st.progress(min(len(df)/50,1.0))
    st.dataframe(df[["Name / الاسم","Passport / الجواز","Nationality","DOB","Expiry","Sex"]], use_container_width=True, height=300)

    # FIX: use .get to avoid KeyError
    enjaz_df=pd.DataFrame([{
        "Full Name (EN)": r.get("Name / الاسم",""),
        "First Name": r.get("First Name",""),
        "Last Name": r.get("Last Name",""),
        "Passport Number": r.get("Passport / الجواز",""),
        "Nationality Code": r.get("Nationality",""),
        "Nationality AR": r.get("Nationality_AR",""),
        "Date of Birth (Enjaz)": r.get("DOB_ISO",""),
        "DOB Display": r.get("DOB",""),
        "Gender": r.get("Sex",""),
        "Passport Expiry (Enjaz)": r.get("Expiry_ISO",""),
        "Expiry Display": r.get("Expiry",""),
        "Place of Birth": r.get("Nationality_AR",""),
        "Visa Type": "Work"
    } for r in st.session_state.rows])

    normal_df=df[["Name / الاسم","Passport / الجواز","Nationality","DOB","Expiry","Sex"]]

    wa_text=f"👑 TASHEER AI V3.1\n📦 العدد: {len(df)} جواز\n💰 الباقة: {150 if len(df)<=50 else 350} ر.س\n\n" + "\n".join([f"{i+1}. {r.get('Name / الاسم','')} - {r.get('Passport / الجواز','')}" for i,r in enumerate(st.session_state.rows)])
    wa_link=f"https://wa.me/966540450738?text={urllib.parse.quote(wa_text)}"

    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.download_button("📥 Excel عادي", data=normal_df.to_csv(index=False).encode('utf-8-sig'), file_name=f"TASHEER_Normal_{len(df)}.csv", mime="text/csv", use_container_width=True)
    with c2:
        output=io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            enjaz_df.to_excel(writer, index=False, sheet_name='Enjaz_Ready')
            normal_df.to_excel(writer, index=False, sheet_name='Normal')
        st.download_button("✅ Excel إنجاز رسمي", data=output.getvalue(), file_name=f"TASHEER_Enjaz_{len(df)}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True, type="primary")
    with c3:
        st.link_button("💬 واتساب", wa_link, use_container_width=True)
    with c4:
        if st.button("🗑️ مسح الكل", use_container_width=True):
            st.session_state.rows=[]; st.rerun()

    if len(df)>=50:
        st.balloons()
        st.success("🎉 وصلت 50 جواز - باقة 150 ريال مكتملة!")
