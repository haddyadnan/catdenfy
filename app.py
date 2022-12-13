import base64
import os
import urllib.request

import requests
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads/"

app.secret_key = "summer"  # test
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

allowed_ext = set(["png", "jpg", "jpeg"])


def check_allowed_file(filename):
    """check file extension"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_ext


@app.route("/")
def home():
    """render home page"""
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload_image():
    """upload image file"""
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
    """
    display img
    filename: Name of image file
    """
    return redirect(url_for("static", filename="uploads/" + filename))


@app.route("/clear", methods=["POST"])
def clear():
    """
    remove image file
    global filename
    """
    os.remove(UPLOAD_FOLDER + filename)
    return redirect("/")


@app.route("/predict", methods=["POST", "GET"])
def predict():
    """
    predict image
    """
    with open(UPLOAD_FOLDER + filename, "rb") as img_file:
        img_str = base64.b64encode(img_file.read()).decode()

    response = requests.post(
        "https://haddy-catdenfy.hf.space/run/predict",
        json={
            "data": [
                "data:image/png;base64,{}".format(img_str),
            ]
        },
    ).json()

    results = response["data"][0]
    print(results.get("label").replace("_", " "))
    probs = results.get("confidences")
    probs_dict = {
        list(p.values())[0].replace("_", " "): list(p.values())[1] for p in probs
    }
    # print(probs_dict)

    return jsonify(probs, probs.label)


if __name__ == "__main__":
    # test
    app.run(port="5020", host="0.0.0.0", debug=True)
