from flask import Flask, request, jsonify, render_template, redirect, session
from google import genai
from dotenv import load_dotenv
import os
# ---------------- LOAD ENV ---------------- #
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ---------------- LOGIN ---------------- #
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "1234":
            session["user"] = "admin"
            return redirect("/dashboard")
    return render_template("login.html")

# ---------------- DASHBOARD ---------------- #
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("index.html")

# ---------------- LOGOUT ---------------- #
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- SENSOR ---------------- #
@app.route("/recommendation", methods=["POST"])
def recommendation():

    data = request.json
    m = int(data["moisture"])
    t = int(data["temperature"])

    if m < 30:
        result = "🌱 Low moisture → Drip irrigation"
    elif m < 60:
        result = "💧 Moderate → Sprinkler irrigation"
    else:
        result = "✅ High moisture → No irrigation needed"

    if t > 35:
        result += " (High temperature)"

    return jsonify({"result": result})

# ---------------- CHATBOT ---------------- #
@app.route("/chat", methods=["POST"])
def chat():

    msg = request.json.get("message", "")

    if not msg:
        return jsonify({"reply": "Please enter a message"})

    reply = None

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=f"You are an agriculture assistant. Answer clearly: {msg}if you get anything not related to aggriculture pleaase reply you are an ai agriculture assistant and you can't answer that type of questions"
        )
        reply = response.text

    except Exception as e:
        print("Gemini Error:", e)

    # ✅ ADD HISTORY (ONLY THIS PART NEW)
    if "chat_history" not in session:
        session["chat_history"] = []

    session["chat_history"].append({
        "user": msg,
        "bot": reply
    })

    session.modified = True

    return jsonify({"reply": reply})

# ---------------- HISTORY PAGE ---------------- #
@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/")

    chat_history = session.get("chat_history", [])
    return render_template("history.html", history=chat_history)

# ---------------- RUN ---------------- #
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True)