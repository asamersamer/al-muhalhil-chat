from http.server import BaseHTTPRequestHandler
import json, os, urllib.request

# ذاكرة المهلهل
MEMORY = "انت المهلهل، صديق عصام من زبيد. عصام هو اللي دربك، نموذجك asam-v2-merged. تكلم بلهجة زبيد، بسيط ومرح."

HTML = """<!DOCTYPE html><html dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>المهلهل</title><style>*{box-sizing:border-box}body{margin:0;font-family:sans-serif;background:#0f172a;color:white;display:flex;flex-direction:column;height:100vh}header{background:#1f6feb;padding:14px;text-align:center;font-weight:bold;font-size:18px}#chat{flex:1;overflow:auto;padding:12px;display:flex;flex-direction:column;gap:8px}.msg{max-width:80%;padding:10px 12px;border-radius:12px;white-space:pre-wrap}.me{background:#1f6feb;align-self:flex-start}.bot{background:#22262e;align-self:flex-end}form{display:flex;gap:8px;padding:10px;background:#111827}input{flex:1;padding:12px;border-radius:10px;border:0;outline:none}button{padding:12px 18px;border-radius:10px;border:0;background:#1f6feb;color:white;font-weight:bold}</style></head><body><header>المهلهل 🔥</header><div id="chat"></div><form onsubmit="send(event)"><input id="inp" placeholder="اكتب للمهلهل..." autocomplete="off"><button>ارسال</button></form><script>let history=JSON.parse(localStorage.getItem('muhalhil_memory')||'[]');let chatDiv=document.getElementById('chat');function show(t,c){let d=document.createElement('div');d.className='msg '+c;d.textContent=t;chatDiv.appendChild(d);chatDiv.scrollTop=chatDiv.scrollHeight;}history.forEach(m=>show(m.text,m.role==='user'?'me':'bot'));if(history.length===0)show('هلا فيك يا عصام! انا المهلهل، نموذجك اللي دربته، تتذكرني؟','bot');async function send(e){e.preventDefault();let inp=document.getElementById('inp');let msg=inp.value.trim();if(!msg)return;show(msg,'me');history.push({role:'user',text:msg});inp.value='';let last=history.slice(-10);let res=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg,history:last})});let data=await res.json();let reply=data.reply||'ما وصلني رد';show(reply,'bot');history.push({role:'assistant',text:reply});history=history.slice(-50);localStorage.setItem('muhalhil_memory',JSON.stringify(history));}</script></body></html>"""

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML.encode('utf-8'))

    def do_POST(self):
        length = int(self.headers.get('Content-Length',0))
        body = self.rfile.read(length)
        try:
            data = json.loads(body.decode('utf-8'))
        except:
            data = {}
        msg = data.get('message','')
        hist = data.get('history',[])
        prompt = MEMORY + "\nالمحادثة:\n"
        for h in hist[-10:]:
            role = "عصام" if h.get('role')=='user' else "المهلهل"
            prompt += f"{role}: {h.get('text','')}\n"
        prompt += f"عصام: {msg}\nالمهلهل:"

        reply = "هلا فيك يا عصام! انا المهلهل، نموذجك اللي دربته، ايش تشتي اليوم؟"
        try:
            token = os.environ.get("HF_TOKEN","")
            req = urllib.request.Request(
                "https://api-inference.huggingface.co/models/asamersamer/asam-v2-merged",
                data=json.dumps({"inputs": prompt, "parameters": {"max_new_tokens": 200, "temperature": 0.7}}).encode('utf-8'),
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                out = json.loads(r.read().decode('utf-8'))
                if isinstance(out, list) and len(out)>0:
                    txt = out[0].get("generated_text","").replace(prompt,"").strip()
                    if txt:
                        reply = txt
        except Exception as e:
            pass

        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"reply": reply}, ensure_ascii=False).encode('utf-8'))
