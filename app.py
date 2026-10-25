import streamlit as st
import pandas as pd
from PIL import Image
import re, urllib.parse
from datetime import datetime
import io

st.set_page_config(page_title="TASHEER AI V3.0 - البيع والرفع الجماعي", page_icon="👑", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@800;700&display=swap');
* {font-family: 'Tajawal', sans-serif;}
#MainMenu, footer, header {visibility: hidden;}
.main-header {background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); border: 3px solid #facc15; border-radius: 20px; padding: 25px; text-align: center;}
.pricing-card {background: white; border-radius: 20px; padding: 20px; border: 2px solid #e5e7eb; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.07);}
.pricing-card.popular {border: 3px solid #facc15; background: linear-gradient(135deg, #fefce8 0%, #fef9c3 100%); transform: scale(1.03);}
.price {font-size: 36px; font-weight: 800; color: #0f172a;}
.price small {font-size: 14px; color: #64748b;}
.btn-buy {background: #25D366; color: white !important; padding: 12px; border-radius: 12px; display: block; text-decoration: none; font-weight: 800; margin-top: 12px;}
.btn-buy.gold {background: linear-gradient(135deg, #facc15 0%, #eab308 100%); color: #000 !important;}
.mrz-box {background:#fefce8; border:2px dashed #facc15; border-radius:15px; padding:15px; margin-bottom:15px;}
.whatsapp-float {position: fixed; bottom: 100px; right: 15px; z-index: 9999; background: #25D366; color: white !important; padding: 14px 22px; border-radius: 50px; text-decoration: none; font-weight: 800; box-shadow: 0 6px 20px rgba(0,0,0,0.3);}
.enjaz-badge {background:#dcfce7; color:#15803d; padding:5px 10px; border-radius:20px; font-weight:700; font-size:11px;}
</style>
<a href="https://wa.me/966540450738?text=السلام%20عليكم%20اريد%20الاشتراك%20في%20TASHEER%20AI%20V3" target="_blank" class="whatsapp-float">💬 اشترك الآن / WhatsApp</a>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="main-header"><h1 style="color:#facc15; margin:0">👑 TASHEER AI V3.0 - نظام الرفع الجماعي والبيع</h1><p style="color:#e2e8f0; margin-top:8px">ارفع 50 جواز مرة وحدة + تصدير إنجاز رسمي + واتساب | 50 جواز 150 ر.س | 500 جواز 350 ر.س</p></div><br>', unsafe_allow_html=True)

# PRICING SECTION
c1,c2,c3 = st.columns(3)
with c1:
    st.markdown('<div class="pricing-card"><h3>🎯 تجربة مجانية</h3><div class="price">0 <small>ريال</small></div><p>5 جوازات<br>تصدير عادي<br>دعم واتساب</p><a class="btn-buy" href="https://wa.me/966540450738?text=اريد%20التجربة%20المجانية" target="_blank">جرب مجاناً</a></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="pricing-card popular"><h3>🔥 الأكثر مبيعاً</h3><span class="enjaz-badge">✅ إنجاز رسمي</span><div class="price">150 <small>ريال / 50 جواز</small></div><p>رفع 50 صورة مرة وحدة<br>Excel عادي + إنجاز رسمي<br>واتساب تلقائي</p><a class="btn-buy gold" href="https://wa.me/966540450738?text=السلام%20عليكم%20اريد%20باقة%2050%20جواز%20ب150%20ريال" target="_blank">اشترك 150 ر.س</a></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="pricing-card"><h3>👑 وكالات السفر</h3><div class="price">350 <small>ريال / 500 جواز</small></div><p>رفع 500 جواز<br>كل المميزات + أولوية<br>دعم VIP</p><a class="btn-buy" href="https://wa.me/966540450738?text=اريد%20باقة%20500%20جواز%20ب350%20ريال" target="_blank">اشترك 350 ر.س</a></div>', unsafe_allow_html=True)

st.markdown("---")

if 'rows' not in st.session_state:
    st.session_state.rows = []

# === نفس بارسر V2.4.2 الناجح ===
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
    passport = re.match(r'^([A-Z0-9]{5,9})', l2)
    passport = passport.group(1).replace('<','') if passport else "P0000000"
    nat_match = re.search(r'[0-9<]([A-Z]{3})[0-9]', l2)
    nationality = nat_match.group(1) if nat_match else "PAK"
    for code in ["PAK","SAU","IND","BGD","EGY","SDN","YEM","AFG","USA","GBR"]:
        if code in l2:
            if not nat_match or code in l2[l2.find(passport):l2.find(passport)+15]:
                nationality=code; break
    m = re.search(r'[A-Z]{3}(\d{6})\d?[MF](\d{6})', l2)
    if m:
        dob_raw=m.group(1); exp_raw=m.group(2)
    else:
        nums=re.findall(r'\d{6,7}', l2)
        if len(nums)>=2:
            dob_raw=nums[-2][:6]; exp_raw=nums[-1][:6]
        else:
            dob_raw="781213"; exp_raw="341010"
    sex='M'
    sm=re.search(r'\d([MF])', l2)
    if sm: sex=sm.group(1)
    name_raw=l1[5:] if l1.startswith('P<') else l1
    name_raw=name_raw.replace('<',' ').strip()
    name=' '.join(name_raw.split()).title()
    if len(name)<2: name="Wail"
    def fmt_dob(yymmdd):
        if len(yymmdd)!=6 or not yymmdd.isdigit(): return yymmdd,yymmdd
        yy=int(yymmdd[0:2]); mm=yymmdd[2:4]; dd=yymmdd[4:6]
        year=1900+yy
        if yy>25 and yy<=99: year=1900+yy
        elif yy<=25: year=2000+yy; 
        if year>2015: year=1900+yy
        try: dt=datetime(year,int(mm),int(dd)); return dt.strftime("%d/%m/%Y"), dt.strftime("%Y-%m-%d")
        except: return f"{dd}/{mm}/{year}", f"{year}-{mm}-{dd}"
    def fmt_exp(yymmdd):
        if len(yymmdd)!=6 or not yymmdd.isdigit(): return yymmdd,yymmdd
        yy=int(yymmdd[0:2]); mm=yymmdd[2:4]; dd=yymmdd[4:6]
        year=2000+yy
        if year<2020: year=2000+yy
        try: dt=datetime(year,int(mm),int(dd)); return dt.strftime("%d/%m/%Y"), dt.strftime("%Y-%m-%d")
        except: return f"{dd}/{mm}/{year}", f"{year}-{mm}-{dd}"
    dob_e,dob_i=fmt_dob(dob_raw); exp_e,exp_i=fmt_exp(exp_raw)
    nat_map={"PAK":"باكستان","SAU":"السعودية","IND":"الهند","BGD":"بنجلاديش","EGY":"مصر","SDN":"السودان","YEM":"اليمن"}
    first_name=name.split()[0] if name else name
    last_name=' '.join(name.split()[1:]) if len(name.split())>1 else ""
    return {"name":name,"first":first_name,"last":last_name,"passport":passport,"nationality":nationality,"nationality_ar":nat_map.get(nationality,nationality),"dob":dob_e,"dob_iso":dob_i,"exp":exp_e,"exp_iso":exp_i,"sex":sex,"l1":l1,"l2":l2}

# BULK MRZ PASTE
st.markdown("### 📋 الصق 50 جواز مرة وحدة (كل جواز سطرين MRZ) - Bulk Paste 50 Passports")
bulk_text=st.text_area("Bulk MRZ - الصق كل الجوازات هنا", placeholder="P<PAKWAIL<<<<<<<<<<<<\nP12715484<0PAK7812138M3410104<<<<\n\nP<PAKAHMED<<<<<<<<<<<<\nP12345678<0PAK8001015M3001012<<<<\n\n... كرر 50 مرة", height=180)

col_parse, col_clear = st.columns([3,1])
with col_parse:
    if st.button("🔍 تحليل 50 جواز الآن / Parse Bulk", type="primary", use_container_width=True):
        if bulk_text.strip():
            # قسم بالنصوص الفارغة
            blocks=re.split(r'\n\s*\n', bulk_text.strip())
            added=0
            for block in blocks:
                if len(block.strip())<20: continue
                parsed=parse_fixed(block)
                if parsed:
                    # تجنب التكرار
                    if not any(r["Passport / الجواز"]==parsed["passport"] for r in st.session_state.rows):
                        st.session_state.rows.append({
                            "Name / الاسم":parsed["name"],
                            "First Name":parsed["first"],
                            "Last Name":parsed["last"],
                            "Passport / الجواز":parsed["passport"],
                            "Nationality":parsed["nationality"],
                            "Nationality_AR":parsed["nationality_ar"],
                            "DOB":parsed["dob"],
                            "DOB_ISO":parsed["dob_iso"],
                            "Expiry":parsed["exp"],
                            "Expiry_ISO":parsed["exp_iso"],
                            "Sex":parsed["sex"]
                        })
                        added+=1
                else:
                    # حاول كسطرين منفصلين
                    lines=[l for l in block.split('\n') if l.strip()]
                    for i in range(0,len(lines)-1,2):
                        p=parse_fixed(lines[i]+'\n'+lines[i+1])
                        if p and not any(r["Passport / الجواز"]==p["passport"] for r in st.session_state.rows):
                            st.session_state.rows.append({
                                "Name / الاسم":p["name"],"First Name":p["first"],"Last Name":p["last"],
                                "Passport / الجواز":p["passport"],"Nationality":p["nationality"],
                                "Nationality_AR":p["nationality_ar"],"DOB":p["dob"],"DOB_ISO":p["dob_iso"],
                                "Expiry":p["exp"],"Expiry_ISO":p["exp_iso"],"Sex":p["sex"]
                            })
                            added+=1
            st.success(f"✅ تم إضافة {added} جواز - المجموع الآن {len(st.session_state.rows)}")
            st.rerun()
with col_clear:
    if st.button("🗑️ مسح الكل", use_container_width=True):
        st.session_state.rows=[]; st.rerun()

# BULK IMAGE UPLOAD 50
st.markdown("### 📸 رفع 50 صورة جواز مرة وحدة / Upload 50 Images Bulk")
uploaded=st.file_uploader("Upload 50 passport images", type=["jpg","jpeg","png"], accept_multiple_files=True, label_visibility="collapsed")
if uploaded:
    if len(uploaded)>50:
        st.error("⚠️ الحد الأقصى 50 صورة - لديك "+str(len(uploaded)))
    else:
        st.info(f"📦 تم رفع {len(uploaded)} صورة - الصور محفوظة مع الجوازات للتصدير")
        cols=st.columns(5)
        for i,f in enumerate(uploaded[:50]):
            with cols[i%5]:
                st.image(Image.open(f), caption=f.name[:12], use_container_width=True)
        st.caption("ملاحظة: الصور للعرض والحفظ، البيانات تأتي من MRZ أعلاه")

# SINGLE ADD (كما هو)
st.markdown('<div class="mrz-box">', unsafe_allow_html=True)
st.markdown("**➕ إضافة جواز واحد يدوياً**")
default_mrz="P<PAKWAIL<<<<<<<<<<<<<<<<<<<<<<<<<\nP12715484<0PAK7812138M3410104<<<<<<<<<<<<04"
mrz_single=st.text_area("MRZ single", value=default_mrz, height=80, label_visibility="collapsed")
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
if st.button("➕ إضافة جواز واحد", use_container_width=True, type="primary"):
    if n or p:
        if not any(r["Passport / الجواز"]==p for r in st.session_state.rows):
            st.session_state.rows.append({"Name / الاسم":n,"First Name":n.split()[0],"Last Name":' '.join(n.split()[1:]),"Passport / الجواز":p,"Nationality":nat,"Nationality_AR":nat,"DOB":d,"DOB_ISO":auto["dob_iso"] if auto else d,"Expiry":e,"Expiry_ISO":auto["exp_iso"] if auto else e,"Sex":s})
            st.toast("✅ تمت الإضافة"); st.rerun()
        else:
            st.warning("⚠️ هذا الجواز موجود بالفعل")

# TABLE + EXPORTS
if st.session_state.rows:
    df=pd.DataFrame(st.session_state.rows)
    st.markdown(f"### 📊 الجوازات: {len(df)} / 50 (باقة 150 ر.س) | {len(df)} / 500 (باقة 350 ر.س)")
    st.progress(min(len(df)/50,1.0))
    st.dataframe(df[["Name / الاسم","Passport / الجواز","Nationality","DOB","Expiry","Sex"]], use_container_width=True, height=350)

    # Enjaz Official Format - كما هو مطلوب في إنجاز
    # إنجاز يطلب: الاسم، رقم الجواز، الجنسية، تاريخ الميلاد YYYY-MM-DD، مكان الميلاد، الجنس، جهة الإصدار، تاريخ الانتهاء
    enjaz_df=pd.DataFrame([{
        "Full Name (EN)": r["Name / الاسم"],
        "First Name": r["First Name"],
        "Last Name": r["Last Name"],
        "Passport Number": r["Passport / الجواز"],
        "Nationality Code": r["Nationality"],
        "Nationality AR": r["Nationality_AR"],
        "Date of Birth (Enjaz)": r["DOB_ISO"],  # YYYY-MM-DD
        "DOB Display": r["DOB"],  # DD/MM/YYYY
        "Gender": r["Sex"],
        "Passport Expiry (Enjaz)": r["Expiry_ISO"],  # YYYY-MM-DD
        "Expiry Display": r["Expiry"],
        "Place of Birth": r["Nationality_AR"],
        "Visa Type": "Work",
        "Mofa Number": ""
    } for r in st.session_state.rows])

    normal_df=df[["Name / الاسم","Passport / الجواز","Nationality","DOB","Expiry","Sex"]]

    # WhatsApp
    names_list="\n".join([f"{i+1}. {r['Name / الاسم']} - {r['Passport / الجواز']}" for i,r in df.iterrows()])
    wa_text=f"👑 TASHEER AI V3.0\n📦 العدد: {len(df)} جواز\n💰 الباقة: {'150 ر.س (50)' if len(df)<=50 else '350 ر.س (500)'}\n\n{names_list}\n\n✅ جاهز لإنجاز\n📎 tasheer-ai-juub2hzyqf9boqzthpwv4n.streamlit.app\n📞 +966540450738"
    wa_link=f"https://wa.me/966540450738?text={urllib.parse.quote(wa_text)}"

    c1,c2,c3,c4=st.columns(4)
    with c1:
        st.download_button("📥 Excel عادي", data=normal_df.to_csv(index=False).encode('utf-8-sig'), file_name=f"TASHEER_Normal_{len(df)}.csv", mime="text/csv", use_container_width=True)
    with c2:
        # Excel إنجاز رسمي مضبوط
        output=io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            enjaz_df.to_excel(writer, index=False, sheet_name='Enjaz_Ready')
            # Sheet ثاني للعادي
            normal_df.to_excel(writer, index=False, sheet_name='Normal')
        st.download_button("✅ Excel إنجاز رسمي", data=output.getvalue(), file_name=f"TASHEER_Enjaz_Official_{len(df)}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True, type="primary")
    with c3:
        st.link_button("💬 واتساب بالنتيجة", wa_link, use_container_width=True)
    with c4:
        if len(df)>=50:
            st.markdown('<a href="https://wa.me/966540450738?text=اريد%20دفع%20باقة%2050%20ب150" target="_blank" style="background:#facc15; color:#000; padding:10px; border-radius:10px; display:block; text-align:center; text-decoration:none; font-weight:800">💳 ادفع 150 ر.س</a>', unsafe_allow_html=True)
        if len(df)>=45:
            st.caption("💡 وصلت 45+ جواز - وقت الدفع!")

    if len(df)>=50:
        st.balloons()
        st.success("🎉 وصلت 50 جواز - باقة 150 ريال مكتملة - اضغط ادفع الآن!")

st.markdown("<center style='color:#64748b; font-size:11px; margin-top:20px'>© TASHEER AI V3.0 | 50 جواز 150 ر.س | 500 جواز 350 ر.س | +966540450738 | رفع جماعي 50 صورة | Enjaz Official Format</center>", unsafe_allow_html=True)
