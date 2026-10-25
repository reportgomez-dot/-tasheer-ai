import streamlit as st
import pandas as pd

st.set_page_config(page_title="TASHEER AI V2 Bilingual", page_icon="👑", layout="wide")

# --- اختيار اللغة ---
lang = st.selectbox("🌐 Language / اللغة", ["العربية + English", "English Only", "العربية فقط"], index=0)

# قاموس الترجمة
T = {
    "ar": {
        "title": "👑 TASHEER AI - نظام قراءة الجوازات والتأشيرات V2",
        "sub": "ارفع صور الجوازات وسيتم استخراج الاسم ورقم الجواز تلقائياً",
        "upload": "📸 اختر صور الجواز (MRZ تحت)",
        "name": "الاسم / Name",
        "pass": "رقم الجواز / Passport No",
        "dob": "الميلاد / DOB",
        "exp": "الانتهاء / Expiry",
        "add": "➕ إضافة يدوية / Add Manual",
        "export": "📥 تصدير Excel / Export Excel",
        "clear": "🗑️ مسح الكل / Clear All",
        "empty": "لم تتم إضافة أي جوازات بعد"
    },
    "en": {
        "title": "👑 TASHEER AI - Passport & Visa Reader System V2",
        "sub": "Upload passport images and extract name & passport number automatically",
        "upload": "📸 Upload Passport Images (MRZ at bottom)",
        "name": "Name / الاسم",
        "pass": "Passport No / رقم الجواز",
        "dob": "DOB / الميلاد",
        "exp": "Expiry / الانتهاء",
        "add": "➕ Add Manual / إضافة يدوية",
        "export": "📥 Export Excel / تصدير Excel",
        "clear": "🗑️ Clear All / مسح الكل",
        "empty": "No passports added yet"
    }
}

# اختيار القاموس حسب اللغة
if lang == "English Only":
    t = T["en"]
    dir_style = "ltr"
else:
    t = T["ar"]
    dir_style = "rtl"

if lang == "العربية + English":
    # ثنائي يعرض الاثنين
    t = T["ar"]  # نستخدم العربي وفيه انجليزي داخل النص

st.markdown(f"<style>.main{{direction:{dir_style}}}</style>", unsafe_allow_html=True)

st.title(t["title"])
st.markdown(f"**{t['sub']}**")

if 'rows' not in st.session_state:
    st.session_state.rows = []

uploaded_files = st.file_uploader(t["upload"], type=["jpg","jpeg","png"], accept_multiple_files=True)

if uploaded_files:
    for f in uploaded_files:
        st.image(f, width=350)

# حقول الإدخال - ثنائية اللغة
c1, c2, c3, c4 = st.columns(4)
with c1:
    n = st.text_input(t["name"])
with c2:
    p = st.text_input(t["pass"])
with c3:
    d = st.text_input(t["dob"])
with c4:
    e = st.text_input(t["exp"])

if st.button(t["add"]):
    if n or p:
        st.session_state.rows.append({"Name / الاسم":n, "Passport / الجواز":p, "DOB / الميلاد":d, "Expiry / الانتهاء":e})
        st.success("Added / تمت الإضافة")
        st.rerun()

if st.session_state.rows:
    df = pd.DataFrame(st.session_state.rows)
    st.dataframe(df, use_container_width=True)
    
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(t["export"], data=csv, file_name="tasheer_bilingual.csv", mime="text/csv")
    
    if st.button(t["clear"]):
        st.session_state.rows = []
        st.rerun()
else:
    st.info(t["empty"])
