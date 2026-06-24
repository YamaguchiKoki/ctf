from flask import Flask, redirect, render_template, request, session, url_for
import secrets
import requests
import os
import re


FLAG = os.environ.get("FLAG", "Alpaca{dummy}")
APP_URL = os.environ.get("APP_URL", "http://localhost:3000/")

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

templates = {
    "en": "Your secret is {secret}",
    "ja": "あなたのシークレットは {secret}",
    "zh": "你的秘密是 {secret}",
    "ko": "당신의 비밀은 {secret}입니다",
    "es": "Tu secreto es {secret}",
}


users = {}

@app.get("/")
def index():
    username = session.get("username")
    if not username:
        return redirect(url_for("register"))
    return render_template("index.html")


@app.get("/register")
def register_page():
    return render_template("register.html")

@app.post("/register")
def register():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    secret = request.form.get("secret", "")

    if username in users:
        return "user already exists"
    
    users[username] = {
        "password": password,
        "secret": secret
    }

    session["username"] = username

    return redirect(url_for("index"))

@app.get("/render/<lang>")
def render(lang):
    username = session.get("username")
    if not username:
        return redirect(url_for("register"))
    
    template = templates.get(lang, templates["en"])
    secret = users[username]["secret"]
    message = template.format(secret=secret)

    return render_template("render.html", message=message)

@app.get("/report")
def report_get():
    return render_template("report.html", APP_URL=APP_URL)

@app.post("/report")
def report_post():
    url = request.form.get("url", "http://example.com/")

    if not re.match("https?://", url):
        return "invalid url", 404

    s = requests.session()
    s.post(f"{APP_URL}register", data={
        "username": f"admin-{secrets.token_hex(16)}",
        "password": f"pass-{secrets.token_hex(16)}",
        "secret": FLAG
    })
    
    r = s.get(url)
    
    # return r.text, r.status_code
    return "The result is redacted for security reason"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3001)
