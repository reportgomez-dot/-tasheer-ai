import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="UN-BIO-SHIELD - Gene Balance")

st.title("تصنيع رصيد من أكواد الجينات")

gene = st.text_input("Enter Gene Sequence", "ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG")

# حساب الرصيد المحلي
if gene:
    balance = len(gene) * 1000
    st.success(f"تم تصنيع الرصيد: {balance} GENE")
    col1, col2 = st.columns(2)
    col1.metric("رصيدك", f"{balance} GENE")
    col1.metric("Award Price", "50M SAR")
    col2.metric("Recom Price", "100M SAR")

st.divider()
st.subheader("تحويل الرصيد للبلوكشين - BEP20")

# كود ربط الميتاماسك - يشتغل في Streamlit
components.html("""
<script src="https://cdn.jsdelivr.net/npm/web3@1.8.2/dist/web3.min.js"></script>
<button id="connect" style="padding:12px 25px; background:#f0b90b; border:none; border-radius:8px; font-weight:bold; cursor:pointer;">Connect MetaMask & Mint GENE</button>
<p id="status" style="margin-top:15px;"></p>

<script>
const contractAddress = "0xYOUR_CONTRACT_ADDRESS_HERE"; // حط عنوان عقدك من Remix هنا
const abi = [{"inputs":[{"internalType":"string","name":"_geneCode","type":"string"}],"name":"createBalanceFromGene","outputs":[],"stateMutability":"nonpayable","type":"function"}];

document.getElementById('connect').onclick = async () => {
  if (window.ethereum) {
    try {
      const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
      const web3 = new Web3(window.ethereum);
      const contract = new web3.eth.Contract(abi, contractAddress);
      const geneInput = window.parent.document.querySelector('input[type="text"]')?.value || "ATCG";
      
      document.getElementById('status').innerText = "جاري تصنيع الرصيد في محفظتك...";
      
      await contract.methods.createBalanceFromGene(geneInput).send({ from: accounts[0] });
      
      document.getElementById('status').innerText = "✅ تم! الرصيد الآن في محفظتك: " + geneInput.length * 1000 + " GENE";
    } catch (e) {
      document.getElementById('status').innerText = "خطأ: " + e.message;
    }
  } else {
    document.getElementById('status').innerText = "ثبت MetaMask أولا";
  }
}
</script>
""", height=200)

st.info("1. انشر العقد في Remix على BSC Testnet\n2. انسخ عنوان العقد والصقه في contractAddress فوق\n3. اعمل Commit")
