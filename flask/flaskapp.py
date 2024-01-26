import io
import base64

from flask import Flask, render_template, request, redirect, session
from werkzeug.exceptions import NotFound

from note_api import NoteAPI
from calcimetry.config import Config
from calcimetry.calcimetry_api import CalcimetryAPI
from calcimetry.thumbnail_api import ThumbnailAPI
from calcimetry.carrot_img import CarrotImage

from PIL import ImageDraw

app = Flask(__name__)
app.config['SECRET_KEY'] = 'oh, my secret'

@app.route("/calci_note/")
def index():

    session['idx'] = 0 # reset idx when we go back home

    if 'what' in request.args:
        all = request.args['what'] == 'all'
        session['what'] = all
    else:
        all = session.get('what', False)

    with NoteAPI() as note_api:
        if 'refresh' in request.args:
            note_api.update_thumbnails()
        thumbnails_by_drills = note_api.get_thumbnails_by_drill(all)
    
    return render_template('index.html', measures_by_drill=thumbnails_by_drills)


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


@app.route("/calci_note/<drill>", methods=['GET', 'POST'])
def note(drill):

    all = session.get('what', False)

    with NoteAPI() as note_api:
        thumbnails_by_drill = note_api.get_thumbnails_by_drill(all)

    thumbnails = thumbnails_by_drill[drill]

    if 'idx' in request.args:
        idx = int(request.args['idx'])
        if idx < 0:
            idx = 0
        if idx > len(thumbnails) - 1:
            idx = len(thumbnails) - 1
        session['idx'] = idx
    else:
        idx = session.get('idx', 0)

    if request.method == 'POST':
        value = request.form.get('rangeInput', 10)
        print(value)

        measure_id = session.get('measure_id', -1)
        if measure_id > 0:
            with NoteAPI() as note_api:
                print(f'update {thumbnails[idx]} ({measure_id}) with {value}')
                note_api.update_note(measure_id=measure_id, note=value)

        return redirect(f'?idx={idx}')
 
    thu_id = thumbnails[idx]
    
    with ThumbnailAPI() as thumbnail_api:
        thumbnail = thumbnail_api.read(thu_id=thu_id)
        measurement = thumbnail.measurement
        session['measure_id'] = measurement.measure_id

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

    return render_template('note.html', **context)



if __name__ == '__main__':
    app.run(debug=True)
