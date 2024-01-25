import io
import base64

from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from werkzeug.exceptions import NotFound

from note_api import NoteAPI
from calcimetry.config import Config
from calcimetry.calcimetry_api import CalcimetryAPI
from calcimetry.thumbnail_api import ThumbnailAPI
from calcimetry.carrot_img import CarrotImage

from PIL import Image
from PIL import ImageDraw

app = Flask(__name__)


@app.route('/')
def index():

    with NoteAPI() as note_api:
        measures_by_drill = note_api.get_thumbnails_by_drill()
        
    return render_template('index.html', measures_by_drill=measures_by_drill)


@app.route('/favicon.ico')
def favico():
    raise NotFound

def encode_img(img: CarrotImage, measurement):
    assert img is not None, "no image"
    img = img.to_resolution(0.035)
    
    half_dim = 64
    cx = img.p_x(measurement.cote)
    cy = img.k_arrow.p_y(cx)
    left = cx - half_dim
    top  = cy - half_dim
    right =  cx + half_dim
    bottom = cy + half_dim
    draw = ImageDraw.Draw(img.jpg, "RGBA")
    draw.rectangle( ((left, top), (right, bottom)), outline=(255, 0, 0, 255), fill=(200, 100, 0, 64))
    data = io.BytesIO()
    img.jpg.save(data, "JPEG")

    return base64.b64encode(data.getvalue())


@app.route("/<drill>", methods=['GET', 'POST'])
def display_rock(drill):

    with NoteAPI() as note_api:
            thumbnails_by_drill = note_api.get_thumbnails_by_drill()

    thumbnails = thumbnails_by_drill[drill]

    if 'idx' in request.args:
        idx = int(request.args['idx'])
        if idx < 0:
            idx = 0
        if idx > len(thumbnails) - 1:
            idx = len(thumbnails) - 1
    else:
        idx = 0

    if request.method == 'POST':
        value = request.form.get('rangeInput')
        print(value)
        idx = request.form.get('index')
        return redirect(f'?idx={idx}')
 
    thu_id = thumbnails[idx]
    
    with ThumbnailAPI() as thumbnail_api:
        thumbnail = thumbnail_api.read(thu_id=thu_id)
        measurement = thumbnail.measurement

    with CalcimetryAPI() as calcimetry_api:
        image = calcimetry_api.read_image(image_id=thumbnail.image_id)

    b64_img= encode_img(image, measurement)

    context = {
        'drill': drill,
        'image': b64_img.decode('utf-8'),
        'image_id': thumbnail.image_id,
        'idx': idx,
        'total': len(thumbnails),
        'quality': measurement.quality,
        'filename': image.infos['filename']
    }

    return render_template('displayrock.html', **context)



if __name__ == '__main__':
    app.run(debug=True)
