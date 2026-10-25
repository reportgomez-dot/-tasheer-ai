import streamlit as st
import pandas as pd
from PIL import Image
import re, urllib.parse
from datetime import datetime
import io

# محاولة استيراد Excel - لو مو موجود يشتغل CSV
try:
    import openpyxl
    HAS_EXCEL = True
except:
    HAS_EXCEL = False

st.set_page_config(page_title="TASHEER AI V3.3 EXCEL", page_icon="👑", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@800&display=swap');
* {font-family: 'Tajawal', sans-serif;}
#MainMenu, footer, header {visibility: hidden;}
.main-header {background: linear-gradient(135deg, #0f172a 0%, #065f46 100%); border: 3px solid #facc15; border-radius: 20px; padding: 20px; text-align: center;}
.pricing-card {background: white; border-radius: 18px; padding: 16px; border: 2px solid #e5e7eb; text-align: center;}
.pricing-card.popular {border: 3px solid #facc15; background: linear-gradient(135deg, #fefce8 0%, #fef9c3 100%);}
.price {font-size: 30px; font-weight: 800;}
.btn-buy {background: #25D366; color: white !important; padding: 10px; border-radius: 10px; display: block; text-decoration: none; font-weight: 800; margin-top: 8px;}
.btn-buy.gold {background: linear-gradient(135deg, #facc15 0%, #eab308 100%); color: #000 !important;}
.whatsapp-float {position: fixed; bottom: 100px; right: 15px; z-index: 9999; background: #25D366; color: white !important; padding: 12px 20px; border-radius: 50px; text-decoration: none; font-weight: 800;}
</style>
<a href="https://wa.me/966540450738?text=V3.3%20EXCEL" target="_blank" class="whatsapp-float">💬 اشترك V3.3</a>
""", unsafe_allow_html=True)

st.markdown(f'<div class="main-header"><h1 style="color:#facc15">👑 TASHEER AI V3.3 - Excel + CSV</h1><p style="color:#e2e8f0">50 جواز 150 ر.س | 500 جواز 350 ر.س | Excel: {"✅ شغال" if HAS_EXCEL else "⏳ بيتفعل بعد Reboot"}</p></div><br>', unsafe_allow_html=True)

c1,c2,c3 = st.columns(3)
with c1: st.markdown('<div class="pricing-card"><h3>🎯 مجاني</h3><div class="price">0 ر.س</div><p>5 جوازات</p><a class="btn-buy" href="https://wa.me/966540450738?text=مجاني" target="_blank">جرب</a></div>', unsafe_allow_html=True)
with c2: st.markdown('<div class="pricing-card popular"><h3>🔥 50 جواز</h3><div class="price">150 ر.س</div><p>إنجاز + أبشر مقيم Excel</p><a class="btn-buy gold" href="https://wa.me/966540450738?text=50ب150" target="_blank">اشترك</a></div>', unsafe_allow_html=True)
with c3: st.markdown('<div class="pricing-card"><h3>👑 500 جواز</h3><div class="price">350 ر.س</div><p>للوكالات</p><a class="btn-buy" href="https://wa.me/966540450738?text=500ب350" target="_blank">اشترك</a></div>', unsafe_allow_html=True)

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
    passport=re.match(r'^([A-Z0-9]{5,9})', l2)
    passport=passport.group(1).replace('<','') if passport else "P0000000"
    nat="PAK"
    for code in ["PAK","SAU","IND","BGD","EGY"]: 
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
    nat_map={"PAK":"باكستان","SAU":"السعودية","IND":"الهند","BGD":"بنجلاديش","EGY":"مصر"}
    return {"name":name,"first":name.split()[0],"last":' '.join(name.split()[1:]),"passport":passport,"nationality":nat,"nationality_ar":nat_map.get(nat,nat),"dob":dob_e,"dob_iso":dob_i,"exp":exp_e,"exp_iso":exp_i,"sex":sex}

st.markdown("### 📋 الصق 50 جواز MRZ مرة وحدة")
bulk_text=st.text_area("Bulk", height=120, label_visibility="collapsed", placeholder="P<PAK...\nP127...")
if st.button("🔍 تحليل 50 جواز", type="primary", use_container_width=True):
    if bulk_text.strip():
        blocks=re.split(r'\n\s*\n', bulk_text.strip())
        added=0
        for block in blocks:
            if len(block.strip())<20: continue
            p=parse_fixed(block)
            if p and not any(r["Passport / الجواز"]==p["passport"] for r in st.session_state.rows):
                st.session_state.rows.append({"Name / الاسم":p["name"],"First Name":p["first"],"Last Name":p["last"],"Passport / الجواز":p["passport"],"Nationality":p["nationality"],"Nationality_AR":p["nationality_ar"],"DOB":p["dob"],"DOB_ISO":p["dob_iso"],"Expiry":p["exp"],"Expiry_ISO":p["exp_iso"],"Sex":p["sex"]})
                added+=1
        st.success(f"✅ تم {added}"); st.rerun()

st.markdown("### 📸 رفع 50 صورة")
uploaded=st.file_uploader("Upload", type=["jpg","jpeg","png"], accept_multiple_files=True, label_visibility="collapsed")
if uploaded:
    cols=st.columns(5)
    for i,f in enumerate(uploaded[:50]):
        with cols[i%5]: st.image(Image.open(f), use_container_width=True)

mrz_single=st.text_area("MRZ واحد", value="P<PAKWAIL<<<<<<<<<<\nP12715484<0PAK7812138M3410104", height=70)
auto=parse_fixed(mrz_single) if mrz_single else None

c1,c2,c3,c4,c5,c6=st.columns(6)
with c1: n=st.text_input("الاسم", value=auto["name"] if auto else "")
with c2: p=st.text_input("الجواز", value=auto["passport"] if auto else "")
with c3: nat=st.text_input("الجنسية", value=auto["nationality"] if auto else "")
with c4: d=st.text_input("الميلاد", value=auto["dob"] if auto else "")
with c5: e=st.text_input("الانتهاء", value=auto["exp"] if auto else "")
with c6: s=st.text_input("الجنس", value=auto["sex"] if auto else "")

if st.button("➕ إضافة", use_container_width=True, type="primary"):
    if p and not any(r["Passport / الجواز"]==p for r in st.session_state.rows):
        st.session_state.rows.append({"Name / الاسم":n,"First Name":n.split()[0],"Last Name":' '.join(n.split()[1:]),"Passport / الجواز":p,"Nationality":nat,"Nationality_AR":nat,"DOB":d,"DOB_ISO":auto["dob_iso"] if auto else d,"Expiry":e,"Expiry_ISO":auto["exp_iso"] if auto else e,"Sex":s})
        st.rerun()

if st.session_state.rows:
    df=pd.DataFrame(st.session_state.rows)
    st.markdown(f"### 📊 العدد: {len(df)} / 50")
    st.progress(min(len(df)/50,1.0))
    st.dataframe(df, use_container_width=True)

    enjaz_df=pd.DataFrame([{
        "Full Name": r.get("Name / الاسم",""),"First Name": r.get("First Name",""),"Last Name": r.get("Last Name",""),
        "Passport": r.get("Passport / الجواز",""),"Nationality": r.get("Nationality",""),
        "DOB_ISO": r.get("DOB_ISO",""),"DOB": r.get("DOB",""),"Sex": r.get("Sex",""),
        "Expiry_ISO": r.get("Expiry_ISO",""),"Expiry": r.get("Expiry",""),
    } for r in st.session_state.rows])

    absher_df=pd.DataFrame([{
        "الاسم الكامل": r.get("Name / الاسم",""),"رقم الجواز": r.get("Passport / الجواز",""),
        "الجنسية": r.get("Nationality_AR",""),"رمز الجنسية": r.get("Nationality",""),
        "تاريخ الميلاد YYYY-MM-DD": r.get("DOB_ISO",""),"الجنس": "ذكر" if r.get("Sex","M")=="M" else "أنثى",
        "تاريخ الانتهاء YYYY-MM-DD": r.get("Expiry_ISO",""),
    } for r in st.session_state.rows])

    wa_text=f"👑 TASHEER V3.3 - {len(df)} جواز\n"
    wa_link=f"https://wa.me/966540450738?text={urllib.parse.quote(wa_text)}"

    if HAS_EXCEL:
        output=io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            enjaz_df.to_excel(writer, index=False, sheet_name='Enjaz_Official')
            absher_df.to_excel(writer, index=False, sheet_name='Absher_Muqeem')
            df.to_excel(writer, index=False, sheet_name='All_Data')
        excel_data=output.getvalue()

        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.download_button("✅ إنجاز Excel", data=excel_data, file_name=f"Enjaz_Official_{len(df)}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True, type="primary")
        with col2:
            out2=io.BytesIO()
            with pd.ExcelWriter(out2, engine='openpyxl') as writer:
                absher_df.to_excel(writer, index=False, sheet_name='Absher_Muqeem')
            st.download_button("🟦 أبشر Excel", data=out2.getvalue(), file_name=f"Absher_Muqeem_{len(df)}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        with col3:
            st.download_button("📦 الكل Excel", data=excel_data, file_name=f"TASHEER_ALL_{len(df)}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        with col4:
            st.link_button("💬 واتساب", wa_link, use_container_width=True)
    else:
        st.warning("⏳ Excel بيتفعل بعد Reboot - حمل CSV الآن")
        col1,col2,col3=st.columns(3)
        with col1: st.download_button("✅ إنجاز CSV", data=enjaz_df.to_csv(index=False).encode('utf-8-sig'), file_name=f"Enjaz_{len(df)}.csv", mime="text/csv", use_container_width=True)
        with col2: st.download_button("🟦 أبشر CSV", data=absher_df.to_csv(index=False).encode('utf-8-sig'), file_name=f"Absher_{len(df)}.csv", mime="text/csv", use_container_width=True)
        with col3: st.link_button("💬 واتساب", wa_link, use_container_width=True)

    if st.button("🗑️ مسح الكل"):
        st.session_state.rows=[]; st.rerun()

    if len(df)>=50:
        st.balloons()
        st.success("🎉 50 جواز مكتمل - باقة 150 ر.س")

st.markdown("<center style='color:#64748b; font-size:11px; margin-top:20px'>© TASHEER AI V3.3 | Excel + CSV | 50=150 ر.س | 500=350 ر.س</center>", unsafe_allow_html=True)
