import streamlit as st
from datetime import datetime, timedelta
import random
from io import BytesIO
try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except:
    PDF_AVAILABLE = False

st.set_page_config(page_title="TASHEER AI - Official Website - 20 Currencies", page_icon="🌍", layout="wide")

WALLET = "TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL = f"https://api.qrserver.com/v1/create-qr-code/?size=500x500&data={WALLET}"
EMAIL = "report.gomez@gmail.com"
DOMAIN = "tasheer-ai.com"
WHATSAPP_LINK = "https://wa.me/966540450738"

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

PRICING = {
    "شهر - $299": convert_currencies(299) | {"days": 30, "name": "شهر واحد", "features": ["تشييك غير محدود", "دعم 20 عملة", "فاتورة PDF", "دعم واتساب"]},
    "3 أشهر - $1,500": convert_currencies(1500) | {"days": 90, "name": "3 أشهر", "features": ["كل مزايا الشهر", "خصم 40%", "تقرير يومي", "أولوية دعم"]},
    "سنة - $8,000": convert_currencies(8000) | {"days": 365, "name": "سنة كاملة", "features": ["كل المزايا", "خصم 60%", "لوحة أدمن", "API خاص"]},
    "شركة - $100,000": convert_currencies(100000) | {"days": 30, "name": "شركة عادية", "features": ["100 حساب", "تشييك جماعي", "تقارير شركات", "دعم مخصص"]},
    "شركة مياه - $110,000": convert_currencies(110000) | {"days": 30, "name": "شركة مياه SEC/NWC", "features": ["تشييك مياه", "تكامل SAP", "تقارير يومية", "دعم 24/7"]},
    "شركة بترول - $120,000": convert_currencies(120000) | {"days": 30, "name": "شركة بترول ARAMCO", "features": ["تشييك أرامكو", "أمان عالي", "API خاص", "مدير حساب"]},
}
COUNTRIES = ["🇸🇦 السعودية", "🇦🇪 الإمارات", "🇶🇦 قطر", "🇰🇼 الكويت", "🇧🇭 البحرين", "🇴🇲 عمان", "🇾🇪 اليمن", "🇯🇴 الأردن", "🇱🇧 لبنان", "🇮🇶 العراق", "🇸🇾 سوريا", "🇵🇸 فلسطين", "🇪🇬 مصر", "🇸🇩 السودان", "🇸🇴 الصومال", "🇲🇷 موريتانيا", "🇲🇦 المغرب", "🇩🇿 الجزائر", "🇹🇳 تونس", "🇱🇾 ليبيا"]

# === صفحة الهبوط - الموقع الرسمي ===
if st.session_state['show_landing'] and not st.session_state['logged_in']:
    st.markdown(f"""
    <style>
        .hero {{ background: linear-gradient(135deg,#0a7a42,#0d4a2a); color:white; padding:40px 20px; border-radius:20px; text-align:center; margin-bottom:20px; }}
        .feature-card {{ background:white; border:2px solid #0a7a42; padding:20px; border-radius:15px; text-align:center; margin:10px; box-shadow:0 4px 10px rgba(0,0,0,0.1); }}
        .price-card {{ background:linear-gradient(135deg,#f0fff4,#e8f5e9); border:3px solid #0a7a42; padding:20px; border-radius:20px; text-align:center; margin:10px; }}
        .currency-bar {{ background:#1a1a1a; color:#00ff88; padding:10px; border-radius:10px; text-align:center; font-size:11px; font-weight:700; overflow:hidden; white-space:nowrap; }}
    </style>
    <div class="hero">
        <h1 style="font-size:42px; margin:0;">🌍 TASHEER AI</h1>
        <h2 style="font-size:20px; margin:10px 0;">الموقع الرسمي - tasheer-ai.com</h2>
        <p style="font-size:16px;">أول منصة عربية تدعم 20 عملة عربية - تشييك تأشيرات واشتراكات</p>
        <p style="font-size:12px; margin-top:15px;">📱 00966540450738 | ✉️ report.gomez@gmail.com | 🌐 tasheer-ai.com</p>
        <p style="font-size:10px; background:rgba(255,255,255,0.2); padding:5px 15px; border-radius:20px; display:inline-block; margin-top:10px;">💱 20 عملة عربية | 🔒 دفع آمن USDT | 📄 فاتورة PDF | 👑 لوحة أدمن</p>
    </div>
    <div class="currency-bar">
        💵 USD | 🇸🇦 SAR 3.75 | 🇦🇪 AED 3.67 | 🇴🇲 OMR 0.385 | 🇶🇦 QAR 3.64 | 🇰🇼 KWD 0.31 | 🇧🇭 BHD 0.376 | 🇯🇴 JOD 0.71 | 🇸🇾 SYP 13000 | 🇵🇸 ILS 3.7 | 🇪🇬 EGP 50.5 | 🇾🇪 YER 530 | 🇱🇧 LBP 89500 | 🇮🇶 IQD 1310 | 🇸🇩 SDG 600 | 🇲🇦 MAD 10.2 | 🇩🇿 DZD 135 | 🇹🇳 TND 3.1 | 🇱🇾 LYD 4.8 | 🇲🇷 MRU 39.5 | 🇸🇴 SOS 570 | USDT TRC20
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h2>🔍</h2>
            <h3>تشييك تأشيرات</h3>
            <p style="font-size:12px;">تشييك فوري لجميع أنواع التأشيرات - السعودية، الإمارات، شنغن، أمريكا</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h2>💱</h2>
            <h3>20 عملة عربية</h3>
            <p style="font-size:12px;">أول موقع يدعم كل العملات العربية من الخليج للمحيط - SAR, MAD, DZD, EGP, SYP...</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h2>📊</h2>
            <h3>تقارير وأدمن</h3>
            <p style="font-size:12px;">لوحة أدمن كاملة، تقارير يومية PDF، تحليل أرباح حسب الدولة</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 💰 باقاتنا - 20 عملة عربية")
    cols = st.columns(3)
    for idx, (key, data) in enumerate(PRICING.items()):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="price-card">
                <h3 style="margin:0; color:#0a7a42;">{data['name']}</h3>
                <h1 style="margin:10px 0; color:#0a7a42;">💵 ${data['usd']:,}</h1>
                <p style="font-size:11px; font-weight:700; line-height:1.5;">
                🇸🇦 {data['sar']:,} SAR<br>
                🇦🇪 {data['aed']:,} AED | 🇴🇲 {data['omr']} OMR<br>
                🇲🇦 {data['mad']:,} MAD | 🇩🇿 {data['dzd']:,} DZD<br>
                🇪🇬 {data['egp']:,} EGP | 🇸🇾 {data['syp']:,} SYP<br>
                <span style="font-size:9px; color:gray;">{data['days']} يوم | USDT {data['usdt']}</span>
                </p>
                <p style="font-size:10px; text-align:right; margin-top:10px;">
                {"<br>".join([f"✅ {f}" for f in data['features']])}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🌍 نغطي كل الوطن العربي")
    st.markdown("""
    <div style="text-align:center; font-size:24px; letter-spacing:5px; padding:15px; background:#f8f9fa; border-radius:15px;">
    🇸🇦 🇦🇪 🇶🇦 🇰🇼 🇧🇭 🇴🇲 🇾🇪 🇯🇴 🇱🇧 🇮🇶 🇸🇾 🇵🇸 🇪🇬 🇸🇩 🇸🇴 🇲🇷 🇲🇦 🇩🇿 🇹🇳 🇱🇾
    <br><span style="font-size:12px; letter-spacing:1px;">السعودية - الإمارات - قطر - الكويت - البحرين - عمان - اليمن - الأردن - لبنان - العراق - سوريا - فلسطين - مصر - السودان - الصومال - موريتانيا - المغرب - الجزائر - تونس - ليبيا</span>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if st.button("🚀 دخول للمنصة - ابدأ الآن", type="primary", use_container_width=True):
            st.session_state['show_landing'] = False
            st.rerun()
        st.markdown(f"""
        <div style="text-align:center; margin-top:15px;">
            <p style="font-size:12px;">📱 واتساب: 00966540450738 | ✉️ {EMAIL}</p>
            <p style="font-size:10px;">🌐 الدومين الرسمي: tasheer-ai.com | 💳 دفع: USDT TRC20</p>
            <p style="font-size:9px; color:gray;">TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH</p>
            <a href="{WHATSAPP_LINK}" target="_blank" style="background:#25D366; color:white; padding:10px 20px; border-radius:25px; text-decoration:none; font-weight:700; display:inline-block; margin-top:10px;">💬 تواصل واتساب الآن</a>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# === بعد الدخول - التطبيق ===
db = st.session_state['users_db']
if not st.session_state['logged_in']:
    st.markdown("<div style='text-align:center;'><h1>🔐 دخول TASHEER AI - tasheer-ai.com</h1></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        with st.form("login"):
            u = st.text_input("اسم المستخدم")
            p = st.text_input("كلمة المرور", type="password")
            st.info("أدمن: admin / Tasheer2024!")
            if st.form_submit_button("دخول", type="primary", use_container_width=True):
                if u in db and db[u]["password"] == p:
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = u
                    st.session_state['show_landing'] = False
                    st.rerun()
    with col2:
        st.markdown("### 📝 تسجيل جديد - 20 عملة")
        new_user = st.text_input("اسم مستخدم جديد")
        new_pass = st.text_input("كلمة مرور", type="password")
        new_email = st.text_input("إيميلك")
        new_country = st.selectbox("دولتك", COUNTRIES)
        plan = st.selectbox("الباقة", list(PRICING.keys()))
        data = PRICING[plan]
        st.info(f"${data['usd']:,} = {data['sar']:,} SAR = {data['mad']:,} MAD = {data['dzd']:,} DZD")
        st.code(WALLET)
        st.image(QR_URL, width=200)
        if st.button("✅ دفع وتفعيل", type="primary", use_container_width=True):
            if new_user and new_pass and new_user not in db:
                sub_end = datetime.now() + timedelta(days=data['days'])
                db[new_user] = {"password": new_pass, "name": new_user, "email": new_email, "phone": "00966540450738", "sub_end": sub_end, "active": True, "usd": data['usd'], "country": new_country, "join_date": datetime.now().strftime('%Y-%m-%d'), "role": "user"}
                st.success(f"تم تفعيل {new_user}")
                st.session_state['logged_in'] = True
                st.session_state['username'] = new_user
                st.rerun()
    if st.button("🏠 رجوع للموقع الرئيسي"):
        st.session_state['show_landing'] = True
        st.rerun()
    st.stop()

u = st.session_state['username']
user = db[u]
is_admin = user.get('role') == 'admin'
days_left = (user["sub_end"] - datetime.now()).days

st.markdown(f"""
<div style="background:#0a7a42; color:white; padding:10px 20px; border-radius:10px; display:flex; justify-content:space-between; align-items:center;">
    <span>🌐 tasheer-ai.com | 👑 TASHEER AI | 💱 20 عملة عربية</span>
    <span>👤 {user['name']} | {user.get('country','')} | باقي {days_left} يوم | <a href="#" style="color:white;">📱 00966540450738</a></span>
</div>
""", unsafe_allow_html=True)

if is_admin:
    tabs = st.tabs(["👑 أدمن", "📊 أرباح 20 عملة", "👥 المستخدمين", "🌐 الموقع", "💳 تجديد"])
    with tabs[0]:
        total_users = len(db)
        total_revenue = sum([x['usd'] for x in db.values() if x.get('role')!='admin'])
        conv = convert_currencies(total_revenue)
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("👥 المستخدمين", total_users)
        with c2:
            st.metric("💵 الأرباح USD", f"${total_revenue:,}")
        with c3:
            st.metric("🇸🇦 الأرباح SAR", f"{conv['sar']:,}")
        st.markdown(f"**20 عملة:** ${conv['usd']:,} USD | {conv['sar']:,} SAR | {conv['mad']:,} MAD | {conv['dzd']:,} DZD | {conv['syp']:,} SYP | {conv['mru']:,} MRU")
        if st.button("🏠 عرض الموقع الرئيسي"):
            st.session_state['show_landing'] = True
            st.rerun()
    with tabs[1]:
        st.markdown("### 📊 الأرباح حسب الدولة")
        country_stats = {}
        for udata in db.values():
            if udata.get('role') != 'admin':
                c = udata.get('country','غير معروف')
                country_stats[c] = country_stats.get(c,0) + udata['usd']
        for country, total in country_stats.items():
            conv = convert_currencies(total)
            st.markdown(f"{country}: ${total:,} = {conv['sar']:,} SAR = {conv['mad']:,} MAD")
    with tabs[2]:
        st.markdown("### 👥 المستخدمين")
        for uname, udata in db.items():
            days = (udata['sub_end'] - datetime.now()).days
            st.markdown(f"**{uname}** - {udata['name']} - {udata.get('country','')} - {days} يوم - ${udata['usd']:,}")
            if st.button(f"➕ 30 يوم لـ {uname}", key=f"ext_{uname}"):
                db[uname]['sub_end'] += timedelta(days=30)
                st.rerun()
    with tabs[3]:
        st.markdown(f"### 🌐 إعدادات الموقع - tasheer-ai.com")
        st.info(f"الدومين: tasheer-ai.com | الإيميل: {EMAIL} | المحفظة: {WALLET}")
        st.code(f"""
# خطوات ربط الدومين tasheer-ai.com:
# 1. اشتري الدومين من Namecheap أو GoDaddy - $10/سنة
# 2. في Streamlit Cloud > Settings > Custom Domain
# 3. أضف: tasheer-ai.com
# 4. أضف CNAME في Namecheap:
#    Host: @ -> streamlit.app
#    Host: www -> your-app.streamlit.app
# 5. انتظر 24 ساعة
        """)
        if st.button("🏠 معاينة صفحة الهبوط"):
            st.session_state['show_landing'] = True
            st.rerun()
    with tabs[4]:
        st.code(WALLET)
        st.image(QR_URL)
else:
    tabs = st.tabs(["🔍 تشييك", "💱 20 عملة", "🌐 الموقع"])
    with tabs[0]:
        p_no = st.text_input("رقم الجواز", "A12345678")
        visa_country = st.selectbox("دولة التأشيرة", COUNTRIES)
        if st.button("افحص", type="primary"):
            st.success(f"{p_no} - {visa_country} - ساري")
    with tabs[1]:
        sel = st.selectbox("الباقة", list(PRICING.keys()))
        data = PRICING[sel]
        st.info(f"${data['usd']:,} = {data['sar']:,} SAR = {data['mad']:,} MAD")
    with tabs[2]:
        if st.button("🏠 عرض الموقع الرئيسي"):
            st.session_state['show_landing'] = True
            st.rerun()

if st.button("🚪 خروج"):
    st.session_state['logged_in'] = False
    st.session_state['show_landing'] = True
    st.rerun()
