#!/usr/bin/python3

from flask import Flask, render_template, jsonify, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from fastai.vision.all import *
from io import BytesIO
import base64

app = Flask(__name__)

learn = None
labels = None

allowed_ext = ["jpg", "jpeg", "png", "JPG", "JPEG", "PNG"]


def check_allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_ext


# def load_model():
#     global learn
#     global labels
#     learn = load_learner("export.pkl")
#     labels = learn.dls.vocab


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            print("No files here")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            print("No file selected here")
            return redirect(request.url)
        if file and check_allowed_file(file.filename):
            filename = secure_filename(file.filename)
            img = Image.open(file.stream)
            with BytesIO() as buf:
                img.save(buf, "jpeg")
                image_bytes = buf.getvalue()
            encoded_string = base64.b64encode(image_bytes).decode()
        return render_template("index.html", img_data=encoded_string), 200
    else:
        return render_template("index.html", img_data=""), 200


@app.route("/predict", methods=["GET", "POST"])
def predict():
    """
    receive image
    """

    return jsonify(message="Success")


if __name__ == "__main__":
    print(" * Loading Model . . .")
    # load_model()
    print(" * Model Loaded . . .")
    app.run(port="5020", host="0.0.0.0", debug=True)
