import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
try:
    import folium
    from streamlit_folium import st_folium
    MAP_AVAILABLE = True
except:
    MAP_AVAILABLE = False

st.set_page_config(page_title="TASHEER AI - Map Search", page_icon="🔍", layout="wide")

WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={WALLET}"
EMAIL = "report.gomez@gmail.com"

COUNTRIES_COORDS = {
    "🇸🇦 السعودية": {"lat": 23.8859, "lon": 45.0792, "code": "SA", "currency": "SAR 3.75", "capital": "الرياض", "search": "saudi saud السعودية sa"},
    "🇦🇪 الإمارات": {"lat": 23.4241, "lon": 53.8478, "code": "AE", "currency": "AED 3.67", "capital": "أبوظبي", "search": "uae emirates الإمارات ae dubai"},
    "🇶🇦 قطر": {"lat": 25.3548, "lon": 51.1839, "code": "QA", "currency": "QAR 3.64", "capital": "الدوحة", "search": "qatar قطر qa"},
    "🇰🇼 الكويت": {"lat": 29.3117, "lon": 47.4818, "code": "KW", "currency": "KWD 0.31", "capital": "الكويت", "search": "kuwait الكويت kw"},
    "🇧🇭 البحرين": {"lat": 26.0667, "lon": 50.5577, "code": "BH", "currency": "BHD 0.376", "capital": "المنامة", "search": "bahrain البحرين bh"},
    "🇴🇲 عمان": {"lat": 21.5126, "lon": 55.9233, "code": "OM", "currency": "OMR 0.385", "capital": "مسقط", "search": "oman عمان om"},
    "🇾🇪 اليمن": {"lat": 15.5527, "lon": 48.5164, "code": "YE", "currency": "YER 530", "capital": "صنعاء", "search": "yemen اليمن ye"},
    "🇯🇴 الأردن": {"lat": 31.9454, "lon": 35.9284, "code": "JO", "currency": "JOD 0.71", "capital": "عمان", "search": "jordan الأردن jo"},
    "🇱🇧 لبنان": {"lat": 33.8547, "lon": 35.8623, "code": "LB", "currency": "LBP 89500", "capital": "بيروت", "search": "lebanon لبنان lb"},
    "🇮🇶 العراق": {"lat": 33.2232, "lon": 43.6793, "code": "IQ", "currency": "IQD 1310", "capital": "بغداد", "search": "iraq العراق iq baghdad"},
    "🇸🇾 سوريا": {"lat": 34.8021, "lon": 38.9968, "code": "SY", "currency": "SYP 13000", "capital": "دمشق", "search": "syria سوريا sy"},
    "🇵🇸 فلسطين": {"lat": 31.9522, "lon": 35.2332, "code": "PS", "currency": "ILS 3.7", "capital": "القدس", "search": "palestine فلسطين ps"},
    "🇪🇬 مصر": {"lat": 26.8206, "lon": 30.8025, "code": "EG", "currency": "EGP 50.5", "capital": "القاهرة", "search": "egypt مصر eg cairo"},
    "🇸🇩 السودان": {"lat": 12.8628, "lon": 30.2176, "code": "SD", "currency": "SDG 600", "capital": "الخرطوم", "search": "sudan السودان sd"},
    "🇸🇴 الصومال": {"lat": 5.1521, "lon": 46.1996, "code": "SO", "currency": "SOS 570", "capital": "مقديشو", "search": "somalia الصومال so"},
    "🇲🇷 موريتانيا": {"lat": 21.0079, "lon": -10.9408, "code": "MR", "currency": "MRU 39.5", "capital": "نواكشوط", "search": "mauritania موريتانيا mr"},
    "🇲🇦 المغرب": {"lat": 31.7917, "lon": -7.0926, "code": "MA", "currency": "MAD 10.2", "capital": "الرباط", "search": "morocco المغرب ma maroc"},
    "🇩🇿 الجزائر": {"lat": 28.0339, "lon": 1.6596, "code": "DZ", "currency": "DZD 135", "capital": "الجزائر", "search": "algeria الجزائر dz algiers"},
    "🇹🇳 تونس": {"lat": 33.8869, "lon": 9.5375, "code": "TN", "currency": "TND 3.1", "capital": "تونس", "search": "tunisia تونس tn"},
    "🇱🇾 ليبيا": {"lat": 26.3351, "lon": 17.2283, "code": "LY", "currency": "LYD 4.8", "capital": "طرابلس", "search": "libya ليبيا ly"},
    "🇺🇸 أمريكا": {"lat": 37.0902, "lon": -95.7129, "code": "US", "currency": "USD", "capital": "واشنطن", "search": "usa america أمريكا us washington"},
    "🇬🇧 بريطانيا": {"lat": 55.3781, "lon": -3.4360, "code": "GB", "currency": "GBP", "capital": "لندن", "search": "uk britain بريطانيا gb london"},
    "🇪🇺 أوروبا": {"lat": 50.8503, "lon": 4.3517, "code": "EU", "currency": "EUR", "capital": "بروكسل", "search": "europe أوروبا eu schengen"},
    "🇹🇷 تركيا": {"lat": 38.9637, "lon": 35.2433, "code": "TR", "currency": "TRY", "capital": "أنقرة", "search": "turkey تركيا tr"},
    "🇮🇳 الهند": {"lat": 20.5937, "lon": 78.9629, "code": "IN", "currency": "INR", "capital": "نيودلهي", "search": "india الهند in"},
    "🇵🇰 باكستان": {"lat": 30.3753, "lon": 69.3451, "code": "PK", "currency": "PKR", "capital": "إسلام آباد", "search": "pakistan باكستان pk"},
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
if 'search_center' not in st.session_state:
    st.session_state['search_center'] = [25, 20]
if 'search_zoom' not in st.session_state:
    st.session_state['search_zoom'] = 2.5
if 'selected_country_search' not in st.session_state:
    st.session_state['selected_country_search'] = None

c1, c2, c3 = st.columns([6,2,2])
with c2:
    if st.button("🇸🇦 عربي", use_container_width=True, type="primary" if st.session_state['lang']=='ar' else "secondary"):
        st.session_state['lang'] = 'ar'
        st.rerun()
with c3:
    if st.button("🇺🇸 English", use_container_width=True, type="primary" if st.session_state['lang']=='en' else "secondary"):
        st.session_state['lang'] = 'en'
        st.rerun()

def search_countries(query):
    if not query:
        return []
    query = query.lower()
    results = []
    for name, data in COUNTRIES_COORDS.items():
        if query in name.lower() or query in data['search'].lower() or query in data['code'].lower() or query in data['capital'].lower():
            results.append((name, data))
    return results

if st.session_state['show_landing'] and not st.session_state['logged_in']:
    lang = st.session_state['lang']
    st.markdown(f"""
    <div style="background: linear-gradient(135deg,#0a7a42,#0d4a2a); color:white; padding:30px 20px; border-radius:20px; text-align:center;">
        <h1 style="margin:0;">🔍🗺️ TASHEER AI - Map Search</h1>
        <h3>{"ابحث عن أي دولة وانتقل لها مباشرة على الخريطة" if lang=='ar' else "Search Any Country & Go Directly On Map"}</h3>
        <p>🌐 26 دولة | 🔍 بحث ذكي عربي + إنجليزي | tasheer-ai.com</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"### {'🔍 ابحث عن دولة - عربي أو إنجليزي أو كود' if lang=='ar' else '🔍 Search Country - Arabic or English or Code'}")
    
    col_search1, col_search2 = st.columns([3,1])
    with col_search1:
        search_query = st.text_input("🔍 بحث" if lang=='ar' else "🔍 Search", placeholder="مثال: السعودية أو Saudi أو SA أو المغرب أو Morocco أو MA أو مصر أو Egypt...", label_visibility="collapsed")
    with col_search2:
        if st.button("🗺️ كل الدول" if lang=='ar' else "🗺️ All Countries", use_container_width=True):
            st.session_state['search_center'] = [25, 20]
            st.session_state['search_zoom'] = 2.5
            st.session_state['selected_country_search'] = None
            st.rerun()
    
    # نتائج البحث
    if search_query:
        results = search_countries(search_query)
        if results:
            st.success(f"✅ {'وجدنا' if lang=='ar' else 'Found'} {len(results)} {'دولة' if lang=='ar' else 'countries'} لـ '{search_query}'")
            cols = st.columns(min(len(results), 3))
            for idx, (name, data) in enumerate(results):
                with cols[idx % 3]:
                    if st.button(f"📍 {name}\n{data['code']} - {data['capital']}", key=f"search_{name}", use_container_width=True):
                        st.session_state['search_center'] = [data['lat'], data['lon']]
                        st.session_state['search_zoom'] = 6
                        st.session_state['selected_country_search'] = name
                        st.rerun()
        else:
            st.warning(f"❌ {'لم نجد' if lang=='ar' else 'No results for'} '{search_query}' - {'جرب: السعودية، SA، Morocco، Egypt، MA' if lang=='ar' else 'Try: Saudi, SA, Morocco, Egypt, MA'}")
    
    # اختيار سريع
    st.markdown(f"**{'⚡ اختيار سريع:' if lang=='ar' else '⚡ Quick Select:'}**")
    quick_cols = st.columns(6)
    quick_countries = ["🇸🇦 السعودية", "🇲🇦 المغرب", "🇩🇿 الجزائر", "🇪🇬 مصر", "🇦🇪 الإمارات", "🇺🇸 أمريكا"]
    for idx, qc in enumerate(quick_countries):
        with quick_cols[idx]:
            if st.button(qc, key=f"quick_{qc}", use_container_width=True):
                data = COUNTRIES_COORDS[qc]
                st.session_state['search_center'] = [data['lat'], data['lon']]
                st.session_state['search_zoom'] = 6
                st.session_state['selected_country_search'] = qc
                st.rerun()
    
    st.markdown("---")
    st.markdown(f"### 🗺️ {'الخريطة التفاعلية' if lang=='ar' else 'Interactive Map'} {'- ' + st.session_state['selected_country_search'] if st.session_state['selected_country_search'] else ''}")
    
    if st.session_state['selected_country_search']:
        data = COUNTRIES_COORDS[st.session_state['selected_country_search']]
        st.markdown(f"""
        <div style="background:#e8f5e9; border:2px solid #0a7a42; padding:15px; border-radius:15px; text-align:center; margin-bottom:10px;">
            <h2 style="margin:0; color:#0a7a42;">📍 {st.session_state['selected_country_search']}</h2>
            <p style="margin:5px 0;"><b>Code:</b> {data['code']} | <b>Capital:</b> {data['capital']} | <b>Currency:</b> {data['currency']} | <b>Lat/Lon:</b> {data['lat']:.2f}, {data['lon']:.2f}</p>
            <p style="background:#0a7a42; color:white; padding:5px 15px; border-radius:20px; display:inline-block; font-size:12px;">✅ TASHEER AI Supported - {data['code']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    if MAP_AVAILABLE:
        m = folium.Map(location=st.session_state['search_center'], zoom_start=st.session_state['search_zoom'], tiles="OpenStreetMap")
        
        for country_name, data in COUNTRIES_COORDS.items():
            is_arab = data['code'] in ["SA","AE","QA","KW","BH","OM","YE","JO","LB","IQ","SY","PS","EG","SD","SO","MR","MA","DZ","TN","LY"]
            is_selected = country_name == st.session_state['selected_country_search']
            
            color = "red" if is_selected else ("green" if is_arab else "blue")
            
            popup_html = f"""
            <div style='text-align:center; font-family: Arial; min-width:200px;'>
                <h3 style='color:{"red" if is_selected else "#0a7a42"}; margin:0;'>{country_name} {"⭐ SELECTED" if is_selected else ""}</h3>
                <p><b>Code:</b> {data['code']}<br><b>Capital:</b> {data['capital']}<br><b>Currency:</b> {data['currency']}</p>
                <p style='background:{"#d32f2f" if is_selected else "#0a7a42"}; color:white; padding:5px; border-radius:10px;'>✅ Supported</p>
            </div>
            """
            
            folium.Marker(
                location=[data['lat'], data['lon']],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{'⭐ ' if is_selected else ''}{country_name} - {data['code']} - {data['currency']}",
                icon=folium.Icon(color=color, icon="flag" if not is_selected else "star", prefix="fa")
            ).add_to(m)
        
        # دائرة حول الدولة المحددة
        if st.session_state['selected_country_search']:
            data = COUNTRIES_COORDS[st.session_state['selected_country_search']]
            folium.Circle(
                location=[data['lat'], data['lon']],
                radius=200000,
                color="red",
                fill=True,
                fill_color="red",
                fill_opacity=0.2,
                popup=f"📍 {st.session_state['selected_country_search']}"
            ).add_to(m)
        
        st_folium(m, width=None, height=550)
    else:
        df = pd.DataFrame([{"lat": v["lat"], "lon": v["lon"], "country": k} for k, v in COUNTRIES_COORDS.items()])
        st.map(df)
        if st.session_state['selected_country_search']:
            data = COUNTRIES_COORDS[st.session_state['selected_country_search']]
            st.map(pd.DataFrame([{"lat": data["lat"], "lon": data["lon"]}] ), zoom=6)
    
    st.markdown("**SA AE QA KW BH OM YE JO LB IQ SY PS EG SD SO MR MA DZ TN LY | US GB EU TR IN PK**")
    
    if st.button("🚀 دخول للمنصة - مع البحث", type="primary", use_container_width=True):
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
    if st.button("🏠 الموقع الرئيسي مع البحث"):
        st.session_state['show_landing'] = True
        st.rerun()
    st.stop()

st.success(f"✅ مع بحث الخريطة - {st.session_state.get('selected_country_search','كل الدول')}")
if st.button("🚪 خروج"):
    st.session_state['logged_in'] = False
    st.session_state['show_landing'] = True
    st.rerun()
