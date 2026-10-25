<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TASHEER FAST</title>
<style>body{background:#f8fafc;font-family:Tahoma;padding:10px} .c{max-width:700px;margin:auto;background:#fff;padding:14px;border-radius:12px;border:1px solid #e2e8f0} input{width:100%;padding:12px;margin:4px 0;border:1px solid #cbd5e1;border-radius:8px;font-size:16px} button{width:100%;padding:14px;background:#0f172a;color:#fff;border-radius:10px;font-size:16px;font-weight:bold;margin-top:8px} table{width:100%;margin-top:10px;border-collapse:collapse} td,th{border:1px solid #e2e8f0;padding:6px;font-size:13px}</style></head>
<body><div class="c">
<h3>تأشير - إدخال سريع</h3>
<input id="n" placeholder="الاسم كما في الجواز - انسخ ولصق">
<input id="p" placeholder="رقم الجواز" style="direction:ltr">
<input id="d" placeholder="تاريخ الميلاد">
<input id="e" placeholder="تاريخ الانتهاء">
<button onclick="add()">إضافة + Enter</button>
<table><thead><tr><th>#</th><th>الاسم</th><th>الجواز</th><th>حذف</th></tr></thead><tbody id="tb"></tbody></table>
<button onclick="exp()" style="background:#16a34a">تصدير Excel</button>
</div>
<script>
let r=[]; function add(){let o={n:document.getElementById('n').value,p:document.getElementById('p').value,d:document.getElementById('d').value,e:document.getElementById('e').value}; if(!o.n&&!o.p)return; r.push(o); render(); document.getElementById('n').value='';document.getElementById('p').value='';document.getElementById('n').focus();}
function render(){let tb=document.getElementById('tb');tb.innerHTML='';r.forEach((x,i)=>{tb.innerHTML+=`<tr><td>${i+1}</td><td>${x.n}</td><td>${x.p}</td><td><button onclick="r.splice(${i},1);render()">x</button></td></tr>`})}
function exp(){let csv='Name,Passport,DOB,Expiry\n';r.forEach(x=>csv+=`"${x.n}","${x.p}","${x.d}","${x.e}"\n`);let a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));a.download='tasheer.csv';a.click();}
document.addEventListener('keydown',e=>{if(e.key==='Enter')add()});
</script></body></html>
