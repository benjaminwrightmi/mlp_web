from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import cv2

app = Flask(__name__)

upload_folder = os.path.join('static', 'uploads')
 
app.config['UPLOAD'] = upload_folder
 
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        if not os.path.isfile(os.path.join(app.config['UPLOAD'], filename)):
            return render_template('index.html')
        file.save(os.path.join(app.config['UPLOAD'], filename))
        img = os.path.join(app.config['UPLOAD'], filename)
        print(img)
        colours_hex,inv_hex = get_colours(img)
        return render_template('index.html', img=img, colours=colours_hex, inv=inv_hex)
    return render_template('index.html')


def get_colours(image_path):
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Extract the colors and convert them to hex values
    pixels = image_rgb.reshape(-1, 3)
    pixels = [tuple(pixel) for pixel in pixels]
    unique_colors = set(pixels)
    hex_values = []
    inv_hex = []
    for color in unique_colors:
        color_inv = (256-val for val in color)
        inv_hex.append('#{:02x}{:02x}{:02x}'.format(*color_inv))
        hex_values.append('#{:02x}{:02x}{:02x}'.format(*color))
    return hex_values, inv_hex


