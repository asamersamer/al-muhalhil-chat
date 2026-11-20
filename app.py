from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

HTML = """
<h1>المهلهل شغال 🔥</h1>
<form method="post" action="/chat">
<input name="msg" placeholder="اكتب هنا">
<button>ارسل</button>
</form>
"""

@app.route("/")
def home():
    return HTML

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.form.get("msg", "")
    return f"وصلتني رسالتك: {msg}"

# مهم لـ Vercel: لا تحط app.run هنا
