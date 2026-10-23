import streamlit as st
from datetime import datetime, timedelta
import random
from io import BytesIO
try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except:
    PDF_AVAILABLE = False

st.set_page_config(page_title="TASHEER AI - Bilingual - 20 Currencies", page_icon="🌐", layout="wide")

WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={WALLET}"
EMAIL = "report.gomez@gmail.com"

USD_TO_SAR = 3.75
USD_TO_AED = 3.67
USD_TO_EGP = 50.5
USD_TO_KWD = 0.31
USD_TO_BHD = 0.376
USD_TO_QAR = 3.64
USD_TO_OMR = 0.385
USD_TO_YER = 530
USD_TO_JOD = 0.71
USD_TO_LBP = 89500
USD_TO_IQD = 1310
USD_TO_SDG = 600
USD_TO_MAD = 10.2
USD_TO_DZD = 135
USD_TO_TND = 3.1
USD_TO_LYD = 4.8
USD_TO_SYP = 13000
USD_TO_MRU = 39.5
USD_TO_SOS = 570
USD_TO_ILS = 3.7

def convert_currencies(usd):
    return {
        "usd": usd, "sar": int(usd*USD_TO_SAR), "aed": int(usd*USD_TO_AED),
        "egp": int(usd*USD_TO_EGP), "kwd": round(usd*USD_TO_KWD,2),
        "bhd": round(usd*USD_TO_BHD,2), "qar": int(usd*USD_TO_QAR),
        "omr": round(usd*USD_TO_OMR,2), "yer": int(usd*USD_TO_YER),
        "jod": round(usd*USD_TO_JOD,2), "lbp": int(usd*USD_TO_LBP),
        "iqd": int(usd*USD_TO_IQD), "sdg": int(usd*USD_TO_SDG),
        "mad": int(usd*USD_TO_MAD), "dzd": int(usd*USD_TO_DZD),
        "tnd": round(usd*USD_TO_TND,2), "lyd": round(usd*USD_TO_LYD,2),
        "syp": int(usd*USD_TO_SYP), "mru": int(usd*USD_TO_MRU),
        "sos": int(usd*USD_TO_SOS), "ils": round(usd*USD_TO_ILS,2),
        "usdt": usd
    }

# === قاموس الترجمة عربي / انجليزي ===
TRANSLATIONS = {
    "ar": {
        "site_title": "تسهير AI - الموقع الرسمي",
        "site_sub": "أول منصة عربية تدعم 20 عملة عربية",
        "currencies": "20 عملة عربية | دفع آمن USDT | فاتورة PDF | لوحة أدمن",
        "check": "تشييك تأشيرات",
        "check_desc": "تشييك فوري لجميع أنواع التأشيرات - السعودية، الإمارات، شنغن، أمريكا",
        "curr_title": "20 عملة عربية",
        "curr_desc": "أول موقع يدعم كل العملات العربية من الخليج للمحيط - SAR, MAD, DZD, EGP, SYP...",
        "report_title": "تقارير وأدمن",
        "report_desc": "لوحة أدمن كاملة، تقارير يومية PDF، تحليل أرباح حسب الدولة",
        "packages": "باقاتنا - 20 عملة عربية",
        "coverage": "نغطي كل الوطن العربي",
        "coverage_countries": "السعودية - الإمارات - قطر - الكويت - البحرين - عمان - اليمن - الأردن - لبنان - العراق - سوريا - فلسطين - مصر - السودان - الصومال - موريتانيا - المغرب - الجزائر - تونس - ليبيا",
        "enter_btn": "🚀 دخول للمنصة - ابدأ الآن",
        "contact": "تواصل واتساب الآن",
        "login": "دخول",
        "register": "تسجيل جديد",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "new_user": "اسم مستخدم جديد",
        "new_pass": "كلمة مرور جديدة",
        "email": "إيميلك",
        "country": "دولتك",
        "package": "الباقة",
        "pay_activate": "✅ دفع وتفعيل",
        "wallet": "محفظة USDT",
        "days_left": "باقي",
        "day": "يوم",
        "admin_panel": "لوحة الأدمن",
        "profit": "الأرباح 20 عملة",
        "users": "المستخدمين",
        "website": "الموقع",
        "renew": "تجديد",
        "invoices": "فواتيري",
        "check_tab": "تشييك",
        "passport": "رقم الجواز",
        "visa_country": "دولة التأشيرة",
        "check_btn": "افحص",
        "valid": "ساري",
        "total_users": "إجمالي المستخدمين",
        "total_profit_usd": "إجمالي الأرباح USD",
        "total_profit_sar": "إجمالي الأرباح SAR",
        "profit_by_country": "الأرباح حسب الدولة",
        "extend_30": "➕ 30 يوم",
        "logout": "🚪 خروج",
        "home": "🏠 الموقع الرئيسي",
        "landing_preview": "🏠 معاينة صفحة الهبوط",
        "domain_info": "إعدادات الموقع - tasheer-ai.com",
        "features": ["تشييك غير محدود", "دعم 20 عملة", "فاتورة PDF", "دعم واتساب"],
        "features_3m": ["كل مزايا الشهر", "خصم 40%", "تقرير يومي", "أولوية دعم"],
        "features_year": ["كل المزايا", "خصم 60%", "لوحة أدمن", "API خاص"],
        "features_company": ["100 حساب", "تشييك جماعي", "تقارير شركات", "دعم مخصص"],
        "features_water": ["تشييك مياه", "تكامل SAP", "تقارير يومية", "دعم 24/7"],
        "features_oil": ["تشييك أرامكو", "أمان عالي", "API خاص", "مدير حساب"],
    },
    "en": {
        "site_title": "TASHEER AI - Official Website",
        "site_sub": "First Arab Platform Supporting 20 Arab Currencies",
        "currencies": "20 Arab Currencies | Secure USDT Payment | PDF Invoice | Admin Panel",
        "check": "Visa Checking",
        "check_desc": "Instant checking for all visa types - Saudi, UAE, Schengen, USA",
        "curr_title": "20 Arab Currencies",
        "curr_desc": "First site supporting all Arab currencies from Gulf to Ocean - SAR, MAD, DZD, EGP, SYP...",
        "report_title": "Reports & Admin",
        "report_desc": "Full admin panel, daily PDF reports, profit analysis by country",
        "packages": "Our Packages - 20 Arab Currencies",
        "coverage": "We Cover All Arab World",
        "coverage_countries": "Saudi - UAE - Qatar - Kuwait - Bahrain - Oman - Yemen - Jordan - Lebanon - Iraq - Syria - Palestine - Egypt - Sudan - Somalia - Mauritania - Morocco - Algeria - Tunisia - Libya",
        "enter_btn": "🚀 Enter Platform - Start Now",
        "contact": "Contact WhatsApp Now",
        "login": "Login",
        "register": "Register",
        "username": "Username",
        "password": "Password",
        "new_user": "New Username",
        "new_pass": "New Password",
        "email": "Your Email",
        "country": "Your Country",
        "package": "Package",
        "pay_activate": "✅ Pay & Activate",
        "wallet": "USDT Wallet",
        "days_left": "Remaining",
        "day": "days",
        "admin_panel": "Admin Panel",
        "profit": "Profits 20 Currencies",
        "users": "Users",
        "website": "Website",
        "renew": "Renew",
        "invoices": "My Invoices",
        "check_tab": "Check",
        "passport": "Passport No",
        "visa_country": "Visa Country",
        "check_btn": "Check",
        "valid": "Valid",
        "total_users": "Total Users",
        "total_profit_usd": "Total Profit USD",
        "total_profit_sar": "Total Profit SAR",
        "profit_by_country": "Profit by Country",
        "extend_30": "➕ 30 Days",
        "logout": "🚪 Logout",
        "home": "🏠 Main Website",
        "landing_preview": "🏠 Landing Preview",
        "domain_info": "Website Settings - tasheer-ai.com",
        "features": ["Unlimited checking", "20 currencies support", "PDF invoice", "WhatsApp support"],
        "features_3m": ["All monthly features", "40% discount", "Daily report", "Priority support"],
        "features_year": ["All features", "60% discount", "Admin panel", "Private API"],
        "features_company": ["100 accounts", "Bulk checking", "Company reports", "Dedicated support"],
        "features_water": ["Water checking", "SAP integration", "Daily reports", "24/7 support"],
        "features_oil": ["Aramco checking", "High security", "Private API", "Account manager"],
    }
}

if 'lang' not in st.session_state:
    st.session_state['lang'] = 'ar'
if 'users_db' not in st.session_state:
    st.session_state['users_db'] = {
        "admin": {"password": "Tasheer2024!", "name": "Gomez Admin", "email": EMAIL, "phone": "00966540450738", "sub_end": datetime.now() + timedelta(days=365), "active": True, "usd": 8000, "country": "🇸🇦 السعودية", "join_date": "2024-01-01", "role": "admin"},
    }
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ""
if 'invoices' not in st.session_state:
    st.session_state['invoices'] = []
if 'show_landing' not in st.session_state:
    st.session_state['show_landing'] = True

def t(key):
    lang = st.session_state['lang']
    return TRANSLATIONS[lang].get(key, key)

PRICING = {
    "شهر - $299 / Month $299": convert_currencies(299) | {"days": 30, "name_ar": "شهر واحد", "name_en": "1 Month", "features_ar": TRANSLATIONS['ar']['features'], "features_en": TRANSLATIONS['en']['features']},
    "3 أشهر - $1,500 / 3 Months $1500": convert_currencies(1500) | {"days": 90, "name_ar": "3 أشهر", "name_en": "3 Months", "features_ar": TRANSLATIONS['ar']['features_3m'], "features_en": TRANSLATIONS['en']['features_3m']},
    "سنة - $8,000 / Year $8000": convert_currencies(8000) | {"days": 365, "name_ar": "سنة كاملة", "name_en": "Full Year", "features_ar": TRANSLATIONS['ar']['features_year'], "features_en": TRANSLATIONS['en']['features_year']},
    "شركة - $100,000 / Company $100k": convert_currencies(100000) | {"days": 30, "name_ar": "شركة عادية", "name_en": "Company", "features_ar": TRANSLATIONS['ar']['features_company'], "features_en": TRANSLATIONS['en']['features_company']},
    "شركة مياه - $110,000 / Water $110k": convert_currencies(110000) | {"days": 30, "name_ar": "شركة مياه SEC/NWC", "name_en": "Water Company SEC", "features_ar": TRANSLATIONS['ar']['features_water'], "features_en": TRANSLATIONS['en']['features_water']},
    "شركة بترول - $120,000 / Oil $120k": convert_currencies(120000) | {"days": 30, "name_ar": "شركة بترول ARAMCO", "name_en": "Oil Company ARAMCO", "features_ar": TRANSLATIONS['ar']['features_oil'], "features_en": TRANSLATIONS['en']['features_oil']},
}
COUNTRIES = ["🇸🇦 السعودية / Saudi", "🇦🇪 الإمارات / UAE", "🇶🇦 قطر / Qatar", "🇰🇼 الكويت / Kuwait", "🇧🇭 البحرين / Bahrain", "🇴🇲 عمان / Oman", "🇾🇪 اليمن / Yemen", "🇯🇴 الأردن / Jordan", "🇱🇧 لبنان / Lebanon", "🇮🇶 العراق / Iraq", "🇸🇾 سوريا / Syria", "🇵🇸 فلسطين / Palestine", "🇪🇬 مصر / Egypt", "🇸🇩 السودان / Sudan", "🇸🇴 الصومال / Somalia", "🇲🇷 موريتانيا / Mauritania", "🇲🇦 المغرب / Morocco", "🇩🇿 الجزائر / Algeria", "🇹🇳 تونس / Tunisia", "🇱🇾 ليبيا / Libya"]

# === زر تبديل اللغة ===
col_lang1, col_lang2, col_lang3 = st.columns([6,2,2])
with col_lang2:
    if st.button("🇸🇦 عربي", use_container_width=True, type="primary" if st.session_state['lang']=='ar' else "secondary"):
        st.session_state['lang'] = 'ar'
        st.rerun()
with col_lang3:
    if st.button("🇺🇸 English", use_container_width=True, type="primary" if st.session_state['lang']=='en' else "secondary"):
        st.session_state['lang'] = 'en'
        st.rerun()

# === صفحة الهبوط ===
if st.session_state['show_landing'] and not st.session_state['logged_in']:
    lang = st.session_state['lang']
    dir_style = "rtl" if lang=='ar' else "ltr"
    st.markdown(f"""
    <style>
        .hero {{ background: linear-gradient(135deg,#0a7a42,#0d4a2a); color:white; padding:40px 20px; border-radius:20px; text-align:center; margin-bottom:20px; direction:{dir_style}; }}
        .feature-card {{ background:white; border:2px solid #0a7a42; padding:20px; border-radius:15px; text-align:center; margin:10px; box-shadow:0 4px 10px rgba(0,0,0,0.1); direction:{dir_style}; }}
        .price-card {{ background:linear-gradient(135deg,#f0fff4,#e8f5e9); border:3px solid #0a7a42; padding:20px; border-radius:20px; text-align:center; margin:10px; direction:{dir_style}; }}
        .currency-bar {{ background:#1a1a1a; color:#00ff88; padding:10px; border-radius:10px; text-align:center; font-size:11px; font-weight:700; }}
    </style>
    <div class="hero">
        <h1 style="font-size:42px; margin:0;">🌍 TASHEER AI</h1>
        <h2 style="font-size:20px; margin:10px 0;">{t('site_title')}</h2>
        <p style="font-size:16px;">{t('site_sub')}</p>
        <p style="font-size:12px; margin-top:15px;">📱 00966540450738 | ✉️ report.gomez@gmail.com | 🌐 tasheer-ai.com</p>
        <p style="font-size:10px; background:rgba(255,255,255,0.2); padding:5px 15px; border-radius:20px; display:inline-block; margin-top:10px;">{t('currencies')}</p>
    </div>
    <div class="currency-bar">
        💵 USD | 🇸🇦 SAR 3.75 | 🇦🇪 AED 3.67 | 🇴🇲 OMR 0.385 | 🇶🇦 QAR 3.64 | 🇰🇼 KWD 0.31 | 🇧🇭 BHD 0.376 | 🇯🇴 JOD 0.71 | 🇸🇾 SYP 13000 | 🇵🇸 ILS 3.7 | 🇪🇬 EGP 50.5 | 🇾🇪 YER 530 | 🇱🇧 LBP 89500 | 🇮🇶 IQD 1310 | 🇸🇩 SDG 600 | 🇲🇦 MAD 10.2 | 🇩🇿 DZD 135 | 🇹🇳 TND 3.1 | 🇱🇾 LYD 4.8 | 🇲🇷 MRU 39.5 | 🇸🇴 SOS 570 | USDT TRC20
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="feature-card">
            <h2>🔍</h2>
            <h3>{t('check')}</h3>
            <p style="font-size:12px;">{t('check_desc')}</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="feature-card">
            <h2>💱</h2>
            <h3>{t('curr_title')}</h3>
            <p style="font-size:12px;">{t('curr_desc')}</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="feature-card">
            <h2>📊</h2>
            <h3>{t('report_title')}</h3>
            <p style="font-size:12px;">{t('report_desc')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"### {t('packages')}")
    cols = st.columns(3)
    for idx, (key, data) in enumerate(PRICING.items()):
        with cols[idx % 3]:
            name = data['name_ar'] if lang=='ar' else data['name_en']
            feats = data['features_ar'] if lang=='ar' else data['features_en']
            st.markdown(f"""
            <div class="price-card">
                <h3 style="margin:0; color:#0a7a42;">{name}</h3>
                <h1 style="margin:10px 0; color:#0a7a42;">💵 ${data['usd']:,}</h1>
                <p style="font-size:11px; font-weight:700; line-height:1.5;">
                🇸🇦 {data['sar']:,} SAR<br>
                🇦🇪 {data['aed']:,} AED | 🇴🇲 {data['omr']} OMR<br>
                🇲🇦 {data['mad']:,} MAD | 🇩🇿 {data['dzd']:,} DZD<br>
                🇪🇬 {data['egp']:,} EGP | 🇸🇾 {data['syp']:,} SYP<br>
                <span style="font-size:9px; color:gray;">{data['days']} {t('day')} | USDT {data['usdt']}</span>
                </p>
                <p style="font-size:10px; text-align:{'right' if lang=='ar' else 'left'}; margin-top:10px;">
                {"<br>".join([f"✅ {f}" for f in feats])}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"### 🌍 {t('coverage')}")
    st.markdown(f"""
    <div style="text-align:center; font-size:24px; letter-spacing:5px; padding:15px; background:#f8f9fa; border-radius:15px; direction:{dir_style};">
    🇸🇦 🇦🇪 🇶🇦 🇰🇼 🇧🇭 🇴🇲 🇾🇪 🇯🇴 🇱🇧 🇮🇶 🇸🇾 🇵🇸 🇪🇬 🇸🇩 🇸🇴 🇲🇷 🇲🇦 🇩🇿 🇹🇳 🇱🇾
    <br><span style="font-size:12px; letter-spacing:1px;">{t('coverage_countries')}</span>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if st.button(t('enter_btn'), type="primary", use_container_width=True):
            st.session_state['show_landing'] = False
            st.rerun()
        st.markdown(f"""
        <div style="text-align:center; margin-top:15px; direction:{dir_style};">
            <p style="font-size:12px;">📱 WhatsApp: 00966540450738 | ✉️ {EMAIL}</p>
            <p style="font-size:10px;">🌐 Domain: tasheer-ai.com | 💳 Payment: USDT TRC20</p>
            <a href="https://wa.me/966540450738" target="_blank" style="background:#25D366; color:white; padding:10px 20px; border-radius:25px; text-decoration:none; font-weight:700; display:inline-block; margin-top:10px;">💬 {t('contact')}</a>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# === تسجيل الدخول ===
db = st.session_state['users_db']
if not st.session_state['logged_in']:
    st.markdown(f"<div style='text-align:center;'><h1>🔐 {t('login')} TASHEER AI - tasheer-ai.com</h1></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        with st.form("login"):
            u = st.text_input(t('username'))
            p = st.text_input(t('password'), type="password")
            if st.form_submit_button(t('login'), type="primary", use_container_width=True):
                if u in db and db[u]["password"] == p:
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = u
                    st.session_state['show_landing'] = False
                    st.rerun()
    with col2:
        st.markdown(f"### {t('register')} - 20 {t('curr_title')}")
        new_user = st.text_input(t('new_user'))
        new_pass = st.text_input(t('new_pass'), type="password")
        new_email = st.text_input(t('email'))
        new_country = st.selectbox(t('country'), COUNTRIES)
        plan = st.selectbox(t('package'), list(PRICING.keys()))
        data = PRICING[plan]
        st.info(f"${data['usd']:,} = {data['sar']:,} SAR = {data['mad']:,} MAD = {data['dzd']:,} DZD")
        st.code(WALLET)
        st.image(QR_URL, width=200)
        if st.button(t('pay_activate'), type="primary", use_container_width=True):
            if new_user and new_pass and new_user not in db:
                sub_end = datetime.now() + timedelta(days=data['days'])
                db[new_user] = {"password": new_pass, "name": new_user, "email": new_email, "phone": "00966540450738", "sub_end": sub_end, "active": True, "usd": data['usd'], "country": new_country, "join_date": datetime.now().strftime('%Y-%m-%d'), "role": "user"}
                st.success(f"✅ {new_user}")
                st.session_state['logged_in'] = True
                st.session_state['username'] = new_user
                st.rerun()
    if st.button(t('home')):
        st.session_state['show_landing'] = True
        st.rerun()
    st.stop()

u = st.session_state['username']
user = db[u]
is_admin = user.get('role') == 'admin'
days_left = (user["sub_end"] - datetime.now()).days

st.markdown(f"""
<div style="background:#0a7a42; color:white; padding:10px 20px; border-radius:10px; text-align:center;">
    🌐 tasheer-ai.com | 👑 TASHEER AI | 💱 20 {t('curr_title')} | 👤 {user['name']} | {t('days_left')} {days_left} {t('day')} | 📱 00966540450738 | {t('lang')}: {st.session_state['lang']}
</div>
""", unsafe_allow_html=True)

if is_admin:
    tabs = st.tabs([f"👑 {t('admin_panel')}", f"📊 {t('profit')}", f"👥 {t('users')}", f"🌐 {t('website')}", f"💳 {t('renew')}"])
    with tabs[0]:
        total_users = len(db)
        total_revenue = sum([x['usd'] for x in db.values() if x.get('role')!='admin'])
        conv = convert_currencies(total_revenue)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(t('total_users'), total_users)
        with c2:
            st.metric(t('total_profit_usd'), f"${total_revenue:,}")
        with c3:
            st.metric(t('total_profit_sar'), f"{conv['sar']:,}")
        st.markdown(f"**20 Currencies:** ${conv['usd']:,} USD | {conv['sar']:,} SAR | {conv['mad']:,} MAD | {conv['dzd']:,} DZD | {conv['syp']:,} SYP")
        if st.button(t('landing_preview')):
            st.session_state['show_landing'] = True
            st.rerun()
    with tabs[1]:
        st.markdown(f"### {t('profit_by_country')}")
        country_stats = {}
        for udata in db.values():
            if udata.get('role') != 'admin':
                c = udata.get('country','غير معروف')
                country_stats[c] = country_stats.get(c,0) + udata['usd']
        for country, total in country_stats.items():
            conv = convert_currencies(total)
            st.markdown(f"{country}: ${total:,} = {conv['sar']:,} SAR = {conv['mad']:,} MAD")
    with tabs[2]:
        for uname, udata in db.items():
            days = (udata['sub_end'] - datetime.now()).days
            st.markdown(f"**{uname}** - {udata['name']} - {udata.get('country','')} - {days} {t('day')} - ${udata['usd']:,}")
            if st.button(f"{t('extend_30')} {uname}", key=f"ext_{uname}"):
                db[uname]['sub_end'] += timedelta(days=30)
                st.rerun()
    with tabs[3]:
        st.markdown(f"### {t('domain_info')}")
        st.code(WALLET)
    with tabs[4]:
        st.code(WALLET)
        st.image(QR_URL)
else:
    tabs = st.tabs([f"🔍 {t('check_tab')}", f"💱 20 {t('curr_title')}", f"🌐 {t('website')}"])
    with tabs[0]:
        p_no = st.text_input(t('passport'), "A12345678")
        visa_country = st.selectbox(t('visa_country'), COUNTRIES)
        if st.button(t('check_btn'), type="primary"):
            st.success(f"{p_no} - {visa_country} - {t('valid')}")
    with tabs[1]:
        sel = st.selectbox(t('package'), list(PRICING.keys()))
        data = PRICING[sel]
        st.info(f"${data['usd']:,} = {data['sar']:,} SAR = {data['mad']:,} MAD")
    with tabs[2]:
        if st.button(t('landing_preview')):
            st.session_state['show_landing'] = True
            st.rerun()

if st.button(t('logout')):
    st.session_state['logged_in'] = False
    st.session_state['show_landing'] = True
    st.rerun()
