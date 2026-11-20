from flask import Flask, request, jsonify
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>المهلهل</title>
<style>
*{box-sizing:border-box}body{margin:0;font-family:system-ui;background:#0f1115;color:#fff;height:100vh;display:flex;flex-direction:column}
header{background:#1f6feb;padding:14px;text-align:center;font-weight:900;font-size:20px}
#chat{flex:1;overflow:auto;padding:12px;display:flex;flex-direction:column;gap:8px}
.msg{max-width:80%;padding:10px 12px;border-radius:16px;line-height:1.5}
.me{background:#1f6feb;align-self:flex-start}
.bot{background:#22262e;align-self:flex-end}
form{display:flex;gap:8px;padding:10px;background:#16181d}
input{flex:1;padding:12px;border-radius:20px;border:0;outline:0;background:#22262e;color:#fff}
button{padding:12px 18px;border-radius:20px;border:0;background:#1f6feb;color:#fff;font-weight:800}
</style></head><body>
<header>المهلهل 🔥</header>
<div id="chat"><div class="msg bot">هلا والله! أنا المهلهل، اسألني أي شي 😎</div></div>
<form onsubmit="send(event)"><input id="i" placeholder="اكتب رسالتك..."><button>ارسال</button></form>
<script>
async function send(e){e.preventDefault();let inp=document.getElementById('i');let t=inp.value.trim();if(!t)return;let c=document.getElementById('chat');c.innerHTML+='<div class="msg me">'+t+'</div>';inp.value='';c.scrollTop=c.scrollHeight;let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({msg:t})});let d=await r.json();c.innerHTML+='<div class="msg bot">'+d.reply+'</div>';c.scrollTop=c.scrollHeight}
</script></body></html>
"""

@app.route("/")
def home():
    return HTML

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    msg = data.get("msg","").lower()
    if "هلا" in msg or "سلام" in msg or "مرحبا" in msg:
        reply = "هلاااا فيك! نورت المهلهل 🔥 وش عندك اليوم؟"
    elif "اسمك" in msg:
        reply = "أنا المهلهل، صديقك اليمني 😎"
    elif "كيفك" in msg or "كيف حالك" in msg:
        reply = "الحمدلله تمام، وانت كيفك؟ عساك بخير"
    elif "من" in msg and "وين" in msg:
        reply = "أنا من صنعاء، من قلب اليمن ❤️"
    elif "شكرا" in msg:
        reply = "العفو يا غالي، هذا واجبي ✨"
    elif "باي" in msg or "وداعا" in msg:
        reply = "باي باي، لا تطول الغيبة! 👋"
    else:
        reply = f"فهمت عليك، قلت: {data.get('msg','')} .. حلو! كمل، أنا اسمعك 👂"
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run()
"""

**4. اضغط `Commit changes`**

**5. انتظر دقيقة في Vercel لين يصير `Ready`، وادخل على موقعك من جديد.**

**بيطلع لك شات مثل الواتساب، رسايلك بالأزرق ورد المهلهل بالرمادي.**

**سويته؟ صور لي الشكل الجديد لما يفتح معك.**
