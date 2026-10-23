import streamlit as st
from datetime import datetime, timedelta
import json, os, pandas as pd

st.set_page_config(page_title="TASHEER AI - Official", page_icon="🌐", layout="wide")

WALLET="TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL=f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={WALLET}"
USERS_FILE="users_db.json"; MSG_FILE="messages_db.json"

def load_json(f,d):
    if os.path.exists(f):
        try: 
            with open(f,"r",encoding="utf-8") as file: return json.load(file)
        except: return d
    return d
def save_json(f,d):
    with open(f,"w",encoding="utf-8") as file: json.dump(file,d,ensure_ascii=False,indent=2)

st.markdown("""
<style>
.hero {background:linear-gradient(135deg, #0A1931 0%, #0E4D4F 50%, #B8860B 100%); color:white; padding:40px 30px; border-radius:20px; text-align:center; margin-bottom:20px;}
.about-hero {background:#0A1931; border:1px solid #B8860B; border-radius:16px; padding:30px; margin:20px 0;}
.about-name {font-size:32px; font-weight:800; color:white; letter-spacing:1px;}
.about-title {font-size:22px; font-weight:700; color:#B8860B; margin-top:5px;}
.offer-card {background:white; border:2px solid #E2E8F0; border-radius:16px; padding:24px; text-align:center; height:420px; position:relative; box-shadow:0 4px 12px rgba(10,25,49,0.06);}
.offer-card.popular {border:2px solid #B8860B; background:linear-gradient(180deg, #FFFBEB 0%, #FFFFFF 100%);}
.price {font-size:38px; font-weight:800; color:#0A1931;}
.feature {text-align:left; margin:6px 0; font-size:12px;}
.tasheer-header{background:#FFF; border-bottom:2px solid #0A1931; padding:12px 20px; display:flex; justify-content:space-between; align-items:center;}
.trusted-box {background:#0E4D4F; border:1px solid #B8860B; border-radius:12px; padding:16px; text-align:center; color:white; margin:8px;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="tasheer-header">
<div style="font-size:26px; font-weight:800; color:#0A1931;">TASHEER<span style="color:#B8860B;">AI</span> <span style="font-size:9px; background:#0A1931; color:white; padding:4px 10px; border-radius:12px;">OFFICIAL IP</span></div>
<div style="font-size:11px; font-weight:600;">WAIL SALAHELDIN ABDULLA | wail.ungm1191731.lab@gmail.com</div>
</div>
<div style="background:linear-gradient(90deg, #0A1931, #0E4D4F, #B8860B); height:5px; margin-bottom:12px;"></div>
""", unsafe_allow_html=True)

# DB
default_admin={"password":"Tasheer2024","name":"Wail Salaheldin Abdulla","email":"wail.ungm1191731.lab@gmail.com","sub_end":(datetime.now()+timedelta(days=365)).isoformat(),"active":True,"usd":0,"tx":"MASTER"}
loaded=load_json(USERS_FILE, {"admin":default_admin}); loaded["admin"]=default_admin
if 'users_db' not in st.session_state: st.session_state['users_db']=loaded
else: st.session_state['users_db']["admin"]=default_admin
if 'logged_in' not in st.session_state: st.session_state['logged_in']=False
if 'username' not in st.session_state: st.session_state['username']=""
if 'show_landing' not in st.session_state: st.session_state['show_landing']=True
def save_all(): save_json(USERS_FILE, st.session_state['users_db'])

if st.session_state['show_landing'] and not st.session_state['logged_in']:
    nav1, nav2, nav3, nav4 = st.tabs(["🏠 الرئيسية / Home & Offers", "👤 عني / About Us", "🔑 دخول / Login", "🚀 تسجيل / Register"])

    with nav1:
        st.markdown("""
        <div class="hero">
            <h1>TASHEER AI</h1>
            <p>المنصة الرسمية الآمنة لإدارة التأشيرات والمراسلات - IP Original مسجل</p>
            <p style="font-size:13px; margin-top:10px;">Official: tasheer-ai-juub2hzyqf9boqzthpwv4n.streamlit.app | Founder: WAIL SALAHELDIN ABDULLA</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("### 💎 الباقات الرسمية - Official Offers")
        c1,c2,c3=st.columns(3)
        with c1: st.markdown('<div class="offer-card"><h3>🥉 الأساسية</h3><div class="price">$299 <span style="font-size:14px;">/شهر</span></div><div class="feature">✅ 5 حسابات</div><div class="feature">✅ 500 مراسلة</div><div class="feature">✅ Gmail آمن</div><div class="feature">✅ فواتير تلقائية</div></div>', unsafe_allow_html=True)
        with c2: st.markdown('<div class="offer-card popular"><div style="background:#B8860B; color:white; padding:4px 12px; border-radius:12px; font-size:11px; position:absolute; top:-10px; left:50%; transform:translateX(-50%);">🔥 الأكثر مبيعاً</div><h3>🥇 الاحترافية</h3><div class="price">$599 <span style="font-size:14px;">/شهر</span></div><div class="feature">✅ 20 حساب</div><div class="feature">✅ غير محدود</div><div class="feature">✅ AI ذكي</div><div class="feature">✅ تقارير متقدمة</div><div class="feature">✅ دعم 24/7</div></div>', unsafe_allow_html=True)
        with c3: st.markdown('<div class="offer-card"><h3>💎 المؤسسات</h3><div class="price">$999 <span style="font-size:14px;">/شهر</span></div><div class="feature">✅ غير محدود</div><div class="feature">✅ White Label</div><div class="feature">✅ API مفتوح</div><div class="feature">✅ مدير حساب خاص</div><div class="feature">✅ حماية WIPO IP</div></div>', unsafe_allow_html=True)

    with nav2:
        st.markdown("""
        <div class="about-hero">
            <div style="color:#5EE9C6; font-size:14px; letter-spacing:2px;">About Us</div>
            <div class="about-name">WAIL SALAHELDIN ABDULLA</div>
            <div class="about-title">Founder of TASHEER AI</div>
            <div style="color:#7DD8C6; font-size:16px; margin-top:5px;">AI Communication Platform for Visa Services</div>
            <div style="margin-top:15px;">
                <span style="background:#0E4D4F; border:1px solid #B8860B; color:#FDE68A; padding:6px 14px; border-radius:20px; font-size:12px; margin-right:8px;">Launched October 2026</span>
                <span style="background:#0E4D4F; border:1px solid #B8860B; color:#FDE68A; padding:6px 14px; border-radius:20px; font-size:12px;">Original IP Registered</span>
            </div>
            <div style="margin-top:20px; color:white;">
                <div style="color:#FDE68A; font-weight:700;">Mission</div>
                <p style="font-size:13px; line-height:1.6; opacity:0.9;">To automate visa companies with secure, scalable, and intelligent AI communication, reducing processing time and enhancing client trust through innovative technology.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        col_a,col_b,col_c,col_d=st.columns(4)
        with col_a: st.markdown('<div class="trusted-box"><div style="font-size:22px;">🛡️</div><div style="color:#FDE68A; font-weight:700;">Trusted</div><div style="font-size:11px;">Reliable processes built on transparency</div></div>', unsafe_allow_html=True)
        with col_b: st.markdown('<div class="trusted-box"><div style="font-size:22px;">🔒</div><div style="color:#FDE68A; font-weight:700;">Secure</div><div style="font-size:11px;">Enterprise-grade security & compliance</div></div>', unsafe_allow_html=True)
        with col_c: st.markdown('<div class="trusted-box"><div style="font-size:22px;">💡</div><div style="color:#FDE68A; font-weight:700;">Innovative</div><div style="font-size:11px;">Pioneering AI solutions for visa operations</div></div>', unsafe_allow_html=True)
        with col_d: st.markdown('<div class="trusted-box"><div style="font-size:22px;">📈</div><div style="color:#FDE68A; font-weight:700;">Scalable</div><div style="font-size:11px;">Built to grow with businesses globally</div></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:white; border-radius:12px; padding:20px; margin-top:20px; border-top:3px solid #B8860B;">
        <h4 style="color:#0A1931;">من أنا - ببساطة</h4>
        <p style="font-size:13px; line-height:1.8;">
        أنا <b>WAIL SALAHELDIN ABDULLA</b> - مؤسس منصة TASHEER AI<br>
        المنصة انطلقت أكتوبر 2026 لحل مشكلة الفوضى في مراسلات شركات التأشيرات.<br>
        نظام ذكي آمن بديل Gmail - كل رسالة منظمة، كل عميل حساب، كل فاتورة تلقائية.<br>
        عمل أصلي 100% مسجل IP - ألوان كحلي ذهبي تركوازي - لا نستخدم ألوان جوجل.<br>
        هدفي: أخلي شركتك تشتغل لحالها وأنت تتابع الأرباح فقط.<br><br>
        <b>📧</b> wail.ungm1191731.lab@gmail.com<br>
        <b>🌐</b> tasheer-ai-juub2hzyqf9boqzthpwv4n.streamlit.app
        </p>
        </div>
        """, unsafe_allow_html=True)

    with nav3:
        with st.form("login_form"):
            u=st.text_input("Username", value="admin"); p=st.text_input("Password", type="password", value="Tasheer2024")
            if st.form_submit_button("Login", type="primary", use_container_width=True):
                db_lower={k.lower():k for k in st.session_state['users_db'].keys()}
                if u.strip().lower() in db_lower:
                    real=db_lower[u.strip().lower()]
                    if st.session_state['users_db'][real]["password"]==p:
                        st.session_state['logged_in']=True; st.session_state['username']=real; st.session_state['show_landing']=False; st.rerun()

    with nav4:
        with st.form("reg_form"):
            u=st.text_input("Username"); e=st.text_input("Email"); p=st.text_input("Password", type="password")
            st.code(WALLET); st.image(QR_URL,width=130)
            offer=st.selectbox("اختر الباقة",["$299 Basic","$599 Pro 🔥","$999 Enterprise"]); tx=st.text_input("TxID")
            if st.form_submit_button(f"تفعيل {offer}", type="primary", use_container_width=True):
                if u and e and p and len(tx)>=10:
                    price=299 if "299" in offer else 599 if "599" in offer else 999
                    st.session_state['users_db'][u.strip().lower()]={"password":p,"name":u,"email":e,"sub_end":(datetime.now()+timedelta(days=30)).isoformat(),"active":True,"usd":price,"tx":tx.strip(),"offer":offer}
                    save_all(); st.session_state['logged_in']=True; st.session_state['username']=u.strip().lower(); st.session_state['show_landing']=False; st.rerun()

    st.markdown('<div style="text-align:center; color:#888; font-size:10px; padding:20px;">© 2026 TASHEER AI - WAIL SALAHELDIN ABDULLA - IP Original - All Rights Reserved</div>', unsafe_allow_html=True)
    st.stop()

# Logged Admin
st.markdown(f'<div style="background:#0A1931; color:white; border-radius:10px; padding:10px 16px;">✅ {st.session_state["username"]} - LIVE - WAIL SALAHELDIN ABDULLA</div>', unsafe_allow_html=True)
if st.button("خروج"): st.session_state['logged_in']=False; st.session_state['show_landing']=True; st.rerun()
if st.session_state['username']=="admin":
    db=st.session_state['users_db']; st.metric("Revenue", f"${sum([v.get('usd',0) for v in db.values()])}")
    st.dataframe(pd.DataFrame([{"User":k,"Offer":v.get("offer",""),"USD":v.get("usd",0),"Email":v.get("email","")} for k,v in db.items() if k!="admin"]), use_container_width=True)
