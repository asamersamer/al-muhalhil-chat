from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/")
def home():
    return "Al-Muhalhil is running"

@app.route("/v1/models")
def models():
    return jsonify({"data": [{"id": "al-muhalhil-chat"}]})

@app.route("/v1/chat/completions", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    msgs = data.get("messages", [])
    last = msgs[-1].get("content", "") if msgs else ""
    reply = "هلا بك! أنا المهلهل، أسألني أي شي باليمني وأنا أجاوبك. أنت قلت: " + last
    return jsonify({"choices": [{"message": {"role": "assistant", "content": reply}}]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)