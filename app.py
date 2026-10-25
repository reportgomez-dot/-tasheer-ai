import streamlit as st
import pandas as pd
from PIL import Image
import re, urllib.parse
from datetime import datetime

st.set_page_config(page_title="TASHEER AI V2.4 Stable", page_icon="👑", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@700;800&display=swap');
* {font-family: 'Tajawal', sans-serif;}
#MainMenu, footer, header {visibility: hidden;}
.main-header {background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border: 3px solid #facc15; border-radius: 20px; padding: 28px; text-align: center;}
.main-header h1 {color: #facc15; font-size: 30px; margin: 0;}
.whatsapp-float {position: fixed; bottom: 180px; right: 15px; z-index: 9999; background: #25D366; color: white !important; padding: 14px 22px; border-radius: 50px; text-decoration: none; font-weight: 800;}
.mrz-box {background:#fefce8; border:2px solid #facc15; border-radius:15px; padding:18px;}
.enjaz-badge {background:#dcfce7; border:1px solid #22c55e; color:#15803d; padding:6px 12px; border-radius:20px; font-size:12px; font-weight:700;}
</style>
<a href="https://wa.me/966540450738?text=السلام%20عليكم%20اريد%20TASHEER%20AI" target="_blank" class="whatsapp-float">💬 واتساب / WhatsApp</a>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1>👑 TASHEER AI V2.4 - Stable Enjaz Ready</h1><p>MRZ + الجنسية + إنجاز + واتساب | يعمل 100% بدون أخطاء</p><p><span class="enjaz-badge">✅ متوافق مع إنجاز ENJAZ - Stable Version</span></p></div><br>', unsafe_allow_html=True)

if 'rows' not in st.session_state: st.session_state.rows = []

def parse_mrz(text):
    text=text.upper().strip(); lines=[re.sub(r'[^A-Z0-9<]', '', l.upper()) for l in text.replace(' ','').split('\n') if l.strip()]; lines=[l for l in lines if len(l)>=30]
    if len(lines)<2 and len(text)>80:
        cleaned=re.sub(r'[^A-Z0-9<]', '', text.upper())
        if len(cleaned)>=88: lines=[cleaned[:44], cleaned[44:88]]
    if len(lines)>=2:
        l1,l2=lines[-2],lines[-1]
        try:
            name_raw=l1[5:] if len(l1)>5 else ""; parts=name_raw.split('<<'); surname=parts[0].replace('<',' ').strip() if parts else ""; given=parts[1].replace('<',' ').strip() if len(parts)>1 else ""
            full=f"{given} {surname}".strip(); full=' '.join(full.split()).title()
            pp=l2[0:9].replace('<','').strip(); nat=l2[10:13].replace('<','').strip() if len(l2)>=13 else "PAK"; dob_raw=l2[13:19] if len(l2)>=19 else ""; sex=l2[20] if len(l2)>=21 else "M"; exp_raw=l2[21:27] if len(l2)>=27 else ""
            def fmt(yymmdd):
                if len(yymmdd)==6 and yymmdd.isdigit():
                    yy=int(yymmdd[0:2]); mm=yymmdd[2:4]; dd=yymmdd[4:6]; year=2000+yy if yy<30 else 1900+yy
                    try: dt=datetime(year,int(mm),int(dd)); return dt.strftime("%d/%m/%Y"), dt.strftime("%Y-%m-%d")
                    except: return f"{dd}/{mm}/{year}", f"{year}-{mm}-{dd}"
                return yymmdd,yymmdd
            dob_e,dob_i=fmt(dob_raw); exp_e,exp_i=fmt(exp_raw); m={"PAK":"باكستان","SAU":"السعودية","IND":"الهند","BGD":"بنجلاديش","EGY":"مصر","YEM":"اليمن","SDN":"السودان"}
            return {"name":full,"passport":pp,"nationality":nat,"nationality_ar":m.get(nat,nat),"dob":dob_e,"dob_iso":dob_i,"exp":exp_e,"exp_iso":exp_i,"sex":sex,"l1":l1,"l2":l2}
        except: return None
    return None

st.markdown('<div class="mrz-box">', unsafe_allow_html=True)
st.markdown("**🤖 الصق سطرين MRZ - يقرأ الجنسية والتاريخ تلقائياً**")
mrz_input=st.text_area("MRZ", placeholder="P<PAKWAIL<<<<<<<<<<<<<<<<<<<<\nP12715484<0PAK7812138M3410104<<<<<<<<<<", height=90, label_visibility="collapsed")
auto={}
if mrz_input:
    auto=parse_mrz(mrz_input)
    if auto: st.success(f"✅ {auto['passport']} | {auto['name']} | {auto['nationality_ar']} ({auto['nationality']}) | {auto['dob']} | {auto['exp']} | {auto['sex']}"); st.code(f"{auto['l1']}\n{auto['l2']}")
    else: st.warning("⚠️ تأكد من لصق سطرين كاملين")
st.markdown('</div><br>', unsafe_allow_html=True)

uploaded=st.file_uploader("📸 صور الجواز / Upload Passport Images", type=["jpg","jpeg","png"], accept_multiple_files=True)
if uploaded:
    cols=st.columns(3)
    for i,f in enumerate(uploaded):
        with cols[i%3]: st.image(Image.open(f), caption=f.name, use_container_width=True)

c1,c2,c3,c4,c5,c6=st.columns(6)
with c1: n=st.text_input("الاسم", value=auto.get("name","") if auto else "")
with c2: p=st.text_input("الجواز", value=auto.get("passport","") if auto else "")
with c3: nat=st.text_input("الجنسية", value=auto.get("nationality","") if auto else "")
with c4: d=st.text_input("الميلاد", value=auto.get("dob","") if auto else "")
with c5: e=st.text_input("الانتهاء", value=auto.get("exp","") if auto else "")
with c6: s=st.text_input("الجنس", value=auto.get("sex","") if auto else "")

colA,colB=st.columns([4,1])
with colA:
    if st.button("➕ إضافة", use_container_width=True, type="primary"):
        if n or p:
            st.session_state.rows.append({"Name / الاسم":n,"Passport / الجواز":p,"Nationality / الجنسية":nat,"DOB / الميلاد":d,"DOB_ISO":auto.get("dob_iso",d) if auto else d,"Expiry / الانتهاء":e,"Expiry_ISO":auto.get("exp_iso",e) if auto else e,"Sex / الجنس":s,"Nationality_AR":auto.get("nationality_ar","") if auto else ""})
            st.toast("✅ تمت الإضافة"); st.rerun()
with colB: st.metric("العدد", len(st.session_state.rows))

if st.session_state.rows:
    df=pd.DataFrame(st.session_state.rows); df_show=df[["Name / الاسم","Passport / الجواز","Nationality / الجنسية","DOB / الميلاد","Expiry / الانتهاء","Sex / الجنس"]]
    st.dataframe(df_show, use_container_width=True, height=300)
    total=len(df_show); names_list="\n".join([f"{i+1}. {row['Name / الاسم']} - {row['Passport / الجواز']} ({row['Nationality / الجنسية']})" for i,row in df_show.iterrows()])
    wa_text=f"👑 تقرير TASHEER AI V2.4 - جاهز لإنجاز\n📊 العدد: {total} جواز\n\n📋 التفاصيل:\n{names_list}\n\n✅ تنسيق إنجاز جاهز\n📎 الموقع: tasheer-ai-juub2hzyqf9boqzthpwv4n.streamlit.app\n📞 +966540450738"
    wa_link=f"https://wa.me/966540450738?text={urllib.parse.quote(wa_text)}"
    c1,c2,c3,c4=st.columns(4)
    with c1: st.download_button("📥 Excel عادي", data=df_show.to_csv(index=False).encode('utf-8-sig'), file_name="TASHEER_V2.4_Normal.csv", mime="text/csv", use_container_width=True)
    with c2:
        df2=pd.DataFrame([{"Name":r["Name / الاسم"],"PassportNo":r["Passport / الجواز"],"Nationality":r["Nationality / الجنسية"],"DOB":r.get("DOB_ISO",r["DOB / الميلاد"]),"Expiry":r.get("Expiry_ISO",r["Expiry / الانتهاء"]),"Sex":r["Sex / الجنس"]} for r in st.session_state.rows])
        st.download_button("✅ Excel إنجاز", data=df2.to_csv(index=False).encode('utf-8-sig'), file_name="TASHEER_V2.4_Enjaz.csv", mime="text/csv", use_container_width=True, type="primary")
    with c3: st.link_button("💬 واتساب", wa_link, use_container_width=True)
    with c4:
        if st.button("🗑️ مسح الكل", use_container_width=True): st.session_state.rows=[]; st.rerun()
