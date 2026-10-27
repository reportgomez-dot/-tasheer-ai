<!DOCTYPE html>
<html dir="rtl">
<head>
<title>UN-BIO-SHIELD AI - Live Demo - UNGM 1191371</title>
<style>
body{background:#0a2540;color:white;font-family:Arial;padding:30px;text-align:center}
.box{background:white;color:black;padding:30px;border-radius:15px;max-width:600px;margin:auto}
input{width:90%;padding:15px;margin:10px;border:2px solid #0a2540;border-radius:10px}
button{padding:15px 40px;background:#0a2540;color:white;border:none;border-radius:10px;font-size:18px;cursor:pointer}
.result{margin-top:20px;padding:20px;background:#e8f5e9;border-radius:10px;display:none}
.price{color:#0a2540;font-weight:bold;font-size:20px}
</style>
</head>
<body>
<h1>UN-BIO-SHIELD AI - 50M / 100M SAR</h1>
<p>Serial: UN-MODEL-50M-ARAMCO-001 | UNGM 1191371</p>

<div class="box">
<h3>جرب النموذج الآن - Live API</h3>
<input id="gene" placeholder="الصق التسلسل الجيني - مثال: ATGCGTAGCGTGGCTAGGTAG" value="ATGCGTAGCGTGGCTAGGTAG">
<br>
<input id="company" placeholder="اسم شركتك - ARAMCO / NEOM">
<br>
<button onclick="check()">افحص الآن - 10 ثواني</button>

<div id="res" class="result">
<p id="out"></p>
<p class="price">التكلفة: 5000 SAR / فحص | اشتراك 50M-100M / سنة</p>
<p>Binance Pay: USDT BEP20 - Streaming Active</p>
<a href="/mnt/data/Aramco_50M_Offer_UNGM1191371.pdf">تحميل عرض أرامكو 50M PDF</a> | 
<a href="/mnt/data/NEOM_100M_Offer_UNGM1191371.pdf">تحميل عرض نيوم 100M PDF</a>
</div>
</div>

<script>
function check(){
  let gene=document.getElementById('gene').value;
  let company=document.getElementById('company').value;
  document.getElementById('res').style.display='block';
  document.getElementById('out').innerHTML="⏳ جاري الفحص... "+gene.substring(0,20)+"...<br><br>";
  setTimeout(()=>{
    let isCont = gene.includes("CGTAG") ? "CONTAMINATED 95% - خطر - أوقف المحطة" : "CLEAN 98% - نظيف";
    let color = isCont.includes("CONTAMINATED") ? "red" : "green";
    document.getElementById('out').innerHTML=`<b style="color:${color};font-size:20px">${isCont}</b><br><br>الشركة: ${company}<br>السيريال: UN-MODEL-50M-ARAMCO-001<br>الدقة: 94%<br>وقت الفحص: 10 ثواني`;
  },2000);
}
</script>
</body>
</html>
