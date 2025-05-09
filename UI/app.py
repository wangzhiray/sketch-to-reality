import os
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from openai import OpenAI

# Load environment
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/transcribe", methods=["POST"])
def transcribe():
    if "file" not in request.files:
        return jsonify({"error":"No audio file provided"}), 400
    audio = request.files["file"]
    filename, fileobj, ctype = audio.filename or "audio.webm", audio.stream, audio.mimetype
    try:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=(filename, fileobj, ctype)
        )
        text = result.text
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"text": text})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msgs = data.get("messages") or [
        {"role":"system","content":"You are helpful."},
        {"role":"user","content":data.get("message","")}
    ]
    try:
        comp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=msgs
        )
        reply = comp.choices[0].message.content
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
