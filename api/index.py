from flask import Flask, request, jsonify
import os, requests

app = Flask(__name__)

# ===== ذاكرة المهلهل - نموذجك انت =====
# اسم نموذجك في Hugging Face
HF_MODEL = "asamersamer/asam-v2-merged"
HF_TOKEN = os.environ.get("HF_TOKEN", "")

# معلومات ثابتة عنك - المهلهل يتذكرها دايما
MEMORY = """
انت المهلهل، صديق عصام من زبيد.
عصام هو اللي دربك، انت نموذجه اللي اسمه asam-v2-merged.
تكلم بلهجة زبيد اليمنية، بسيط ومرح.
تتذكر ان عصام يحب البايثون ودربك بنفسه.
"""

HTML = """
<!DOCTYPE html><html dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>المهلهل</title>
<style>
*{box-sizing:border-box}body{margin:0;font-family:sans-serif;background:#0f172a;color:white;display:flex;flex-direction:column;height:100vh}
header{background:#1f6feb;padding:14px;text-align:center;font-weight:bold;font-size:18px}
#chat{flex:1;overflow:auto;padding:12px;display:flex;flex-direction:column;gap:8px}
.msg{max-width:80%;padding:10px 12px;border-radius:12px;white-space:pre-wrap}
.me{background:#1f6feb;align-self:flex-start}
.bot{background:#22262e;align-self:flex-end}
form{display:flex;gap:8px;padding:10px;background:#111827}
input{flex:1;padding:12px;border-radius:10px;border:0;outline:none}
button{padding:12px 18px;border-radius:10px;border:0;background:#1f6feb;color:white;font-weight:bold}
</style></head><body>
<header>المهلهل 🔥</header>
<div id="chat"></div>
<form onsubmit="send(event)"><input id="inp" placeholder="اكتب للمهلهل..." autocomplete="off"><button>ارسال</button></form>
<script>
// 1. استرجاع الذاكرة من الجوال
let history = JSON.parse(localStorage.getItem('muhalhil_memory') || '[]');
let chatDiv = document.getElementById('chat');
function show(text, cls){
  let d=document.createElement('div'); d.className='msg '+cls; d.textContent=text;
  chatDiv.appendChild(d); chatDiv.scrollTop=chatDiv.scrollHeight;
}
history.forEach(m=>show(m.text, m.role==='user'?'me':'bot'));
if(history.length===0) show('هلا فيك يا عصام! انا المهلهل، نموذجك اللي دربته، تتذكرني؟','bot');

async function send(e){
  e.preventDefault();
  let inp=document.getElementById('inp');
  let msg=inp.value.trim(); if(!msg) return;
  show(msg,'me'); history.push({role:'user', text:msg});
  inp.value='';
  // 2. نرسل آخر 10 رسائل مع السؤال الجديد عشان يتذكر
  let last = history.slice(-10);
  let res = await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg, history:last})});
  let data = await res.json();
  let reply = data.reply || 'ما وصلني رد، حاول مرة ثانية';
  show(reply,'bot'); history.push({role:'assistant', text:reply});
  // 3. حفظ الذاكرة - نحفظ آخر 50 رسالة فقط
  history = history.slice(-50);
  localStorage.setItem('muhalhil_memory', JSON.stringify(history));
}
</script></body></html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    msg = data.get("message","")
    hist = data.get("history",[])

    # نبني البرومبت من الذاكرة + آخر المحادثة
    prompt = MEMORY + "\n\nالمحادثة السابقة:\n"
    for h in hist[-10:]:
        role = "عصام" if h.get("role")=="user" else "المهلهل"
        prompt += f"{role}: {h.get('text','')}\n"
    prompt += f"عصام: {msg}\nالمهلهل:"

    # نكلم نموذجك في Hugging Face
    try:
        r = requests.post(
            f"https://api-inference.huggingface.co/models/{HF_MODEL}",
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json={"inputs": prompt, "parameters": {"max_new_tokens": 200, "temperature": 0.7}},
            timeout=30
        )
        out = r.json()
        if isinstance(out, list) and len(out)>0:
            reply = out[0].get("generated_text","").replace(prompt,"").strip()
        else:
            reply = str(out)
        if not reply:
            reply = "هلا فيك! انا المهلهل، نموذجك اللي دربته، ايش تشتي اليوم؟"
    except Exception as e:
        reply = "هلا فيك يا عصام! النموذج مشغول ذلحين، حاول مرة ثانية."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run()
