# === ضيف هذا الـ CSS الجديد فوق في الـ st.markdown ===
st.markdown("""
<style>
.stApp {background:#ffffff !important;}
/* Google Logo Style Header */
.google-header {
    background:#ffffff; 
    border-bottom:1px solid #dadce0; 
    padding:18px 20px; 
    display:flex; 
    align-items:center; 
    justify-content:space-between;
    position:sticky; top:0; z-index:100;
}
.google-logo {
    font-family: 'Google Sans', 'Roboto', sans-serif;
    font-size:26px;
    font-weight:400;
    letter-spacing:-0.5px;
}
.google-logo span:nth-child(1) {color:#4285F4;}
.google-logo span:nth-child(2) {color:#EA4335;}
.google-logo span:nth-child(3) {color:#FBBC05;}
.google-logo span:nth-child(4) {color:#4285F4;}
.google-logo span:nth-child(5) {color:#34A853;}
.google-logo span:nth-child(6) {color:#EA4335;}
.google-logo span:nth-child(7) {color:#4285F4; font-weight:500;}
.ai-badge {
    background: linear-gradient(135deg, #4285F4, #9C27B0);
    color:white; 
    padding:4px 10px; 
    border-radius:16px; 
    font-size:12px; 
    font-weight:600; 
    margin-left:10px;
    box-shadow:0 2px 6px rgba(66,133,244,0.3);
}
.gmail-table {width:100%; border-collapse: collapse; background:white; border-radius:8px; overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,0.1);}
.gmail-table th {background:#f1f3f4; color:#5f6368; font-weight:500; padding:12px; text-align:left; font-size:13px; border-bottom:1px solid #dadce0;}
.gmail-table td {padding:14px 12px; border-bottom:1px solid #eceff1; font-size:14px; color:#202124;}
.gmail-table tr:hover {background:#f8f9fa;}
.welcome-box {background:#e8f0fe; border:1px solid #d2e3fc; border-radius:8px; padding:12px 16px; color:#1967d2;}
.card-google {background:#ffffff; border:1px solid #e8eaed; border-radius:12px; padding:16px; box-shadow:0 1px 2px rgba(60,64,67,0.1); margin:10px 0;}
.stButton>button {background:#1a73e8 !important; color:white !important; border-radius:24px !important; border:none !important; font-weight:500 !important; padding:0 24px !important; height:36px !important;}
</style>
""", unsafe_allow_html=True)

# === ضيف هذا الهيدر بدل القديم ===
st.markdown("""
<div class="google-header">
    <div style="display:flex; align-items:center;">
        <div class="google-logo">
            <span>T</span><span>A</span><span>S</span><span>H</span><span>E</span><span>E</span><span>R</span>
            <span style="color:#5f6368; font-size:22px; font-weight:400; margin-left:4px;">AI</span>
            <span class="ai-badge">3D • Gmail • PRO</span>
        </div>
    </div>
    <div style="display:flex; align-items:center; gap:12px;">
        <div style="width:32px; height:32px; background:#8ab4f8; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; font-weight:600;">A</div>
    </div>
</div>
<div style="background:linear-gradient(90deg, #4285F4 0%, #EA4335 33%, #FBBC05 66%, #34A853 100%); height:4px; width:100%; margin-bottom:16px;"></div>
""", unsafe_allow_html=True)
