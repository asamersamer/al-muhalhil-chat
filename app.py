import os
from flask import Flask, request, jsonify

app = Flask(__name__)

HTML = """
<!DOCTYPE html><html lang="ar" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>المهلهل</title>
<style>
body{font-family:system-ui;background:#111;color:#fff;margin:0;display:flex;flex-direction:column;height:100vh}
header{padding:14px;text-align:center;background:#1a1a1a;font-weight:bold;font-size:20px}
#chat{flex:1;overflow:auto;padding:12px;display:flex;flex-direction:column;gap:8px}
.msg{padding:10px 14px;border-radius:14px;max-width:85%}
.user{background:#2563eb;align-self:flex-start}
.bot{background:#222;align-self:flex-end;border:1px solid #333}
form{display:flex;gap:8px;padding:10px;background:#1a1a1a}
input{flex:1;padding:12px;border-radius:20px;border:0;outline:none}
button{padding:12px 18px;border-radius:20px;border:0;background:#2563eb;color:#fff;font-weight:bold}
</style></head><body>
<header>🐎 المهلهل - دردشة باليمني</header>
<div id="chat"><div class="msg bot">هلا! أنا المهلهل، هات أي شي ثاني؟</div></div>
<form id="f"><input id="i" placeholder="اكتب هنا..."><button>إرسال</button></form>
<script>
const chat=document.getElementById('chat');
document.getElementById('f').onsubmit=async(e)=>{
e.preventDefault();
let v=document.getElementById('i').value; if(!v) return;
document.getElementById('i').value='';
chat.innerHTML+='<div class="msg user">'+v+'</div>';
let r=await fetch('/v1/chat/completions',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({messages:[{role:'user',content:v}]})});
let j=await r.json();
chat.innerHTML+='<div class="msg bot">'+j.choices[0].message.content+'</div>';
chat.scrollTop=99999;
}
</script></body></html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/v1/models")
def models():
    return jsonify({"data": [{"id": "
