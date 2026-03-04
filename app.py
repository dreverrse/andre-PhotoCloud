from flask import Flask, render_template, request, redirect, session, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os

from utils.auth import check_login
from utils.image_tools import create_thumbnail
from utils.security import check_block, register_attempt, reset_attempt

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

USERNAME = os.getenv("ADMIN_USERNAME")
PASSWORD = os.getenv("ADMIN_PASSWORD")

UPLOAD_FOLDER = "uploads"
THUMB_FOLDER = "thumbnails"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(THUMB_FOLDER, exist_ok=True)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[]
)


@app.route("/", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login():

    ip = request.remote_addr

    if check_block(ip):
        return render_template(
            "login.html",
            error="Too many attempts. Try again in 5 minutes."
        )

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if check_login(username, password, USERNAME, PASSWORD):

            session["login"] = True
            reset_attempt(ip)

            return redirect("/gallery")

        else:

            remaining = register_attempt(ip)

            return render_template(
                "login.html",
                error=f"Invalid username or password. ({remaining}) attempts remaining."
            )

    return render_template("login.html")


@app.route("/gallery")
def gallery():

    if not session.get("login"):
        return redirect("/")

    photos = os.listdir(THUMB_FOLDER)

    return render_template("gallery.html", photos=photos)


from datetime import datetime

@app.route("/upload", methods=["POST"])
def upload():

    if not session.get("login"):
        return "unauthorized"

    if "photo" not in request.files:
        return "no file"

    file = request.files["photo"]

    if file.filename == "":
        return "empty filename"

    ext = file.filename.rsplit(".",1)[1].lower()

    date = datetime.now().strftime("%d-%m-%Y")

    existing = os.listdir(UPLOAD_FOLDER)
    img_count = len([f for f in existing if f.startswith("IMG")]) + 1

    filename = f"IMG-{img_count}_{date}.{ext}"

    path = os.path.join(UPLOAD_FOLDER, filename)

    file.save(path)

    create_thumbnail(filename, UPLOAD_FOLDER, THUMB_FOLDER)

    return "ok"


@app.route("/delete/<name>")
def delete(name):

    if not session.get("login"):
        return "unauthorized"

    path = os.path.join(UPLOAD_FOLDER, name)
    thumb = os.path.join(THUMB_FOLDER, name)

    if os.path.exists(path):
        os.remove(path)

    if os.path.exists(thumb):
        os.remove(thumb)

    return "deleted"


@app.route("/photo/<name>")
def photo(name):

    if not session.get("login"):
        return "unauthorized"

    return send_from_directory(UPLOAD_FOLDER, name)


@app.route("/thumb/<name>")
def thumb(name):

    if not session.get("login"):
        return "unauthorized"

    return send_from_directory(THUMB_FOLDER, name)

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)