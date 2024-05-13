import io
import base64
import os
import json

from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.exceptions import NotFound
from utils import compute_calcimetry

from PIL import Image, ImageDraw

from enum import IntEnum


class ComputeType(IntEnum):
    NOTHING = 0
    NEEDED = 1
    COMPUTED = 2


app = Flask(__name__, static_folder="assets")
app.config["SECRET_KEY"] = "oh, my secret"
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")

DOWNLOADED_FILE = "download.png"
DOWNLOADED_FILEPATH = os.path.join(app.config["UPLOAD_FOLDER"], DOWNLOADED_FILE)


def encode_image(filename):

    img = Image.open(os.path.join(app.config["UPLOAD_FOLDER"], filename)).convert("RGB")

    coords = []

    if "coords" in session:
        for coord in session["coords"]:
            x, y = coord.split(";")
            coords.append((int(float(x) * img.width), int(float(y) * img.height)))

    coords = sorted(coords, key=lambda c: c[0])

    draw = ImageDraw.Draw(img, "RGBA")

    for c in coords:
        left = c[0] - 32
        right = c[0] + 32
        top = c[1] - 32
        bottom = c[1] + 32
        draw.rectangle(
            ((left, top), (right, bottom)),
            outline=(255, 0, 0, 255),
            fill=(200, 100, 0, 64),
        )

    data = io.BytesIO()
    img.save(data, "JPEG")
    return base64.b64encode(data.getvalue()).decode("utf-8"), coords

def clean_session():
    if "coords" in session:
            session.pop("coords")
    if "compute" in session:
        session.pop("compute")

    return "image_upload.png", "No file"

@app.route("/calcipredict/")
def index():
    if "filename" in session:
        image = DOWNLOADED_FILE
        filename = session["filename"]
    else:
        image, filename = clean_session()

    try:
        img, coords = encode_image(image)
    except FileNotFoundError as err:
        if "filename" in session:
            session.pop("filename")
        image, filename = clean_session()
        img, coords = encode_image(image)
        

    if "compute" in session:
        calcimetries = session.get("calcimetries", [])
    else:
        calcimetries = []
    # print(calcimetries)

    return render_template(
        "index.html",
        filename=filename,
        image=img,
        coords=coords,
        chart_data=json.dumps(calcimetries),
    )


@app.route("/calcipredict/compute", methods=["POST"])
def compute():

    # ensures an image is selected
    if "filename" not in session:
        return "no image selected"

    _, coords = encode_image(DOWNLOADED_FILE)
    if len(coords) < 1:
        return "no coords"

    calcimetries = compute_calcimetry(DOWNLOADED_FILEPATH, coords)
    session["compute"] = ComputeType.COMPUTED
    session["calcimetries"] = calcimetries

    return "calcimetries computed"


@app.route("/calcipredict/click", methods=["POST"])
def click():

    coords = session.get("coords", [])
    coord = request.form.get("coords")
    if "clear" in coord:
        if "coords" in session:
            session.pop("coords")
        if "compute" in session:
            session.pop("compute")
        return "coords session cleared"

    coords.append(coord)
    session["coords"] = coords

    return "ok"


@app.route("/calcipredict/upload", methods=["POST"])
def upload_file():
    uploaded_file = request.files["file"]
    if uploaded_file:
        uploaded_file.save(DOWNLOADED_FILEPATH)
        session["filename"] = uploaded_file.filename
        if "coords" in session:
            session.pop("coords")
        if "compute" in session:
            session.pop("compute")
        return "Fichier téléchargé"
    else:
        return "Aucun fichier téléchargé"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
