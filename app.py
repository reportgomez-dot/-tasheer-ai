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
.hero {background:linear-gradient(135deg, #0A1931 0%, #0E4D4F 50%, #B8860B 100%); color:white; padding:50px 30px; border-radius:20px; text-align:center; margin-bottom:20px;}
.hero h1{font-size:48px; font-weight:800; margin:0;} .hero p{font-size:18px; opacity:0.9;}
.offer-card {background:white; border:2px solid #E2E8F0; border-radius:16px; padding:24px; text-align:center; height:420px; position:relative; transition:0.3s; box-shadow:0 4px 12px rgba(10,25,49,0.06);}
.offer-card:hover{border-color:#B8860B; transform:translateY(-5px); box-shadow:0 12px 24px rgba(10,25,49,0.15);}
.offer-card.popular {border:2px solid #B8860B; background:linear-gradient(180deg, #FFFBEB 0%, #FFFFFF 100%);}
.offer-badge {background:#B8860B; color:white; padding:4px 12px; border-radius:12px; font-size:11px; font-weight:700; position:absolute; top:-12px; left:50%; transform:translateX(-50%);}
.price {font-size:42px; font-weight:800; color:#0A1931;} .price span{font-size:16px; color:#718096;}
.feature {text-align:left; margin:8px 0; font-size:13px;} .feature ✅{color:#0E4D4F;}
.tasheer-header{background:#FFF; border-bottom:2px solid #0A1931; padding:12px 20px; display:flex; justify-content:space-between; align-items:center;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="tasheer-header">
<div style="font-size:26px; font-weight:800; color:#0A1931;">TASHEER<span style="color:#B8860B;">AI</span> <span style="font-size:10px; background:linear-gradient(135deg,#0A1931,#B8860B); color:white; padding:4px 10px; border-radius:12px;">OFFICIAL</span></div>
<div style="font-size:11px;">wail.ungm1191731.lab@gmail.com | SECURE</div>
</div>
""", unsafe_allow_html=True)

# Session
default_admin={"password":"Tasheer2024","name":"Admin","email":"wail.ungm1191731.lab@gmail.com","sub_end":(datetime.now()+timedelta(days=365)).isoformat(),"active":True,"usd":0,"tx":"MASTER"}
loaded=load_json(USERS_FILE, {"admin":default_admin}); loaded["admin"]=default_admin
if 'users_db' not in st.session_state: st.session_state['users_db']=loaded
else: st.session_state['users_db']["admin"]=default_admin
if 'logged_in' not in st.session_state: st.session_state['logged_in']=False
if 'username' not in st.session_state: st.session_state['username']=""
if 'show_landing' not in st.session_state: st.session_state['show_landing']=True
def save_all(): save_json(USERS_FILE, st.session_state['users_db'])

if st.session_state['show_landing'] and not st.session_state['logged_in']:
    # === OFFICIAL HERO WITH OFFERS ===
    st.markdown("""
    <div class="hero">
        <h1>TASHEER AI</h1>
        <p>المنصة الرسمية الآمنة لإدارة التأشيرات والمراسلات - IP Original - مسجل للملكية الفكرية</p>
        <p style="font-size:14px; margin-top:10px;">🌐 Official Site: tasheer-ai-juub2hzyqf9boqzthpwv4n.streamlit.app | 📧 wail.ungm1191731.lab@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 💎 الباقات الرسمية - Official Offers")
    col1,col2,col3=st.columns(3)
    with col1:
        st.markdown("""
        <div class="offer-card">
            <h3>🥉 الباقة الأساسية</h3>
            <div class="price">$299 <span>/ شهر</span></div>
            <p style="color:#718096; font-size:12px;">مثالي للشركات الصغيرة</p>
            <div class="feature">✅ 5 حسابات موظفين</div>
            <div class="feature">✅ 500 مراسلة / شهر</div>
            <div class="feature">✅ نظام Gmail آمن</div>
            <div class="feature">✅ فواتير تلقائية</div>
            <div class="feature">✅ دعم فني</div>
            <div style="margin-top:20px; font-size:11px; color:#B8860B; font-weight:700;">الأكثر طلباً للبداية</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="offer-card popular">
            <div class="offer-badge">🔥 الأكثر مبيعاً</div>
            <h3>🥇 الباقة الاحترافية</h3>
            <div class="price">$599 <span>/ شهر</span></div>
            <p style="color:#718096; font-size:12px;">لشركات التأشيرات المتوسطة</p>
            <div class="feature">✅ 20 حساب موظف</div>
            <div class="feature">✅ مراسلات غير محدودة</div>
            <div class="feature">✅ نظام ذكي AI</div>
            <div class="feature">✅ تقارير متقدمة</div>
            <div class="feature">✅ أولوية دعم 24/7</div>
            <div class="feature">✅ دومين خاص</div>
            <div style="margin-top:15px; background:#0A1931; color:white; padding:8px; border-radius:8px; font-size:12px;">وفر $199</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="offer-card">
            <h3>💎 باقة المؤسسات</h3>
            <div class="price">$999 <span>/ شهر</span></div>
            <p style="color:#718096; font-size:12px;">للمؤسسات الكبرى</p>
            <div class="feature">✅ حسابات غير محدودة</div>
            <div class="feature">✅ White Label كامل</div>
            <div class="feature">✅ API مفتوح</div>
            <div class="feature">✅ مدير حساب خاص</div>
            <div class="feature">✅ تدريب فريق</div>
            <div class="feature">✅ حماية WIPO IP</div>
            <div style="margin-top:15px; font-size:11px; color:#0E4D4F; font-weight:700;">للشركات الكبرى فقط</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔐 التسجيل الرسمي - Official Registration")
    tab1,tab2,tab3=st.tabs(["🚀 تسجيل جديد / Register","🔑 دخول / Login","🔒 نسيت كلمة المرور / Forgot"])
    with tab1:
        st.markdown('<div style="background:white; border-radius:14px; padding:20px; border:1px solid #E2E8F0; border-top:3px solid #B8860B;">',unsafe_allow_html=True)
        with st.form("reg"):
            c1,c2=st.columns(2)
            with c1: u=st.text_input("Username / اسم المستخدم",placeholder="almjal_company")
            with c2: e=st.text_input("Email الرسمي",placeholder="info@company.com")
            p=st.text_input("كلمة المرور",type="password")
            st.markdown(f"**الدفع الرسمي - Official Payment:** `{WALLET}` (USDT TRC20)")
            col_qr,col_tx=st.columns([1,2])
            with col_qr: st.image(QR_URL,width=160)
            with col_tx: 
                offer=st.selectbox("اختر الباقة / Select Offer",["$299 Basic - الأساسية","$599 Pro - الاحترافية 🔥","$999 Enterprise - المؤسسات"])
                tx=st.text_input("TxID - بعد الدفع الصق معرف العملية هنا",placeholder="a1b2c3d4e5...")
                st.info(f"بعد دفع {offer.split(' ')[0]} أرسل TxID للتفعيل الفوري")
            if st.form_submit_button(f"✅ تفعيل فوري - Activate {offer.split(' ')[0]}",type="primary",use_container_width=True):
                if u and e and p and len(tx)>=10:
                    price=299 if "299" in offer else 599 if "599" in offer else 999
                    st.session_state['users_db'][u.strip().lower()]={"password":p,"name":u,"email":e,"sub_end":(datetime.now()+timedelta(days=30)).isoformat(),"active":True,"usd":price,"tx":tx.strip(),"offer":offer}
                    save_all(); st.session_state['logged_in']=True; st.session_state['username']=u.strip().lower(); st.session_state['show_landing']=False; st.success(f"تم تفعيل {offer} بنجاح!"); st.rerun()
                else: st.error("أكمل البيانات و TxID صحيح")
        st.markdown('</div>',unsafe_allow_html=True)
    with tab2:
        with st.form("login"):
            u=st.text_input("Username"); p=st.text_input("Password",type="password")
            if st.form_submit_button("Login",type="primary",use_container_width=True):
                db_lower={k.lower():k for k in st.session_state['users_db'].keys()}
                if u.strip().lower() in db_lower:
                    real=db_lower[u.strip().lower()]
                    if st.session_state['users_db'][real]["password"]==p:
                        st.session_state['logged_in']=True; st.session_state['username']=real; st.session_state['show_landing']=False; st.rerun()
                    else: st.error("كلمة مرور خطأ")
    with tab3:
        with st.form("forgot"):
            fu=st.text_input("Username"); ftx=st.text_input("Old TxID"); fn=st.text_input("New Password",type="password"); fc=st.text_input("Confirm",type="password")
            if st.form_submit_button("Reset Password",type="primary",use_container_width=True):
                if fu and ftx and fn and fn==fc:
                    db_lower={k.lower():k for k in st.session_state['users_db'].keys()}
                    if fu.strip().lower() in db_lower:
                        real=db_lower[fu.strip().lower()]
                        if ftx.strip()==st.session_state['users_db'][real].get("tx","") or real=="admin":
                            st.session_state['users_db'][real]["password"]=fn; save_all(); st.success("تم - اذهب للدخول")
    st.markdown('<div style="text-align:center; padding:20px; color:#888; font-size:11px;">© 2026 TASHEER AI - Official Site - IP Original Navy Gold Teal - wail.ungm1191731.lab@gmail.com<br>All Offers Include WIPO IP Protection - No Google Colors</div>',unsafe_allow_html=True)
    st.stop()

# Admin
st.markdown(f'<div style="background:#0A1931; color:white; border-radius:10px; padding:10px 16px;">✅ {st.session_state["username"]} - LIVE</div>',unsafe_allow_html=True)
if st.button("خروج"): st.session_state['logged_in']=False; st.session_state['show_landing']=True; st.rerun()
if st.session_state['username']=="admin":
    db=st.session_state['users_db']
    st.metric("Revenue", f"${sum([v.get('usd',0) for v in db.values()])}")
    st.dataframe(pd.DataFrame([{"User":k,"Offer":v.get("offer",""),"USD":v.get("usd",0),"Email":v.get("email","")} for k,v in db.items() if k!="admin"]), use_container_width=True)
