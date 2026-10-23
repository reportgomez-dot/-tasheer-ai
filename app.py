import streamlit as st
from datetime import datetime, timedelta
import random
import pandas as pd

# تثبيت: pip install folium streamlit-folium
try:
    import folium
    from streamlit_folium import st_folium
    MAP_AVAILABLE = True
except:
    MAP_AVAILABLE = False
    st.warning("لتفعيل الخريطة: pip install folium streamlit-folium - أو استخدم الخريطة البديلة")

st.set_page_config(page_title="TASHEER AI - Interactive Map - 42 Countries", page_icon="🗺️", layout="wide")

WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={WALLET}"
EMAIL = "report.gomez@gmail.com"

# === إحداثيات كل الدول - خريطة تفاعلية ===
COUNTRIES_COORDS = {
    # الوطن العربي 22 دولة
    "🇸🇦 السعودية": {"lat": 23.8859, "lon": 45.0792, "code": "SA", "currency": "SAR 3.75", "capital": "الرياض"},
    "🇦🇪 الإمارات": {"lat": 23.4241, "lon": 53.8478, "code": "AE", "currency": "AED 3.67", "capital": "أبوظبي"},
    "🇶🇦 قطر": {"lat": 25.3548, "lon": 51.1839, "code": "QA", "currency": "QAR 3.64", "capital": "الدوحة"},
    "🇰🇼 الكويت": {"lat": 29.3117, "lon": 47.4818, "code": "KW", "currency": "KWD 0.31", "capital": "الكويت"},
    "🇧🇭 البحرين": {"lat": 26.0667, "lon": 50.5577, "code": "BH", "currency": "BHD 0.376", "capital": "المنامة"},
    "🇴🇲 عمان": {"lat": 21.5126, "lon": 55.9233, "code": "OM", "currency": "OMR 0.385", "capital": "مسقط"},
    "🇾🇪 اليمن": {"lat": 15.5527, "lon": 48.5164, "code": "YE", "currency": "YER 530", "capital": "صنعاء"},
    "🇯🇴 الأردن": {"lat": 31.9454, "lon": 35.9284, "code": "JO", "currency": "JOD 0.71", "capital": "عمان"},
    "🇱🇧 لبنان": {"lat": 33.8547, "lon": 35.8623, "code": "LB", "currency": "LBP 89500", "capital": "بيروت"},
    "🇮🇶 العراق": {"lat": 33.2232, "lon": 43.6793, "code": "IQ", "currency": "IQD 1310", "capital": "بغداد"},
    "🇸🇾 سوريا": {"lat": 34.8021, "lon": 38.9968, "code": "SY", "currency": "SYP 13000", "capital": "دمشق"},
    "🇵🇸 فلسطين": {"lat": 31.9522, "lon": 35.2332, "code": "PS", "currency": "ILS 3.7", "capital": "القدس"},
    "🇪🇬 مصر": {"lat": 26.8206, "lon": 30.8025, "code": "EG", "currency": "EGP 50.5", "capital": "القاهرة"},
    "🇸🇩 السودان": {"lat": 12.8628, "lon": 30.2176, "code": "SD", "currency": "SDG 600", "capital": "الخرطوم"},
    "🇸🇴 الصومال": {"lat": 5.1521, "lon": 46.1996, "code": "SO", "currency": "SOS 570", "capital": "مقديشو"},
    "🇲🇷 موريتانيا": {"lat": 21.0079, "lon": -10.9408, "code": "MR", "currency": "MRU 39.5", "capital": "نواكشوط"},
    "🇲🇦 المغرب": {"lat": 31.7917, "lon": -7.0926, "code": "MA", "currency": "MAD 10.2", "capital": "الرباط"},
    "🇩🇿 الجزائر": {"lat": 28.0339, "lon": 1.6596, "code": "DZ", "currency": "DZD 135", "capital": "الجزائر"},
    "🇹🇳 تونس": {"lat": 33.8869, "lon": 9.5375, "code": "TN", "currency": "TND 3.1", "capital": "تونس"},
    "🇱🇾 ليبيا": {"lat": 26.3351, "lon": 17.2283, "code": "LY", "currency": "LYD 4.8", "capital": "طرابلس"},
    "🇩🇯 جيبوتي": {"lat": 11.8251, "lon": 42.5903, "code": "DJ", "currency": "DJF 178", "capital": "جيبوتي"},
    "🇰🇲 جزر القمر": {"lat": -11.6455, "lon": 43.3333, "code": "KM", "currency": "KMF 450", "capital": "موروني"},
    # العالم 20 دولة
    "🇺🇸 أمريكا": {"lat": 37.0902, "lon": -95.7129, "code": "US", "currency": "USD", "capital": "واشنطن"},
    "🇬🇧 بريطانيا": {"lat": 55.3781, "lon": -3.4360, "code": "GB", "currency": "GBP", "capital": "لندن"},
    "🇪🇺 أوروبا": {"lat": 50.8503, "lon": 4.3517, "code": "EU", "currency": "EUR", "capital": "بروكسل"},
    "🇹🇷 تركيا": {"lat": 38.9637, "lon": 35.2433, "code": "TR", "currency": "TRY", "capital": "أنقرة"},
    "🇮🇳 الهند": {"lat": 20.5937, "lon": 78.9629, "code": "IN", "currency": "INR", "capital": "نيودلهي"},
    "🇵🇰 باكستان": {"lat": 30.3753, "lon": 69.3451, "code": "PK", "currency": "PKR", "capital": "إسلام آباد"},
}

USD_TO_SAR = 3.75
def convert_currencies(usd):
    return {"usd": usd, "sar": int(usd*3.75), "aed": int(usd*3.67), "mad": int(usd*10.2), "dzd": int(usd*135), "egp": int(usd*50.5), "syp": int(usd*13000), "usdt": usd}

if 'users_db' not in st.session_state:
    st.session_state['users_db'] = {"admin": {"password": "Tasheer2024!", "name": "Gomez Admin", "email": EMAIL, "sub_end": datetime.now() + timedelta(days=365), "active": True, "usd": 8000, "country": "🇸🇦 السعودية", "role": "admin"}}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'show_landing' not in st.session_state:
    st.session_state['show_landing'] = True
if 'lang' not in st.session_state:
    st.session_state['lang'] = 'ar'

# زر اللغة
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
        <h1 style="font-size:42px; margin:0;">🗺️ TASHEER AI - Interactive Global Map</h1>
        <h2 style="font-size:22px; margin:10px 0;">{"نغطي كل الوطن العربي والعالم - خريطة تفاعلية" if lang=='ar' else "Cover All Arab World & Global - Interactive Map"}</h2>
        <p style="font-size:12px;">🌐 42 دولة | 27 عملة | 📍 خريطة تفاعلية | tasheer-ai.com | 00966540450738</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"### {'🗺️ الخريطة التفاعلية - اضغط على أي دولة' if lang=='ar' else '🗺️ Interactive Map - Click Any Country'}")
    
    if MAP_AVAILABLE:
        # === خريطة Folium تفاعلية ===
        m = folium.Map(location=[25, 20], zoom_start=2.5, tiles="OpenStreetMap")
        
        # أضف كل الدول
        for country_name, data in COUNTRIES_COORDS.items():
            is_arab = data['code'] in ["SA","AE","QA","KW","BH","OM","YE","JO","LB","IQ","SY","PS","EG","SD","SO","MR","MA","DZ","TN","LY","DJ","KM"]
            color = "green" if is_arab else "blue"
            icon_color = "darkgreen" if is_arab else "darkblue"
            
            popup_html = f"""
            <div style="font-family: Arial; direction: rtl; text-align: center; min-width: 200px;">
                <h3 style="margin:0; color:{icon_color};">{country_name}</h3>
                <p style="margin:5px 0;"><b>Code:</b> {data['code']}<br>
                <b>Capital:</b> {data['capital']}<br>
                <b>Currency:</b> {data['currency']}<br>
                <b>Lat/Lon:</b> {data['lat']:.2f}, {data['lon']:.2f}</p>
                <p style="background:#0a7a42; color:white; padding:5px 10px; border-radius:15px; font-size:11px;">TASHEER AI - {data['code']} Supported ✅</p>
                <p style="font-size:10px;">💳 USDT: TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH</p>
            </div>
            """
            
            folium.Marker(
                location=[data['lat'], data['lon']],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{country_name} - {data['code']} - {data['currency']}",
                icon=folium.Icon(color=color, icon="flag" if is_arab else "globe", prefix="fa")
            ).add_to(m)
        
        # عرض الخريطة
        map_data = st_folium(m, width=None, height=500, returned_objects=["last_object_clicked"])
        
        if map_data["last_object_clicked"]:
            clicked = map_data["last_object_clicked"]
            st.success(f"📍 اخترت: Lat {clicked['lat']:.2f}, Lon {clicked['lng']:.2f} - أقرب دولة: {min(COUNTRIES_COORDS.items(), key=lambda x: abs(x[1]['lat']-clicked['lat'])+abs(x[1]['lon']-clicked['lng']))[0]}")
    else:
        # === خريطة بديلة باستخدام st.map ===
        st.info("🗺️ خريطة بديلة - تظهر كل الدول")
        df = pd.DataFrame([
            {"lat": data["lat"], "lon": data["lon"], "country": name, "code": data["code"], "currency": data["currency"]}
            for name, data in COUNTRIES_COORDS.items()
        ])
        st.map(df, latitude="lat", longitude="lon", size=20, color="#0a7a42")
        st.dataframe(df, use_container_width=True)
        
        # خريطة ثانية تفاعلية بالأعلام
        st.markdown("#### 🌍 كل الدول على الخريطة")
        selected_country = st.selectbox("اختر دولة لعرضها على الخريطة" if lang=='ar' else "Select Country to View on Map", list(COUNTRIES_COORDS.keys()))
        if selected_country:
            data = COUNTRIES_COORDS[selected_country]
            st.markdown(f"""
            <div style="background:white; border:2px solid #0a7a42; padding:15px; border-radius:15px; text-align:center;">
                <h2>{selected_country}</h2>
                <p><b>Code:</b> {data['code']} | <b>Capital:</b> {data['capital']} | <b>Currency:</b> {data['currency']}</p>
                <p><b>Coordinates:</b> {data['lat']}, {data['lon']}</p>
                <p style="background:#0a7a42; color:white; padding:8px; border-radius:10px;">✅ {selected_country} Supported - TASHEER AI</p>
            </div>
            """, unsafe_allow_html=True)
            df_single = pd.DataFrame([{"lat": data["lat"], "lon": data["lon"]}])
            st.map(df_single, zoom=4)
    
    st.markdown("---")
    st.markdown(f"### {'🌍 نغطي كل الوطن العربي - 22 دولة' if lang=='ar' else '🌍 Arab World Coverage - 22 Countries'}")
    st.markdown("**SA AE QA KW BH OM YE JO LB IQ SY PS EG SD SO MR MA DZ TN LY DJ KM**")
    st.markdown("السعودية - الإمارات - قطر - الكويت - البحرين - عمان - اليمن - الأردن - لبنان - العراق - سوريا - فلسطين - مصر - السودان - الصومال - موريتانيا - المغرب - الجزائر - تونس - ليبيا - جيبوتي - جزر القمر")
    
    st.markdown(f"### {'🌐 نغطي العالم - 20 دولة' if lang=='ar' else '🌐 Global Coverage - 20 Countries'}")
    st.markdown("**US GB EU TR IN PK BD PH ID NG ET KE ZA BR CA AU CN RU MY SG**")
    st.markdown("أمريكا - بريطانيا - أوروبا - تركيا - الهند - باكستان - بنغلاديش - الفلبين - إندونيسيا - نيجيريا - إثيوبيا - كينيا - جنوب أفريقيا - البرازيل - كندا - أستراليا - الصين - روسيا - ماليزيا - سنغافورة")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 دخول للمنصة - مع الخريطة التفاعلية" if lang=='ar' else "🚀 Enter Platform - With Interactive Map", type="primary", use_container_width=True):
            st.session_state['show_landing'] = False
            st.rerun()
        st.markdown(f"""
        <div style="text-align:center; margin-top:15px;">
            <p>📱 00966540450738 | ✉️ {EMAIL} | 🌐 tasheer-ai.com</p>
            <p style="font-size:10px;">TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH - USDT TRC20</p>
            <a href="https://wa.me/966540450738" target="_blank" style="background:#25D366; color:white; padding:10px 20px; border-radius:25px; text-decoration:none; font-weight:700; display:inline-block; margin-top:10px;">💬 تواصل واتساب - مع الخريطة</a>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# === بعد الدخول - مع الخريطة ===
db = st.session_state['users_db']
if not st.session_state['logged_in']:
    st.markdown("### 🔐 دخول - مع خريطة تفاعلية")
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
days_left = (user["sub_end"] - datetime.now()).days

st.success(f"✅ {user['name']} - باقي {days_left} يوم - مع خريطة تفاعلية 42 دولة")

tab1, tab2, tab3 = st.tabs(["🗺️ الخريطة التفاعلية", "🌍 كل الدول", "💳 تجديد"])

with tab1:
    st.markdown("### 🗺️ خريطة تفاعلية - 42 دولة - اضغط على أي دولة")
    
    if MAP_AVAILABLE:
        m = folium.Map(location=[25, 20], zoom_start=2, tiles="CartoDB positron")
        for country_name, data in COUNTRIES_COORDS.items():
            is_arab = data['code'] in ["SA","AE","QA","KW","BH","OM","YE","JO","LB","IQ","SY","PS","EG","SD","SO","MR","MA","DZ","TN","LY","DJ","KM"]
            color = "green" if is_arab else "blue"
            folium.Marker(
                location=[data['lat'], data['lon']],
                popup=f"{country_name}<br>Code: {data['code']}<br>Currency: {data['currency']}<br>Capital: {data['capital']}<br>TASHEER AI Supported ✅",
                tooltip=f"{country_name} - {data['code']}",
                icon=folium.Icon(color=color, icon="flag")
            ).add_to(m)
        st_folium(m, width=None, height=500)
    else:
        df = pd.DataFrame([{"lat": v["lat"], "lon": v["lon"], "country": k} for k, v in COUNTRIES_COORDS.items()])
        st.map(df)
        st.dataframe(df, use_container_width=True)

with tab2:
    st.markdown("### 🌍 كل الدول - 42 دولة - عربي وعالمي")
    for name, data in COUNTRIES_COORDS.items():
        st.markdown(f"**{name}** - {data['code']} - {data['capital']} - {data['currency']} - {data['lat']:.2f}, {data['lon']:.2f}")

with tab3:
    st.code(WALLET)
    st.image(QR_URL)
    if st.button("🏠 رجوع للخريطة التفاعلية"):
        st.session_state['show_landing'] = True
        st.rerun()

if st.button("🚪 خروج"):
    st.session_state['logged_in'] = False
    st.session_state['show_landing'] = True
    st.rerun()
