import streamlit as st

st.set_page_config(page_title="TASHEER AI", layout="wide")

st.markdown("""
<h1 style='text-align:center;'>TASHEER AI</h1>
<p style='text-align:center;'>Riyadh - Serving Pakistan Travel Agencies</p>
<p style='text-align:center;'>Founder: WAIL SALAHELDIN ABDULLA</p>
<p style='text-align:center;'>Contact: contact@tasheer.ai</p>
""", unsafe_allow_html=True)

st.divider()

st.write("Auto-organizes passports from WhatsApp into client folders.")
st.write("Saves 3hrs/day for travel agencies.")

st.link_button("Contact us: contact@tasheer.ai", "mailto:tasheerai.contact@gmail.com")
st.link_button("WhatsApp Demo", "https://wa.me/966500000000")
