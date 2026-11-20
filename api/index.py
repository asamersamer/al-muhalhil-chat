from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>المهلهل شغال 🔥</h1>
    <form method="post" action="/chat">
    <input name="msg" placeholder="اكتب هنا">
    <button>ارسل</button>
    </form>
    """

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.form.get("msg", "")
    return f"وصلتني: {msg}"
