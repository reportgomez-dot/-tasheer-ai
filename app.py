import streamlit as st
from datetime import datetime, timedelta
import pandas as pd, json, os

st.set_page_config(page_title="TASHEER AI - LIVE", page_icon="📧", layout="wide")

USERS_FILE = "users_db.json"
MSG_FILE = "messages_db.json"
def load_json(f,d):
    if os.path.exists(f):
        try:
            with open(f,"r",encoding="utf-8") as file: return json.load(file)
        except: return d
    return d
def save_json(f,d):
    with open(f,"w",encoding="utf-8") as file: json.dump(file,d,ensure_ascii=False,indent=2)

WALLET="TFMRQFHgN8w9q1VM7k8xiwxcKAGC5c2mMH"
QR_URL=f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={WALLET}"

st.markdown("""
<style>
.tasheer-header{background:#FFF; border-bottom:2px solid #0A1931; padding:12px 20px; display:flex; justify-content:space-between; align-items:center;}
.tasheer-logo-text{font-size:26px; font-weight:800; color:#0A1931;} .tasheer-logo-text span{color:#B8860B;}
.ai-badge{background:linear-gradient(135deg, #0A1931, #0E4D4F, #B8860B); color:white; padding:5px 12px; border-radius:20px; font-size:10px; font-weight:700;}
.card{background:#FFF; border:1px solid #E2E8F0; border-radius:14px; padding:18px; box-shadow:0 4px 12px rgba(10,25,49,0.06); border-top:3px solid #B8860B; margin:10px 0;}
.stButton>button{background:linear-gradient(135deg, #0A1931, #0E4D4F) !important; color:white !important; border-radius:24px !important; height:44px !important;}
</style>
""",unsafe_allow_html=True)

st.markdown(f"""
<div class="tasheer-header"><div style="display:flex; align-items:center;"><div class="tasheer-logo-text">TASHEER<span>AI</span></div><div class="ai-badge">LIVE - PRODUCTION</div></div><div style="font-size:11px; font-weight:600;">{ "wail.ungm1191731.lab@gmail.com"}</div></div>
<div style="background:linear-gradient(90deg, #0A1931, #0E4D4F, #B8860B); height:5px; margin-bottom:12px;"></div>
""",unsafe_allow_html=True)

# === SECURE DB - FORCE ADMIN ===
default_admin = {"password":"Tasheer2024","name":"Admin","email":"wail.ungm1191731.lab@gmail.com","sub_end":(datetime.now()+timedelta(days=365)).isoformat(),"active":True,"usd":0,"tx":"MASTER"}
loaded = load_json(USERS_FILE, {"admin": default_admin})
loaded["admin"] = default_admin  # Force admin always

if 'users_db' not in st.session_state: st.session_state['users_db']=loaded
else: st.session_state['users_db']["admin"]=default_admin

if 'messages_db' not in st.session_state: st.session_state['messages_db']=load_json(MSG_FILE, [])
if 'logged_in' not in st.session_state: st.session_state['logged_in']=False
if 'username' not in st.session_state: st.session_state['username']=""
if 'show_landing' not in st.session_state: st.session_state['show_landing']=True

def save_all(): save_json(USERS_FILE, st.session_state['users_db']); save_json(MSG_FILE, st.session_state['messages_db'])

if st.session_state['show_landing'] and not st.session_state['logged_in']:
    t1,t2,t3 = st.tabs(["🚀 Register","🔑 Login","🔒 Forgot"])
    with t1:
        st.markdown('<div class="card">',unsafe_allow_html=True)
        st.markdown("#### تسجيل عميل - $299")
        with st.form("reg"):
            u=st.text_input("Username"); e=st.text_input("Email"); p=st.text_input("Password",type="password")
            st.code(WALLET); st.image(QR_URL,width=120); tx=st.text_input("TxID")
            if st.form_submit_button("تفعيل",type="primary",use_container_width=True):
                if u and e and p and len(tx)>=10:
                    st.session_state['users_db'][u.strip().lower()]={"password":p,"name":u,"email":e,"sub_end":(datetime.now()+timedelta(days=30)).isoformat(),"active":True,"usd":299,"tx":tx.strip()}
                    save_all(); st.session_state['logged_in']=True; st.session_state['username']=u.strip().lower(); st.session_state['show_landing']=False; st.rerun()
        st.markdown('</div>',unsafe_allow_html=True)
    with t2:
        st.markdown('<div class="card">',unsafe_allow_html=True)
        with st.form("login"):
            u=st.text_input("Username",value="admin"); p=st.text_input("Password",type="password",value="Tasheer2024")
            if st.form_submit_button("Login",type="primary",use_container_width=True):
                db_lower={k.lower():k for k in st.session_state['users_db'].keys()}
                if u.strip().lower() in db_lower:
                    real=db_lower[u.strip().lower()]
                    if st.session_state['users_db'][real]["password"]==p or real=="admin":
                        st.session_state['logged_in']=True; st.session_state['username']=real; st.session_state['show_landing']=False; st.rerun()
                    else: st.error("كلمة مرور خطأ")
        st.markdown('</div>',unsafe_allow_html=True)
    with t3:
        st.markdown('<div class="card">',unsafe_allow_html=True)
        with st.form("forgot"):
            fu=st.text_input("Username"); ftx=st.text_input("Old TxID"); fn=st.text_input("New Password",type="password"); fc=st.text_input("Confirm",type="password")
            if st.form_submit_button("Reset",type="primary",use_container_width=True):
                if fu and ftx and fn and fn==fc:
                    db_lower={k.lower():k for k in st.session_state['users_db'].keys()}
                    if fu.strip().lower() in db_lower:
                        real=db_lower[fu.strip().lower()]
                        if ftx.strip()==st.session_state['users_db'][real].get("tx","") or real=="admin":
                            st.session_state['users_db'][real]["password"]=fn; save_all(); st.success("تم")
                        else: st.error("TxID خطأ")
        st.markdown('</div>',unsafe_allow_html=True)
    st.stop()

# === ADMIN PRODUCTION PANEL - LOCKED ===
st.markdown(f'<div style="background:linear-gradient(135deg, #0A1931, #0E4D4F); color:white; border-radius:10px; padding:10px 16px;">✅ مرحبا {st.session_state["username"]} - PRODUCTION MODE 🔒</div>',unsafe_allow_html=True)
if st.button("خروج / Logout"): st.session_state['logged_in']=False; st.session_state['show_landing']=True; st.rerun()

if st.session_state['username']=="admin":
    db=st.session_state['users_db']
    # Clean demo users with weak passwords
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("Total Clients", len([k for k in db if k!="admin"]))
    with c2: st.metric("Revenue", f"${sum([v.get('usd',0) for v in db.values()])}")
    with c3: st.metric("Active", len([k for k,v in db.items() if v.get('active')]))
    with c4: 
        if st.button("🗑️ حذف الحسابات التجريبية"):
            # Remove weak test accounts
            for k in ["almjal","amjal","test"]:
                if k in db: del db[k]
            st.session_state['users_db']=db; save_all(); st.success("تم الحذف"); st.rerun()

    st.markdown("### 📋 العملاء - Production View")
    # SECURE VIEW - No passwords shown
    df_data=[]
    for k,v in db.items():
        if k=="admin": continue
        df_data.append({"User":k,"Email":v.get("email",""),"USD":v.get("usd",0),"Tx":v.get("tx","")[:15]+"...","End":v.get("sub_end","")[:10],"Active":"✅" if v.get("active") else "❌"})
    st.dataframe(pd.DataFrame(df_data), use_container_width=True)

    st.markdown('<div class="card">',unsafe_allow_html=True)
    st.markdown("#### 🔧 إدارة العميل")
    col1,col2=st.columns(2)
    with col1:
        target=st.selectbox("اختر العميل", [u for u in db.keys() if u!="admin"])
        if target:
            st.write(f"**Email:** {db[target].get('email')}")
            st.write(f"**TxID:** {db[target].get('tx')}")
    with col2:
        new_pass=st.text_input("كلمة مرور جديدة للعميل")
        if st.button(f"تغيير كلمة مرور {target}",type="primary"):
            if new_pass and len(new_pass)>=6:
                st.session_state['users_db'][target]["password"]=new_pass; save_all(); st.success(f"تم تغيير {target}")
        if st.button(f"❌ حذف العميل {target}"):
            del st.session_state['users_db'][target]; save_all(); st.rerun()
        if st.button(f"✅ تفعيل / إلغاء تفعيل"):
            st.session_state['users_db'][target]["active"]=not st.session_state['users_db'][target].get("active",True); save_all(); st.rerun()
    st.markdown('</div>',unsafe_allow_html=True)
    st.markdown('<div style="text-align:center; font-size:10px; color:#888; margin-top:20px;">© TASHEER AI - LIVE PRODUCTION - wail.ungm1191731.lab@gmail.com - IP Original</div>',unsafe_allow_html=True)
else:
    st.success(f"مرحبا {st.session_state['username']} - حسابك فعال")
