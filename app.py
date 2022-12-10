from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
import urllib.request

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads/"

app.secret_key = "summer"  # test
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

allowed_ext = set(["png", "jpg", "jpeg"])


def check_allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_ext


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload_image():
    global filename
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("No image selected for uploading")
        return redirect(request.url)
    if file and check_allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        # print('upload_image filename: ' + filename)
        flash("Image successfully uploaded")
        return render_template("index.html", filename=filename)
    else:
        flash("Allowed image types are - png, jpg, jpeg")
        return redirect(request.url)


@app.route("/display/<filename>")
def display_image(filename):
    return redirect(url_for("static", filename="uploads/" + filename))


@app.route("/clear", methods=["POST"])
def clear():
    os.remove(UPLOAD_FOLDER + filename)
    return redirect("/")


if __name__ == "__main__":
    # test
    app.run(port="5020", host="0.0.0.0", debug=True)
