import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="GENE Factory - 1000 Trillion", layout="centered")
st.title("🏭 مصنع GENE - 1000 تريليون")
st.write("اضغط الزر يصنع لك 1,000,000,000,000,000 حبة مرة وحدة")
CONTRACT_ADDRESS = "0x123... عنوان عقدك الحقيقي هنا"

html_code = f"""
<script src="https://cdn.jsdelivr.net/npm/web3@1.8.2/dist/web3.min.js"></script>
<button id="btn" style="width:100%; padding:20px; font-size:22px; background:#f0b90b; border:none; border-radius:12px; cursor:pointer; font-weight:bold;">🔨 اصنع 1000 تريليون الان</button>
<p id="status" style="text-align:center; margin-top:15px;"></p>
<script>
const contractAddress = "{CONTRACT_ADDRESS}";
const abi = [{{"inputs":[],"name":"mint1000T","outputs":[],"stateMutability":"nonpayable","type":"function"}}];
async function mint() {{
    if (!window.ethereum) {{ alert("افتح MetaMask"); return; }}
    const web3 = new Web3(window.ethereum);
    await window.ethereum.request({{method:'eth_requestAccounts'}});
    const accounts = await web3.eth.getAccounts();
    const contract = new web3.eth.Contract(abi, contractAddress);
    document.getElementById("status").innerText = "⏳ جاري الصنع...";
    try {{
        await contract.methods.mint1000T().send({{from: accounts[0]}});
        document.getElementById("status").innerText = "✅ تم صنع 1000 تريليون بنجاح!";
    }} catch(e) {{
        document.getElementById("status").innerText = "❌ فشل: " + e.message;
    }}
}}
document.getElementById("btn").onclick = mint;
</script>
"""
components.html(html_code, height=200)
