from flask import Flask, request
from flask_cors import CORS
import cv2 as cv
import os
import random
from image import *
from waitress import serve

app = Flask(__name__)
CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']
app.config['UPLOAD_PATH'] = 'images'


@app.route('/', methods=["GET"])
def hello_world():
    return "hello world"


@app.route('/tanks', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    num = random.randint(0, 10000000)
    uploaded_file.save(f"images/{num}.png")
    img = cv.imread(f"images/{num}.png")
    img = cv.resize(img, (750, 1334))
    u, x, y = get_dist(img)
    wind = get_wind_val(img)
    result = compute(x, y, 8.7)
    power = set_power(wind)
    os.remove(f"images/{num}.png")
    return (f"u:{u} x:{x} y:{y} wind:{wind} angle:{result} power:{power}")


if __name__ == '__main__':
    # app.run()
    serve(app, host='0.0.0.0', port=os.environ.get('PORT', 5000))
    print(f"App listening on port:{os.environ.get('PORT', 5000)}")
