import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import random

# === Try Import Map ===
try:
    import folium
    from streamlit_folium import st_folium
    MAP_AVAILABLE = True
except:
    MAP_AVAILABLE = False

st.set_page_config(page_title="TASHEER AI - Auto Launch", page_icon="🚀", layout="wide")

WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={WALLET}"

# === 26 دولة ===
COUNTRIES_COORDS = {
    "🇸🇦 السعودية": {"lat": 23.8859, "lon": 45.0792, "code": "SA", "currency": "SAR 3.75", "capital": "الرياض", "search": "saudi السعودية sa"},
    "🇦🇪 الإمارات": {"lat": 23.4241, "lon": 53.8478, "code": "AE", "currency": "AED 3.67", "capital": "أبوظبي", "search": "uae الإمارات ae"},
    "🇶🇦 قطر": {"lat": 25.3548, "lon": 51.1839, "code": "QA", "currency": "QAR 3.64", "capital": "الدوحة", "search": "qatar قطر qa"},
    "🇰🇼 الكويت": {"lat": 29.3117, "lon": 47.4818, "code": "KW", "currency": "KWD 0.31", "capital": "الكويت", "search": "kuwait الكويت kw"},
    "🇧🇭 البحرين": {"lat": 26.0667, "lon": 50.5577, "code": "BH", "currency": "BHD 0.376", "capital": "المنامة", "search": "bahrain البحرين bh"},
    "🇴🇲 عمان": {"lat": 21.5126, "lon": 55.9233, "code": "OM", "currency": "OMR 0.385", "capital": "مسقط", "search": "oman عمان om"},
    "🇾🇪 اليمن": {"lat": 15.5527, "lon": 48.5164, "code": "YE", "currency": "YER 530", "capital": "صنعاء", "search": "yemen اليمن ye"},
    "🇯🇴 الأردن": {"lat": 31.9454, "lon": 35.9284, "code": "JO", "currency": "JOD 0.71", "capital": "عمان", "search": "jordan الأردن jo"},
    "🇱🇧 لبنان": {"lat": 33.8547, "lon": 35.8623, "code": "LB", "currency": "LBP 89500", "capital": "بيروت", "search": "lebanon لبنان lb"},
    "🇮🇶 العراق": {"lat": 33.2232, "lon": 43.6793, "code": "IQ", "currency": "IQD 1310", "capital": "بغداد", "search": "iraq العراق iq"},
    "🇸🇾 سوريا": {"lat": 34.8021, "lon": 38.9968, "code": "SY", "currency": "SYP 13000", "capital": "دمشق", "search": "syria سوريا sy"},
    "🇵🇸 فلسطين": {"lat": 31.9522, "lon": 35.2332, "code": "PS", "currency": "ILS 3.7", "capital": "القدس", "search": "palestine فلسطين ps"},
    "🇪🇬 مصر": {"lat": 26.8206, "lon": 30.8025, "code": "EG", "currency": "EGP 50.5", "capital": "القاهرة", "search": "egypt مصر eg"},
    "🇸🇩 السودان": {"lat": 12.8628, "lon": 30.2176, "code": "SD", "currency": "SDG 600", "capital": "الخرطوم", "search": "sudan السودان sd"},
    "🇲🇷 موريتانيا": {"lat": 21.0079, "lon": -10.9408, "code": "MR", "currency": "MRU 39.5", "capital": "نواكشوط", "search": "mauritania موريتانيا mr"},
    "🇲🇦 المغرب": {"lat": 31.7917, "lon": -7.0926, "code": "MA", "currency": "MAD 10.2", "capital": "الرباط", "search": "morocco المغرب ma maroc"},
    "🇩🇿 الجزائر": {"lat": 28.0339, "lon": 1.6596, "code": "DZ", "currency": "DZD 135", "capital": "الجزائر", "search": "algeria الجزائر dz"},
    "🇹🇳 تونس": {"lat": 33.8869, "lon": 9.5375, "code": "TN", "currency": "TND 3.1", "capital": "تونس", "search": "tunisia تونس tn"},
    "🇱🇾 ليبيا": {"lat": 26.3351, "lon": 17.2283, "code": "LY", "currency": "LYD 4.8", "capital": "طرابلس", "search": "libya ليبيا ly"},
    "🇺🇸 أمريكا": {"lat": 37.0902, "lon": -95.7129, "code": "US", "currency": "USD", "capital": "واشنطن", "search": "usa america أمريكا us"},
    "🇬🇧 بريطانيا": {"lat": 55.3781, "lon": -3.4360, "code": "GB", "currency": "GBP", "capital": "لندن", "search": "uk بريطانيا gb"},
    "🇪🇺 أوروبا": {"lat": 50.8503, "lon": 4.3517, "code": "EU", "currency": "EUR", "capital": "بروكسل", "search": "europe أوروبا eu"},
    "🇹🇷 تركيا": {"lat": 38.9637, "lon": 35.2433, "code": "TR", "currency": "TRY", "capital": "أنقرة", "search": "turkey تركيا tr"},
    "🇮🇳 الهند": {"lat": 20.5937, "lon": 78.9629, "code": "IN", "currency": "INR", "capital": "نيودلهي", "search": "india الهند in"},
    "🇵🇰 باكستان": {"lat": 30.3753, "lon": 69.3451, "code": "PK", "currency": "PKR", "capital": "إسلام آباد", "search": "pakistan باكستان pk"},
}

# === Database ===
if 'users_db' not in st.session_state:
    st.session_state['users_db'] = {
        "admin": {"password": "Tasheer2024!", "name": "Gomez Admin", "email": "report.gomez@gmail.com", "sub_end": datetime.now() + timedelta(days=365), "role": "admin", "active": True}
    }
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'show_landing' not in st.session_state:
    st.session_state['show_landing'] = True
if 'search_center' not in st.session_state:
    st.session_state['search_center'] = [25, 20]
if 'search_zoom' not in st.session_state:
    st.session_state['search_zoom'] = 2.5
if 'selected_country_search' not in st.session_state:
    st.session_state['selected_country_search'] = None

# === FIX: Get client param safely - بدون NameError ===
client_view = ""
try:
    # الطريقة الجديدة
    client_view = st.query_params.get("client", "")
except:
    try:
        # الطريقة القديمة
        params = st.experimental_get_query_params()
        client_view = params.get("client", [""])[0]
    except:
        client_view = ""

# === Language ===
c1, c2, c3 = st.columns([6,2,2])
with c2:
    if st.button("🇸🇦 عربي", use_container_width=True):
        st.session_state['show_landing'] = True
with c3:
    if st.button("🇺🇸 English", use_container_width=True):
        st.session_state['show_landing'] = True

def search_countries(query):
    if not query:
        return []
    query = query.lower()
    results = []
    for name, data in COUNTRIES_COORDS.items():
        if query in name.lower() or query in data['search'].lower() or query in data['code'].lower():
            results.append((name, data))
    return results

def check_payment_auto(tx_hash):
    return len(tx_hash.strip()) >= 10

# === LANDING + AUTO LAUNCH ===
if st.session_state['show_landing'] and not st.session_state['logged_in']:
    
    # إذا دخل برابط شركة
    if client_view:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg,#0a7a42,#0d4a2a); color:white; padding:25px; border-radius:20px; text-align:center; margin-bottom:20px;">
            <h1>🏢 موقع {client_view} الخاص</h1>
            <p>Powered by TASHEER AI | 26 دولة | 27 عملة | خريطة MA DZ SA</p>
            <p>رابطك: tasheer-ai.com/?client={client_view}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg,#0a7a42,#0d4a2a); color:white; padding:30px 20px; border-radius:20px; text-align:center;">
            <h1>🚀 TASHEER AI - Auto Launch</h1>
            <h3>سجل - ادفع - انطلق - بدون ما ترجع لنا</h3>
            <p>🌐 26 دولة | 🔍 بحث MA DZ SA EG | 💱 27 عملة | tasheer-ai.com</p>
        </div>
        """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🚀 تسجيل أوتوماتيك", "🗺️ خريطة + بحث", "🔑 دخول"])
    
    with tab1:
        st.markdown("### 🚀 سجل وانطلق مباشرة - موقعك يشتغل لحاله")
        col_a, col_b = st.columns([2,1])
        with col_a:
            username = st.text_input("اختر اسم شركتك / يوزرك - سيكون رابطك الخاص", placeholder="مثال: almajal - سيكون رابطك tasheer-ai.com/?client=almajal", key="auto_user")
            email = st.text_input("ايميلك الرسمي - نرسل لك التفاصيل", placeholder="info@company.com", key="auto_email")
            password = st.text_input("اختر باسورد - انت تحدده", type="password", key="auto_pass")
            package = st.selectbox("الباقة", ["شهر $299 - 1121 SAR - 100 حساب - أوتوماتيك", "3 أشهر $1500 - 5625 SAR", "سنة $8000 - 30,000 SAR - VIP"], key="auto_pack")
            
            st.markdown("#### 💳 حول على المحفظة - USDT TRC20")
            st.code(WALLET)
            st.image(QR_URL, width=200)
            
            tx = st.text_input("الصق TxID - رقم العملية من محفظتك بعد التحويل", placeholder="a1b2c3d4e5f6f7...", key="auto_tx")

            if st.button("✅ تحققت من الدفع - فعل حسابي الآن أوتوماتيك", type="primary", use_container_width=True):
                if username and email and password and tx:
                    if check_payment_auto(tx):
                        days = 30 if "شهر" in package else (90 if "3 أشهر" in package else 365)
                        usd_val = 299 if "شهر" in package else (1500 if "3 أشهر" in package else 8000)
                        st.session_state['users_db'][username] = {
                            "password": password, "name": username, "email": email,
                            "sub_end": datetime.now() + timedelta(days=days),
                            "active": True, "role": "user", "tx": tx,
                            "link": f"tasheer-ai.com/?client={username}",
                            "usd": usd_val,
                            "auto": True,
                            "join": datetime.now().strftime('%Y-%m-%d %H:%M')
                        }
                        st.success(f"✅ تم! حسابك مفعل أوتوماتيك - بدون ما ترجع لنا!")
                        st.info(f"🔗 رابطك الخاص: tasheer-ai.com/?client={username}")
                        st.info(f"👤 يوزر: {username} | باسورد: {password}")
                        st.info(f"📧 ايميلك: {email}")
                        st.balloons()
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = username
                        st.session_state['show_landing'] = False
                        st.rerun()
                    else:
                        st.error("❌ TxID غير صحيح - انسخه من محفظة USDT بعد التحويل - على الأقل 10 أحرف")
                else:
                    st.error("املأ كل الحقول")
        
        with col_b:
            st.markdown("""
            **🎯 كيف يطلق موقعك بدون ما ترجع لي؟**
            
            **القديم:**
            تحول > ترسل صورة واتساب > أنتظر أنا أفعل > أرسل لك يوزر
            
            **الجديد - أوتوماتيك:**
            1. تحول USDT
            2. تنسخ TxID
            3. تلصقه هنا
            4. تنطلق مباشرة - 10 ثواني
            
            **مميزاتك بعد التفعيل:**
            - 🔗 رابطك: tasheer-ai.com/?client=اسمك
            - 🗺️ خريطة MA DZ SA EG بحث
            - 💱 27 عملة
            - 👥 100 حساب
            - 📊 تقارير
            - 🔄 تجديد أوتوماتيك
            
            **بدون واتساب - بدون انتظار**
            
            **📱 دعم: 00966540450738**
            """)
            if client_view:
                st.success(f"🏢 أنت الآن في موقع {client_view}")
    
    with tab2:
        st.markdown("### 🔍 ابحث - MA DZ SA EG - وانتقل مباشرة")
        col_search1, col_search2 = st.columns([3,1])
        with col_search1:
            search_query = st.text_input("🔍 بحث", placeholder="مثال: السعودية أو Saudi أو SA أو المغرب أو Morocco أو MA أو DZ أو EG", label_visibility="collapsed", key="search_q")
        with col_search2:
            if st.button("🗺️ كل الدول", use_container_width=True, key="all_countries"):
                st.session_state['search_center'] = [25, 20]
                st.session_state['search_zoom'] = 2.5
                st.session_state['selected_country_search'] = None
                st.rerun()
        
        if search_query:
            results = search_countries(search_query)
            if results:
                st.success(f"✅ وجدنا {len(results)} دولة لـ '{search_query}'")
                cols = st.columns(min(len(results), 3))
                for idx, (name, data) in enumerate(results):
                    with cols[idx % 3]:
                        if st.button(f"📍 {name}\n{data['code']}", key=f"search_{name}", use_container_width=True):
                            st.session_state['search_center'] = [data['lat'], data['lon']]
                            st.session_state['search_zoom'] = 6
                            st.session_state['selected_country_search'] = name
                            st.rerun()
            else:
                st.warning(f"❌ لم نجد '{search_query}' - جرب SA MA DZ EG")
        
        # اختيار سريع
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
        
        if st.session_state['selected_country_search']:
            data = COUNTRIES_COORDS[st.session_state['selected_country_search']]
            st.markdown(f"""
            <div style="background:#e8f5e9; border:2px solid #0a7a42; padding:10px; border-radius:15px; text-align:center;">
                <h3 style="margin:0; color:#0a7a42;">📍 {st.session_state['selected_country_search']} - {data['code']} - {data['currency']}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        if MAP_AVAILABLE:
            m = folium.Map(location=st.session_state['search_center'], zoom_start=st.session_state['search_zoom'], tiles="OpenStreetMap")
            for country_name, data in COUNTRIES_COORDS.items():
                is_selected = country_name == st.session_state['selected_country_search']
                color = "red" if is_selected else "green"
                folium.Marker(
                    location=[data['lat'], data['lon']],
                    popup=f"{country_name} - {data['code']} - {data['currency']}",
                    tooltip=f"{'⭐ ' if is_selected else ''}{country_name}",
                    icon=folium.Icon(color=color, icon="star" if is_selected else "flag", prefix="fa")
                ).add_to(m)
            if st.session_state['selected_country_search']:
                data = COUNTRIES_COORDS[st.session_state['selected_country_search']]
                folium.Circle(location=[data['lat'], data['lon']], radius=200000, color="red", fill=True, fill_opacity=0.2).add_to(m)
            st_folium(m, width=None, height=400)
        else:
            df = pd.DataFrame([{"lat": v["lat"], "lon": v["lon"]} for v in COUNTRIES_COORDS.values()])
            st.map(df)
    
    with tab3:
        with st.form("login_form"):
            u = st.text_input("اسم المستخدم")
            p = st.text_input("كلمة المرور", type="password")
            if st.form_submit_button("دخول", type="primary", use_container_width=True):
                db = st.session_state['users_db']
                if u in db and db[u]["password"] == p:
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = u
                    st.session_state['show_landing'] = False
                    st.rerun()
                else:
                    st.error("خطأ")
    st.stop()

# === LOGGED IN ===
st.success(f"✅ مرحبا {st.session_state['username']} - موقعك: tasheer-ai.com/?client={st.session_state['username']} - أوتوماتيك")
st.info(f"🔗 رابطك الخاص: https://tasheer-ai-juub2hzyqf9boqzthpwv4n.streamlit.app/?client={st.session_state['username']}")

if st.button("🚪 خروج"):
    st.session_state['logged_in'] = False
    st.session_state['show_landing'] = True
    st.rerun()

if st.session_state['username'] == "admin":
    st.markdown("### 📊 لوحة الأدمن - العملاء الأوتوماتيك")
    db = st.session_state['users_db']
    rows = []
    for uname, data in db.items():
        rows.append({
            "User": uname,
            "Email": data.get("email",""),
            "Role": data.get("role","user"),
            "USD": data.get("usd",0),
            "Auto": "✅ أوتوماتيك" if data.get("auto") else "يدوي",
            "TxID": data.get("tx","")[:15] + "..." if data.get("tx") else "",
            "Link": data.get("link",""),
            "End": data.get("sub_end").strftime('%Y-%m-%d') if isinstance(data.get("sub_end"), datetime) else str(data.get("sub_end",""))
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
    st.metric("إجمالي العملاء", len(db)-1)
    st.metric("إجمالي $", sum([d.get("usd",0) for d in db.values()]))
