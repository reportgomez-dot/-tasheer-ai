# === رابط خاص لكل عميل ===
query_params = st.query_params
client_param = query_params.get("client", None)

if client_param:
    # إذا دخل: tasheer-ai.com/?client=almajal
    # يطلع له: مرحبا شركة المجال - موقعك الخاص
    st.markdown(f"""
    <div style="background: linear-gradient(135deg,#0a7a42,#0d4a2a); color:white; padding:20px; border-radius:15px; text-align:center;">
        <h1>🏢 موقع {client_param} الخاص</h1>
        <p>Powered by TASHEER AI - tasheer-ai.com</p>
        <p>26 دولة | 27 عملة | خريطة MA DZ SA</p>
    </div>
    """, unsafe_allow_html=True)
