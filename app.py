import streamlit as st
import pandas as pd
from PIL import Image
import re, urllib.parse
from datetime import datetime

st.set_page_config(page_title="TASHEER AI V2.4 Enjaz", page_icon="👑", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@700;800&display=swap');
* {font-family: 'Tajawal', sans-serif;}
#MainMenu, footer, header {visibility: hidden;}
.main-header {background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border: 3px solid #facc15; border-radius: 20px; padding: 28px; text-align: center;}
.main-header h1 {color: #facc15; font-size: 32px; margin: 0;}
.main-header p {color: #e2e8f0; font-size: 15px; margin-top: 10px;}
.whatsapp-float {position: fixed; bottom: 180px; right: 15px; z-index: 9999; background: #25D366; color: white !important; padding: 14px 22px; border-radius: 50px; text-decoration: none; font-weight: 800; box-shadow: 0 6px 20px rgba(37,211,102,0.5);}
.mrz-box {background:linear-gradient(135deg, #fefce8 0%, #fef9c3 100%); border:2px solid #facc15; border-radius:15px; padding:18px; box-shadow: 0 4px 15px rgba(250,204,21,0.2);}
.enjaz-badge {background:#dcfce7; border:1px solid #22c55e; color:#15803d; padding:6px 12px; border-radius:20px; font-size:12px; font-weight:700;}
</style>
<a href="https://wa.me/966540450738?text=السلام%20عليكم%20اريد%20TASHEER%20AI%20V2.4" target="_blank" class="whatsapp-float">💬 تواصل واتساب / WhatsApp</a>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>👑 TASHEER AI V2.4 - جاهز لمنصة إنجاز</h1><p>قراءة MRZ + الجنسية + تنسيق إنجاز + إرسال واتساب | Enjaz Ready Format</p><p><span class="enjaz-badge">✅ متوافق مع إنجاز ENJAZ</span> <span style="color:#facc15; font-size:13px; margin-left:10px">⭐ V2.4 - 966540450738 ⭐</span></p></div><br>', unsafe_allow_html=True)

if 'rows' not in st.session_state:
    st.session_state.rows = []

def parse_mrz_v24(text):
    text = text.upper().strip()
    lines = [re.sub(r'[^A-Z0-9<]', '', l.upper()) for l in text.replace(' ','').split('\n') if l.strip()]
    lines = [l for l in lines if len(l) >= 30]
    if len(lines) < 2 and len(text) > 80:
        cleaned = re.sub(r'[^A-Z0-9<]', '', text.upper())
        if len(cleaned) >= 88:
            lines = [cleaned[:44], cleaned[44:88]]
    if len(lines) >= 2:
        l1, l2 = lines[-2], lines[-1]
        try:
            # اسم
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
            
            def fmt_enjaz(yymmdd):
                if len(yymmdd)==6 and yymmdd.isdigit():
                    yy = int(yymmdd[0:2]); mm = yymmdd[2:4]; dd = yymmdd[4:6]
                    year = 2000+yy if yy < 30 else 1900+yy
                    try:
                        dt = datetime(year, int(mm), int(dd))
                        return dt.strftime("%d/%m/%Y"), dt.strftime("%Y-%m-%d")
                    except:
                        return f"{dd}/{mm}/{year}", f"{year}-{mm}-{dd}"
                return yymmdd, yymmdd

            dob_enjaz, dob_iso = fmt_enjaz(dob_raw)
            exp_enjaz, exp_iso = fmt_enjaz(exp_raw)
            
            # خريطة جنسيات
            nat_map = {"PAK":"باكستان","SAU":"السعودية","IND":"الهند","BGD":"بنجلاديش","EGY":"مصر","YEM":"اليمن","SDN":"السودان"}
            nat_ar = nat_map.get(nationality, nationality)
            
            return {"name": full_name, "passport": passport_no, "nationality": nationality, "nationality_ar": nat_ar, "dob": dob_enjaz, "dob_iso": dob_iso, "exp": exp_enjaz, "exp_iso": exp_iso, "sex": sex, "l1": l1, "l2": l2, "dob_raw": dob_raw, "exp_raw": exp_raw}
        except Exception as e:
            return {"error": str(e)}
    return None

# MRZ BOX
st.markdown('<div class="mrz-box">', unsafe_allow_html=True)
st.markdown("**🤖 الصق سطرين MRZ هنا - سيتم قراءة الجنسية والتاريخ تلقائياً بصيغة إنجاز**")
mrz_input = st.text_area("MRZ V2.4", placeholder="P<PAKWAIL<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<\nP12715484<0PAK7812138M3410104<<<<<<<<<<<<<<<04", height=95, label_visibility="collapsed")
auto = {}
if mrz_input:
    auto = parse_mrz_v24(mrz_input)
    if auto and "name" in auto:
        st.success(f"✅ {auto['passport']} | {auto['name']} | {auto['nationality_ar']} ({auto['nationality']}) | ميلاد: {auto['dob']} | انتهاء: {auto['exp']} | الجنس: {auto['sex']}")
        st.code(f"{auto['l1']}\n{auto['l2']}")
    elif auto and "error" in auto:
        st.error(f"خطأ: {auto['error']}")
    else:
        st.warning("⚠️ الصق سطرين MRZ كاملين بدون مسافات")
st.markdown('</div><br>', unsafe_allow_html=True)

uploaded = st.file_uploader("📸 اختر صور الجواز / Upload Passport Images", type=["jpg","jpeg","png"], accept_multiple_files=True)
if uploaded:
    cols = st.columns(4)
    for i, f in enumerate(uploaded):
        with cols[i % 4]:
            st.image(Image.open(f), caption=f.name, use_container_width=True)

# حقول - 6 حقول الآن
c1, c2, c3, c4, c5, c6 = st.columns(6)
with c1: n = st.text_input("الاسم / Name", value=auto.get("name","") if auto else "")
with c2: p = st.text_input("رقم الجواز / Passport", value=auto.get("passport","") if auto else "")
with c3: nat = st.text_input("الجنسية / Nationality", value=auto.get("nationality","") if auto else "")
with c4: d = st.text_input("الميلاد / DOB", value=auto.get("dob","") if auto else "", help="صيغة إنجاز: يوم/شهر/سنة")
with c5: e = st.text_input("الانتهاء / Expiry", value=auto.get("exp","") if auto else "")
with c6: s = st.text_input("الجنس / Sex", value=auto.get("sex","") if auto else "", max_chars=1)

colA, colB = st.columns([4,1])
with colA:
    if st.button("➕ إضافة / Add", use_container_width=True, type="primary"):
        if n or p:
            st.session_state.rows.append({
                "Name / الاسم": n, 
                "Passport / الجواز": p, 
                "Nationality / الجنسية": nat,
                "DOB / الميلاد": d,
                "DOB_ISO": auto.get("dob_iso","") if auto else d,
                "Expiry / الانتهاء": e,
                "Expiry_ISO": auto.get("exp_iso","") if auto else e,
                "Sex / الجنس": s,
                "Nationality_AR": auto.get("nationality_ar","") if auto else ""
            })
            st.toast(f"✅ تمت إضافة {n}")
            st.rerun()
with colB:
    st.metric("عدد الجوازات / Total", len(st.session_state.rows))

if st.session_state.rows:
    df_display = pd.DataFrame(st.session_state.rows)[["Name / الاسم","Passport / الجواز","Nationality / الجنسية","DOB / الميلاد","Expiry / الانتهاء","Sex / الجنس"]]
    st.dataframe(df_display, use_container_width=True, height=350)
    
    # إعداد للتصدير - نسختين
    df_enjaz = pd.DataFrame(st.session_state.rows)
    df_enjaz_export = df_enjaz[["Name / الاسم","Passport / الجواز","Nationality / الجنسية","DOB / الميلاد","Expiry / الانتهاء","Sex / الجنس"]].copy()
    # نسخة إنجاز مع ISO
    df_enjaz_iso = pd.DataFrame([{"Name": r["Name / الاسم"], "PassportNo": r["Passport / الجواز"], "Nationality": r["Nationality / الجنسية"], "DOB": r.get("DOB_ISO",r["DOB / الميلاد"]), "Expiry": r.get("Expiry_ISO",r["Expiry / الانتهاء"]), "Sex": r["Sex / الجنس"]} for r in st.session_state.rows])
    
    total = len(df_display)
    names_list = "\n".join([f"{i+1}. {row['Name / الاسم']} - {row['Passport / الجواز']} ({row['Nationality / الجنسية']})" for i, row in df_display.iterrows()])
    wa_text = f"👑 تقرير TASHEER AI V2.4 - جاهز لإنجاز\n📊 العدد: {total} جواز\n\n📋 التفاصيل:\n{names_list}\n\n✅ تنسيق إنجاز جاهز\n📎 الموقع: tasheer-ai-juub2hzyqf9boqzthpwv4n.streamlit.app\n📞 +966540450738"
    wa_link = f"https://wa.me/966540450738?text={urllib.parse.quote(wa_text)}"
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        csv = df_enjaz_export.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 Excel عادي / Normal", data=csv, file_name="TASHEER_V2.4_Normal.csv", mime="text/csv", use_container_width=True)
    with c2:
        csv2 = df_enjaz_iso.to_csv(index=False).encode('utf-8-sig')
        st.download_button("✅ Excel إنجاز / Enjaz", data=csv2, file_name="TASHEER_V2.4_Enjaz_Ready.csv", mime="text/csv", use_container_width=True, type="primary")
    with c3:
        st.link_button("💬 واتساب / WhatsApp", wa_link, use_container_width=True)
    with c4:
        if st.button("🗑️ مسح الكل / Clear", use_container_width=True):
            st.session_state.rows = []
            st.rerun()

st.markdown("<center style='color:#64748b; font-size:12px; margin-top:30px'>© 2026 TASHEER AI V2.4 Enjaz Ready - +966 54 045 0738 - متوافق مع منصة إنجاز</center>", unsafe_allow_html=True)
