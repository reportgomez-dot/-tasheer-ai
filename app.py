import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
try:
    import folium
    from streamlit_folium import st_folium
    MAP_AVAILABLE = True
except:
    MAP_AVAILABLE = False

st.set_page_config(page_title="TASHEER AI - Interactive Map", page_icon="🗺️", layout="wide")

WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={WALLET}"
EMAIL = "report.gomez@gmail.com"

COUNTRIES_COORDS = {
    "🇸🇦 السعودية": {"lat": 23.8859, "lon": 45.0792, "code": "SA", "currency": "SAR 3.75"},
    "🇦🇪 الإمارات": {"lat": 23.4241, "lon": 53.8478, "code": "AE", "currency": "AED 3.67"},
    "🇶🇦 قطر": {"lat": 25.3548, "lon": 51.1839, "code": "QA", "currency": "QAR 3.64"},
    "🇰🇼 الكويت": {"lat": 29.3117, "lon": 47.4818, "code": "KW", "currency": "KWD 0.31"},
    "🇧🇭 البحرين": {"lat": 26.0667, "lon": 50.5577, "code": "BH", "currency": "BHD 0.376"},
    "🇴🇲 عمان": {"lat": 21.5126, "lon": 55.9233, "code": "OM", "currency": "OMR 0.385"},
    "🇾🇪 اليمن": {"lat": 15.5527, "lon": 48.5164, "code": "YE", "currency": "YER 530"},
    "🇯🇴 الأردن": {"lat": 31.9454, "lon": 35.9284, "code": "JO", "currency": "JOD 0.71"},
    "🇱🇧 لبنان": {"lat": 33.8547, "lon": 35.8623, "code": "LB", "currency": "LBP 89500"},
    "🇮🇶 العراق": {"lat": 33.2232, "lon": 43.6793, "code": "IQ", "currency": "IQD 1310"},
    "🇸🇾 سوريا": {"lat": 34.8021, "lon": 38.9968, "code": "SY", "currency": "SYP 13000"},
    "🇵🇸 فلسطين": {"lat": 31.9522, "lon": 35.2332, "code": "PS", "currency": "ILS 3.7"},
    "🇪🇬 مصر": {"lat": 26.8206, "lon": 30.8025, "code": "EG", "currency": "EGP 50.5"},
    "🇸🇩 السودان": {"lat": 12.8628, "lon": 30.2176, "code": "SD", "currency": "SDG 600"},
    "🇸🇴 الصومال": {"lat": 5.1521, "lon": 46.1996, "code": "SO", "currency": "SOS 570"},
    "🇲🇷 موريتانيا": {"lat": 21.0079, "lon": -10.9408, "code": "MR", "currency": "MRU 39.5"},
    "🇲🇦 المغرب": {"lat": 31.7917, "lon": -7.0926, "code": "MA", "currency": "MAD 10.2"},
    "🇩🇿 الجزائر": {"lat": 28.0339, "lon": 1.6596, "code": "DZ", "currency": "DZD 135"},
    "🇹🇳 تونس": {"lat": 33.8869, "lon": 9.5375, "code": "TN", "currency": "TND 3.1"},
    "🇱🇾 ليبيا": {"lat": 26.3351, "lon": 17.2283, "code": "LY", "currency": "LYD 4.8"},
    "🇺🇸 أمريكا": {"lat": 37.0902, "lon": -95.7129, "code": "US", "currency": "USD"},
    "🇬🇧 بريطانيا": {"lat": 55.3781, "lon": -3.4360, "code": "GB", "currency": "GBP"},
    "🇪🇺 أوروبا": {"lat": 50.8503, "lon": 4.3517, "code": "EU", "currency": "EUR"},
    "🇹🇷 تركيا": {"lat": 38.9637, "lon": 35.2433, "code": "TR", "currency": "TRY"},
    "🇮🇳 الهند": {"lat": 20.5937, "lon": 78.9629, "code": "IN", "currency": "INR"},
    "🇵🇰 باكستان": {"lat": 30.3753, "lon": 69.3451, "code": "PK", "currency": "PKR"},
}

if 'users_db' not in st.session_state:
    st.session_state['users_db'] = {"admin": {"password": "Tasheer2024!", "name": "Gomez Admin", "email": EMAIL, "sub_end": datetime.now() + timedelta(days=365), "role": "admin"}}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'show_landing' not in st.session_state:
    st.session_state['show_landing'] = True
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'ar'

c1, c2, c3 = st.columns([6,2,2])
with c2:
    if st.button("🇸🇦 عربي", use_container_width=True, type="primary" if st.session_state['lang']=='ar' else "secondary"):
        st.session_state['lang'] = 'ar'
        st.rerun()
with c3:
    if st.button("🇺🇸 English", use_container_width=True, type="primary" if st.session_state['lang']=='en' else "secondary"):
        st.session_state['lang'] = 'en'
        st.rerun()

if st.session_state['show_landing'] and not st.session_state['logged_in']:
    lang = st.session_state['lang']
    st.markdown(f"""
    <div style="background: linear-gradient(135deg,#0a7a42,#0d4a2a); color:white; padding:40px 20px; border-radius:20px; text-align:center;">
        <h1>🗺️ TASHEER AI - Interactive Global Map</h1>
        <h2>{"نغطي كل الوطن العربي والعالم - خريطة تفاعلية" if lang=='ar' else "Cover All Arab World & Global - Interactive Map"}</h2>
        <p>🌐 26 دولة | 27 عملة | 📍 خريطة تفاعلية | tasheer-ai.com | 00966540450738</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"### {'🗺️ الخريطة التفاعلية - اضغط على أي دولة' if lang=='ar' else '🗺️ Interactive Map'}")
    if MAP_AVAILABLE:
        m = folium.Map(location=[25, 20], zoom_start=2.5, tiles="OpenStreetMap")
        for country_name, data in COUNTRIES_COORDS.items():
            is_arab = data['code'] in ["SA","AE","QA","KW","BH","OM","YE","JO","LB","IQ","SY","PS","EG","SD","SO","MR","MA","DZ","TN","LY"]
            color = "green" if is_arab else "blue"
            folium.Marker(location=[data['lat'], data['lon']], popup=f"{country_name}<br>{data['code']}<br>{data['currency']}", tooltip=country_name, icon=folium.Icon(color=color, icon="flag")).add_to(m)
        st_folium(m, width=None, height=500)
    else:
        df = pd.DataFrame([{"lat": v["lat"], "lon": v["lon"], "country": k} for k, v in COUNTRIES_COORDS.items()])
        st.map(df)
        st.dataframe(df, use_container_width=True)
    st.markdown("**SA AE QA KW BH OM YE JO LB IQ SY PS EG SD SO MR MA DZ TN LY | US GB EU TR IN PK**")
    if st.button("🚀 دخول للمنصة - مع الخريطة", type="primary", use_container_width=True):
        st.session_state['show_landing'] = False
        st.rerun()
    st.stop()

db = st.session_state['users_db']
if not st.session_state['logged_in']:
    with st.form("login"):
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة المرور", type="password")
        if st.form_submit_button("دخول", type="primary"):
            if u in db and db[u]["password"] == p:
                st.session_state['logged_in'] = True
                st.session_state['username'] = u
                st.session_state['show_landing'] = False
                st.rerun()
    if st.button("🏠 الموقع الرئيسي مع الخريطة"):
        st.session_state['show_landing'] = True
        st.rerun()
    st.stop()

u = st.session_state['username']
user = db[u]
st.success(f"✅ {user['name']} - باقي {(user['sub_end'] - datetime.now()).days} يوم - مع خريطة تفاعلية")
tab1, tab2 = st.tabs(["🗺️ الخريطة", "💳 تجديد"])
with tab1:
    if MAP_AVAILABLE:
        m = folium.Map(location=[25, 20], zoom_start=2)
        for country_name, data in COUNTRIES_COORDS.items():
            color = "green" if data['code'] in ["SA","AE","QA","KW","BH","OM","YE","JO","LB","IQ","SY","PS","EG","SD","SO","MR","MA","DZ","TN","LY"] else "blue"
            folium.Marker(location=[data['lat'], data['lon']], popup=f"{country_name}<br>{data['code']}", icon=folium.Icon(color=color)).add_to(m)
        st_folium(m, width=None, height=500)
    else:
        st.map(pd.DataFrame([{"lat": v["lat"], "lon": v["lon"]} for v in COUNTRIES_COORDS.values()]))
with tab2:
    st.code(WALLET)
    st.image(QR_URL)
    if st.button("🏠 رجوع للخريطة"):
        st.session_state['show_landing'] = True
        st.rerun()
if st.button("🚪 خروج"):
    st.session_state['logged_in'] = False
    st.session_state['show_landing'] = True
    st.rerun()
